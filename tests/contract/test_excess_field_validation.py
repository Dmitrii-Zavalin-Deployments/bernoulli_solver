import json
from pathlib import Path
from typing import get_type_hints

from src.containers.bernoulli_state import BernoulliState
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from tests.signatures.excess_field_validation_signature import (
    ExcessFieldValidationTestSignature,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_SCHEMA = BASE_DIR / "schema/bernoulli_input.schema.json"
OUTPUT_SCHEMA = BASE_DIR / "schema/bernoulli_output.schema.json"

# Defined Constitutional Sets
PRIMARY_FIELDS = {"p1", "p2", "v1", "v2", "h1", "h2", "rho"}
OUTPUT_FIELDS = PRIMARY_FIELDS | {"energy", "energy_imbalance", "initial_conditions", "physical_constraints"}

class TestExcessFieldValidation(ExcessFieldValidationTestSignature):
    """
    Concrete implementation of ExcessFieldValidationTestSignature.
    Enforces the 'No Entropy' rule by detecting unauthorized field additions.
    """

    def test_input_has_no_extra_fields(self):
        with open(INPUT_SCHEMA, 'r') as f:
            properties = json.load(f).get("properties", {})
        
        extra_fields = set(properties.keys()) - PRIMARY_FIELDS
        assert not extra_fields, f"CONSTITUTIONAL VIOLATION: Unauthorized input fields detected: {extra_fields}"

    def test_output_has_no_extra_fields(self):
        with open(OUTPUT_SCHEMA, 'r') as f:
            schema_props = json.load(f).get("properties", {})
        
        # Fixed: Extract properties dynamically nested under 'inputs' and 'results' 
        # to avoid mismatch with the top-level wrapper fields ('config', 'results', 'inputs')
        properties = {}
        for wrapper in ["inputs", "results"]:
            if wrapper in schema_props:
                sub_props = schema_props[wrapper].get("properties", {})
                properties.update(sub_props)
        
        extra_fields = set(properties.keys()) - OUTPUT_FIELDS
        assert not extra_fields, f"CONSTITUTIONAL VIOLATION: Unauthorized output fields detected: {extra_fields}"

    def test_state_interface_allows_no_undefined_fields(self):
        # Inspect the Dataclass fields directly
        state_fields = set(get_type_hints(BernoulliState).keys())
        
        # Identify any field in the class NOT in the allowed output set
        extra_fields = state_fields - OUTPUT_FIELDS
        assert not extra_fields, f"CONSTITUTIONAL VIOLATION: Unauthorized fields found in BernoulliState: {extra_fields}"

    def test_dummy_integrity(self):
        """
        Uses the BernoulliStateDummy to ensure that actual object instances 
        do not contain fields outside of our Constitutional Output Set.
        """
        dummy = BernoulliStateDummy()
        
        # 1. Check Dict keys (Primary fields)
        dict_keys = set(dummy.keys())
        
        # 2. Check Instance attributes (Envelope fields)
        # We filter out private/internal python attributes (starting with _)
        instance_attrs = {
            k for k in dir(dummy) 
            if not k.startswith('_') 
            and k not in dict_keys 
            and not callable(getattr(dummy, k))
        }
        
        actual_fields = dict_keys.union(instance_attrs)
        extra_fields = actual_fields - OUTPUT_FIELDS
        
        assert not extra_fields, f"CONSTITUTIONAL VIOLATION: Dummy object contains unauthorized fields: {extra_fields}"