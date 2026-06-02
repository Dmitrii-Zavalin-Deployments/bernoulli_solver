from typing import List
from dataclasses import dataclass
from src.interfaces.bernoulli_state_interface import BernoulliStateInterface

@dataclass(init=False)
class BernoulliState(BernoulliStateInterface):
    """
    The concrete Sovereign Container.
    A pure data container with absolutely zero operational logic, methods, 
    or internal functions, ensuring a 100% pristine structural match 
    with the frozen project constitution contract.
    """
    
    # Enforce a strict memory layout and prevent the injection of excess properties
    __slots__ = (
        'p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho',
        'energy', 'energy_imbalance',
        'p_min', 'p_max', 'v_min', 'v_max'
    )

    # Explicit class-level type annotations matching BernoulliStateInterface 100%
    p1: float
    p2: float
    v1: float
    v2: float
    h1: float
    h2: float
    rho: float
    energy: List[float]
    energy_imbalance: float
    p_min: float
    p_max: float
    v_min: float
    v_max: float

    def __init__(
        self,
        p1: float,
        p2: float,
        v1: float,
        v2: float,
        h1: float,
        h2: float,
        rho: float,
        energy: List[float],
        energy_imbalance: float,
        p_min: float,
        p_max: float,
        v_min: float,
        v_max: float
    ):
        """
        Pure assignment constructor. No defaults, no implicit type casting, 
        and no computations. All states (including UNFILLED fields) must 
        be explicitly supplied by the caller step.
        """
        self.p1 = p1
        self.p2 = p2
        self.v1 = v1
        self.v2 = v2
        self.h1 = h1
        self.h2 = h2
        self.rho = rho
        self.energy = energy
        self.energy_imbalance = energy_imbalance
        self.p_min = p_min
        self.p_max = p_max
        self.v_min = v_min
        self.v_max = v_max