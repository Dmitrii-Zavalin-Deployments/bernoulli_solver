from typing import Dict, Any
from src.config.config_interface import SolverConfig
from src.containers.bernoulli_state import BernoulliState

# Import the direct, concrete step implementations of the Minimal Step Chain
from src.steps.step_s0_filled_unfilled_classifier import StepS0FilledUnfilledClassifier
from src.steps.step_s1_exactly_one_missing import StepS1ExactlyOneMissing
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
from src.steps.step_s3_solve_missing_variable import StepS3SolveMissingVariable
from src.steps.step_s4_compute_energy_residual import StepS4ComputeEnergyResidual
from src.steps.step_s5_compute_min_max_constraints import StepS5ComputeMinMaxConstraints


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