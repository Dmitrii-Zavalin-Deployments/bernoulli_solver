import json
from pathlib import Path
from typing import get_type_hints
from src.containers.bernoulli_state import BernoulliState
from tests.signatures.excess_field_validation_signature import ExcessFieldValidationTestSignature

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_SCHEMA = BASE_DIR / "schema/bernoulli_input.schema.json"
OUTPUT_SCHEMA = BASE_DIR / "schema/bernoulli_output.schema.json"

# Defined Constitutional Sets
PRIMARY_FIELDS = {"p1", "p2", "v1", "v2", "h1", "h2", "rho"}
OUTPUT_FIELDS = PRIMARY_FIELDS | {"energy", "energy_imbalance", "p_min", "p_max", "v_min", "v_max"}

class TestExcessFieldValidation(ExcessFieldValidationTestSignature):
    """
    Concrete implementation of ExcessFieldValidationTestSignature.
    Enforces the 'No Entropy' rule by detecting unauthorized field additions.
    """

    def test_input_has_no_extra_fields(self):
        with open(INPUT_SCHEMA, 'r') as f:
            properties = json.load(f).get("properties", {})
        
        # Identify any key in the schema NOT in the allowed primary set
        extra_fields = set(properties.keys()) - PRIMARY_FIELDS
        assert not extra_fields, f"CONSTITUTIONAL VIOLATION: Unauthorized input fields detected: {extra_fields}"

    def test_output_has_no_extra_fields(self):
        with open(OUTPUT_SCHEMA, 'r') as f:
            properties = json.load(f).get("properties", {})
        
        # Identify any key in the schema NOT in the allowed output set
        extra_fields = set(properties.keys()) - OUTPUT_FIELDS
        assert not extra_fields, f"CONSTITUTIONAL VIOLATION: Unauthorized output fields detected: {extra_fields}"

    def test_state_interface_allows_no_undefined_fields(self):
        # Inspect the Dataclass fields directly
        state_fields = set(get_type_hints(BernoulliState).keys())
        
        # Identify any field in the class NOT in the allowed output set
        extra_fields = state_fields - OUTPUT_FIELDS
        assert not extra_fields, f"CONSTITUTIONAL VIOLATION: Unauthorized fields found in BernoulliState: {extra_fields}"