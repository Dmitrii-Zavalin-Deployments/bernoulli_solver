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
        Computes physical boundary constraint parameters using physics-informed 
        tuning coefficients (Stagnation, Cavitation, Constriction, and Recirculation).
        Accepts 'state_with_energy' parameter exactly as mandated by the pipeline contract.
        """
        # 1. Extract inputs
        p1, p2 = state_with_energy.p1, state_with_energy.p2
        v1, v2 = state_with_energy.v1, state_with_energy.v2
        rho = state_with_energy.rho
        imbalance = state_with_energy.energy_imbalance
        
        # 2. Compute Characteristic Scales
        v_max_abs = max(abs(v1), abs(v2))
        
        # The true driver of pressure variation inside a fluid domain is Dynamic Pressure.
        dynamic_pressure = 0.5 * rho * (v_max_abs ** 2)
        
        # Base static boundaries
        p_low = min(p1, p2)
        p_high = max(p1, p2)
        p_diff = abs(p1 - p2)
        
        # We use the maximum of dynamic pressure or static differential as our envelope scaler.
        # This protects against pure hydrostatic flows (v=0) where dynamic pressure is 0.
        p_scale = max(dynamic_pressure, p_diff)
        
        # 3. Velocity Envelopes
        # (1.0 + k) explicitly builds a multiplier ON TOP of the maximum boundary velocity.
        # config.k_v_max represents internal geometric constriction (e.g., flow doubling in speed).
        v_max = v_max_abs * (1.0 + config.k_v_max)
        
        # config.k_v_min represents recirculation/eddy strength. 
        # A negative multiplier ensures a deep enough envelope for backward flow.
        v_min = -v_max_abs * (1.0 + config.k_v_min)
        
        # 4. Pressure Envelopes (Physics-Grounded)
        # Stagnation Limit: Flow hits a wall, converting kinetic energy into pressure.
        p_max = p_high + p_scale * (1.0 + config.k_p_max)
        
        # Cavitation Limit (Venturi): Flow accelerates through a constriction, dropping pressure.
        p_min = p_low - p_scale * (1.0 + config.k_p_min)
        
        # 5. Return fresh sovereign container with nested constraint dictionaries
        return BernoulliState(
            p1=p1, p2=p2, v1=v1, v2=v2, 
            h1=state_with_energy.h1, h2=state_with_energy.h2, rho=rho,
            energy=state_with_energy.energy, 
            energy_imbalance=imbalance,
            initial_conditions={
                "velocity": [v1, 0.0, 0.0],
                "pressure": p1
            },
            physical_constraints={
                "min_pressure": p_min,
                "max_pressure": p_max,
                "min_velocity": v_min,
                "max_velocity": v_max
            }
        )