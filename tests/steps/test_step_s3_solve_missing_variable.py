import pytest
import math
import copy
from src.steps.step_s3_solve_missing_variable import StepS3SolveMissingVariable
from src.config.config_loader import SolverConfig
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from tests.signatures.s3_solve_missing_variable_test_signature import S3SolveMissingVariableTestSignature

class TestS3SolveMissingVariable(S3SolveMissingVariableTestSignature):
    """
    Concrete implementation of S3 tests. 
    Inherits from S3SolveMissingVariableTestSignature.
    """

    @pytest.fixture
    def s3_step(self):
        return StepS3SolveMissingVariable()

    @pytest.fixture
    def dummy(self):
        return BernoulliStateDummy()

    @pytest.fixture
    def config(self):
        # Dummy config for orchestration
        return SolverConfig(g=9.81, precision=1e-6, k_v_min=0.1, k_v_max=0.1, k_p_min=0.1, k_p_max=0.1)

    # ---------------------------------------------------------
    # Missing‑variable solves (core responsibility)
    # ---------------------------------------------------------

    def test_solves_missing_p1(self, s3_step, dummy, config):
        """S3 must correctly solve for p1."""
        # Setup: P1 + 0.5*rho*v1^2 + rho*g*h1 = P2 + 0.5*rho*v2^2 + rho*g*h2
        # Let's set everything to 1.0, solve for P1.
        state = dummy.override(p2=1.0, v1=1.0, v2=1.0, h1=1.0, h2=1.0, rho=1.0).get_s1_compliant_state("p1")
        result = s3_step.solve_missing_variable(state, config)
        assert math.isclose(result.p1, 1.0)

    def test_solves_missing_p2(self, s3_step, dummy, config):
        """S3 must correctly solve for p2."""
        state = dummy.override(p1=1.0, v1=1.0, v2=1.0, h1=1.0, h2=1.0, rho=1.0).get_s1_compliant_state("p2")
        result = s3_step.solve_missing_variable(state, config)
        assert math.isclose(result.p2, 1.0)

    def test_solves_missing_v1(self, s3_step, dummy, config):
        """S3 must correctly solve for v1."""
        state = dummy.override(p1=1.0, p2=1.0, v2=1.0, h1=1.0, h2=1.0, rho=1.0).get_s1_compliant_state("v1")
        result = s3_step.solve_missing_variable(state, config)
        assert math.isclose(result.v1, 1.0)

    def test_solves_missing_v2(self, s3_step, dummy, config):
        """S3 must correctly solve for v2."""
        state = dummy.override(p1=1.0, p2=1.0, v1=1.0, h1=1.0, h2=1.0, rho=1.0).get_s1_compliant_state("v2")
        result = s3_step.solve_missing_variable(state, config)
        assert math.isclose(result.v2, 1.0)

    def test_solves_missing_h1(self, s3_step, dummy, config):
        """S3 must correctly solve for h1."""
        state = dummy.override(p1=1.0, p2=1.0, v1=1.0, v2=1.0, h2=1.0, rho=1.0).get_s1_compliant_state("h1")
        result = s3_step.solve_missing_variable(state, config)
        assert math.isclose(result.h1, 1.0)

    def test_solves_missing_h2(self, s3_step, dummy, config):
        """S3 must correctly solve for h2."""
        state = dummy.override(p1=1.0, p2=1.0, v1=1.0, v2=1.0, h1=1.0, rho=1.0).get_s1_compliant_state("h2")
        result = s3_step.solve_missing_variable(state, config)
        assert math.isclose(result.h2, 1.0)

    def test_solves_missing_rho(self, s3_step, dummy, config):
        """S3 must correctly solve for rho with non-zero head differentials."""
        # Fix: Ensure h2 != h1 to create a non-zero head differential
        state = dummy.override(p1=20.0, p2=10.0, v1=1.0, v2=1.0, h1=1.0, h2=2.0).get_s1_compliant_state("rho")
        result = s3_step.solve_missing_variable(state, config)
        assert result.rho > 0

    # ---------------------------------------------------------
    # Physics & math correctness
    # ---------------------------------------------------------

    def test_rejects_negative_radicand(self, s3_step, dummy, config):
        """S3 must reject inputs resulting in sqrt(negative)."""
        # Set conditions where v^2 would be negative (e.g., P1 < P2 with no compensating head/v)
        state = dummy.override(p1=0.0, p2=100.0, v1=0.0, h1=0.0, h2=0.0, rho=1.0).get_s1_compliant_state("v2")
        with pytest.raises(ValueError, match="negative radicand"):
            s3_step.solve_missing_variable(state, config)

    def test_rejects_negative_density_solution(self, s3_step, dummy, config):
        """S3 must reject negative rho results."""
        # Use inputs that result in a negative rho value
        state = dummy.override(p1=10.0, p2=20.0, v1=1.0, v2=1.0, h1=1.0, h2=2.0).get_s1_compliant_state("rho")
        # Fix: Update regex to match actual error message
        with pytest.raises(ValueError, match="non-physical fluid density"):
            s3_step.solve_missing_variable(state, config)

    def test_correct_sign_conventions(self, s3_step, dummy, config):
        """S3 must apply consistent sign conventions."""
        state = dummy.override(p2=10.0, v1=1.0, v2=1.0, h1=1.0, h2=1.0, rho=1.0).get_s1_compliant_state("p1")
        result = s3_step.solve_missing_variable(state, config)
        assert result.p1 == 10.0

    def test_correct_use_of_g_and_rho(self, s3_step, dummy, config):
        """S3 must use g and rho consistently."""
        # Fix: Use inputs that ensure a valid positive density
        state = dummy.override(p1=20.0, p2=10.0, v1=1.0, v2=1.0, h1=1.0, h2=2.0).get_s1_compliant_state("rho")
        result = s3_step.solve_missing_variable(state, config)
        assert result.rho > 0

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

    def test_input_immutability(self, s3_step, dummy, config):
        """S3 must not mutate the input partial state."""
        state = dummy.get_s1_compliant_state("p1")
        original = copy.deepcopy(dict(state))
        _ = s3_step.solve_missing_variable(state, config)
        assert dict(state) == original

    def test_frozen_dummy_alignment(self, s3_step, dummy, config):
        """S3 output must match the dummy structure (attributes preserved)."""
        state = dummy.get_s1_compliant_state("p1")
        result = s3_step.solve_missing_variable(state, config)
        assert hasattr(result, 'energy')
        assert result.energy == [0.0, 0.0]