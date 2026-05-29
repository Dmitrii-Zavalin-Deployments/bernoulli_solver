from dataclasses import dataclass

@dataclass
class SolverConfig:
    """
    Contract-only interface for runtime configuration.
    Defines required configuration fields but does not assign values.

    All coefficients must be explicitly provided by the developer.
    No defaults, no implicit symmetry, no hidden coupling.
    """

    g: float                 # gravitational acceleration (m/s^2)
    precision: float         # numerical precision for residuals and rounding

    # S5 looseness coefficients (all four independent)
    k_v_min: float           # looseness factor for minimum velocity bound
    k_v_max: float           # looseness factor for maximum velocity bound
    k_p_min: float           # looseness factor for minimum pressure bound
    k_p_max: float           # looseness factor for maximum pressure bound

    # Identifier for observability and pipeline tracking.
    # Default value allows compatibility with legacy config files.
    id: str = "default_run"