import pytest
import math
import copy
from types import SimpleNamespace
from tests.signatures.s4_compute_energy_residual_test_signature import S4ComputeEnergyResidualTestSignature
from src.steps.step_s4_compute_energy_residual import StepS4ComputeEnergyResidual
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

class TestS3ComputeEnergyResidual(S4ComputeEnergyResidualTestSignature):
    """
    Implementation of the S4 Compute Energy Residual tests.
    """

    @pytest.fixture
    def s4_step(self):
        return StepS4ComputeEnergyResidual()

    @pytest.fixture
    def dummy(self):
        return BernoulliStateDummy()

    @pytest.fixture
    def config(self):
        # Providing standard gravity for physical consistency
        return SimpleNamespace(g=9.81)

    # ---------------------------------------------------------
    # Energy computation
    # ---------------------------------------------------------

    def test_computes_correct_E1(self, s4_step, dummy, config):
        """S4 must compute E1 correctly: p1 + 0.5 * rho * v1^2 + rho * g * h1."""
        state = dummy.override(p1=10.0, v1=2.0, h1=5.0, rho=2.0)
        result = s4_step.compute_energy_and_residual(state, config)
        
        # Expected: 10.0 + 0.5 * 2.0 * (2.0^2) + 2.0 * 9.81 * 5.0
        # 10.0 + 4.0 + 98.1 = 112.1
        expected_e1 = 112.1
        assert math.isclose(result.energy[0], expected_e1, rel_tol=1e-6)

    def test_computes_correct_E2(self, s4_step, dummy, config):
        """S4 must compute E2 correctly: p2 + 0.5 * rho * v2^2 + rho * g * h2."""
        state = dummy.override(p2=20.0, v2=3.0, h2=2.0, rho=2.0)
        result = s4_step.compute_energy_and_residual(state, config)
        
        # Expected: 20.0 + 0.5 * 2.0 * (3.0^2) + 2.0 * 9.81 * 2.0
        # 20.0 + 9.0 + 39.24 = 68.24
        expected_e2 = 68.24
        assert math.isclose(result.energy[1], expected_e2, rel_tol=1e-6)

    def test_computes_correct_energy_imbalance(self, s4_step, dummy, config):
        """S4 must compute energy_imbalance = E1 - E2 correctly."""
        # E1 = 112.1, E2 = 68.24 -> Imbalance = 43.86
        state = dummy.override(p1=10.0, v1=2.0, h1=5.0, p2=20.0, v2=3.0, h2=2.0, rho=2.0)
        result = s4_step.compute_energy_and_residual(state, config)
        
        expected_imbalance = 112.1 - 68.24
        assert math.isclose(result.energy_imbalance, expected_imbalance, rel_tol=1e-6)

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

    def test_input_immutability(self, s4_step, dummy, config):
        """S4 must not mutate the input state."""
        # Capture deepcopy before
        state = dummy.override(p1=10.0, p2=20.0)
        original_state_dict = copy.deepcopy(state)
        
        s4_step.compute_energy_and_residual(state, config)
        
        # Ensure values didn't change
        assert state['p1'] == original_state_dict['p1']
        assert state['p2'] == original_state_dict['p2']

    def test_frozen_dummy_alignment(self, s4_step, dummy, config):
        """S4 output must match structure and preserve metadata."""
        state = dummy.override(p_min=0.5, v_max=100.0)
        result = s4_step.compute_energy_and_residual(state, config)
        
        # Verify metadata (not computed by S4, but preserved)
        assert result.p_min == 0.5
        assert result.v_max == 100.0
        
        # Verify structure: energy must be a list of two floats
        assert isinstance(result.energy, list)
        assert len(result.energy) == 2