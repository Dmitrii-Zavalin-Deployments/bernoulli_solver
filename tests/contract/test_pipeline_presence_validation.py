import pytest
from tests.signatures.presence_validation_signature import PresenceValidationTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator

@pytest.fixture
def orchestrator():
    return BernoulliPipelineOrchestrator()

@pytest.fixture
def ground_truth():
    # Returns the default, fully populated state
    return BernoulliStateDummy()

@pytest.fixture
def valid_config():
    return {"k_p_min": 0.1, "k_p_max": 0.1, "k_v_min": 0.1, "k_v_max": 0.1}

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

    def test_input_has_exactly_one_missing_variable(self, orchestrator, ground_truth):
        """
        Verify that the pipeline handles inputs. 
        Note: We use execute_pipeline as the orchestrator entry point.
        """
        # Test 1 missing (Should pass)
        valid_input = ground_truth.override(p1=None)
        assert orchestrator.execute_pipeline(valid_input, {"k_p_min": 0.1}) is not None

        # Test 0 missing (Full input) - Depending on your pipeline logic, 
        # this may either pass or raise a specific validation error.
        # Adjust 'pytest.raises' if your pipeline strictly requires one missing variable.
        with pytest.raises(Exception): 
             orchestrator.execute_pipeline(ground_truth, {"k_p_min": 0.1})

    def test_output_has_all_required_fields(self, orchestrator, ground_truth, valid_config):
        """
        Validate that the returned state object contains every required field.
        """
        # Create input with one missing variable
        input_state = ground_truth.override(p1=None)
        
        res = orchestrator.execute_pipeline(input_state, valid_config)
        
        # Check primary fields
        for field in ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]:
            assert hasattr(res, field) or field in res, f"Missing primary field: {field}"
            
        # Check envelope fields
        for field in ["p_min", "p_max", "v_min", "v_max"]:
            value = getattr(res, field, None) or res.get(field)
            assert value is not None, f"Envelope field {field} is None or missing"

    def test_no_optional_or_missing_fields_allowed(self, orchestrator, ground_truth, valid_config):
        """
        Ensure the output object is fully initialized with no None values.
        """
        # We test with valid input (or whatever state is expected)
        res = orchestrator.execute_pipeline(ground_truth.override(p1=None), valid_config)
        
        all_fields = ["p1", "p2", "v1", "v2", "h1", "h2", "rho", 
                      "p_min", "p_max", "v_min", "v_max", "energy", "energy_imbalance"]
        
        for field in all_fields:
            # Check attribute (if object) or key (if dict)
            value = getattr(res, field, None) if not isinstance(res, dict) else res.get(field)
            assert value is not None, f"Field {field} is missing or None in output"