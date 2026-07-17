import json
import os
from jsonschema import validate, ValidationError

def load_and_validate_config(
    config_path: str = "config/config.json", 
    schema_path: str = None
) -> dict:
    """
    Loads the runtime configuration file from disk and validates 
    it against the bernoulli_config.schema.json contract.
    
    Aborts execution immediately if the JSON structure does not 
    perfectly match the expected configuration parameters.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration Invariant Violation: Required runtime configuration file "
            f"not found at target path: '{config_path}'"
        )

    # Automatically resolve schema directory if none is explicitly passed
    if schema_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate_nested = os.path.join(base_dir, "schema", "bernoulli_config.schema.json")
        candidate_flat = os.path.join(os.path.dirname(base_dir), "schema", "bernoulli_config.schema.json")
        
        if os.path.exists(candidate_nested):
            schema_path = candidate_nested
        elif os.path.exists(candidate_flat):
            schema_path = candidate_flat
        else:
            # Fallback configuration directory coordinate
            schema_path = "schema/bernoulli_config.schema.json"

    if not os.path.exists(schema_path):
        raise FileNotFoundError(
            f"Configuration Invariant Violation: Required schema file "
            f"not found at target path: '{schema_path}'"
        )

    # 1. Read and parse runtime configuration file
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Configuration Invariant Violation: '{config_path}' is not valid JSON. Internal error: {e}"
            ) from e

    # 2. Read and parse structural schema file
    with open(schema_path, "r", encoding="utf-8") as f:
        try:
            schema_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Configuration Invariant Violation: Schema '{schema_path}' is not valid JSON. Internal error: {e}"
            ) from e

    # 3. Validate runtime configurations against structural schema
    try:
        validate(instance=raw_data, schema=schema_data)
    except ValidationError as e:
        raise ValueError(
            f"Configuration Invariant Violation: The runtime configuration file does not "
            f"match the structural contract defined in '{schema_path}'. "
            f"Validation failure message: {e.message}"
        ) from e

    return raw_data