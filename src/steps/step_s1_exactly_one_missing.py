from typing import Dict, Any, Tuple
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface

class ValidationError(ValueError):
    """Structural validation failure."""

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
        
        # 1. Check for unexpected fields
        input_keys = set(raw_input_dict.keys())
        unexpected_keys = input_keys - primary_universe
        if unexpected_keys:
            raise ValidationError(f"Unexpected fields: {unexpected_keys}")

        # 2. Determine missing fields (Handles absent keys AND None values)
        present_fields = {
            field for field in primary_universe 
            if field in raw_input_dict and raw_input_dict[field] is not None
        }
        
        missing_fields = primary_universe - present_fields

        missing_variable = ""
        if len(missing_fields) == 0:
            missing_variable = ""
        elif len(missing_fields) == 1:
            missing_variable = list(missing_fields)[0]
        else:
            # Too many missing variables
            raise ValidationError(f"Validation failed: Too many missing variables: {missing_fields}")
        
        return raw_input_dict, missing_variable
