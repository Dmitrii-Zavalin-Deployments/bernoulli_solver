import pytest
import copy
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
# Assuming BernoulliStateDummy is available in your path or included above

class TestS2PartialStateEdgeCases:
    """
    Concrete implementation of S2 Partial State construction edge-case tests.
    """

    @pytest.fixture
    def s2_step(self):
        return StepS2ConstructPartialState()

    # -------------------------
    # Sensitivity edge cases
    # -------------------------

    def test_rejects_negative_pressures(self, s2_step, dummy):
        """S2 must reject states containing negative pressures."""
        bad_state = dummy.override(p1=-10.0)
        with pytest.raises(ValueError, match="negative"):
            s2_step.construct(bad_state)

    def test_rejects_extreme_velocities(self, s2_step, dummy):
        """S2 must reject velocities far outside engineering plausibility."""
        bad_state = dummy.override(v1=1e15) # Unphysically high
        with pytest.raises(ValueError, match="extreme"):
            s2_step.construct(bad_state)

    def test_handles_tiny_delta_h_or_v(self, s2_step, dummy):
        """S2 must still construct a partial state when Δh or Δv is extremely small."""
        # Use valid, tiny differences
        tiny_state = dummy.override(h1=1.0, h2=1.0000000001)
        result = s2_step.construct(tiny_state)
        assert result is not None

    def test_rejects_malformed_input_structures(self, s2_step):
        """S2 must reject malformed inputs: wrong types, wrong shapes."""
        malformed = {"invalid": "structure"}
        with pytest.raises(TypeError):
            s2_step.construct(malformed)

    def test_rejects_missing_required_fields(self, s2_step, dummy):
        """S2 must reject states missing required primary variables."""
        # Force a missing field that isn't the single expected hole
        bad_state = dummy.override(p1=1.0)
        del bad_state['p2']
        with pytest.raises(KeyError):
            s2_step.construct(bad_state)

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self, s2_step, dummy):
        """S2 must not mis-handle v1=0 or v2=0."""
        state = dummy.override(v1=0.0)
        result = s2_step.construct(state)
        assert result.v1 == 0.0

    def test_equal_pressures(self, s2_step, dummy):
        """S2 must correctly propagate fields when p1 == p2."""
        state = dummy.override(p1=100.0, p2=100.0)
        result = s2_step.construct(state)
        assert result.p1 == result.p2

    def test_flat_line_delta_h_zero(self, s2_step, dummy):
        """S2 must correctly propagate fields when h1 == h2 (Δh = 0)."""
        state = dummy.override(h1=10.0, h2=10.0)
        result = s2_step.construct(state)
        assert result.h1 == result.h2

    def test_other_degenerate_configurations(self, s2_step, dummy):
        """S2 must behave correctly under other degenerate but admissible configurations."""
        # All zeros except rho
        state = dummy.override(p1=0.0, p2=0.0, v1=0.0, v2=0.0, h1=0.0, h2=0.0, rho=1.0)
        result = s2_step.construct(state)
        assert result is not None

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self, s2_step, dummy):
        """S2 must remain deterministic when inputs contain tiny floating‑point drift."""
        state = dummy.override(p1=1.000000000000001)
        result1 = s2_step.construct(state)
        result2 = s2_step.construct(state)
        assert result1.p1 == result2.p1

    def test_near_cancellation_scenarios(self, s2_step, dummy):
        """S2 must correctly propagate fields when values nearly cancel."""
        state = dummy.override(p1=100.0, p2=100.00000001)
        result = s2_step.construct(state)
        assert abs(result.p1 - result.p2) < 1e-6

    def test_predictable_behavior_under_edge_conditions(self, s2_step, dummy):
        """S2 must remain predictable near pathological boundaries."""
        # e.g., Extreme heights combined with low density
        state = dummy.override(h1=1000000.0, h2=0.0, rho=0.00001)
        result = s2_step.construct(state)
        assert result is not None

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self, s2_step, dummy):
        """S2 must not mutate the input structure."""
        original_dict = copy.deepcopy(dict(dummy))
        s2_step.construct(dummy)
        assert dict(dummy) == original_dict

    def test_frozen_dummy_alignment(self, s2_step, dummy):
        """S2 output must match the expected frozen structure."""
        state = dummy.get_s1_compliant_state(missing_key="p1")
        result = s2_step.construct(state)
        
        # Verify keys are preserved exactly
        expected_keys = {'p2', 'v1', 'v2', 'h1', 'h2', 'rho'}
        assert set(result.keys()) == expected_keys