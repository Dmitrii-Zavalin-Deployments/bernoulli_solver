import math
import logging
from typing import Any
from src.interfaces.step_interfaces.step_s3_solve_missing_variable_interface import StepS3SolveMissingVariableInterface
from src.containers.bernoulli_state import BernoulliState

# Configure module-level logger
logger = logging.getLogger(__name__)

class StepS3SolveMissingVariable(StepS3SolveMissingVariableInterface):
    """
    Concrete implementation of Step S3: Solve the missing Bernoulli primary variable.
    Includes diagnostic logging and arithmetic error handling for pipeline stability.
    """

    def solve_missing_variable(self, partial_state: BernoulliState, config: Any) -> BernoulliState:
        """
        Applies the appropriate rearranged form of Bernoulli's equation to 
        compute and fill the single missing primary variable with error handling.
        """
        primary_fields = ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]
        missing_field = next((field for field in primary_fields if math.isnan(getattr(partial_state, field))), None)
        
        if missing_field is None:
            raise ValueError("S3 Solver: No UNFILLED primary variables detected.")

        # Extract current numerical states
        p1, p2 = partial_state.p1, partial_state.p2
        v1, v2 = partial_state.v1, partial_state.v2
        h1, h2 = partial_state.h1, partial_state.h2
        rho = partial_state.rho
        g = config.g

        try:
            # Execute deterministic equation rearrangement
            if missing_field == "p1":
                p1 = p2 + 0.5 * rho * (v2**2 - v1**2) + rho * g * (h2 - h1)
            elif missing_field == "p2":
                p2 = p1 + 0.5 * rho * (v1**2 - v2**2) + rho * g * (h1 - h2)
            elif missing_field == "v1":
                radicand = v2**2 + (2.0 / rho) * (p2 - p1) + 2.0 * g * (h2 - h1)
                if radicand < 0:
                    raise ValueError(f"Non-physical negative radicand ({radicand}) for v1.")
                v1 = math.sqrt(radicand)
            elif missing_field == "v2":
                radicand = v1**2 + (2.0 / rho) * (p1 - p2) + 2.0 * g * (h1 - h2)
                if radicand < 0:
                    raise ValueError(f"Non-physical negative radicand ({radicand}) for v2.")
                v2 = math.sqrt(radicand)
            elif missing_field == "h1":
                h1 = h2 + (p2 - p1) / (rho * g) + (v2**2 - v1**2) / (2.0 * g)
            elif missing_field == "h2":
                h2 = h1 + (p1 - p2) / (rho * g) + (v1**2 - v2**2) / (2.0 * g)
            elif missing_field == "rho":
                denominator = 0.5 * (v2**2 - v1**2) + g * (h2 - h1)
                if denominator == 0:
                    raise ZeroDivisionError("Kinetic and potential head differentials cancel out.")
                rho = (p1 - p2) / denominator
                if rho <= 0:
                    raise ValueError(f"Calculated non-physical fluid density 'rho' ({rho}) <= 0.")

        except Exception as e:
            # Log the full context before re-raising
            error_msg = f"Numerical solver failure at field '{missing_field}': {str(e)}"
            logger.error(error_msg, exc_info=True) 
            raise ValueError(error_msg) from e

        # Construct the Sovereign Container
        # We propagate existing constraints and update initial conditions with solved values
        return BernoulliState(
            p1=p1, p2=p2, v1=v1, v2=v2, h1=h1, h2=h2, rho=rho,
            energy=partial_state.energy, 
            energy_imbalance=partial_state.energy_imbalance,
            initial_conditions={
                "velocity": [v1, 0.0, 0.0],
                "pressure": p1
            },
            physical_constraints=partial_state.physical_constraints
        )