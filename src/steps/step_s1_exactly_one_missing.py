from typing import Dict, Any, Tuple
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface

class ValidationError(ValueError):
    """Exception raised for structural validation failures."""
    pass

class StepS1ExactlyOneMissing(StepS1ExactlyOneMissingInterface):
    """
    Implementation of Step S1: Enforce "exactly one missing" rule.
    Strictly adheres to the contract: exactly one missing field required.
    """

    def enforce_exactly_one_missing(self, raw_input_dict: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        # The canonical primary universe
        primary_universe = {"p1", "p2", "v1", "v2", "h1", "h2", "rho"}
        
        # 1. Check for unexpected fields
        input_keys = set(raw_input_dict.keys())
        unexpected = input_keys - primary_universe
        if unexpected:
            raise ValidationError(f"Unexpected fields present: {unexpected}")
        
        # 2. Determine missing fields
        # Note: We assume fields present in the dict are 'present'
        missing = primary_universe - input_keys
        
        # 3. Enforce contract: Exactly one missing
        if len(missing) == 1:
            return raw_input_dict, list(missing)[0]
        else:
            raise ValidationError(f"Validation failed: Expected 1 missing variable, found {len(missing)}: {missing}")