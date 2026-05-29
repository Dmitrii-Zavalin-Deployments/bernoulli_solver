import json
import logging
import sys
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any

import jsonschema
import numpy as np

# Rule 5: Force global arithmetic trapping for deterministic stability
np.seterr(all="raise")

from src.config.config_interface import SolverConfig
from src.config.config_loader import load_and_validate_config
from src.containers.bernoulli_state import BernoulliState

# Import the direct, concrete step implementations of the Minimal Step Chain
from src.steps.step_s0_filled_unfilled_classifier import StepS0FilledUnfilledClassifier
from src.steps.step_s1_exactly_one_missing import StepS1ExactlyOneMissing
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
from src.steps.step_s3_solve_missing_variable import StepS3SolveMissingVariable
from src.steps.step_s4_compute_energy_residual import StepS4ComputeEnergyResidual
from src.steps.step_s5_compute_min_max_constraints import StepS5ComputeMinMaxConstraints

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

    def execute_pipeline(self, raw_input: Dict[str, Any], config: SolverConfig) -> BernoulliState:
        """
        Executes the full chain sequentially (S0 -> S1 -> S2 -> S3 -> S4 -> S5).
        
        Inputs:
            raw_input: Dict[str, Any]
                The raw input matching fields defined in the input schema.
            config: SolverConfig
                The runtime validated internal configuration instance.
                
        Returns:
            final_state: BernoulliState
                The fully completed Sovereign Container satisfying the Output Schema.
        """
        
        # --- Step S0: Classify Filled vs Unfilled Fields ---
        # Breaks circular dependency between raw validation and container construction.
        filled_fields, unfilled_fields = self.s0_classifier.classify_fields(raw_input)

        # --- Step S1: Enforce "Exactly One Missing" Rule ---
        # Quality Gate verifying structural schema rules. Returns target identity key.
        validated_input, missing_variable = self.s1_validator.enforce_one_missing_rule(
            raw_input=raw_input, 
            filled_fields=filled_fields, 
            unfilled_fields=unfilled_fields
        )

        # --- Step S2: Construct Partial State ---
        # Builds the initial Sovereign Container mapping sentinels to unresolved parameters.
        partial_state: BernoulliState = self.s2_constructor.construct_partial_state(
            validated_input=validated_input, 
            missing_variable=missing_variable
        )

        # --- Step S3: Solve Missing Bernoulli Primary Variable ---
        # Applies deterministic physical formulas to evaluate the unpopulated state field.
        solved_state: BernoulliState = self.s3_solver.solve_missing_variable(
            partial_state=partial_state, 
            config=config
        )

        # --- Step S4: Compute Energy and Residuals ---
        # Builds non-leakage internal verification diagnostics without altering primary steps.
        state_with_energy: BernoulliState = self.s4_diagnician.compute_energy_and_residual(
            solved_state=solved_state, 
            config=config
        )

        # --- Step S5: Compute Min/Max Constraints Envelopes ---
        # Maps industrial-grade tuning looseness coefficients to export final boundaries.
        final_state: BernoulliState = self.s5_enveloper.compute_min_max_constraints(
            state_with_energy=state_with_energy, 
            config=config
        )

        # Return the completely resolved, immutable Sovereign Container mapping
        return final_state


def run_solver(input_path: str) -> str:
    """
    Main execution routine handling file input/output lifecycle, schema compliance,
    and state injection mapping.
    """
    full_input_path = Path(input_path)
    if not full_input_path.is_absolute():
        full_input_path = BASE_DIR / input_path

    if not full_input_path.exists():
        raise FileNotFoundError(f"Input file missing at absolute path location: {full_input_path}")

    # 1. Acquire and validate the physical parameter layout contract at startup
    config_json_path = BASE_DIR / "src/config/config.json"
    config = load_and_validate_config(str(config_json_path))
    logger.info("Configuration contract verified and locked into internal scope.")

    # 2. Extract the incoming raw simulation parameters
    with open(full_input_path, "r", encoding="utf-8") as f:
        raw_input = json.load(f)

    # 3. Quality Gate: Validate incoming input data payload structure against JSON Schema
    input_schema_path = BASE_DIR / "schema/bernoulli_input.schema.json"
    if not input_schema_path.exists():
        raise FileNotFoundError(f"Input schema schema definitions missing at: {input_schema_path}")

    with open(input_schema_path, "r", encoding="utf-8") as f:
        input_schema = json.load(f)

    try:
        jsonschema.validate(instance=raw_input, schema=input_schema)
        logger.info("Input packet matches structural specifications of bernoulli_input.schema.json")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"!!! INPUT CONTRACT VIOLATION: {e.message}")
        raise

    # 4. Instantiate components and process data through the DAG
    orchestrator = BernoulliPipelineOrchestrator()
    final_state = orchestrator.execute_pipeline(raw_input, config)
    logger.info("Sovereign execution loop evaluated without precision exceptions.")

    # 5. Extract structural mapping from Sovereign Container dataclass 
    output_dict = asdict(final_state)

    # 6. Quality Gate: Validate output payload dictionary structure against JSON Schema
    output_schema_path = BASE_DIR / "schema/bernoulli_output.schema.json"
    if not output_schema_path.exists():
        raise FileNotFoundError(f"Output schema definitions missing at: {output_schema_path}")

    with open(output_schema_path, "r", encoding="utf-8") as f:
        output_schema = json.load(f)

    try:
        jsonschema.validate(instance=output_dict, schema=output_schema)
        logger.info("Output contract verified against bernoulli_output.schema.json rules.")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"!!! OUTPUT STATE CONTRACT VIOLATION: {e.message}")
        raise

    # 7. Write finalized output back to the specific directory where input lives
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