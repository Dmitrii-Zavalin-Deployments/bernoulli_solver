from typing import Dict, Any, Tuple
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface

class ValidationError(ValueError):
    """
    Project-specific validation exception raised when the structural structural 
    invariants of the input stream fail to pass the S1 gatekeeper requirements.
    """
    pass

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
        
        # 1. Enforce Excess Field Validation: Ensure no unexpected fields exist
        input_keys = set(raw_input_dict.keys())
        unexpected_keys = input_keys - primary_universe
        if unexpected_keys:
            raise ValidationError(
                f"Contract-Validation failed: Unexpected fields present in input: {unexpected_keys}. "
                f"Excess or convenience fields are strictly prohibited."
            )
            
        # 2. Determine which primary fields are structurally present and active
        present_fields = {
            field for field in primary_universe 
            if field in raw_input_dict and raw_input_dict[field] is not None
        }
        
        # 3. Determine missing primary variables
        missing_fields = primary_universe - present_fields
        missing_count = len(missing_fields)
        
        # 4. Enforce the exactly-one-missing invariant rules
        if missing_count == 0:
            raise ValidationError(
                "Contract-Validation failed: Zero primary variables are missing. "
                "The solver requires exactly one variable to be unfilled."
            )
        elif missing_count > 1:
            raise ValidationError(
                f"Contract-Validation failed: More than one primary variable is missing: {missing_fields}. "
                f"The solver requires exactly one missing variable to operate."
            )
            
        # Extract the singular valid missing variable name
        missing_variable_name = next(iter(missing_fields))
        
        # Return the raw input completely unchanged along with the extracted string token
        return raw_input_dict, missing_variable_name