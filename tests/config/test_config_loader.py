import json

import pytest

from config.config_loader import load_and_validate_config


def test_load_config_file_not_found():
    """Validates branch: FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="not found at target path"):
        load_and_validate_config("non_existent_path.json")

def test_load_config_invalid_json(tmp_path):
    """Validates branch: JSONDecodeError handled as ValueError."""
    config_file = tmp_path / "bad_syntax.json"
    config_file.write_text("{ 'invalid': json... }") 
    
    with pytest.raises(ValueError, match="not valid JSON"):
        load_and_validate_config(str(config_file))

def test_load_config_with_extra_fields(tmp_path):
    """
    Validates that extra fields are filtered out (not raising an error)
    and the config loads successfully.
    """
    config_file = tmp_path / "extra_fields.json"
    
    # Valid fields + an 'extra' field that should be ignored
    data = {
        "g": 9.81, 
        "precision": 0.001, 
        "k_v_min": 0.0, "k_v_max": 100.0, 
        "k_p_min": 0.0, "k_p_max": 1000.0,
        "extra_field": "ignore_me" 
    }
    config_file.write_text(json.dumps(data))
    
    # This should now succeed
    result = load_and_validate_config(str(config_file))
    assert result.g == 9.81
    assert not hasattr(result, "extra_field")

def test_load_config_missing_fields(tmp_path):
    """Validates that missing required fields still raise a TypeError."""
    config_file = tmp_path / "missing_fields.json"
    
    # Missing the 'g' field
    data = {
        "precision": 0.001, 
        "k_v_min": 0.0, "k_v_max": 100.0, 
        "k_p_min": 0.0, "k_p_max": 1000.0
    }
    config_file.write_text(json.dumps(data))
    
    with pytest.raises(TypeError, match="Missing required parameters"):
        load_and_validate_config(str(config_file))

def test_load_config_success(tmp_path):
    """Validates happy path with exact fields."""
    config_file = tmp_path / "valid_config.json"
    
    # Update this dictionary to match your SolverConfig fields exactly
    valid_data = {
        "g": 9.81, 
        "precision": 0.001, 
        "k_v_min": 0.0, "k_v_max": 100.0, 
        "k_p_min": 0.0, "k_p_max": 1000.0,
    }
    config_file.write_text(json.dumps(valid_data))
    
    # This should now succeed and return the object
    result = load_and_validate_config(str(config_file))
    assert result.g == 9.81