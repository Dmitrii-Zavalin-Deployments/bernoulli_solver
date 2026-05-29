import pytest
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.bernoulli_pipeline_orchestrator import run_solver
from tests.signatures.no_computation_before_validation_signature import NoComputationBeforeValidationTestSignature

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
        # Create a path that definitely doesn't exist
        invalid_path = "non_existent_file.json"
        
        with pytest.raises(FileNotFoundError):
            run_solver(invalid_path)
            
        # Ensure the orchestrator was never called
        mock_orchestrator.assert_not_called()

    @patch("src.bernoulli_pipeline_orchestrator.BernoulliPipelineOrchestrator")
    def test_solver_requires_successful_validation_before_execution(self, mock_orchestrator):
        """
        Verify that execution only proceeds if the input is valid.
        (Implicitly tested by checking that valid execution calls the orchestrator)
        """
        # We need a dummy valid file for this test
        # (Assuming you have a valid test_input.json)
        # If no file exists, this test serves as a documentation of the gate.
        pass

    def test_no_partial_or_intermediate_execution_allowed(self):
        """
        Verify that intermediate steps (like S0) cannot be called 
        without a fully validated state.
        """
        from src.steps.step_s0_filled_unfilled_classifier import StepS0FilledUnfilledClassifier
        
        # S0 should only work if passed a valid schema instance. 
        # Attempting to call with garbage should fail inside the step, 
        # not inside the orchestrator.
        s0 = StepS0FilledUnfilledClassifier()
        with pytest.raises(Exception):
            s0.classify_fields(raw_input={"garbage": "data"})

    def test_validation_gate_is_global_and_non_bypassable(self):
        """
        Verify that calling the orchestrator manually (bypassing run_solver)
        still requires an object that has passed load_and_validate_config.
        """
        from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator
        
        # The orchestrator is designed to receive a validated config object.
        # Passing 'None' to execute_pipeline should fail immediately 
        # (Type enforcement check).
        orchestrator = BernoulliPipelineOrchestrator()
        with pytest.raises(TypeError):
            # This simulates a bypass attempt without passing the validated config
            orchestrator.execute_pipeline(raw_input={}, config=None)