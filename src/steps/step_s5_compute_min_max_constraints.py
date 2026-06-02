from typing import Any
from src.interfaces.step_interfaces.step_s5_compute_min_max_constraints_interface import StepS5ComputeMinMaxConstraintsInterface
from src.containers.bernoulli_state import BernoulliState

class StepS5ComputeMinMaxConstraints(StepS5ComputeMinMaxConstraintsInterface):
    """
    Concrete implementation of Step S5: Compute the Bernoulli-derived physical 
    constraint envelopes required by the Navier–Stokes solver.
    """

    def compute_min_max_constraints(self, state_with_energy: BernoulliState, config: Any) -> BernoulliState:
        """
        Computes physical boundary constraint parameters using independent tuning coefficients.
        Accepts 'state_with_energy' parameter exactly as mandated by the pipeline contract.
        """
        # 1. Extract inputs
        p1, p2 = state_with_energy.p1, state_with_energy.p2
        v1, v2 = state_with_energy.v1, state_with_energy.v2
        imbalance = state_with_energy.energy_imbalance

        # 2. Compute Constraints with Imbalance Awareness
        # If imbalance > 0, we apply the buffer (looseness coefficients).
        # If imbalance == 0, we return the minimal/tightest envelopes.
        if imbalance > 0:
            p_diff = abs(p1 - p2)
            v_max_abs = max(abs(v1), abs(v2))
            
            p_min = min(p1, p2) - config.k_p_min * p_diff
            p_max = max(p1, p2) + config.k_p_max * p_diff
            v_min = -config.k_v_min * v_max_abs
            v_max =  config.k_v_max * v_max_abs
        else:
            # Minimal Envelopes (Zero Imbalance)
            p_min = min(p1, p2)
            p_max = max(p1, p2)
            v_min = min(v1, v2)
            v_max = max(v1, v2)
        
        # 3. Return a brand new instance protecting historical immutability
        return BernoulliState(
            p1=p1, p2=p2, v1=v1, v2=v2, 
            h1=state_with_energy.h1, h2=state_with_energy.h2, rho=state_with_energy.rho,
            energy=state_with_energy.energy, 
            energy_imbalance=imbalance,
            p_min=p_min, p_max=p_max, v_min=v_min, v_max=v_max
        )