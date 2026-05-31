import pytest
import copy
from tests.signatures.s1_exactly_one_missing_edge_cases_signature import S1ExactlyOneMissingEdgeCasesTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from src.steps.step_s1_exactly_one_missing import StepS1ExactlyOneMissing

class TestS1ExactlyOneMissingEdgeCases(S1ExactlyOneMissingEdgeCasesTestSignature):

    @pytest.fixture
    def classifier(self):
        return StepS1ExactlyOneMissing()

    @pytest.fixture
    def valid_state(self):
        return BernoulliStateDummy()

    # -------------------------
    # Sensitivity edge cases
    # -------------------------

    def test_rejects_negative_pressures(self, classifier, valid_state):
        state = valid_state.override(p1=-0.1)
        with pytest.raises(ValueError):
            classifier.enforce_exactly_one_missing(state)

    def test_rejects_extreme_velocities(self, classifier, valid_state):
        # Velocity at light speed is not physically plausible for Bernoulli water solvers
        state = valid_state.override(v1=3e8)
        with pytest.raises(ValueError):
            classifier.enforce_exactly_one_missing(state)

    def test_handles_tiny_delta_h_or_v(self, classifier, valid_state):
        # Valid state, just very small differences
        state = valid_state.override(h1=1.0, h2=1.000000000001)
        classifier.enforce_exactly_one_missing(state)

    def test_rejects_malformed_input_structures(self, classifier):
        # Passing an invalid type or structure
        with pytest.raises(ValueError):
            classifier.enforce_exactly_one_missing({"p1": 1.0}) # Missing required fields

    def test_rejects_missing_required_fields(self, classifier, valid_state):
        # Remove a mandatory field
        del valid_state['p1']
        with pytest.raises(ValueError):
            classifier.enforce_exactly_one_missing(valid_state)

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self, classifier, valid_state):
        # Stagnation point is valid
        state = valid_state.override(v1=0.0)
        classifier.enforce_exactly_one_missing(state)

    def test_equal_pressures(self, classifier, valid_state):
        # Horizontal pipe with no pressure drop is valid
        state = valid_state.override(p1=10.0, p2=10.0)
        classifier.enforce_exactly_one_missing(state)

    def test_flat_line_delta_h_zero(self, classifier, valid_state):
        # Flat geometry is valid
        state = valid_state.override(h1=5.0, h2=5.0)
        classifier.enforce_exactly_one_missing(state)

    def test_other_degenerate_configurations(self, classifier, valid_state):
        # All inputs zero (rho=0 is usually invalid, but let's test a known degenerate)
        state = valid_state.override(p1=0.0, p2=0.0, v1=0.0, v2=0.0, h1=0.0, h2=0.0, rho=0.0)
        # Assuming S1 should reject non-physical rho=0
        with pytest.raises(ValueError):
            classifier.enforce_exactly_one_missing(state)

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self, classifier, valid_state):
        state = valid_state.override(p1=1.00000000000001)
        classifier.enforce_exactly_one_missing(state)

    def test_near_cancellation_scenarios(self, classifier, valid_state):
        state = valid_state.override(p1=1.0, p2=1.000000000001, h1=10.0, h2=10.000000000001)
        classifier.enforce_exactly_one_missing(state)

    def test_predictable_behavior_under_edge_conditions(self, classifier, valid_state):
        # Ensure it handles valid boundary states consistently
        classifier.enforce_exactly_one_missing(valid_state)

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self, classifier, valid_state):
        original_state = copy.deepcopy(valid_state)
        classifier.enforce_exactly_one_missing(valid_state)
        assert valid_state == original_state

    def test_frozen_dummy_alignment(self, classifier, valid_state):
        # Verify the classifier accepts the dummy structure as valid
        result = classifier.enforce_exactly_one_missing(valid_state)
        # Assert result indicates success (if your validator returns bool or object)
        assert result is not None