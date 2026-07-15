import json
import pytest
from typing import get_type_hints

from src.interfaces.bernoulli_state_interface import BernoulliStateInterface
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from tests.signatures.schema_state_mapping_signature import SchemaStateMappingTestSignature

class TestSchemaStateMapping(SchemaStateMappingTestSignature):
    """
    Concrete implementation of the Schema → State mapping validation.
    """

    @pytest.fixture
    def state_interface_fields(self):
        """Returns the set of all fields defined in the BernoulliStateInterface."""
        return set(get_type_hints(BernoulliStateInterface).keys())

    @pytest.fixture
    def schema_fields(self):
        """Loads JSON schemas from disk and returns the set of fields."""
        with open("schema/bernoulli_input.schema.json", "r") as f:
            input_schema = json.load(f)
        with open("schema/bernoulli_output.schema.json", "r") as f:
            output_schema = json.load(f)

        # Input schema is flat
        input_fields = set(input_schema.get("properties", {}).keys())
        
        # Fixed: Extract and flatten output properties nested under 'inputs' and 'results'
        output_fields = set()
        out_props = output_schema.get("properties", {})
        for wrapper in ["inputs", "results"]:
            if wrapper in out_props:
                sub_props = out_props[wrapper].get("properties", {})
                output_fields.update(sub_props.keys())
                
        return input_fields, output_fields

    def test_all_schema_fields_map_to_state_fields(self, state_interface_fields, schema_fields):
        input_fields, output_fields = schema_fields
        all_schema_fields = input_fields | output_fields
        
        unmapped_fields = all_schema_fields - state_interface_fields
        assert not unmapped_fields, f"Schema fields found that do not map to the interface: {unmapped_fields}"

    def test_all_state_fields_are_covered_by_schemas(self, state_interface_fields, schema_fields):
        input_fields, output_fields = schema_fields
        all_schema_fields = input_fields | output_fields
        
        missing_fields = state_interface_fields - all_schema_fields
        assert not missing_fields, f"Interface fields missing from schemas: {missing_fields}"

    def test_no_duplicate_or_conflicting_mappings(self, schema_fields):
        input_fields, output_fields = schema_fields
        intersection = input_fields & output_fields
        
        # Primary variables, energy, and imbalance are expected to exist in both
        allowed_overlap = {'p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho', 'energy', 'energy_imbalance'}
        conflicts = intersection - allowed_overlap
        
        assert not conflicts, f"Conflicting field mappings detected (ambiguous origin): {conflicts}"

    def test_unified_state_container_is_schema_compatible(self, state_interface_fields):
        """
        Validates that the BernoulliStateDummy correctly implements the interface 
        without introducing unexpected structural drift.
        """
        dummy = BernoulliStateDummy()
        
        # 1. Verify existence
        for field in state_interface_fields:
            is_present = hasattr(dummy, field) or field in dummy
            assert is_present, f"Unified State Container (Dummy) is missing field: {field}"
            
        # 2. Verify structural drift (No unexpected extra fields)
        dummy_fields = set(dummy.keys()) | set(dummy.__dict__.keys())
        extra_fields = dummy_fields - state_interface_fields
        
        # Define internal helper artifacts to ignore
        expected_artifacts = {'_abc_impl', '__weakref__'} 
        ignore_methods = {'override', 'get_s1_compliant_state'}
        
        final_extra = extra_fields - expected_artifacts - ignore_methods
        
        assert not final_extra, f"Structural drift: Dummy contains undefined fields: {final_extra}"