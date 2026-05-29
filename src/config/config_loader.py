import json
import os
from src.config.config_interface import SolverConfig

def load_and_validate_config(config_path: str = "config/config.json") -> SolverConfig:
    """
    Loads the actual configuration file from disk and explicitly validates 
    it against the frozen SolverConfig contract-only interface.
    
    Aborts execution immediately if any structural deviation is detected.
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
                f"Configuration Invariant Violation: 'config.json' is not valid JSON. Internal error: {e}"
            ) from e

    try:
        # Dictionary unpacking creates the direct, un-defaulted link to the interface fields
        validated_config = SolverConfig(**raw_data)
    except TypeError as e:
        raise TypeError(
            f"Configuration Invariant Violation: The runtime 'config.json' file does not "
            f"match the structural contract defined in 'config_interface.py'. Internal validation error: {e}"
        ) from e

    return validated_config