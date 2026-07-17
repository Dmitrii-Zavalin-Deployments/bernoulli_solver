import pytest
import json
from config.config_loader import load_and_validate_config

def test_load_config_file_not_found():
    """Validates branch: Lines 13-17 (FileNotFoundError)."""
    with pytest.raises(FileNotFoundError, match="not found at target path"):
        load_and_validate_config("non_existent_path.json")

def test_load_config_invalid_json(tmp_path):
    """Validates branch: Lines 20-25 (JSONDecodeError handled as ValueError)."""
    config_file = tmp_path / "bad_syntax.json"
    config_file.write_text("{ 'invalid': json... }") # Invalid JSON syntax
    
    with pytest.raises(ValueError, match="not valid JSON"):
        load_and_validate_config(str(config_file))

def test_load_config_schema_mismatch(tmp_path):
    """Validates branch: Lines 27-36 (TypeError due to Schema Mismatch)."""
    config_file = tmp_path / "invalid_schema.json"
    # Using an 'extra' field that isn't in your SolverConfig dataclass
    # to trigger the TypeError during unpacking.
    invalid_data = {"extra_field": "oops", "another_field": 1}
    config_file.write_text(json.dumps(invalid_data))
    
    with pytest.raises(TypeError, match="structural contract"):
        load_and_validate_config(str(config_file))

def test_load_config_success(tmp_path):
    """
    Validates branch: Lines 27-38 (Happy path).
    
    NOTE: Replace the dictionary below with the EXACT fields present in 
    your src/config/config_interface.py (SolverConfig dataclass).
    """
    config_file = tmp_path / "valid_config.json"
    
    # Update this dictionary to match your SolverConfig fields exactly
    valid_data = {
        "g": 9.81, 
        "precision": 0.001, "k_v_min": 0.0, "k_v_max": 100.0, "k_p_min": 0.0, "k_p_max": 1000.0,
    }
    config_file.write_text(json.dumps(valid_data))
    
    # This should now succeed and return the object
    result = load_and_validate_config(str(config_file))
    assert result is not None