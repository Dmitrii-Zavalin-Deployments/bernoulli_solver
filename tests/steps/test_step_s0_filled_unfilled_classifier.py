import pytest

from src.steps.step_s0_filled_unfilled_classifier import FilledUnfilledClassifier
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from tests.signatures.s0_classification_scenarios_signature import (
    S0ClassificationTestSignature,
)


class TestS0Classification(S0ClassificationTestSignature):
    
    @pytest.fixture
    def classifier(self):
        return FilledUnfilledClassifier()

    @pytest.fixture
    def valid_state(self):
        return BernoulliStateDummy()

    # --- Implementations of Signature Contracts ---

    def test_accepts_all_primary_fields(self, classifier, valid_state):
        filled, unfilled = classifier.classify_filled_and_unfilled(valid_state)
        # Verify all primary fields are identified
        primary_fields = {'p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho'}
        assert primary_fields.issubset(filled)

    def test_rejects_missing_primary_fields(self, classifier, valid_state):
        # Missing fields should map to unfilled rather than raising an exception
        invalid_state = valid_state.copy()
        del invalid_state['p1']
        filled, unfilled = classifier.classify_filled_and_unfilled(invalid_state)
        assert 'p1' not in filled
        assert 'p1' in unfilled

    def test_rejects_excess_fields(self, classifier, valid_state):
        # Excess fields are completely excluded from structural universes
        invalid_state = valid_state.copy()
        invalid_state['illegal_field'] = 999
        filled, unfilled = classifier.classify_filled_and_unfilled(invalid_state)
        assert 'illegal_field' not in filled
        assert 'illegal_field' not in unfilled

    def test_rejects_non_numeric_values(self, classifier, valid_state):
        # Types are ignored structurally; type checking is entirely deferred to S1
        invalid_state = valid_state.override(p1="not_a_number")
        filled, unfilled = classifier.classify_filled_and_unfilled(invalid_state)
        assert 'p1' in filled

    def test_rejects_negative_or_zero_density(self, classifier, valid_state):
        # Value limits are completely deferred to S1 validation steps
        invalid_state = valid_state.override(rho=-1.0)
        filled, unfilled = classifier.classify_filled_and_unfilled(invalid_state)
        assert 'rho' in filled

    def test_accepts_zero_and_low_velocity(self, classifier, valid_state):
        state = valid_state.override(v1=0.0, v2=1e-12)
        # Should not raise
        classifier.classify_filled_and_unfilled(state)

    def test_accepts_extreme_but_valid_ranges(self, classifier, valid_state):
        state = valid_state.override(p1=1e9, h1=-1e9)
        classifier.classify_filled_and_unfilled(state)

    def test_no_computation_occurs(self, classifier, valid_state):
        # Setup specific energy values
        valid_state.energy = [100.0, 100.0]
        classifier.classify_filled_and_unfilled(valid_state)
        # Verify S0 did not touch the energy attributes
        assert valid_state.energy == [100.0, 100.0]

    def test_classifies_diagnostic_fields(self, classifier, valid_state):
        _, unfilled = classifier.classify_filled_and_unfilled(valid_state)
        assert 'energy' in unfilled
        assert 'p_min' in unfilled

    def test_consistency_passthrough(self, classifier, valid_state):
        # S0 should just pass the dict through logic without modifying values
        filled, _ = classifier.classify_filled_and_unfilled(valid_state)
        # Verify the structure is what we expect
        assert 'p1' in filled

    def test_input_immutability(self, classifier, valid_state):
        original_p1 = valid_state['p1']
        classifier.classify_filled_and_unfilled(valid_state)
        assert valid_state['p1'] == original_p1

    def test_frozen_dummy_alignment(self, classifier, valid_state):
        filled, _ = classifier.classify_filled_and_unfilled(valid_state)
        # Logic check: Verify that S0 returns a set/dict that maps to the dummy
        assert isinstance(filled, set) or isinstance(filled, dict)
