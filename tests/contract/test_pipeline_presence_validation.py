import pytest
from types import SimpleNamespace
from tests.signatures.presence_validation_signature import PresenceValidationTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator

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
    """

    @pytest.fixture
    def primary_fields(self):
        return ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]

    @pytest.fixture
    def envelope_fields(self):
        return ["p_min", "p_max", "v_min", "v_max"]

    def test_input_has_exactly_one_missing_variable(self, orchestrator, ground_truth, valid_config):
        # Test 1 missing (Should pass through solver mode)
        valid_input = ground_truth.override(p1=None)
        assert orchestrator.execute_pipeline(valid_input, valid_config) is not None

        # Test >1 missing (Should fail early validation)
        invalid_input = ground_truth.override(p1=None, p2=None)
        with pytest.raises(Exception): 
             orchestrator.execute_pipeline(invalid_input, valid_config)

    def test_output_has_all_required_fields(self, orchestrator, ground_truth, valid_config):
        input_state = ground_truth.override(p1=None)
        res = orchestrator.execute_pipeline(input_state, valid_config)
        
        for field in ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]:
            assert hasattr(res, field) or field in res, f"Missing primary field: {field}"
            
        for field in ["p_min", "p_max", "v_min", "v_max"]:
            value = getattr(res, field, None) or res.get(field)
            assert value is not None, f"Envelope field {field} is None or missing"

    def test_no_optional_or_missing_fields_allowed(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth.override(p1=None), valid_config)
        
        all_fields = ["p1", "p2", "v1", "v2", "h1", "h2", "rho", 
                      "p_min", "p_max", "v_min", "v_max", "energy", "energy_imbalance"]
        
        for field in all_fields:
            value = getattr(res, field, None) if not isinstance(res, dict) else res.get(field)
            assert value is not None, f"Field {field} is missing or None in output"