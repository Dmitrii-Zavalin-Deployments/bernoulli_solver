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
    - classify diagnostic or derived fields (energy, energy_imbalance,
      p_min, p_max, v_min, v_max),
    - or interact with removed fields such as delta_h or delta_v.

    This is a pure structural validation step and the gatekeeper for the solver.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # The list of strictly permitted members defined by the Constitution
        ALLOWED_MEMBERS = {"enforce_exactly_one_missing"}
        
        # Inspect the subclass members to ensure no 'unauthorized' logic is injected
        for name in cls.__dict__:
            # Skip dunder methods (e.g., __init__, __doc__)
            if name.startswith("__"):
                continue
                
            # If a member is defined that isn't explicitly in the contract, block it
            if name not in ALLOWED_MEMBERS:
                raise TypeError(
                    f"CONSTITUTION VIOLATION: Subclass '{cls.__name__}' is strictly "
                    f"prohibited from defining custom member '{name}'. "
                    f"Allowed interface members are: {ALLOWED_MEMBERS}"
                )

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