import pytest
import sys
from unittest.mock import patch, MagicMock, mock_open
from src.bernoulli_pipeline_orchestrator import BernoulliPipelineOrchestrator, run_solver, main
from src.containers.bernoulli_state import BernoulliState

@pytest.fixture
def orchestrator():
    return BernoulliPipelineOrchestrator()

@pytest.fixture
def mock_config():
    # Mocking SolverConfig dataclass
    config = MagicMock()
    config.g = 9.81
    return config

def test_execute_pipeline_identity_path(orchestrator, mock_config):
    """Covers lines 106-116 (Identity Path where missing_variable is None)."""
    raw_input = {"p1": 100, "p2": 50, "v1": 10, "v2": 5, "h1": 0, "h2": 0, "rho": 1.0}
    
    # Mocking steps to return valid data without solving for a missing variable
    with patch.object(orchestrator.s0_classifier, 'classify_filled_and_unfilled', return_value=(None, None)):
        with patch.object(orchestrator.s1_validator, 'enforce_exactly_one_missing', return_value=(raw_input, None)):
            # Fixed: Initialized all required fields for BernoulliState
            with patch.object(orchestrator.s2_constructor, 'construct_partial_state', 
                              return_value=BernoulliState(p1=100, p2=50, v1=10, v2=5, h1=0, h2=0, rho=1.0,
                                                          energy=[100.0, 100.0], energy_imbalance=0.0,
                                                          p_min=50.0, p_max=100.0, v_min=5.0, v_max=10.0)):
                with patch.object(orchestrator.s4_diagnician, 'compute_energy_and_residual') as mock_s4:
                    with patch.object(orchestrator.s5_enveloper, 'compute_min_max_constraints') as mock_s5:
                        
                        mock_s4.return_value = MagicMock(spec=BernoulliState)
                        mock_s5.return_value = MagicMock(spec=BernoulliState)
                        
                        orchestrator.execute_pipeline(raw_input, mock_config)
                        # Assert that S4 was called, confirming execution flow
                        assert mock_s4.called

@patch("pathlib.Path.exists", return_value=True) # Fixed: Mocking filesystem existence
@patch("src.bernoulli_pipeline_orchestrator.load_and_validate_config")
@patch("builtins.open", new_callable=mock_open, read_data='{"p1": 100, "p2": 50, "v1": 10, "v2": 5, "h1": 0, "h2": 0, "rho": 1.0}')
@patch("jsonschema.validate")
@patch("json.load")
def test_run_solver_full_path(mock_json_load, mock_validate, mock_file, mock_config_loader, mock_exists):
    """Covers lines 164-195 (Run solver success path)."""
    mock_json_load.return_value = {"p1": 100, "p2": 50, "v1": 10, "v2": 5, "h1": 0, "h2": 0, "rho": 1.0}
    
    # We use a dummy path
    result = run_solver("input.json")
    
    assert "bernoulli_solver_output.json" in result
    assert mock_config_loader.called

@patch("src.bernoulli_pipeline_orchestrator.run_solver")
def test_main_success(mock_run_solver):
    """Covers lines 199-205 (Main success path)."""
    with patch.object(sys, 'argv', ['script.py', 'input.json']):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0

@patch("src.bernoulli_pipeline_orchestrator.run_solver")
def test_main_failure(mock_run_solver):
    """Covers lines 199, 206-209 (Main failure path)."""
    mock_run_solver.side_effect = Exception("Fatal failure")
    
    with patch.object(sys, 'argv', ['script.py', 'input.json']):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1

def test_validate_boundaries_error(orchestrator):
    """Covers error handling in validation logic."""
    with pytest.raises(ValueError, match="Negative pressure"):
        orchestrator._validate_boundaries({"p1": -10})