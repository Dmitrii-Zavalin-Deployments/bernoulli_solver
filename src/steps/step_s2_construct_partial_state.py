import math
from typing import Any

from src.containers.bernoulli_state import BernoulliState
from src.interfaces.step_interfaces.step_s2_construct_partial_state_interface import (
    StepS2ConstructPartialStateInterface,
)


class StepS2ConstructPartialState(StepS2ConstructPartialStateInterface):
    """
    Concrete implementation of Step S2: Construct BernoulliState (partial).
    Inherits explicitly from StepS2ConstructPartialStateInterface to guarantee 
    a 100% structural match of the core code to the constitution.
    """

    def construct_partial_state(
        self, 
        validated_input_dict: dict[str, Any], 
        missing_variable_name: str, 
        unfilled_sentinel: Any
    ) -> BernoulliState:
        """
        Constructs a structurally complete BernoulliState instance (Sovereign Container).
        
        Maps all verified active input fields directly into the container. Forces the 
        isolated missing primary variable and all diagnostic/execution-derived fields 
        to the uniform unfilled sentinel state.
        """
        # [Validation Gate - Computational Sanity Check]
        # Ensures all active primary variables are mathematically finite, 
        # protecting the solver from NaNs and Inf while allowing physical extremes.
        for key in ["p1", "p2", "v1", "v2", "rho"]:
            if missing_variable_name != key and validated_input_dict.get(key) is not None:
                val = validated_input_dict[key]
                if not math.isfinite(val):
                    raise ValueError(f"Invalid input: {key} must be a finite number (got {val})")

        # Canonical primary variables universe
        primary_fields = ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]
        
        # Build assignment arguments for primary variables
        assigned_values = {}
        for field in primary_fields:
            if field == missing_variable_name:
                assigned_values[field] = unfilled_sentinel
            else:
                # Direct extraction of values verified and passed through the S1 gatekeeper
                assigned_values[field] = validated_input_dict[field]

        # Populate diagnostic and execution-derived fields with the sentinel.
        # Since the pure BernoulliState container strictly type-annotates 'energy' 
        # as a List[float], we initialize its elements with the sentinel to remain type-safe.
        assigned_values["energy"] = [unfilled_sentinel, unfilled_sentinel]
        assigned_values["energy_imbalance"] = unfilled_sentinel
        assigned_values["p_min"] = unfilled_sentinel
        assigned_values["p_max"] = unfilled_sentinel
        assigned_values["v_min"] = unfilled_sentinel
        assigned_values["v_max"] = unfilled_sentinel

        # Define the structural dictionaries for the Sovereign Container
        physical_constraints = {
            "min_pressure": assigned_values["p_min"],
            "max_pressure": assigned_values["p_max"],
            "min_velocity": assigned_values["v_min"],
            "max_velocity": assigned_values["v_max"]
        }

        initial_conditions = {
            "velocity": [assigned_values["v1"], 0.0, 0.0],
            "pressure": assigned_values["p1"]
        }

        # Return the pristine, logic-free Sovereign Container
        return BernoulliState(
            p1=assigned_values["p1"],
            p2=assigned_values["p2"],
            v1=assigned_values["v1"],
            v2=assigned_values["v2"],
            h1=assigned_values["h1"],
            h2=assigned_values["h2"],
            rho=assigned_values["rho"],
            energy=assigned_values["energy"],
            energy_imbalance=assigned_values["energy_imbalance"],
            initial_conditions=initial_conditions,
            physical_constraints=physical_constraints
        )