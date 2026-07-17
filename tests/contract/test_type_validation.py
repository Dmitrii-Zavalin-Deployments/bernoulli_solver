import json
from pathlib import Path
from typing import get_type_hints, get_origin
from src.containers.bernoulli_state import BernoulliState
from tests.signatures.type_validation_signature import TypeValidationTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

# Resolve paths to schema definitions
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_SCHEMA_PATH = BASE_DIR / "schema/bernoulli_input.schema.json"
OUTPUT_SCHEMA_PATH = BASE_DIR / "schema/bernoulli_output.schema.json"

# Type mapping for schema verification
TYPE_MAPPING = {
    "number": float,
    "integer": int,
    "array": list,
    "string": str
}

class TestTypeValidation(TypeValidationTestSignature):
    """
    Concrete implementation of the TypeValidationTestSignature.
    This suite acts as the constitutional gatekeeper for BernoulliState types,
    dynamically verifying against the BernoulliStateDummy.
    """

    def test_input_schema_field_types(self):
        with open(INPUT_SCHEMA_PATH, 'r') as f:
            schema = json.load(f)
        
        type_hints = get_type_hints(BernoulliState)
        properties = schema.get("properties", {})

        for field, schema_def in properties.items():
            assert field in type_hints, f"Schema field '{field}' is missing from BernoulliState definition."
            
            expected_type = TYPE_MAPPING.get(schema_def["type"])
            # Normalize generic types (e.g., List[float]) to their origin (list)
            actual_type = get_origin(type_hints[field]) or type_hints[field]
            
            assert actual_type == expected_type, \
                f"Type mismatch for input field '{field}': Expected {expected_type}, got {type_hints[field]}"

    def test_output_schema_field_types(self):
        with open(OUTPUT_SCHEMA_PATH, 'r') as f:
            schema = json.load(f)
        
        type_hints = get_type_hints(BernoulliState)
        schema_props = schema.get("properties", {})

        # Fixed: Extract properties dynamically nested under 'inputs' and 'results'
        # to avoid mismatch with structural wrapper fields.
        properties = {}
        for wrapper in ["inputs", "results"]:
            if wrapper in schema_props:
                sub_props = schema_props[wrapper].get("properties", {})
                properties.update(sub_props)

        for field, schema_def in properties.items():
            assert field in type_hints, f"Schema field '{field}' is missing from BernoulliState definition."
            
            expected_type = TYPE_MAPPING.get(schema_def["type"])
            # Normalize generic types (e.g., List[float]) to their origin (list)
            actual_type = get_origin(type_hints[field]) or type_hints[field]
            
            assert actual_type == expected_type, \
                f"Type mismatch for output field '{field}': Expected {expected_type}, got {type_hints[field]}"

    def test_state_interface_type_completeness(self):
        """
        Dynamically verifies that BernoulliState implements the exact fields
        defined by the BernoulliStateDummy interface.
        """
        type_hints = get_type_hints(BernoulliState)
        dummy = BernoulliStateDummy()
        
        # Define fields from the dummy's structure
        primary_fields = set(dummy.keys())
        # Extra fields are instance attributes in the dummy
        extra_fields = {'energy', 'energy_imbalance', 'initial_conditions', 'physical_constraints'}
        
        required_fields = primary_fields | extra_fields
        
        # 1. Verify existence of all required fields
        for field in required_fields:
            assert field in type_hints, f"Constitutional failure: Missing mandatory field '{field}' in BernoulliState."
            
        # 2. Verify no unauthorized/convenience fields (Strict Compliance)
        for field in type_hints:
            assert field in required_fields, f"Constitutional failure: Unauthorized field '{field}' detected in BernoulliState."