from types import SimpleNamespace

import pytest

from src.main import BernoulliPipelineOrchestrator
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from tests.signatures.presence_validation_signature import (
    PresenceValidationTestSignature,
)


@pytest.fixture
def orchestrator():
    return BernoulliPipelineOrchestrator()

@pytest.fixture
def ground_truth():
    return BernoulliStateDummy()

@pytest.fixture
def valid_config():
    return SimpleNamespace(
        g=9.80665, 
        k_p_min=0.1, k_p_max=0.1, 
        k_v_min=0.1, k_v_max=0.1
    )

class TestPipelinePresenceValidation(PresenceValidationTestSignature):
    """
    Implementation of presence validation tests for the Bernoulli pipeline.
    Uses BernoulliStateDummy fixtures for contract enforcement.
    """

    @pytest.fixture
    def primary_fields(self):
        return ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]

    @pytest.fixture
    def envelope_fields(self):
        return ["initial_conditions", "physical_constraints"]

    def test_input_has_exactly_one_missing_variable(self, orchestrator, ground_truth, valid_config):
        # Test 1 missing (Should pass through solver mode)
        valid_input = ground_truth.override(p1=None)
        assert orchestrator.execute_pipeline(valid_input, valid_config) is not None

        # Test >1 missing (Should fail early validation)
        invalid_input = ground_truth.override(p1=None, p2=None)
        with pytest.raises(Exception): 
             orchestrator.execute_pipeline(invalid_input, valid_config)

    def test_output_has_all_required_fields(self, orchestrator, ground_truth, valid_config, primary_fields, envelope_fields):
        input_state = ground_truth.override(p1=None)
        res = orchestrator.execute_pipeline(input_state, valid_config)
        
        # Check primary fields
        for field in primary_fields:
            # Handle both object attributes and dict keys
            assert hasattr(res, field) or (isinstance(res, dict) and field in res), f"Missing primary field: {field}"
            
        # Check envelope fields
        for field in envelope_fields:
            value = getattr(res, field, None)
            if value is None and isinstance(res, dict):
                value = res.get(field)
            assert value is not None, f"Envelope field {field} is None or missing"

    def test_no_optional_or_missing_fields_allowed(self, orchestrator, ground_truth, valid_config, primary_fields, envelope_fields):
        res = orchestrator.execute_pipeline(ground_truth.override(p1=None), valid_config)
        
        # Combine lists dynamically to ensure future-proofing
        all_fields = primary_fields + envelope_fields + ["energy", "energy_imbalance"]
        
        for field in all_fields:
            value = getattr(res, field, None)
            if value is None and isinstance(res, dict):
                value = res.get(field)
            assert value is not None, f"Field {field} is missing or None in output"