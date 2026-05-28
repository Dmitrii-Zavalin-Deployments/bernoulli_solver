# step_s3_solve_missing_variable_interface.py

class StepS3SolveMissingVariableInterface:
    """
    Contract-only interface for Step S3: Solve the missing Bernoulli variable.

    This step performs the first computational action in the solver. Given a
    partial BernoulliState (with exactly one primary variable marked UNFILLED),
    S3 applies the appropriate rearranged form of Bernoulli’s equation to compute
    the missing variable.

    S3 does NOT:
    - compute delta_h or delta_v,
    - compute energy or energy_imbalance,
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

        This method performs the Bernoulli computation but no other computations.
        """
        raise NotImplementedError