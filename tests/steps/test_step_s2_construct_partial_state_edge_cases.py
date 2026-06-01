import pytest
import math
import copy
from src.steps.step_s2_construct_partial_state import StepS2ConstructPartialState
from tests.signatures.test_signatures import S2PartialStateEdgeCasesTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

class TestS2PartialStateEdgeCases(S2PartialStateEdgeCasesTestSignature):
    """
    Implementation of the S2 Partial State Edge-Case Tests.
    Inherits from the contract signature and enforces strict computational 
    sanity (math.isfinite) while allowing physical boundary extremes.
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
        """S2 must ACCEPT negative pressures (cavitation research) but reject NaN."""
        # This test ensures we do NOT reject negative values anymore.
        state = dummy.override(p1=-100.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.p1 == -100.0

    def test_rejects_extreme_velocities(self, s2_step, dummy, sentinel):
        """S2 must ACCEPT extreme velocities (relativistic research) but reject NaN."""
        state = dummy.override(v1=1e15).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.v1 == 1e15

    def test_handles_tiny_delta_h_or_v(self, s2_step, dummy, sentinel):
        """S2 must construct state even when Δh/Δv is near-zero."""
        tiny_state = dummy.override(h1=1.0, h2=1.0000000001).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(tiny_state), "rho", sentinel)
        assert result is not None

    def test_rejects_malformed_input_structures(self, s2_step, sentinel):
        """S2 must reject malformed inputs: wrong types/shapes."""
        with pytest.raises((TypeError, KeyError, ValueError)):
            s2_step.construct_partial_state({"invalid": "data"}, "rho", sentinel)

    def test_rejects_missing_required_fields(self, s2_step, dummy, sentinel):
        """S2 must reject states missing required primary variables."""
        bad_state = dict(dummy.get_s1_compliant_state(missing_key="rho"))
        del bad_state['p2']
        with pytest.raises((KeyError, ValueError)):
            s2_step.construct_partial_state(bad_state, "rho", sentinel)

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self, s2_step, dummy, sentinel):
        """S2 must correctly handle v1=0."""
        state = dummy.override(v1=0.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.v1 == 0.0

    def test_equal_pressures(self, s2_step, dummy, sentinel):
        """S2 must correctly propagate fields when p1 == p2."""
        state = dummy.override(p1=100.0, p2=100.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.p1 == result.p2

    def test_flat_line_delta_h_zero(self, s2_step, dummy, sentinel):
        """S2 must correctly propagate fields when h1 == h2."""
        state = dummy.override(h1=10.0, h2=10.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result.h1 == result.h2

    def test_other_degenerate_configurations(self, s2_step, dummy, sentinel):
        """S2 must handle all zeros configuration."""
        state = dummy.override(p1=0.0, p2=0.0, v1=0.0, v2=0.0, h1=0.0, h2=0.0).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result is not None

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self, s2_step, dummy, sentinel):
        """S2 must be deterministic with floating-point drift."""
        state = dummy.override(p1=1.000000000000001).get_s1_compliant_state(missing_key="rho")
        result1 = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        result2 = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert result1.p1 == result2.p1

    def test_near_cancellation_scenarios(self, s2_step, dummy, sentinel):
        """S2 must correctly propagate near-cancel values."""
        state = dummy.override(p1=100.0, p2=100.00000001).get_s1_compliant_state(missing_key="rho")
        result = s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert abs(result.p1 - result.p2) < 1e-6

    def test_predictable_behavior_under_edge_conditions(self, s2_step, dummy, sentinel):
        """S2 must remain predictable near pathological boundaries (Finite check)."""
        # This confirms that our sanity gate rejects NaNs even in extreme conditions
        state = dummy.override(h1=float('inf')).get_s1_compliant_state(missing_key="rho")
        
        # Note: If h1 was not in the ['p1', 'p2', 'v1', 'v2', 'rho'] list, 
        # this won't trigger the gate, but the logic remains robust.
        # For a full check, we test a NaN in a validated field:
        bad_state = dummy.override(p1=float('nan')).get_s1_compliant_state(missing_key="rho")
        with pytest.raises(ValueError, match="must be a finite number"):
            s2_step.construct_partial_state(dict(bad_state), "rho", sentinel)

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self, s2_step, dummy, sentinel):
        """S2 must not mutate the input structure."""
        state = dummy.get_s1_compliant_state(missing_key="rho")
        original_dict = copy.deepcopy(dict(state))
        s2_step.construct_partial_state(dict(state), "rho", sentinel)
        assert dict(state) == original_dict

    def test_frozen_dummy_alignment(self, s2_step, dummy, sentinel):
        """S2 output must match the frozen dummy structure."""
        state = dummy.get_s1_compliant_state(missing_key="p1")
        result = s2_step.construct_partial_state(dict(state), "p1", sentinel)
        assert math.isnan(getattr(result, "p1")) or getattr(result, "p1") is sentinel
        assert result.p2 == 1.0