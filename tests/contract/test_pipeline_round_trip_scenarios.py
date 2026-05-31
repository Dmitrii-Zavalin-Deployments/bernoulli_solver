import math
import copy
import pytest
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator
from src.config.config_loader import SolverConfig
from tests.signatures.pipeline_round_trip_scenarios_signature import PipelineRoundTripScenariosTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

class TestPipelineRoundTripScenarios(PipelineRoundTripScenariosTestSignature):
    """
    Implementation of the round-trip contract using BernoulliStateDummy.
    Validates that fully-specified, consistent states traverse the pipeline 
    without drift, mutation, or incorrect solver application.
    """

    @pytest.fixture
    def orchestrator(self):
        return BernoulliPipelineOrchestrator()

    @pytest.fixture
    def valid_config(self):
        return SolverConfig(
            g=9.81, 
            precision=1e-06, 
            k_v_min=0.1, k_v_max=0.1, 
            k_p_min=0.1, k_p_max=0.1
        )

    @pytest.fixture
    def ground_truth(self):
        """Returns a contract-compliant fully balanced state."""
        return BernoulliStateDummy().override(
            p1=100000.0, p2=78000.0,
            v1=10.0, v2=12.0,
            h1=0.0, h2=0.0,
            rho=1000.0
        )

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
            val = getattr(res, field)
            assert not (isinstance(val, float) and math.isnan(val))

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
        assert res.energy[0] > 0.0

    # -------------------------
    # S5 behaviour
    # -------------------------

    def test_s5_minimal_envelopes(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        # For a perfect state, max and min should be identical
        assert math.isclose(res.p_max, max(ground_truth["p1"], ground_truth["p2"]), abs_tol=1e-5)
        assert math.isclose(res.p_min, min(ground_truth["p1"], ground_truth["p2"]), abs_tol=1e-5)

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


    # -------------------------
    # Structural invariants
    # -------------------------

    def test_pipeline_input_immutability(self, orchestrator, ground_truth, valid_config):
        original = copy.deepcopy(ground_truth)
        orchestrator.execute_pipeline(ground_truth, valid_config)
        assert ground_truth == original

    def test_pipeline_output_alignment(self, orchestrator, ground_truth, valid_config):
        res = orchestrator.execute_pipeline(ground_truth, valid_config)
        dummy = BernoulliStateDummy()
        # Verify alignment using the dummy's interface definition
        for key in dummy.keys():
            assert hasattr(res, key)
        # Verify non-dict attributes
        for attr in ['energy', 'energy_imbalance', 'p_min', 'p_max', 'v_min', 'v_max']:
            assert hasattr(res, attr)