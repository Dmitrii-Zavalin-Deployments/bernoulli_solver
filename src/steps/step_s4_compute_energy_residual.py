from typing import Any
from src.interfaces.step_interfaces.step_s4_compute_energy_residual_interface import StepS4ComputeEnergyResidualInterface
from src.containers.bernoulli_state import BernoulliState

class StepS4ComputeEnergyResidual(StepS4ComputeEnergyResidualInterface):
    """
    Concrete implementation of Step S4: Compute Bernoulli energy terms and energy_imbalance diagnostic.
    Inherits explicitly from StepS4ComputeEnergyResidualInterface to guarantee 
    a 100% structural match to the project constitution.
    """

    def compute_energy_residual(self, solved_state: BernoulliState, config: Any) -> BernoulliState:
        """
        Computes total energy terms (E1, E2) and the energy_imbalance diagnostic value.
        
        Returns a brand NEW BernoulliState instance with energy and energy_imbalance 
        populated, leaving all primary variables and downstream bounds completely unchanged.
        """
        # Extract fully populated primary variables from the state solved in Step S3
        p1 = solved_state.p1
        p2 = solved_state.p2
        v1 = solved_state.v1
        v2 = solved_state.v2
        h1 = solved_state.h1
        h2 = solved_state.h2
        rho = solved_state.rho
        
        # Read environmental constants from the injected runtime config
        g = config.g
        
        # Compute individual total energy heads for both fluid tracking nodes
        e1 = p1 + 0.5 * rho * (v1 ** 2) + rho * g * h1
        e2 = p2 + 0.5 * rho * (v2 ** 2) + rho * g * h2
        
        # Calculate the diagnostic tracking residual/drift
        energy_imbalance = e1 - e2
        energy_list = [e1, e2]
        
        # Yield a completely fresh Sovereign Container instance ensuring no in-place mutation
        return BernoulliState(
            p1=p1,
            p2=p2,
            v1=v1,
            v2=v2,
            h1=h1,
            h2=h2,
            rho=rho,
            energy=energy_list,
            energy_imbalance=energy_imbalance,
            p_min=solved_state.p_min,
            p_max=solved_state.p_max,
            v_min=solved_state.v_min,
            v_max=solved_state.v_max
        )