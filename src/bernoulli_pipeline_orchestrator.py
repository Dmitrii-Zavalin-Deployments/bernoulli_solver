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
        self.s0_classifier = StepS0FilledUnfilledClassifier()
        self.s1_validator = StepS1ExactlyOneMissing()
        self.s2_constructor = StepS2ConstructPartialState()
        self.s3_solver = StepS3SolveMissingVariable()
        self.s4_diagnician = StepS4ComputeEnergyResidual()
        self.s5_enveloper = StepS5ComputeMinMaxConstraints()

    def execute_pipeline(self, raw_input: Dict[str, Any], config: SolverConfig) -> BernoulliState:
        """
        Executes the full chain sequentially (S0 -> S1 -> S2 -> S3 -> S4 -> S5).
        """
        
        # --- Step S0: Classify Filled vs Unfilled Fields ---
        filled_fields, unfilled_fields = self.s0_classifier.classify_filled_and_unfilled(
            input_schema_instance=raw_input
        )

        # --- Step S1: Enforce "Exactly One Missing" Rule ---
        validated_input, missing_variable = self.s1_validator.enforce_exactly_one_missing(
            raw_input_dict=raw_input
        )

        # --- Step S2: Construct Partial State ---
        # Fixed: Passed all three required arguments to match StepS2ConstructPartialStateInterface
        # 'None' is passed as the sentinel for unfilled fields.
        partial_state: BernoulliState = self.s2_constructor.construct_partial_state(
            validated_input_dict=validated_input, 
            missing_variable_name=missing_variable,
            unfilled_sentinel=None 
        )

        # --- Step S3: Solve Missing Bernoulli Primary Variable ---
        solved_state: BernoulliState = self.s3_solver.solve_missing_variable(
            partial_state=partial_state, 
            config=config
        )

        # --- Step S4: Compute Energy and Residuals ---
        state_with_energy: BernoulliState = self.s4_diagnician.compute_energy_and_residual(
            solved_state=solved_state, 
            config=config
        )

        # --- Step S5: Compute Min/Max Constraints Envelopes ---
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