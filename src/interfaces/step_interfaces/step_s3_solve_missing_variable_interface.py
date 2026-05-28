# step_s3_solve_missing_variable_interface.py

class StepS3SolveMissingVariableInterface:
    """
    Contract-only interface for Step S3: Solve the missing Bernoulli primary variable.

    This step performs the first computational action in the solver. Given a
    partial BernoulliState (with exactly one primary variable marked UNFILLED),
    S3 applies the appropriate rearranged form of Bernoulli’s equation to compute
    the missing variable.

    S3 does NOT:
    - compute energy or energy_imbalance (computed in S4),
    - compute p_min, p_max, v_min, or v_max (computed in S5),
    - mutate the input state,
    - perform type validation,
    - or infer any values other than the single missing primary variable.

    S3 returns a NEW BernoulliState instance with the missing variable filled in.
    """

    def solve_missing_variable(self, partial_state, config):
        """
        Inputs:
            partial_state: BernoulliState
                The state produced by S2, containing exactly one UNFILLED primary variable.

            config: SolverConfig
                Runtime configuration (e.g., g, precision).

        Returns:
            new_state: BernoulliState
                A new state with the missing primary variable computed and populated.
                All other fields remain unchanged and any diagnostic or derived fields
                remain UNFILLED.

        This method performs the Bernoulli computation but no other computations.
        """
        raise NotImplementedError