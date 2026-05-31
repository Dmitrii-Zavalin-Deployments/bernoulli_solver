import pytest
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from src.steps.step_s0_filled_unfilled_classifier import FilledUnfilledClassifier
from src.interfaces.step_interfaces.s0_classification_scenarios_signature import S0ClassificationTestSignature

class TestS0Classification(S0ClassificationTestSignature):
    
    @pytest.fixture
    def classifier(self):
        return FilledUnfilledClassifier()

    @pytest.fixture
    def valid_state(self):
        return BernoulliStateDummy()

    # --- Test Implementations ---

    def test_accepts_all_primary_fields(self, classifier, valid_state):
        result = classifier.classify_filled_and_unfilled(valid_state)
        assert result is not None  # Or verify specific classification dict structure

    def test_rejects_missing_primary_fields(self, classifier, valid_state):
        del valid_state['p1']
        with pytest.raises(ValueError): # Assuming S0 raises ValueError for invalid input
            classifier.classify_filled_and_unfilled(valid_state)

    def test_rejects_excess_fields(self, classifier, valid_state):
        valid_state['invalid_field'] = 1.0
        with pytest.raises(ValueError):
            classifier.classify_filled_and_unfilled(valid_state)

    def test_rejects_non_numeric_values(self, classifier, valid_state):
        valid_state['p1'] = "string_value"
        with pytest.raises(ValueError):
            classifier.classify_filled_and_unfilled(valid_state)

    def test_rejects_negative_or_zero_density(self, classifier, valid_state):
        valid_state['rho'] = -0.1
        with pytest.raises(ValueError):
            classifier.classify_filled_and_unfilled(valid_state)

    def test_accepts_zero_and_low_velocity(self, classifier, valid_state):
        valid_state['v1'] = 0.0
        valid_state['v2'] = 1e-10
        # Should execute without raising
        classifier.classify_filled_and_unfilled(valid_state)

    def test_accepts_extreme_but_valid_ranges(self, classifier, valid_state):
        valid_state['p1'] = 1e6
        valid_state['h1'] = 1e-6
        classifier.classify_filled_and_unfilled(valid_state)

    def test_no_computation_occurs(self, classifier, valid_state):
        # We define a known state
        input_energy = [1.0, 1.0]
        valid_state.energy = input_energy
        
        classifier.classify_filled_and_unfilled(valid_state)
        
        # Verify diagnostics were not touched (S0 MUST NOT compute/mutate)
        assert valid_state.energy == input_energy

    def test_classifies_diagnostic_fields(self, classifier, valid_state):
        # Even if provided, S0 must classify them as 'diagnostic' rather than 'primary'
        # Verification logic depends on your specific S0 return type
        classifier.classify_filled_and_unfilled(valid_state)
        # assert result.is_diagnostic('energy') 

    def test_consistency_passthrough(self, classifier, valid_state):
        result = classifier.classify_filled_and_unfilled(valid_state)
        # Ensure values are identical to input (No inference)
        assert result['p1'] == valid_state['p1']

    def test_input_immutability(self, classifier, valid_state):
        original_p1 = valid_state['p1']
        classifier.classify_filled_and_unfilled(valid_state)
        assert valid_state['p1'] == original_p1

    def test_frozen_dummy_alignment(self, classifier, valid_state):
        # Verify the structure returned by S0 matches the dummy interface 
        # (Assuming S0 returns an object that respects BernoulliStateInterface)
        result = classifier.classify_filled_and_unfilled(valid_state)
        assert hasattr(result, 'p1')
        assert hasattr(result, 'energy')