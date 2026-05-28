# step_s1_exactly_one_missing_interface.py

class StepS1ExactlyOneMissingInterface:
    """
    Contract-only interface for Step S1: Enforce “exactly one missing” rule.

    This step enforces the structural invariant that exactly one Bernoulli
    primary variable is missing from the input. The canonical primary set is:

        {p1, p2, v1, v2, h1, h2, rho}

    Responsibilities of S1:
    - Determine which primary fields are present.
    - Determine which primary fields are missing.
    - Enforce that exactly one primary variable is missing.
    - Return the validated input (unchanged) and the identity of the missing variable.
    - Raise a validation error if zero or more than one primary variables are missing.

    S1 does NOT:
    - perform type validation,
    - perform computation,
    - infer values,
    - construct or mutate the Sovereign Container,
    - inspect numerical ranges,
    - classify diagnostic fields (energy, energy_imbalance),
    - or interact with Δh or Δv.

    This is a pure structural validation step and the gatekeeper for the solver.
    """

    def enforce_exactly_one_missing(self, raw_input_dict):
        """
        Inputs:
            raw_input_dict: dict
                The raw input dictionary that passed schema-level validation.

        Returns:
            (validated_input_dict, missing_variable_name)

        Raises:
            ValidationError (or project-specific equivalent) if:
            - zero primary variables are missing,
            - more than one primary variable is missing,
            - unexpected fields are present.

        This method performs no computation and no type validation.
        """
        raise NotImplementedError