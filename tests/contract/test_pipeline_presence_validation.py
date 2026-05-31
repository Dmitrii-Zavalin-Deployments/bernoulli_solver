import pytest
from tests.signatures.presence_validation_signature import PresenceValidationTestSignature

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
        Verify that the pipeline orchestrator rejects inputs with 0, 2, or more 
        missing fields, but accepts inputs with exactly one.
        """
        # Test 0 missing (Full input)
        with pytest.raises(ValueError, match="Input must have exactly one missing variable"):
            orchestrator.validate_input(ground_truth)

        # Test 2 missing
        invalid_input = ground_truth.copy()
        invalid_input["p1"] = None
        invalid_input["p2"] = None
        with pytest.raises(ValueError, match="Input must have exactly one missing variable"):
            orchestrator.validate_input(invalid_input)

        # Test 1 missing (Should pass)
        valid_input = ground_truth.copy()
        valid_input["p1"] = None
        assert orchestrator.validate_input(valid_input) is True

    def test_output_has_all_required_fields(self, orchestrator, ground_truth, valid_config):
        """
        Validate that the returned state object contains every required field.
        """
        # Create valid input with one missing variable
        input_state = ground_truth.copy()
        input_state["p1"] = None
        
        res = orchestrator.execute_pipeline(input_state, valid_config)
        
        # Check primary fields
        for field in ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]:
            assert hasattr(res, field), f"Missing primary field: {field}"
            
        # Check envelope fields
        for field in ["p_min", "p_max", "v_min", "v_max"]:
            assert hasattr(res, field), f"Missing envelope field: {field}"
            assert getattr(res, field) is not None, f"Envelope field {field} is None"

    def test_no_optional_or_missing_fields_allowed(self, orchestrator, ground_truth, valid_config):
        """
        Ensure the output object is fully initialized with no None values.
        """
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        
        # Ensure all fields are populated
        all_fields = ["p1", "p2", "v1", "v2", "h1", "h2", "rho", 
                      "p_min", "p_max", "v_min", "v_max", "energy", "energy_imbalance"]
        
        for field in all_fields:
            value = getattr(res, field)
            assert value is not None, f"Field {field} is missing in output"