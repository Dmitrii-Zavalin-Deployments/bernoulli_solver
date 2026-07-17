import pytest
import json
from config.config_loader import load_and_validate_config

@pytest.fixture
def mock_schema(tmp_path):
    """Generates a valid test schema on the fly to isolate filesystem dependencies."""
    schema_file = tmp_path / "bernoulli_config.schema.json"
    schema_data = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "g": {"type": "number"},
            "precision": {"type": "number", "minimum": 0},
            "k_v_min": {"type": "number"},
            "k_v_max": {"type": "number"},
            "k_p_min": {"type": "number"},
            "k_p_max": {"type": "number"}
        },
        "required": ["g", "precision", "k_v_min", "k_v_max", "k_p_min", "k_p_max"],
        "additionalProperties": false
    }
    schema_file.write_text(json.dumps(schema_data))
    return str(schema_file)

def test_load_config_file_not_found(mock_schema):
    """Validates branch: FileNotFoundError is thrown when config file doesn't exist."""
    with pytest.raises(FileNotFoundError, match="not found at target path"):
        load_and_validate_config("non_existent_config.json", schema_path=mock_schema)

def test_load_schema_file_not_found(tmp_path):
    """Validates branch: FileNotFoundError is thrown when schema file doesn't exist."""
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"g": 9.81}))
    
    with pytest.raises(FileNotFoundError, match="not found at target path"):
        load_and_validate_config(str(config_file), schema_path="non_existent_schema.json")

def test_load_config_invalid_json(tmp_path, mock_schema):
    """Validates branch: ValueError is thrown when config file contains broken JSON syntax."""
    config_file = tmp_path / "bad_syntax.json"
    config_file.write_text("{ 'invalid': missing_quotes }")
    
    with pytest.raises(ValueError, match="is not valid JSON"):
        load_and_validate_config(str(config_file), schema_path=mock_schema)

def test_load_config_schema_mismatch(tmp_path, mock_schema):
    """Validates branch: ValueError is thrown when configuration violates schema properties (missing files or extra fields)."""
    config_file = tmp_path / "invalid_schema.json"
    
    # Missing required elements (precision, bounds) and includes an extra field
    invalid_data = {
        "g": 9.80665,
        "extra_parameter": "illegal"
    }
    config_file.write_text(json.dumps(invalid_data))
    
    with pytest.raises(ValueError, match="does not match the structural contract"):
        load_and_validate_config(str(config_file), schema_path=mock_schema)

def test_load_config_success(tmp_path, mock_schema):
    """Validates happy path: successfully parses and returns a fully conforming configuration dict."""
    config_file = tmp_path / "valid_config.json"
    valid_data = {
        "g": 9.80665,
        "precision": 0.000001,
        "k_v_min": 0.15,
        "k_v_max": 0.25,
        "k_p_min": 0.12,
        "k_p_max": 0.18
    }
    config_file.write_text(json.dumps(valid_data))
    
    result = load_and_validate_config(str(config_file), schema_path=mock_schema)
    
    # Assert return object matches target input dictionaries perfectly
    assert result == valid_data
    assert result["precision"] == 0.000001