import pytest
import jsonschema
import sys
from unittest.mock import patch, MagicMock, mock_open
from src.main import BernoulliPipelineOrchestrator, run_solver, main
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
            # Fixed: Initialized all required fields for BernoulliState using dictionary constraints mapping
            with patch.object(orchestrator.s2_constructor, 'construct_partial_state', 
                              return_value=BernoulliState(
                                  p1=100, p2=50, v1=10, v2=5, h1=0, h2=0, rho=1.0,
                                  energy=[100.0, 100.0], energy_imbalance=0.0,
                                  initial_conditions={"velocity": [10.0, 0.0, 0.0], "pressure": 100.0},
                                  physical_constraints={
                                      "min_pressure": 50.0, "max_pressure": 100.0,
                                      "min_velocity": 5.0, "max_velocity": 10.0
                                  }
                              )):
                with patch.object(orchestrator.s4_diagnician, 'compute_energy_and_residual') as mock_s4:
                    with patch.object(orchestrator.s5_enveloper, 'compute_min_max_constraints') as mock_s5:
                        
                        mock_s4.return_value = MagicMock(spec=BernoulliState)
                        mock_s5.return_value = MagicMock(spec=BernoulliState)
                        
                        orchestrator.execute_pipeline(raw_input, mock_config)
                        # Assert that S4 was called, confirming execution flow
                        assert mock_s4.called

@patch("pathlib.Path.exists", return_value=True)
@patch("src.main.load_and_validate_config")
@patch("builtins.open", new_callable=mock_open, read_data='{"p1": null, "p2": 50, "v1": 10, "v2": 5, "h1": 0, "h2": 0, "rho": 1.0}')
@patch("jsonschema.validate")
@patch("json.load")
def test_run_solver_full_path(mock_json_load, mock_validate, mock_file, mock_config_loader, mock_exists):
    """Covers lines 164-195 (Run solver success path)."""
    
    # 1. Properly mock the configuration object with required numeric attributes
    mock_config = MagicMock()
    mock_config.g = 9.81
    mock_config.precision = 0.001
    mock_config.k_v_min = 0.0
    mock_config.k_v_max = 100.0
    mock_config.k_p_min = 0.0
    mock_config.k_p_max = 1000.0
    mock_config_loader.return_value = mock_config

    # 2. Mock input data with one null value to satisfy S1
    mock_json_load.return_value = {"p1": None, "p2": 50, "v1": 10, "v2": 5, "h1": 0, "h2": 0, "rho": 1.0}
    
    # Fixed: Passed 3 positional arguments to match signature: run_solver(folder, input, output)
    result = run_solver(".", "input.json", "bernoulli_solver_output.json")
    
    assert "bernoulli_solver_output.json" in result
    assert mock_config_loader.called

@patch("src.main.run_solver")
def test_main_success(mock_run_solver):
    """Covers lines 199-205 (Main success path)."""
    # Fixed: Replaced plain filename positional args with the explicit flags required by ArgumentParser
    cli_args = [
        'script.py', 
        '--input_output_folder', '.', 
        '--input_file_name', 'input.json', 
        '--output_file_name', 'bernoulli_solver_output.json'
    ]
    with patch.object(sys, 'argv', cli_args):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0

@patch("src.main.run_solver")
def test_main_failure(mock_run_solver):
    """Covers lines 199, 206-209 (Main failure path)."""
    mock_run_solver.side_effect = Exception("Fatal failure")
    
    # Fixed: Replaced plain filename positional args with the explicit flags required by ArgumentParser
    cli_args = [
        'script.py', 
        '--input_output_folder', '.', 
        '--input_file_name', 'input.json', 
        '--output_file_name', 'bernoulli_solver_output.json'
    ]
    with patch.object(sys, 'argv', cli_args):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1

def test_validate_boundaries_error(orchestrator):
    """Covers error handling in validation logic."""
    with pytest.raises(ValueError, match="Negative pressure"):
        orchestrator._validate_boundaries({"p1": -10})

@patch("src.main.jsonschema.validate")
@patch("src.main.load_and_validate_config")
@patch("pathlib.Path.exists", return_value=True)
# FIX: Added read_data to satisfy json.load(f)
@patch("builtins.open", new_callable=mock_open, read_data='{"p1": 100, "p2": 50, "v1": 10, "v2": 5, "h1": 0, "h2": 0, "rho": 1.0}')
def test_run_solver_schema_validation_error(mock_file, mock_exists, mock_config, mock_validate):
    """
    Covers lines 176-178: Input schema validation failure.
    """
    # Simulate a validation failure during the schema check (line 174)
    mock_validate.side_effect = jsonschema.exceptions.ValidationError("Schema mismatch")

    # Fixed: Passed 3 positional arguments to match signature: run_solver(folder, input, output)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        run_solver(".", "dummy_path.json", "bernoulli_solver_output.json")

@patch("sys.argv", ["bernoulli_solver"]) # Missing the required input path argument
def test_main_missing_argument():
    """
    Covers lines 200-201: Main execution failure due to missing argument.
    """
    with pytest.raises(SystemExit) as cm:
        main()
    
    # Fixed: Assert that system exited with code 2, since argparse defaults to 2 on missing required fields
    assert cm.value.code == 2