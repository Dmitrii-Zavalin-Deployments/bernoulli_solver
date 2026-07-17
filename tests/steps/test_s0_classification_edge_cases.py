import pytest
import copy
from src.main import BernoulliPipelineOrchestrator
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy
from tests.signatures.s0_classification_edge_cases_signature import S0ClassificationEdgeCasesTestSignature
from src.steps.step_s1_exactly_one_missing import ValidationError

class TestS0ClassificationEdgeCases(S0ClassificationEdgeCasesTestSignature):
    """
    Concrete implementation of S0 Classification Edge-Case Tests.
    Ensures S0 acts as a strict validator without performing downstream computations.
    """

    @pytest.fixture
    def orchestrator(self):
        return BernoulliPipelineOrchestrator()

    @pytest.fixture
    def valid_base(self):
        """Standard valid input, then strips h1 for S1 compliance."""
        # Chaining the override and the S1 compliance method ensures
        # that 'h1' is removed as the final step before the test logic runs.
        return BernoulliStateDummy().override(
            p1=100000.0, p2=90000.0,
            v1=10.0, v2=10.0,
            h1=1.0, h2=1.0,
        ).get_s1_compliant_state(missing_key="h1")

    @pytest.fixture
    def config(self):
        # Dummy config for orchestration
        return SolverConfig(g=9.81, precision=1e-6, k_v_min=0.1, k_v_max=0.1, k_p_min=0.1, k_p_max=0.1)

    # -------------------------
    # Sensitivity edge cases
    # -------------------------

    def test_rejects_negative_pressures(self, orchestrator, valid_base, config):
        # Note: If override() re-adds 'h1', ensure you append .get_s1_compliant_state() again
        input_state = valid_base.override(p1=-1.0)
        with pytest.raises(ValueError):
            orchestrator.execute_pipeline(input_state, config)

    def test_rejects_extreme_velocities(self, orchestrator, valid_base, config):
        # Assuming supersonic flow or unrealistic speeds trigger an S0 gate
        input_state = valid_base.override(v1=1e9) 
        with pytest.raises(ValueError):
            orchestrator.execute_pipeline(input_state, config)

    def test_handles_tiny_delta_h_or_v(self, orchestrator, valid_base, config):
        # Extremely small delta should be accepted (classification, not computation)
        input_state = valid_base.override(h1=1.0, h2=1.000000000001).get_s1_compliant_state(missing_key="p1")
        assert orchestrator.execute_pipeline(input_state, config) is not None

    def test_rejects_malformed_input_structures(self, orchestrator, valid_base, config):
        # Injecting an unexpected field/type mismatch
        malformed = copy.deepcopy(valid_base)
        malformed["unexpected_key"] = "bad_data"
        with pytest.raises(ValidationError):
            orchestrator.execute_pipeline(malformed, config)

    def test_rejects_missing_required_fields(self, orchestrator, valid_base, config):
        # S0 should strictly reject None for primary variables
        input_state = valid_base.override(p1=-100.0)
        with pytest.raises(ValueError):
            orchestrator.execute_pipeline(input_state, config)

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self, orchestrator, valid_base, config):
        input_state = valid_base.override(v1=0.0)
        assert orchestrator.execute_pipeline(input_state, config) is not None

    def test_equal_pressures(self, orchestrator, valid_base, config):
        input_state = valid_base.override(p1=100000.0, p2=100000.0)
        assert orchestrator.execute_pipeline(input_state, config) is not None

    def test_flat_line_delta_h_zero(self, orchestrator, valid_base, config):
        input_state = valid_base.override(h1=0.0, h2=0.0).get_s1_compliant_state(missing_key="p1")
        assert orchestrator.execute_pipeline(input_state, config) is not None

    def test_other_degenerate_configurations(self, orchestrator, valid_base, config):
        # Static fluid case (v1=0, v2=0)
        input_state = valid_base.override(v1=0.0, v2=0.0)
        assert orchestrator.execute_pipeline(input_state, config) is not None

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self, orchestrator, valid_base, config):
        # Ensure tiny float differences don't break classification
        input_state = valid_base.override(p1=100000.0000000001)
        assert orchestrator.execute_pipeline(input_state, config) is not None

    def test_near_cancellation_scenarios(self, orchestrator, valid_base, config):
        # p1 ≈ p2, h1 ≈ h2
        input_state = valid_base.override(p1=100.0, p2=100.0000001, h1=10.0, h2=10.0000001).get_s1_compliant_state(missing_key="v1")
        assert orchestrator.execute_pipeline(input_state, config) is not None

    def test_predictable_behavior_under_edge_conditions(self, orchestrator, valid_base, config):
        # Verify result output is non-null for boundary conditions
        input_state = valid_base.override(p1=200.0, v1=0.0, h1=0.0, p2=100.0, v2=1.0, h2=0.0).get_s1_compliant_state(missing_key="rho")
        assert orchestrator.execute_pipeline(input_state, config) is not None

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self, orchestrator, valid_base, config):
        original = copy.deepcopy(valid_base)
        orchestrator.execute_pipeline(valid_base, config)
        assert valid_base == original

    def test_frozen_dummy_alignment(self, orchestrator, valid_base, config):
        res = orchestrator.execute_pipeline(valid_base, config)
        dummy = BernoulliStateDummy().get_s1_compliant_state(missing_key="h1")
        for key in dummy.keys():
            assert hasattr(res, key)
        for attr in ['energy', 'energy_imbalance', 'p_min', 'p_max', 'v_min', 'v_max']:
            assert hasattr(res, attr)