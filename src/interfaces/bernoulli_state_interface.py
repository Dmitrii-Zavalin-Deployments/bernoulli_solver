from typing import List, Dict, Any

class BernoulliStateInterface:
    """
    Contract-only interface for the Sovereign Container.
    No logic, no defaults, no computations.
    """

    # Primary Bernoulli variables
    p1: float
    p2: float
    v1: float
    v2: float
    h1: float
    h2: float
    rho: float
    initial_conditions: Dict[str, Any]
    physical_constraints: Dict[str, Any]

    # Energy bookkeeping (S4)
    energy: List[float]          # [E1, E2]
    energy_imbalance: float      # E1 - E2

    # Constraint export (S5)
