import json
import logging
import sys
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any

import jsonschema
import numpy as np

from src.config.config_interface import SolverConfig
from src.config.config_loader import load_and_validate_config
from src.containers.bernoulli_state import BernoulliState
from src.steps.step_s0_filled_unfilled_classifier import StepS0FilledUnfilledClassifier
from src.steps.step_s1_exactly_one_missing import StepS1ExactlyOneMissing
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
from src.steps.step_s3_solve_missing_variable import StepS3SolveMissingVariable
from src.steps.step_s4_compute_energy_residual import StepS4ComputeEnergyResidual
from src.steps.step_s5_compute_min_max_constraints import StepS5ComputeMinMaxConstraints

# Rule 5: Force global arithmetic trapping for deterministic stability
np.seterr(all="raise")

# Configure Logger to align with professional execution standards
logger = logging.getLogger("BernoulliSolver.Main")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent


class BernoulliPipelineOrchestrator:
    """
    Orchestrates the sequential execution of the Bernoulli solver pipeline.
    
    Implements a strict, one-way loop-free directed acyclic graph (DAG) moving from
    raw dictionary input processing up to the completed export of loose-but-truthful 
    physical constraints for the downstream Navier-Stokes solver.
    """

    def __init__(self) -> None:
        """
        Statically instantiates the isolated components of the Minimal Step Chain.
        Enforces a clean composition foundation with clear step isolation.
        """
        self.s0_classifier = StepS0FilledUnfilledClassifier()
        self.s1_validator = StepS1ExactlyOneMissing()
        self.s2_constructor = StepS2ConstructPartialState()
        self.s3_solver = StepS3SolveMissingVariable()
        self.s4_diagnician = StepS4ComputeEnergyResidual()
        self.s5_enveloper = StepS5ComputeMinMaxConstraints()

        def _validate_boundaries(self, raw_input: Dict[str, Any]) -> None:
        """
        Pre-flight boundary check to enforce physical plausibility
        before entering the step chain.
        """
        # Physical Constraints - Safely checked only if fields are provided and non-None
        p1, p2 = raw_input.get("p1"), raw_input.get("p2")
        if (p1 is not None and p1 < 0) or (p2 is not None and p2 < 0):
            raise ValueError("Boundary validation failed: Negative pressure detected.")

        v1, v2 = raw_input.get("v1"), raw_input.get("v2")
        if (v1 is not None and abs(v1) > 1e6) or (v2 is not None and abs(v2) > 1e6):
            raise ValueError("Boundary validation failed: Velocity exceeds physical limits.")

    def execute_pipeline(self, raw_input: Dict[str, Any], config: SolverConfig) -> BernoulliState:
        """
        Executes the full chain sequentially.
        """
        # --- Guard Clause: Fail-Fast for missing configuration ---
        # Ensures that a missing config is caught before S1 validation occurs.
        if config is None:
            raise TypeError("Configuration object is mandatory for pipeline execution.")

        # --- Guard Gate: Pre-Flight Boundary Validation ---
        self._validate_boundaries(raw_input)
        
        # S0 & S1: Validation
        _, _ = self.s0_classifier.classify_filled_and_unfilled(input_schema_instance=raw_input)
        validated_input, missing_variable = self.s1_validator.enforce_exactly_one_missing(
            raw_input_dict=raw_input
        )

        # S2: Construct State
        partial_state: BernoulliState = self.s2_constructor.construct_partial_state(
            validated_input_dict=validated_input, 
            missing_variable_name=missing_variable,
            unfilled_sentinel=float('nan') 
        )

        # S3: Solve or Identity Path
        if missing_variable:
            solved_state: BernoulliState = self.s3_solver.solve_missing_variable(
                partial_state=partial_state, 
                config=config
            )
        else:
            # IDENTITY PATH: Manual construction of BernoulliState
            # Ensure we calculate energy and bounds for downstream S4/S5 consistency
            p1, p2 = partial_state.p1, partial_state.p2
            v1, v2 = partial_state.v1, partial_state.v2
            h1, h2 = partial_state.h1, partial_state.h2
            rho = partial_state.rho
            g = config.g

            e1 = p1 + 0.5 * rho * (v1 ** 2) + rho * g * h1
            e2 = p2 + 0.5 * rho * (v2 ** 2) + rho * g * h2

            solved_state = BernoulliState(
                p1=p1, p2=p2, v1=v1, v2=v2, h1=h1, h2=h2, rho=rho,
                energy=[e1, e2],
                energy_imbalance=abs(e1 - e2),
                p_min=min(p1, p2), p_max=max(p1, p2),
                v_min=min(v1, v2), v_max=max(v1, v2)
            )

        # S4: Compute Energy and Residuals
        state_with_energy: BernoulliState = self.s4_diagnician.compute_energy_and_residual(
            solved_state=solved_state, 
            config=config
        )

        # S5: Compute Min/Max Constraints Envelopes ---
        final_state: BernoulliState = self.s5_enveloper.compute_min_max_constraints(
            state_with_energy=state_with_energy, 
            config=config
        )

        return final_state


def run_solver(input_path: str) -> str:
    """
    Main execution routine with explicit pre-flight environment verification.
    """
    full_input_path = Path(input_path)
    if not full_input_path.is_absolute():
        full_input_path = BASE_DIR / input_path
    
    required_paths = {
        "Input File": full_input_path,
        "Config File": BASE_DIR / "src/config/config.json",
        "Input Schema": BASE_DIR / "schema/bernoulli_input.schema.json",
        "Output Schema": BASE_DIR / "schema/bernoulli_output.schema.json"
    }

    for label, path in required_paths.items():
        if not path.exists():
            logger.critical(f"ENVIRONMENT ANOMALY: {label} not found at {path}")
            raise FileNotFoundError(f"Missing dependency: {label} at {path}")

    config = load_and_validate_config(str(required_paths["Config File"]))
    logger.info("Configuration contract verified.")

    with open(full_input_path, "r", encoding="utf-8") as f:
        raw_input = json.load(f)

    with open(required_paths["Input Schema"], "r", encoding="utf-8") as f:
        input_schema = json.load(f)

    try:
        jsonschema.validate(instance=raw_input, schema=input_schema)
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"!!! INPUT CONTRACT VIOLATION: {e.message}")
        raise

    orchestrator = BernoulliPipelineOrchestrator()
    final_state = orchestrator.execute_pipeline(raw_input, config)

    output_dict = asdict(final_state)
    with open(required_paths["Output Schema"], "r", encoding="utf-8") as f:
        output_schema = json.load(f)
    
    jsonschema.validate(instance=output_dict, schema=output_schema)

    output_file_path = full_input_path.parent / "bernoulli_solver_output.json"
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(output_dict, f, indent=2)
        
    return str(output_file_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 src/bernoulli_pipeline_orchestrator.py <input_json_path>")
        sys.exit(1)
    try:
        output_json_path = run_solver(sys.argv[1])
        print(f"Pipeline complete. Output JSON written to: {output_json_path}")
        sys.exit(0)
    except Exception as e:
        print(f"FATAL PIPELINE ERROR: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()