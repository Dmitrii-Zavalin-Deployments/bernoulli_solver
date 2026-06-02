from typing import Any
from src.interfaces.step_interfaces.step_s5_compute_min_max_constraints_interface import StepS5ComputeMinMaxConstraintsInterface
from src.containers.bernoulli_state import BernoulliState

class StepS5ComputeMinMaxConstraints(StepS5ComputeMinMaxConstraintsInterface):
    """
    Concrete implementation of Step S5: Compute the Bernoulli-derived physical 
    constraint envelopes required by the Navier–Stokes solver.
    Inherits explicitly from StepS5ComputeMinMaxConstraintsInterface to guarantee 
    a 100% structural match to the project constitution.
    """

    def compute_min_max_constraints(self, state: BernoulliState, config: Any) -> BernoulliState:
        """
        Computes loose but truthful physical boundary constraint parameters using 
        four independent tuning coefficients provided in the configuration.
        
        Returns a brand NEW BernoulliState instance with all constraint bounds 
        fully populated, leaving all upstream primary and diagnostic fields unchanged.
        """
        # 1. Extract inputs
        p1, p2 = state.p1, state.p2
        v1, v2 = state.v1, state.v2
        
        # 2. Extract coefficients
        k_v_min, k_v_max = config.k_v_min, config.k_v_max
        k_p_min, k_p_max = config.k_p_min, config.k_p_max
        
        # 3. Compute common differentials
        p_diff = abs(p1 - p2)
        v_max_abs = max(abs(v1), abs(v2))
        
        # 4. Compute Constraints (matching test signature formulas)
        v_min = -k_v_min * v_max_abs
        v_max =  k_v_max * v_max_abs
        p_min = min(p1, p2) - k_p_min * p_diff
        p_max = max(p1, p2) + k_p_max * p_diff
        
        # 5. Return immutable state
        return BernoulliState(
            p1=p1, p2=p2, v1=v1, v2=v2, h1=state.h1, h2=state.h2, rho=state.rho,
            energy=state.energy, energy_imbalance=state.energy_imbalance,
            p_min=p_min, p_max=p_max, v_min=v_min, v_max=v_max
        )