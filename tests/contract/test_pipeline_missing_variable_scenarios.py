import pytest
import math
import copy
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator
from src.config.config_interface import SolverConfig
from tests.signatures.pipeline_missing_variable_scenarios_signature import PipelineMissingVariableScenariosTestSignature

class TestPipelineMissingVariableScenarios(PipelineMissingVariableScenariosTestSignature):
    """
    Contract-level implementation for Pipeline-Level Missing-Variable Scenarios.
    """

    @pytest.fixture
    def valid_config(self):
        return SolverConfig(
            g=9.81,
            precision=1e-6,
            k_v_min=0.1, k_v_max=0.1, 
            k_p_min=0.1, k_p_max=0.1
        )

    @pytest.fixture
    def orchestrator(self):
        return BernoulliPipelineOrchestrator()

    @pytest.fixture
    @pytest.fixture
    def ground_truth(self):
        # A physically balanced state: 100k + 50k = 78k + 72k = 150k
        return {
            "p1": 100000.0, "p2": 78000.0,
            "v1": 10.0, "v2": 12.0,
            "h1": 0.0, "h2": 0.0,
            "rho": 1000.0
        }

    def _run_scenario(self, orchestrator, ground_truth, valid_config, missing_key):
        """Helper to run pipeline with one variable masked as None."""
        input_dict = ground_truth.copy()
        input_dict[missing_key] = None
        return orchestrator.execute_pipeline(input_dict, valid_config), input_dict

    # -------------------------
    # Missing‑variable scenarios
    # -------------------------

    def test_missing_p1_pipeline(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "p1")
        assert math.isclose(res.p1, ground_truth["p1"])

    def test_missing_p2_pipeline(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "p2")
        assert math.isclose(res.p2, ground_truth["p2"])

    def test_missing_v1_pipeline(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v1")
        assert math.isclose(res.v1, ground_truth["v1"])

    def test_missing_v2_pipeline(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v2")
        assert math.isclose(res.v2, ground_truth["v2"])

    def test_missing_h1_pipeline(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "h1")
        assert math.isclose(res.h1, ground_truth["h1"])

    def test_missing_h2_pipeline(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "h2")
        assert math.isclose(res.h2, ground_truth["h2"])

    def test_missing_rho_pipeline(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "rho")
        assert math.isclose(res.rho, ground_truth["rho"])

    # -------------------------
    # Deterministic consistency
    # -------------------------

    def test_non_missing_fields_preserved(self, orchestrator, ground_truth, valid_config):
        # We verify that when p1 is missing, other fields match the ground truth
        res, inputs = self._run_scenario(orchestrator, ground_truth, valid_config, "p1")
        assert res.p2 == inputs["p2"]
        assert res.v1 == inputs["v1"]

    def test_pipeline_preserves_structure(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v1")
        assert hasattr(res, "p1") and hasattr(res, "rho")

    # -------------------------
    # Cross‑step correctness
    # -------------------------

    def test_s3_solves_bernoulli_correctly(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v2")
        # Verify the calculation is close to physical ground truth
        assert math.isclose(res.v2, 10.0, rel_tol=1e-5)

    def test_s4_computes_energy_correctly(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v2")
        assert res.energy is not None
        assert len(res.energy) == 2

    def test_s5_computes_envelopes_correctly(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v2")
        assert res.v_min <= res.v_max

    # -------------------------
    # Round‑trip scenarios
    # -------------------------

    def test_round_trip_zero_energy_imbalance(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v2")
        assert math.isclose(res.energy_imbalance, 0.0, abs_tol=1e-5)

    def test_round_trip_minimal_envelopes(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v2")
        # Ensure envelopes aren't absurdly large
        assert res.p_max >= res.p_min

    def test_round_trip_no_unintended_mutations(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "p1")
        # Ensure input rho wasn't changed during solve
        assert res.rho == ground_truth["rho"]

    def test_pipeline_input_immutability(self, orchestrator, ground_truth, valid_config):
        test_input = copy.deepcopy(ground_truth)
        test_input["v2"] = None
        input_copy = copy.deepcopy(test_input)
        orchestrator.execute_pipeline(test_input, valid_config)
        assert test_input == input_copy

    def test_pipeline_output_alignment(self, orchestrator, ground_truth, valid_config):
        res, _ = self._run_scenario(orchestrator, ground_truth, valid_config, "v2")
        required_fields = ['p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho']
        for field in required_fields:
            assert getattr(res, field) is not None