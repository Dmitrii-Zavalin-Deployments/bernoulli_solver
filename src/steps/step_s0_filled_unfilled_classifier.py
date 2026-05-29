from typing import Set, Tuple
from src.interfaces.step_interfaces.step_s0_filled_unfilled_classifier_interface import FilledUnfilledClassifierInterface

class StepS0FilledUnfilledClassifier(FilledUnfilledClassifierInterface):
    """
    Concrete implementation of the FilledUnfilledClassifier step.
    Inherits explicitly from FilledUnfilledClassifierInterface to ensure
    a 100% rigid match of the core code to the constitution.
    """

    def classify_filled_and_unfilled(self, input_schema_instance) -> Tuple[Set[str], Set[str]]:
        """
        Given an input schema instance, return two sets: filled_fields and unfilled_fields.
        
        This structural operation performs zero validation, assigns no defaults or nulls,
        and never creates or mutates container states.
        """
        # Define the strict structural scopes defined in Section 2.1 of the Constitution
        primary_universe = {"p1", "p2", "v1", "v2", "h1", "h2", "rho"}
        derived_universe = {"energy", "energy_imbalance", "p_min", "p_max", "v_min", "v_max"}
        
        # Categorize fields that are structurally present and active in the input instance
        filled_fields = {
            field for field in primary_universe 
            if field in input_schema_instance and input_schema_instance[field] is not None
        }
        
        # Unfilled includes the missing primary fields plus all execution-derived fields
        missing_primary = primary_universe - filled_fields
        unfilled_fields = missing_primary | derived_universe
        
        return filled_fields, unfilled_fields