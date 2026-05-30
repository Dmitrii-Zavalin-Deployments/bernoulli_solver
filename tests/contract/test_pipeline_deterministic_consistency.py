import pytest
import copy
import math
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator
from src.config.config_interface import SolverConfig
from tests.signatures.pipeline_deterministic_consistency_scenarios_signature import PipelineDeterministicConsistencyScenariosTestSignature

class TestPipelineDeterministicConsistency(PipelineDeterministicConsistencyScenariosTestSignature):
    """
    Implementation of the deterministic consistency scenarios.
    """

    @pytest.fixture
    def valid_config(self):
        return SolverConfig(
            g=9.81,
            k_v_min=0.1, k_v_max=0.1, 
            k_p_min=0.1, k_p_max=0.1
        )

    @pytest.fixture
    def fully_specified_input(self):
        # A fully specified input where E1 == E2 for easy round-trip validation
        return {
            "p1": 100000.0, "v1": 10.0, "h1": 0.0,
            "p2": 100000.0, "v2": 10.0, "h2": 0.0,
            "rho": 1000.0
        }

    @pytest.fixture
    def orchestrator(self):
        return BernoulliPipelineOrchestrator()

    @pytest.fixture
    def result_state(self, orchestrator, fully_specified_input, valid_config):
        return orchestrator.execute_pipeline(fully_specified_input, valid_config)

    def test_pipeline_preserves_primary_variables(self, result_state, fully_specified_input):
        assert result_state.p1 == fully_specified_input["p1"]
        assert result_state.p2 == fully_specified_input["p2"]
        assert result_state.v1 == fully_specified_input["v1"]
        assert result_state.v2 == fully_specified_input["v2"]

    def test_pipeline_preserves_diagnostic_fields_until_transformation(self, result_state):
        # We assume result_state is populated, so we check that energy exists
        # and is not the original unset sentinel (which was nan)
        assert not math.isnan(result_state.energy[0])
        assert not math.isnan(result_state.energy_imbalance)

    def test_pipeline_preserves_structure_and_ordering(self, result_state):
        # Check that we didn't lose fields or change types during processing
        assert isinstance(result_state.energy, list)
        assert len(result_state.energy) == 2

    def test_s3_detects_no_missing_variables(self, result_state, fully_specified_input):
        # S3 should produce values consistent with the input since nothing was missing
        assert math.isclose(result_state.p1, fully_specified_input["p1"])

    def test_s4_computes_energy_correctly_for_fully_specified_state(self, result_state, fully_specified_input, valid_config):
        rho = fully_specified_input["rho"]
        g = valid_config.g
        
        expected_e1 = fully_specified_input["p1"] + 0.5 * rho * (fully_specified_input["v1"]**2) + rho * g * fully_specified_input["h1"]
        assert math.isclose(result_state.energy[0], expected_e1)

    def test_s5_computes_envelopes_correctly_for_fully_specified_state(self, result_state, fully_specified_input, valid_config):
        # S5 manual verification based on your interface spec
        v_char = max(abs(result_state.v1), abs(result_state.v2))
        p_low = min(result_state.p1, result_state.p2)
        
        expected_v_min = -valid_config.k_v_min * v_char
        assert math.isclose(result_state.v_min, expected_v_min)

    def test_round_trip_zero_energy_imbalance(self, result_state):
        # Since input E1 == E2, imbalance should be 0
        assert math.isclose(result_state.energy_imbalance, 0.0, abs_tol=1e-5)

    def test_round_trip_minimal_envelopes(self, result_state):
        # Assuming k_v_min/max are small, verify envelopes are within reasonable bounds
        assert result_state.v_min <= 0 <= result_state.v_max

    def test_round_trip_no_unintended_mutations(self, result_state, fully_specified_input):
        # Ensure result fields are not just mutated references
        assert result_state.rho == fully_specified_input["rho"]

    def test_pipeline_input_immutability(self, orchestrator, fully_specified_input, valid_config):
        input_copy = copy.deepcopy(fully_specified_input)
        orchestrator.execute_pipeline(fully_specified_input, valid_config)
        assert fully_specified_input == input_copy

    def test_pipeline_output_alignment(self, result_state):
        # Verify the structure matches the interface expectations
        required_fields = ['p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho', 'energy', 'energy_imbalance']
        for field in required_fields:
            assert hasattr(result_state, field)