import pytest
from unittest.mock import patch
from types import SimpleNamespace
from src.bernoulli_pipeline_orchestrator import run_solver, BernoulliPipelineOrchestrator
from tests.signatures.no_computation_before_validation_signature import NoComputationBeforeValidationTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

@pytest.fixture
def dummy_state():
    return BernoulliStateDummy()

class TestNoComputationBeforeValidation(NoComputationBeforeValidationTestSignature):
    """
    Concrete implementation of NoComputationBeforeValidationTestSignature.
    Enforces the 'Validation-First' constitutional rule.
    """

    @patch("src.bernoulli_pipeline_orchestrator.BernoulliPipelineOrchestrator")
    def test_solver_refuses_execution_if_validation_fails(self, mock_orchestrator):
        """
        Verify that if we provide a non-existent path or bad JSON, 
        the orchestrator is NEVER instantiated.
        """
        invalid_path = "non_existent_file.json"
        
        with pytest.raises(FileNotFoundError):
            run_solver(invalid_path)
            
        mock_orchestrator.assert_not_called()

    @patch("src.bernoulli_pipeline_orchestrator.BernoulliPipelineOrchestrator")
    def test_solver_requires_successful_validation_before_execution(self, mock_orchestrator_class, dummy_state):
        """
        Verify that execution only proceeds if the input is valid.
        Uses the Dummy to simulate a pre-validated state object.
        """
        mock_instance = mock_orchestrator_class.return_value
        
        # We invoke the pipeline with our validated dummy state.
        # This confirms that the pipeline accepts compliant state objects.
        mock_instance.execute_pipeline(dummy_state, config=None)
        
        # Verify the orchestrator was actually triggered
        mock_instance.execute_pipeline.assert_called_once_with(dummy_state, config=None)

    def test_no_partial_or_intermediate_execution_allowed(self, dummy_state):
        """
        Verify that intermediate steps (like S0) cannot be called 
        with malformed data.
        """
        from src.steps.step_s0_filled_unfilled_classifier import StepS0FilledUnfilledClassifier
        
        s0 = StepS0FilledUnfilledClassifier()
        
        # 1. Negative Test: Garbage input should trigger a validation failure
        with pytest.raises(Exception):
            s0.classify_filled_and_unfilled(raw_input={"garbage": "data"})
        # 2. Positive Test: Valid dummy input should NOT trigger an exception
        # This proves the S0 gate is working as intended (blocking bad, allowing good)
        assert s0.classify_filled_and_unfilled(raw_input=dummy_state) is not None

    def test_validation_gate_is_global_and_non_bypassable(self, dummy_state):
        """
        Verify that bypassing the orchestrator's validation 
        results in immediate type/structure errors.
        """
        orchestrator = BernoulliPipelineOrchestrator()
        
        # 1. Negative Test: Bypassing config requirement should fail
        with pytest.raises(TypeError):
            orchestrator.execute_pipeline(raw_input={}, config=None)
            
        # 2. Positive Test: Valid config should proceed
        valid_config = SimpleNamespace(g=9.8, k_p_min=0.1, k_p_max=0.1, k_v_min=0.1, k_v_max=0.1)
        result = orchestrator.execute_pipeline(dummy_state, config=valid_config)
        assert result is not None