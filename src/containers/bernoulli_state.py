from typing import List, Any
import math
from src.interfaces.bernoulli_state_interface import BernoulliStateInterface

# Canonical sentinel for unfilled properties prior to S3-S5 calculation loops
UNFILLED = float('nan')

class BernoulliState(BernoulliStateInterface):
    """
    The concrete Sovereign Container.
    Explicitly inherits from BernoulliStateInterface to enforce a 100% 
    structural match with the frozen project constitution contract.
    """
    __slots__ = (
        'p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho',
        'energy', 'energy_imbalance',
        'p_min', 'p_max', 'v_min', 'v_max'
    )

    def __init__(
        self,
        p1: float = UNFILLED,
        p2: float = UNFILLED,
        v1: float = UNFILLED,
        v2: float = UNFILLED,
        h1: float = UNFILLED,
        h2: float = UNFILLED,
        rho: float = UNFILLED,
        energy: List[float] = None,
        energy_imbalance: float = UNFILLED,
        p_min: float = UNFILLED,
        p_max: float = UNFILLED,
        v_min: float = UNFILLED,
        v_max: float = UNFILLED
    ):
        # Primary Bernoulli variables
        self.p1 = float(p1)
        self.p2 = float(p2)
        self.v1 = float(v1)
        self.v2 = float(v2)
        self.h1 = float(h1)
        self.h2 = float(h2)
        self.rho = float(rho)
        
        # Energy bookkeeping (S4)
        self.energy = energy if energy is not None else [UNFILLED, UNFILLED]
        self.energy_imbalance = float(energy_imbalance)
        
        # Constraint export bounds (S5)
        self.p_min = float(p_min)
        self.p_max = float(p_max)
        self.v_min = float(v_min)
        self.v_max = float(v_max)

    def clone_with(self, **kwargs: Any) -> 'BernoulliState':
        """
        Returns a new, distinct BernoulliState instance with updated fields.
        Preserves the non-mutating execution paradigm across DAG steps.
        """
        base_attrs = {slot: getattr(self, slot) for slot in self.__slots__}
        base_attrs.update(kwargs)
        
        # Deep copy the array container to avoid shared-pointer mutation side effects
        if 'energy' in kwargs and kwargs['energy'] is not None:
            base_attrs['energy'] = list(kwargs['energy'])
            
        return BernoulliState(**base_attrs)

    def validate_fully_filled(self) -> None:
        """
        Quality gate ensuring that zero UNFILLED or NaN properties remain 
        in the Sovereign Container at the pipeline terminal boundary.
        """
        for slot in self.__slots__:
            val = getattr(self, slot)
            if slot == 'energy':
                if any(math.isnan(x) for x in val):
                    raise ValueError("Sovereign Container validation failed: 'energy' array contains UNFILLED elements.")
            elif math.isnan(val):
                raise ValueError(f"Sovereign Container validation failed: Field '{slot}' is left UNFILLED.")