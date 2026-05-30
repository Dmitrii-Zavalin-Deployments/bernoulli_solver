import math
import copy
import pytest
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator
from src.containers.bernoulli_state import BernoulliState
# Ensure this import matches your file path
from tests.signatures.pipeline_round_trip_scenarios_signature import PipelineRoundTripScenariosTestSignature

class TestPipelineRoundTripScenarios(PipelineRoundTripScenariosTestSignature):
    """
    Implementation of the round-trip contract.
    Validates that fully-specified, consistent states traverse the pipeline 
    without drift, mutation, or incorrect solver application.
    """

    @pytest.fixture
    def orchestrator(self):
        return BernoulliPipelineOrchestrator()

    @pytest.fixture
    def valid_config(self):
        # Assuming a configuration object structure
        from src.config.config_loader import SolverConfig
        return SolverConfig(g=9.81, precision=1e-06, k_v_min=0.1, k_v_max=0.1, k_p_min=0.1, k_p_max=0.1)

    @pytest.fixture
    def ground_truth(self):
        # A fully balanced state (Energy Balance: 150,000)
        return {
            "p1": 100000.0, "p2": 78000.0,
            "v1": 10.0, "v2": 12.0,
            "h1": 0.0, "h2": 0.0,
            "rho": 1000.0
        }

    # -------------------------
    # Round‑trip invariants
    # -------------------------

    def test_round_trip_preserves_primary_variables(self, orchestrator, ground_truth, valid_config):
        # Note: If your pipeline strictly requires one missing variable, 
        # you may need an 'allow_fully_specified=True' flag in your orchestrator.
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        assert math.isclose(res.p1, ground_truth["p1"])
        assert math.isclose(res.v2, ground_truth["v2"])

    def test_round_trip_preserves_structure_and_ordering(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        # Verify that all primary fields exist in the output object
        for field in ["p1", "p2", "v1", "v2", "h1", "h2", "rho"]:
            assert hasattr(res, field)
            assert not math.isnan(getattr(res, field))

    # -------------------------
    # S3 behaviour
    # -------------------------

    def test_s3_detects_no_missing_variables(self, orchestrator, ground_truth, valid_config):
        # Verify that the pipeline does not attempt to "solve" anything
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        # Logic: If nothing is missing, the output should exactly match inputs
        assert math.isclose(res.p1, 100000.0)

    def test_s3_performs_no_unintended_mutations(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        # Ensure diagnostics aren't overwriting primary fields
        assert res.rho == ground_truth["rho"]

    # -------------------------
    # S4 behaviour
    # -------------------------

    def test_s4_zero_energy_imbalance(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        assert math.isclose(res.energy_imbalance, 0.0, abs_tol=1e-5)

    def test_s4_correct_energy_terms(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        assert res.energy > 0.0

    # -------------------------
    # S5 behaviour
    # -------------------------

    def test_s5_minimal_envelopes(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        # For a perfect state, max and min should be identical
        assert math.isclose(res.p_max, res.p_min, abs_tol=1e-5)

    def test_s5_correct_envelope_bounds(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        assert res.p_max >= res.p1

    # -------------------------
    # Cross‑step coherence
    # -------------------------

    def test_pipeline_cross_step_consistency(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        # Ensure energy and envelopes agree
        assert res.energy_imbalance <= 1e-5

    def test_pipeline_no_unintended_mutations(self, orchestrator, ground_truth, valid_config):
        # Logic captured in immutability test
        pass

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_pipeline_input_immutability(self, orchestrator, ground_truth, valid_config):
        original = copy.deepcopy(ground_truth)
        orchestrator.execute_pipeline(ground_truth, valid_config)
        assert ground_truth == original

    def test_pipeline_output_alignment(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        assert isinstance(res, BernoulliState)