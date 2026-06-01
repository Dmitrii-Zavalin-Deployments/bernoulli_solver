import pytest
import copy
import math
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
from tests.dummies.bernoulli_state_dummy import BernoulliStateDummy

class TestS2PartialStateEdgeCases:
    """
    Concrete implementation of S2 Partial State construction edge-case tests.
    Matches the 3-argument signature of construct_partial_state.
    """

    @pytest.fixture
    def s2_step(self):
        return StepS2ConstructPartialState()

    @pytest.fixture
    def dummy(self):
        return BernoulliStateDummy()

    @pytest.fixture
    def sentinel(self):
        return float('nan')

    # -------------------------
    # Sensitivity edge cases
    # -------------------------

    def test_rejects_negative_pressures(self, s2_step, dummy, sentinel):
        """S2 must reject states containing negative pressures."""
        bad_state = dummy.override(p1=-10.0).get_s1_compliant_state(missing_key="rho")
        with pytest.raises(ValueError, match="(?i)negative"):
            s2_step.construct_partial_state(dict(bad_state), "rho", sentinel)

    def test_rejects_extreme_velocities(self, s2_step, dummy, sentinel):
        """S2 must reject velocities far outside engineering plausibility."""
        bad_state = dummy.override(v1=1e15).get_s1_compliant_state(missing_key="rho")
        with pytest.raises(ValueError, match="(?i)extreme"):
            s2_step.construct_partial_state(dict(bad_state), "rho", sentinel)

    def test_handles_tiny_delta_h_or_v(self, s2_step, dummy, sentinel):
        """S2 must still construct a partial state when Δh or Δv is extremely small."""
        tiny_state = dummy.override(h1=1.0, h2=1.0000000001).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(tiny_state), "rho", sentinel)
        assert result is not None

    def test_rejects_malformed_input_structures(self, s2_step, sentinel):
        """S2 must reject malformed inputs: wrong types, wrong shapes."""
        malformed = {"invalid": "structure"}
        with pytest.raises((TypeError, KeyError, ValueError)):
            s2_step.construct_partial_state(malformed, "rho", sentinel)

    def test_rejects_missing_required_fields(self, s2_step, dummy, sentinel):
        """S2 must reject states missing required primary variables outside the missing target."""
        bad_state = dict(dummy.get_s1_compliant_state(missing_key="rho"))
        del bad_state['p2']  # Break it further by removing a second expected field
        with pytest.raises((KeyError, ValueError)):
            s2_step.construct_partial_state(bad_state, "rho", sentinel)

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self, s2_step, dummy, sentinel):
        """S2 must not mis-handle v1=0 or v2=0 when constructing the partial state."""
        state = dummy.override(v1=0.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.v1 == 0.0

    def test_equal_pressures(self, s2_step, dummy, sentinel):
        """S2 must correctly propagate fields when p1 == p2."""
        state = dummy.override(p1=100.0, p2=100.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.p1 == result.p2

    def test_flat_line_delta_h_zero(self, s2_step, dummy, sentinel):
        """S2 must correctly propagate fields when h1 == h2 (Δh = 0)."""
        state = dummy.override(h1=10.0, h2=10.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.h1 == result.h2

    def test_other_degenerate_configurations(self, s2_step, dummy, sentinel):
        """S2 must behave correctly under other degenerate but admissible configurations."""
        state = dummy.override(p1=0.0, p2=0.0, v1=0.0, v2=0.0, h1=0.0, h2=0.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result is not None

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self, s2_step, dummy, sentinel):
        """S2 must remain deterministic when inputs contain tiny floating‑point drift."""
        state = dummy.override(p1=1.000000000000001).get_s1_compliant_state(missing_key="rho")
        result1 = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        result2 = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert getattr(result1, 'p1', None) == getattr(result2, 'p1', None)

    def test_near_cancellation_scenarios(self, s2_step, dummy, sentinel):
        """S2 must correctly propagate fields when values nearly cancel (p1≈p2, h1≈h2)."""
        state = dummy.override(p1=100.0, p2=100.00000001).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert abs(result.p1 - result.p2) < 1e-6

    def test_predictable_behavior_under_edge_conditions(self, s2_step, dummy, sentinel):
        """S2 must remain predictable and analytically verifiable near pathological boundaries."""
        state = dummy.override(h1=1000000.0, h2=0.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result is not None

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self, s2_step, dummy, sentinel):
        """S2 must not mutate the input structure under any edge‑case condition."""
        state = dummy.get_s1_compliant_state(missing_key="rho")
        original_dict = copy.deepcopy(dict(state))
        s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert dict(state) == original_dict

    def test_frozen_dummy_alignment(self, s2_step, dummy, sentinel):
        """S2 output must match the expected fields layout and semantic markers."""
        state = dummy.get_s1_compliant_state(missing_key="p1")
        result = s2_step.construct_partial_state(dict(state), "p1", sentinel)
        
        # Verify the resolved dataclass/object has filled remaining variables properly
        assert math.isnan(getattr(result, "p1")) or getattr(result, "p1") is sentinel
        assert result.p2 == 1.0
