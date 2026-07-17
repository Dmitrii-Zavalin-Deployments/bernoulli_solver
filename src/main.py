import argparse
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any

import jsonschema
import numpy as np

# Import your custom modules
from config.config_interface import SolverConfig
from config.config_loader import load_and_validate_config
from src.containers.bernoulli_state import BernoulliState
from src.steps.step_s0_filled_unfilled_classifier import FilledUnfilledClassifier
from src.steps.step_s1_exactly_one_missing import StepS1ExactlyOneMissing
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
from src.steps.step_s3_solve_missing_variable import StepS3SolveMissingVariable
from src.steps.step_s4_compute_energy_residual import StepS4ComputeEnergyResidual
from src.steps.step_s5_compute_min_max_constraints import StepS5ComputeMinMaxConstraints

# Rule 5: Force global arithmetic trapping for deterministic stability
np.seterr(all="raise")

# Initialize module-level logger
logger = logging.getLogger(__name__)

def setup_logging(level=logging.INFO):
    """Configures logging format for terminal and CI/CD output."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

BASE_DIR = Path(__file__).resolve().parent.parent


class BernoulliPipelineOrchestrator:
    def __init__(self) -> None:
        logger.debug("Initializing BernoulliPipelineOrchestrator components.")
        self.s0_classifier = FilledUnfilledClassifier()
        self.s1_validator = StepS1ExactlyOneMissing()
        self.s2_constructor = StepS2ConstructPartialState()
        self.s3_solver = StepS3SolveMissingVariable()
        self.s4_diagnician = StepS4ComputeEnergyResidual()
        self.s5_enveloper = StepS5ComputeMinMaxConstraints()
        logger.info("Pipeline components instantiated successfully.")

    def _validate_boundaries(self, raw_input: Dict[str, Any]) -> None:
        logger.debug("Executing pre-flight boundary validation.")
        p1, p2 = raw_input.get("p1"), raw_input.get("p2")
        if (p1 is not None and p1 < 0) or (p2 is not None and p2 < 0):
            logger.error(f"Boundary validation failed: Negative pressure detected (p1={p1}, p2={p2}).")
            raise ValueError("Negative pressure detected.")

        v1, v2 = raw_input.get("v1"), raw_input.get("v2")
        if (v1 is not None and abs(v1) > 1e6) or (v2 is not None and abs(v2) > 1e6):
            logger.error(f"Boundary validation failed: Velocity exceeds physical limits (v1={v1}, v2={v2}).")
            raise ValueError("Velocity exceeds physical limits.")
        logger.debug("Pre-flight boundary validation passed.")

    def execute_pipeline(self, raw_input: Dict[str, Any], config: SolverConfig) -> BernoulliState:
        logger.info("Starting pipeline execution.")
        
        if config is None:
            logger.critical("Configuration object is None. Pipeline aborted.")
            raise TypeError("Configuration object is mandatory.")

        self._validate_boundaries(raw_input)
        
        # S0 & S1
        logger.debug("S0/S1: Classifying input.")
        _, _ = self.s0_classifier.classify_filled_and_unfilled(input_schema_instance=raw_input)
        validated_input, missing_variable = self.s1_validator.enforce_exactly_one_missing(raw_input_dict=raw_input)
        logger.info(f"S1 Validation complete. Solving for: {missing_variable if missing_variable else 'Identity'}")

        # S2
        logger.debug("S2: Constructing state container.")
        partial_state: BernoulliState = self.s2_constructor.construct_partial_state(
            validated_input_dict=validated_input, 
            missing_variable_name=missing_variable,
            unfilled_sentinel=float('nan') 
        )

        # S3
        if missing_variable:
            logger.info("S3: Solving for missing variable.")
            solved_state: BernoulliState = self.s3_solver.solve_missing_variable(partial_state=partial_state, config=config)
        else:
            logger.info("S3: Identity path (no missing variables).")
            p1, p2, v1, v2, h1, h2, rho = partial_state.p1, partial_state.p2, partial_state.v1, partial_state.v2, partial_state.h1, partial_state.h2, partial_state.rho
            e1 = p1 + 0.5 * rho * (v1 ** 2) + rho * config.g * h1
            e2 = p2 + 0.5 * rho * (v2 ** 2) + rho * config.g * h2

            solved_state = BernoulliState(
                p1=p1, p2=p2, v1=v1, v2=v2, h1=h1, h2=h2, rho=rho,
                energy=[e1, e2], energy_imbalance=abs(e1 - e2),
                p_min=min(p1, p2), p_max=max(p1, p2),
                v_min=min(v1, v2), v_max=max(v1, v2)
            )

        # S4 & S5
        logger.debug("S4: Computing residuals.")
        state_with_energy = self.s4_diagnician.compute_energy_and_residual(solved_state=solved_state, config=config)
        
        logger.debug("S5: Applying constraint envelopes.")
        final_state = self.s5_enveloper.compute_min_max_constraints(state_with_energy=state_with_energy, config=config)

        logger.info("Pipeline execution successfully completed.")
        return final_state


def run_solver(input_output_folder: str, input_file_name: str, output_file_name: str) -> str:
    folder_path = Path(input_output_folder)
    if not folder_path.is_absolute():
        folder_path = BASE_DIR / folder_path
    
    full_input_path = folder_path / input_file_name
    full_output_path = folder_path / output_file_name
    
    logger.info(f"Workspace initialized at: {folder_path}")
    
    required_paths = {
        "Input File": full_input_path,
        "Config File": BASE_DIR / "config/config.json",
        "Input Schema": BASE_DIR / "schema/bernoulli_input.schema.json",
        "Output Schema": BASE_DIR / "schema/bernoulli_output.schema.json"
    }

    # Verify Paths
    for label, path in required_paths.items():
        if not path.exists():
            logger.critical(f"Missing dependency: {label} not found at {path}")
            raise FileNotFoundError(f"Missing dependency: {label} at {path}")

    # Load Config (Strict load of parsed Dataclass contract)
    config = load_and_validate_config(str(required_paths["Config File"]))
    logger.info("Configuration loaded and validated.")

    # Load and Validate Input
    with open(full_input_path, "r", encoding="utf-8") as f:
        raw_input = json.load(f)
    logger.debug("Input JSON loaded.")

    with open(required_paths["Input Schema"], "r", encoding="utf-8") as f:
        input_schema = json.load(f)

    try:
        jsonschema.validate(instance=raw_input, schema=input_schema)
        logger.info("Input schema validation passed.")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Input schema validation failed: {e.message}")
        raise

    # Execute
    orchestrator = BernoulliPipelineOrchestrator()
    final_state = orchestrator.execute_pipeline(raw_input, config)

    # Export (No extra injections required as config and output schema are fully aligned)
    try:
        config_dict = asdict(config)
    except TypeError:
        # Fallback if config isn't declared a Dataclass (safeguard)
        config_dict = {
            "g": config.g,
            "precision": config.precision,
            "k_v_min": config.k_v_min,
            "k_v_max": config.k_v_max,
            "k_p_min": config.k_p_min,
            "k_p_max": config.k_p_max,
        } if hasattr(config, "g") else {}

    output_dict = {
        "inputs": raw_input,
        "config": config_dict,
        "results": asdict(final_state)
    }

    with open(required_paths["Output Schema"], "r", encoding="utf-8") as f:
        output_schema = json.load(f)
    
    jsonschema.validate(instance=output_dict, schema=output_schema)
    logger.debug("Output schema validation passed.")
    
    with open(full_output_path, "w", encoding="utf-8") as f:
        json.dump(output_dict, f, indent=2)
    
    logger.info(f"Pipeline artifacts saved to: {full_output_path}")
    return str(full_output_path)


def main():
    setup_logging()
    
    # Log raw arguments using the logger
    logger.info(f"CLI arguments received -> {sys.argv}")
    
    parser = argparse.ArgumentParser(description="Bernoulli Pipeline Orchestrator")
    parser.add_argument("--input_output_folder", required=True, help="Path to input/output folder")
    parser.add_argument("--input_file_name", required=True, help="Input JSON file name")
    parser.add_argument("--output_file_name", required=True, help="Output JSON file name")
    
    try:
        # We try to parse arguments
        args = parser.parse_args()
    except SystemExit as e:
        # If argparse fails (exit code 2), we capture it in our logs first
        logger.error(f"CLI Argument parsing failed. Ensure all required arguments are passed. SystemExit code: {e.code}")
        # Re-raise the exit to maintain the correct exit code behavior
        sys.exit(e.code)

    try:
        output_json_path = run_solver(
            args.input_output_folder, 
            args.input_file_name, 
            args.output_file_name
        )
        logger.info(f"Run successful. Output: {output_json_path}")
        sys.exit(0)
    except Exception:
        logger.exception("FATAL PIPELINE ERROR")
        sys.exit(1)

if __name__ == "__main__":  # pragma: no cover
    main()