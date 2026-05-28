from dataclasses import dataclass

@dataclass
class SolverConfig:
    """
    Contract-only interface for runtime configuration.
    Defines required configuration fields but does not assign values.
    """
    g: float            # gravitational acceleration (m/s^2)
    precision: float    # numerical precision for residuals and output rounding