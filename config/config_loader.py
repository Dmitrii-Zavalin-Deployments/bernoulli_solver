import json
import os
from config.config_interface import SolverConfig

def load_and_validate_config(config_path: str = "config/config.json") -> SolverConfig:
    """
    Loads configuration, logs extra properties if found, and strips them 
    out before instantiating the SolverConfig dataclass.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration Invariant Violation: Required runtime configuration file "
            f"not found at target path: '{config_path}'"
        )

    with open(config_path, "r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Configuration Invariant Violation: '{config_path}' is not valid JSON. Internal error: {e}"
            ) from e

    # 1. Identify valid fields defined in the dataclass
    valid_fields = set(SolverConfig.__annotations__.keys())
    input_fields = set(raw_data.keys())

    # 2. Find extras (difference between input keys and valid class keys)
    extra_fields = input_fields - valid_fields
    if extra_fields:
        print(f"LOG: Found additional properties in config file: {extra_fields}")
        
        # 3. Create a filtered dictionary containing only valid keys
        filtered_data = {k: v for k, v in raw_data.items() if k in valid_fields}
    else:
        filtered_data = raw_data

    # 4. Instantiate with the filtered (clean) data
    try:
        validated_config = SolverConfig(**filtered_data)
    except TypeError as e:
        # This handles cases where mandatory fields are missing
        raise TypeError(
            f"Configuration Invariant Violation: Missing required parameters. "
            f"Internal error: {e}"
        ) from e

    return validated_config