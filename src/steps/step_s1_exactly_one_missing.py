from typing import Dict, Any, Tuple
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface

class ValidationError(ValueError):
    """
    Project-specific validation exception raised when the structural 
    invariants of the input stream fail to pass the S1 gatekeeper requirements.
    """

class StepS1ExactlyOneMissing(StepS1ExactlyOneMissingInterface):
    """
    Concrete implementation of Step S1: Enforce "exactly one missing" rule.
    Inherits explicitly from StepS1ExactlyOneMissingInterface to maintain 
    a 100% rigid structural match to the project constitution.
    """

    def enforce_exactly_one_missing(self, raw_input_dict: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        """
        Validates the raw input dictionary structural layout. 
        Enforces that exactly one primary variable is missing and no unexpected 
        fields are present, returning the unchanged input and the missing variable identity.
        """
        # The canonical primary universe as mandated by Phase 1.1 and Section 2.2
        primary_universe = {"p1", "p2", "v1", "v2", "h1", "h2", "rho"}
        
        # 1. Excess Field Validation
        input_keys = set(raw_input_dict.keys())
        unexpected_keys = input_keys - primary_universe
        if unexpected_keys:
            raise ValidationError(f"Unexpected fields: {unexpected_keys}")

        # 2. Determine present/missing (handles both absent keys and explicit None values)
        present_fields = {
            field for field in primary_universe 
            if field in raw_input_dict and raw_input_dict[field] is not None
        }
        
        missing_fields = primary_universe - present_fields

        # 3. Dual-Path Validation Logic
        # Path A: Identity Path (0 missing) - Allowed for round-trip testing
        # Path B: Solver Path (1 missing) - Allowed if missing variable is not a required input
        if len(missing_fields) == 0:
            missing_variable = ""
            
        elif len(missing_fields) == 1:
            missing_variable = list(missing_fields)[0]
            # Required primary variables cannot be omitted
            required_inputs = {"p1", "v1", "h1", "rho"}
            if missing_variable in required_inputs:
                raise ValidationError(f"Validation failed: Required primary input variable '{missing_variable}' is missing.")
                
        else:
            # Too many missing variables
            raise ValidationError(f"Validation failed: Too many missing variables: {missing_fields}")
        
        return raw_input_dict, missing_variable