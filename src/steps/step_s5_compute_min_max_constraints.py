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

    def compute_min_max_constraints(self, state_with_energy: BernoulliState, config: Any) -> BernoulliState:
        """
        Computes loose but truthful physical boundary constraint parameters using 
        four independent tuning coefficients provided in the configuration.
        
        Returns a brand NEW BernoulliState instance with all constraint bounds 
        fully populated, leaving all upstream primary and diagnostic fields unchanged.
        """
        # Extract existing fields from the state processed in Step S4
        p1 = state_with_energy.p1
        p2 = state_with_energy.p2
        v1 = state_with_energy.v1
        v2 = state_with_energy.v2
        h1 = state_with_energy.h1
        h2 = state_with_energy.h2
        rho = state_with_energy.rho
        energy = state_with_energy.energy
        energy_imbalance = state_with_energy.energy_imbalance

        # Extract independent looseness tuning coefficients from injected configuration
        k_v_min = config.k_v_min
        k_v_max = config.k_v_max
        k_p_min = config.k_p_min
        k_p_max = config.k_p_max

        # 1. Compute Characteristic Scales with Imbalance-Aware Buffering
        v_char = max(abs(v1), abs(v2))
        p_low = min(p1, p2)
        
        # Apply buffers ONLY if there is an energy imbalance (uncertainty)
        # If imbalance is 0, we trust the input values perfectly.
        p_buffer = (abs(p1 - p2) * config.k_p_max) if energy_imbalance > 0 else 0.0
        v_buffer = (abs(v1 - v2) * config.k_v_max) if energy_imbalance > 0 else 0.0

        p_high = max(p1, p2)
        delta_p = abs(p1 - p2)

        # 2. Compute Velocity Envelope
        v_min = -k_v_min * v_char
        v_max = k_v_max * v_char

        # 3. Compute Pressure Envelope
        p_min = p_low - k_p_min * delta_p
        p_max = p_high + k_p_max * delta_p

        # Yield a completely fresh Sovereign Container instance ensuring no in-place mutation.
        # At this stage, every field is now fully resolved and filled.
        return BernoulliState(
            p1=p1,
            p2=p2,
            v1=v1,
            v2=v2,
            h1=h1,
            h2=h2,
            rho=rho,
            energy=energy,
            energy_imbalance=energy_imbalance,
            p_min=p_min,
            p_max=p_max,
            v_min=v_min,
            v_max=v_max
        )