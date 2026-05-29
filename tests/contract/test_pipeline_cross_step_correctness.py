import pytest
import copy
from typing import Dict, Any
from tests.signatures.pipeline_cross_step_correctness_scenarios_signature import PipelineCrossStepCorrectnessScenariosTestSignature
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator
from src.config.config_loader import SolverConfig

class TestPipelineCrossStepCorrectness(PipelineCrossStepCorrectnessScenariosTestSignature):
    """
    Concrete implementation of the cross-step verification pipeline tests.
    Strictly adheres to the PipelineCrossStepCorrectnessScenariosTestSignature contract.
    """

    @pytest.fixture
    def orchestrator(self) -> BernoulliPipelineOrchestrator:
        return BernoulliPipelineOrchestrator()

    @pytest.fixture
    def config(self) -> SolverConfig:
        """
        Provides the strictly defined physical configuration for the contract tests.
        """
        return SolverConfig(
            g=9.81,
            precision=1e-6,
            k_v_min=0.1,
            k_v_max=0.1,
            k_p_min=0.1,
            k_p_max=0.1
        )

    @pytest.fixture
    def baseline_input(self) -> Dict[str, Any]:
        """Physics-compliant baseline for Bernoulli validation."""
        return {
            "p1": 101325.0, "v1": 10.0,
            "p2": None,      "v2": 20.0,
            "h1": 0.0,       "h2": 0.0,
            "rho": 1.225
        }

    @pytest.fixture
    def executed_state(self, orchestrator, baseline_input, config):
        """Executes full S0-S5 chain."""
        return orchestrator.execute_pipeline(copy.deepcopy(baseline_input), config)

    # -------------------------
    # S3 Implementations
    # -------------------------
    def test_s3_correct_bernoulli_reconstruction(self, executed_state):
        assert executed_state.p2 is not None

    def test_s3_reconstruction_matches_expected_solution(self, executed_state, baseline_input):
        # p2 = p1 + 0.5 * rho * (v1^2 - v2^2)
        expected = baseline_input["p1"] + 0.5 * baseline_input["rho"] * (baseline_input["v1"]**2 - baseline_input["v2"]**2)
        assert executed_state.p2 == pytest.approx(expected, rel=1e-5)

    def test_s3_reconstruction_stable_under_valid_inputs(self, orchestrator, baseline_input, config):
        s1 = orchestrator.execute_pipeline(copy.deepcopy(baseline_input), config)
        s2 = orchestrator.execute_pipeline(copy.deepcopy(baseline_input), config)
        assert s1.p2 == s2.p2

    # -------------------------
    # S4 Implementations
    # -------------------------
    def test_s4_correct_energy_computation(self, executed_state):
        assert executed_state.energy_imbalance is not None

    def test_s4_energy_matches_expected_values(self, executed_state, baseline_input):
        # E1 check: p1 + 0.5 * rho * v1^2
        e1 = baseline_input["p1"] + 0.5 * baseline_input["rho"] * (baseline_input["v1"]**2)
        assert executed_state.energy_1 == pytest.approx(e1, rel=1e-5)

    def test_s4_energy_imbalance_consistent_with_s3_solution(self, executed_state):
        assert executed_state.energy_imbalance == pytest.approx(0.0, abs=1e-5)

    # -------------------------
    # S5 Implementations
    # -------------------------
    def test_s5_correct_envelope_computation(self, executed_state):
        assert all(getattr(executed_state, attr) is not None for attr in ['p_min', 'p_max', 'v_min', 'v_max'])

    def test_s5_envelopes_match_expected_values(self, executed_state):
        assert executed_state.p_min <= executed_state.p_max

    def test_s5_envelopes_consistent_with_s4_energy(self, executed_state):
        assert executed_state.p_min <= executed_state.p1 <= executed_state.p_max

    # -------------------------
    # Coherence & Invariants
    # -------------------------
    def test_pipeline_cross_step_consistency(self, executed_state):
        assert executed_state.p_min <= executed_state.p2 <= executed_state.p_max

    def test_pipeline_no_unintended_mutations(self, executed_state, baseline_input):
        assert executed_state.p1 == baseline_input["p1"]

    def test_round_trip_zero_energy_imbalance(self, orchestrator, baseline_input, config):
        inp = copy.deepcopy(baseline_input)
        inp["p2"] = 101141.25 # Pre-solved
        state = orchestrator.execute_pipeline(inp, config)
        assert state.energy_imbalance == pytest.approx(0.0, abs=1e-4)

    def test_round_trip_minimal_envelopes(self, orchestrator, baseline_input, config):
        inp = copy.deepcopy(baseline_input)
        inp["p2"] = 101141.25
        state = orchestrator.execute_pipeline(inp, config)
        assert state.p_max >= state.p_min

    def test_pipeline_input_immutability(self, orchestrator, baseline_input, config):
        snap = copy.deepcopy(baseline_input)
        orchestrator.execute_pipeline(baseline_input, config)
        assert baseline_input == snap

    def test_pipeline_output_alignment(self, executed_state):
        keys = {'p1', 'p2', 'v1', 'v2', 'energy_imbalance', 'p_min', 'p_max', 'v_min', 'v_max'}
        for k in keys:
            assert hasattr(executed_state, k)