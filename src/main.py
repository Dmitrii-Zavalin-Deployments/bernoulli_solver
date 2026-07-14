import argparse
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any

import jsonschema
import numpy as np

from src.config.config_interface import SolverConfig
from src.config.config_loader import load_and_validate_config
from src.containers.bernoulli_state import BernoulliState
from src.steps.step_s0_filled_unfilled_classifier import FilledUnfilledClassifier
from src.steps.step_s1_exactly_one_missing import StepS1ExactlyOneMissing
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
from src.steps.step_s3_solve_missing_variable import StepS3SolveMissingVariable
from src.steps.step_s4_compute_energy_residual import StepS4ComputeEnergyResidual
from src.steps.step_s5_compute_min_max_constraints import StepS5ComputeMinMaxConstraints

# Rule 5: Force global arithmetic trapping for deterministic stability
np.seterr(all="raise")

# Configure Logger
logger = logging.getLogger("BernoulliSolver")
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s"
)

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
        logger.info("Initializing BernoulliPipelineOrchestrator components...")
        self.s0_classifier = FilledUnfilledClassifier()
        self.s1_validator = StepS1ExactlyOneMissing()
        self.s2_constructor = StepS2ConstructPartialState()
        self.s3_solver = StepS3SolveMissingVariable()
        self.s4_diagnician = StepS4ComputeEnergyResidual()
        self.s5_enveloper = StepS5ComputeMinMaxConstraints()
        logger.info("Pipeline components ready.")

    def _validate_boundaries(self, raw_input: Dict[str, Any]) -> None:
        """
        Pre-flight boundary check to enforce physical plausibility
        before entering the step chain.
        """
        logger.debug("Running pre-flight boundary validation.")
        p1, p2 = raw_input.get("p1"), raw_input.get("p2")
        if (p1 is not None and p1 < 0) or (p2 is not None and p2 < 0):
            logger.error("Boundary validation failed: Negative pressure detected.")
            raise ValueError("Negative pressure detected.")

        v1, v2 = raw_input.get("v1"), raw_input.get("v2")
        if (v1 is not None and abs(v1) > 1e6) or (v2 is not None and abs(v2) > 1e6):
            logger.error("Boundary validation failed: Velocity exceeds physical limits.")
            raise ValueError("Velocity exceeds physical limits.")

    def execute_pipeline(self, raw_input: Dict[str, Any], config: SolverConfig) -> BernoulliState:
        logger.info("Starting pipeline execution.")
        
        if config is None:
            logger.critical("Pipeline execution aborted: Config object is None.")
            raise TypeError("Configuration object is mandatory.")

        self._validate_boundaries(raw_input)
        
        # S0 & S1
        logger.info("Step S0/S1: Classifying and validating input variables.")
        _, _ = self.s0_classifier.classify_filled_and_unfilled(input_schema_instance=raw_input)
        validated_input, missing_variable = self.s1_validator.enforce_exactly_one_missing(
            raw_input_dict=raw_input
        )
        logger.info(f"S1 Validation complete. Missing variable identified: {missing_variable}")

        # S2
        logger.info("Step S2: Constructing partial state container.")
        partial_state: BernoulliState = self.s2_constructor.construct_partial_state(
            validated_input_dict=validated_input, 
            missing_variable_name=missing_variable,
            unfilled_sentinel=float('nan') 
        )

        # S3
        if missing_variable:
            logger.info("Step S3: Solving for missing variable.")
            solved_state: BernoulliState = self.s3_solver.solve_missing_variable(
                partial_state=partial_state, 
                config=config
            )
        else:
            logger.info("Step S3: Identity path (no missing variables).")
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

        # S4
        logger.info("Step S4: Computing energy residuals.")
        state_with_energy: BernoulliState = self.s4_diagnician.compute_energy_and_residual(
            solved_state=solved_state, 
            config=config
        )

        # S5
        logger.info("Step S5: Applying constraint envelopes.")
        final_state: BernoulliState = self.s5_enveloper.compute_min_max_constraints(
            state_with_energy=state_with_energy, 
            config=config
        )

        logger.info("Pipeline execution successfully completed.")
        return final_state


def run_solver(input_output_folder: str, input_file_name: str, output_file_name: str) -> str:
    """
    Main execution routine mapping absolute or relative workspace folders into runtime contexts.
    """
    folder_path = Path(input_output_folder)
    if not folder_path.is_absolute():
        folder_path = BASE_DIR / folder_path
    
    full_input_path = folder_path / input_file_name
    full_output_path = folder_path / output_file_name
    
    logger.info(f"Using workspace folder: {folder_path}")
    logger.info(f"Target Input Spec: {full_input_path.name}")
    
    required_paths = {
        "Input File": full_input_path,
        "Config File": BASE_DIR / "src/config/config.json",
        "Input Schema": BASE_DIR / "schema/bernoulli_input.schema.json",
        "Output Schema": BASE_DIR / "schema/bernoulli_output.schema.json"
    }

    for label, path in required_paths.items():
        if not path.exists():
            logger.critical(f"Missing dependency: {label} not found at {path}")
            raise FileNotFoundError(f"Missing dependency: {label} at {path}")

    config = load_and_validate_config(str(required_paths["Config File"]))
    logger.info("Configuration contract verified.")

    with open(full_input_path, "r", encoding="utf-8") as f:
        raw_input = json.load(f)

    with open(required_paths["Input Schema"], "r", encoding="utf-8") as f:
        input_schema = json.load(f)

    try:
        jsonschema.validate(instance=raw_input, schema=input_schema)
        logger.info("Input JSON schema validation passed.")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Input schema validation failed: {e.message}")
        raise

    orchestrator = BernoulliPipelineOrchestrator()
    final_state = orchestrator.execute_pipeline(raw_input, config)

    output_dict = asdict(final_state)
    with open(required_paths["Output Schema"], "r", encoding="utf-8") as f:
        output_schema = json.load(f)
    
    jsonschema.validate(instance=output_dict, schema=output_schema)
    
    with open(full_output_path, "w", encoding="utf-8") as f:
        json.dump(output_dict, f, indent=2)
    
    logger.info(f"Pipeline artifacts saved to: {full_output_path}")
    return str(full_output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Explicit execution harness mapping CI validation criteria into local workflows."
    )
    parser.add_argument(
        "--input_output_folder",
        type=str,
        required=True,
        help="Path to workspace target folder containing experimental datasets"
    )
    parser.add_argument(
        "--input_file_name",
        type=str,
        required=True,
        help="Name of the target raw parameters definition JSON instance"
    )
    parser.add_argument(
        "--output_file_name",
        type=str,
        required=True,
        help="Output path template target identifier"
    )
    
    args = parser.parse_args()

    try:
        output_json_path = run_solver(
            input_output_folder=args.input_output_folder,
            input_file_name=args.input_file_name,
            output_file_name=args.output_file_name
        )
        logger.info(f"Run successful. Output written to {output_json_path}")
        sys.exit(0)
    except Exception:
        # logger.exception automatically prints the stack trace for CI/CD logs
        logger.exception("FATAL PIPELINE ERROR: Unhandled exception during execution.")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()