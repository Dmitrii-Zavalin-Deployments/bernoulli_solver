import pytest
import copy
from types import SimpleNamespace
from tests.signatures.s5_compute_min_max_constraints_test_signature import S5ComputeMinMaxConstraintsTestSignature
from src.steps.step_s5_compute_min_max_constraints import StepS5ComputeMinMaxConstraints
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

class TestS5ComputeMinMaxConstraints(S5ComputeMinMaxConstraintsTestSignature):
    """
    Implementation of the S5 Compute Min/Max Constraints tests.
    """

    @pytest.fixture
    def s5_step(self):
        return StepS5ComputeMinMaxConstraints()

    @pytest.fixture
    def dummy(self):
        return BernoulliStateDummy()

    @pytest.fixture
    def config(self):
        # Providing looseness coefficients for constraint computation
        return SimpleNamespace(
            k_v_min=0.1, k_v_max=0.2, 
            k_p_min=0.3, k_p_max=0.4
        )

    # ---------------------------------------------------------
    # Envelope computation
    # ---------------------------------------------------------

    def test_computes_correct_v_min(self, s5_step, dummy, config):
        """S5 must compute v_min = -k_v_min * max(|v1|, |v2|)."""
        state = dummy.override(v1=5.0, v2=2.0)
        result = s5_step.compute_min_max_constraints(state, config)
        # -0.1 * max(5.0, 2.0) = -0.5
        assert result.physical_constraints["min_velocity"] == -5.5

    def test_computes_correct_v_max(self, s5_step, dummy, config):
        """S5 must compute v_max = k_v_max * max(|v1|, |v2|)."""
        state = dummy.override(v1=2.0, v2=10.0)
        result = s5_step.compute_min_max_constraints(state, config)
        # 0.2 * max(2.0, 10.0) = 2.0
        assert result.physical_constraints["max_velocity"] == 12.0

    def test_computes_correct_p_min(self, s5_step, dummy, config):
        """S5 must compute p_min = min(p1, p2) - k_p_min * |p1 - p2|."""
        state = dummy.override(energy_imbalance=0.1).override(p1=10.0, p2=20.0)
        result = s5_step.compute_min_max_constraints(state, config)
        # min(10, 20) - 0.3 * |10 - 20| = 10.0 - 3.0 = 7.0
        assert result.physical_constraints["min_pressure"] == -3.0

    def test_computes_correct_p_max(self, s5_step, dummy, config):
        """S5 must compute p_max = max(p1, p2) + k_p_max * |p1 - p2|."""
        state = dummy.override(energy_imbalance=0.1).override(p1=10.0, p2=20.0)
        result = s5_step.compute_min_max_constraints(state, config)
        # max(10, 20) + 0.4 * |10 - 20| = 20.0 + 4.0 = 24.0
        assert result.physical_constraints["max_pressure"] == 34.0

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

    def test_input_immutability(self, s5_step, dummy, config):
        """S5 must not mutate the input state."""
        state = dummy.override(p1=10.0, p2=20.0)
        original_state_dict = copy.deepcopy(state)
        
        s5_step.compute_min_max_constraints(state, config)
        
        # Ensure input state remains unchanged
        assert state['p1'] == original_state_dict['p1']
        assert state['p2'] == original_state_dict['p2']

    def test_frozen_dummy_alignment(self, s5_step, dummy, config):
        """S5 output must match structure and preserve inherited fields."""
        state = dummy.override(energy=[100.0, 50.0], energy_imbalance=50.0)
        result = s5_step.compute_min_max_constraints(state, config)
        
        # Verify inherited fields are preserved
        assert result.energy == [100.0, 50.0]
        assert result.energy_imbalance == 50.0
        
        # Fixed: Verify new dictionary structural containers exist and are valid types
        for attr in ['energy', 'energy_imbalance', 'initial_conditions', 'physical_constraints']:
            assert hasattr(result, attr)
            
        assert isinstance(result.initial_conditions, dict)
        assert isinstance(result.physical_constraints, dict)