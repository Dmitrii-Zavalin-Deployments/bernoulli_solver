# step_s4_compute_energy_residual_interface.py

class StepS4ComputeEnergyResidualInterface:
    """
    Contract-only interface for Step S4: Compute Bernoulli energy terms and
    the energy_imbalance diagnostic. This step is strictly an internal
    diagnostic stage and does not produce any values consumed by the
    Navier–Stokes solver.

    S4 computes:
        E1 = p1 + 0.5 * rho * v1^2 + rho * g * h1
        E2 = p2 + 0.5 * rho * v2^2 + rho * g * h2
        energy_imbalance = E1 - E2

    Purpose:
        - Validate internal numerical precision.
        - Detect inconsistencies in the Bernoulli solve.
        - Provide diagnostic information for testing and debugging.

    S4 does NOT:
        - modify primary variables,
        - compute any missing variable (S3),
        - compute min/max constraints (S5),
        - perform validation or inference,
        - mutate the input state.

    S4 returns a NEW BernoulliState instance with the fields:
        energy: List[float]          # [E1, E2]
        energy_imbalance: float      # E1 - E2
    populated, while all other fields remain unchanged.
    """

    def compute_energy_and_residual(self, solved_state, config):
        """
        Inputs:
            solved_state: BernoulliState
                The fully populated state produced by S3.

            config: SolverConfig
                Provides constants such as g and numerical precision settings.

        Returns:
            new_state: BernoulliState
                A new state with:
                    - energy = [E1, E2]
                    - energy_imbalance = E1 - E2
                computed and populated.

        This method performs no mutation of the input state.
        """
        raise NotImplementedError