# step_s5_compute_min_max_constraints_interface.py

class StepS5ComputeMinMaxConstraintsInterface:
    """
    Contract-only interface for Step S5: Compute the Bernoulli-derived
    physical constraint bounds required by the Navier–Stokes solver.

    S5 computes:
        p_min = min(p1, p2)
        p_max = max(p1, p2)
        v_min = min(|v1|, |v2|)
        v_max = max(|v1|, |v2|)

    Purpose:
        - Provide the Navier–Stokes solver with physically consistent
          bounds for pressure and velocity.
        - Serve as the export layer of the Bernoulli pipeline.
        - Ensure that downstream solvers operate within the physically
          permissible envelope defined by Bernoulli.

    S5 does NOT:
        - compute energy or energy_imbalance (S4),
        - solve any missing variable (S3),
        - modify primary variables,
        - perform validation or inference,
        - mutate the input state.

    S5 returns a NEW BernoulliState instance with the fields:
        p_min: float
        p_max: float
        v_min: float
        v_max: float
    populated, while all other fields remain unchanged.
    """

    def compute_min_max_constraints(self, state_with_energy, config):
        """
        Inputs:
            state_with_energy: BernoulliState
                The state produced by S4, containing all primary variables
                and diagnostic energy fields.

            config: SolverConfig
                Provided for consistency; typically unused in S5.

        Returns:
            new_state: BernoulliState
                A new state with:
                    - p_min
                    - p_max
                    - v_min
                    - v_max
                computed and populated.

        This method performs no mutation of the input state.
        """
        raise NotImplementedError