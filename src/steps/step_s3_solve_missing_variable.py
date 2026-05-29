import math
from typing import Any
from src.interfaces.step_interfaces.step_s3_solve_missing_variable_interface import StepS3SolveMissingVariableInterface
from src.containers.bernoulli_state import BernoulliState

class StepS3SolveMissingVariable(StepS3SolveMissingVariableInterface):
    """
    Concrete implementation of Step S3: Solve the missing Bernoulli primary variable.
    Inherits explicitly from StepS3SolveMissingVariableInterface to enforce 
    a 100% rigid match to the project constitution.
    """

    def solve_missing_variable(self, partial_state: BernoulliState, config: Any) -> BernoulliState:
        """
        Applies the appropriate rearranged form of Bernoulli's equation to 
        compute and fill the single missing primary variable.
        
        Returns a brand NEW BernoulliState instance leaving all diagnostic and 
        constraint fields untouched (UNFILLED).
        """
        # Define the primary universe scope to locate the unfilled field
        primary_fields = ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]
        missing_field = None
        
        for field in primary_fields:
            if math.isnan(getattr(partial_state, field)):
                missing_field = field
                break
                
        if missing_field is None:
            raise ValueError(
                "Numerical solver execution failed: Step S3 expected exactly one "
                "UNFILLED primary variable inside the Sovereign Container, but none were detected."
            )

        # Extract current numerical states
        p1 = partial_state.p1
        p2 = partial_state.p2
        v1 = partial_state.v1
        v2 = partial_state.v2
        h1 = partial_state.h1
        h2 = partial_state.h2
        rho = partial_state.rho
        
        # Read environmental constants from the injected runtime config
        g = config.g

        # Execute deterministic equation rearrangement matching the identified missing key
        if missing_field == "p1":
            p1 = p2 + 0.5 * rho * (v2**2 - v1**2) + rho * g * (h2 - h1)
            
        elif missing_field == "p2":
            p2 = p1 + 0.5 * rho * (v1**2 - v2**2) + rho * g * (h1 - h2)
            
        elif missing_field == "v1":
            # Rearrangement: v1^2 = v2^2 + (2/rho)*(p2 - p1) + 2*g*(h2 - h1)
            radicand = v2**2 + (2.0 / rho) * (p2 - p1) + 2.0 * g * (h2 - h1)
            if radicand < 0:
                raise ValueError(
                    f"Numerical solver error: Non-physical negative radicand ({radicand}) "
                    f"encountered while attempting to solve for velocity 'v1'."
                )
            v1 = math.sqrt(radicand)
            
        elif missing_field == "v2":
            # Rearrangement: v2^2 = v1^2 + (2/rho)*(p1 - p2) + 2*g*(h1 - h2)
            radicand = v1**2 + (2.0 / rho) * (p1 - p2) + 2.0 * g * (h1 - h2)
            if radicand < 0:
                raise ValueError(
                    f"Numerical solver error: Non-physical negative radicand ({radicand}) "
                    f"encountered while attempting to solve for velocity 'v2'."
                )
            v2 = math.sqrt(radicand)
            
        elif missing_field == "h1":
            h1 = h2 + (p2 - p1) / (rho * g) + (v2**2 - v1**2) / (2.0 * g)
            
        elif missing_field == "h2":
            h2 = h1 + (p1 - p2) / (rho * g) + (v1**2 - v2**2) / (2.0 * g)
            
        elif missing_field == "rho":
            denominator = 0.5 * (v2**2 - v1**2) + g * (h2 - h1)
            if denominator == 0:
                raise ValueError(
                    "Numerical solver error: Division by zero encountered while calculating 'rho'. "
                    "Kinetic and potential head differentials cancel out perfectly."
                )
            rho = (p1 - p2) / denominator
            if rho <= 0:
                raise ValueError(
                    f"Numerical solver error: Calculated non-physical fluid density 'rho' ({rho}) <= 0."
                )

        # Yield a completely fresh Sovereign Container instance ensuring no in-place mutation
        return BernoulliState(
            p1=p1,
            p2=p2,
            v1=v1,
            v2=v2,
            h1=h1,
            h2=h2,
            rho=rho,
            energy=partial_state.energy,
            energy_imbalance=partial_state.energy_imbalance,
            p_min=partial_state.p_min,
            p_max=partial_state.p_max,
            v_min=partial_state.v_min,
            v_max=partial_state.v_max
        )