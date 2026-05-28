from typing import List

class BernoulliStateInterface:
    """
    Contract‑only interface for the Sovereign Container.
    No logic, no defaults, no computations.
    """

    p1: float
    p2: float
    v1: float
    v2: float
    h1: float
    h2: float
    delta_h: float
    delta_v: float
    rho: float
    energy: List[float]          # [E1, E2]
    energy_imbalance: float      # E1 - E2