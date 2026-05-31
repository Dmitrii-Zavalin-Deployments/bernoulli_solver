# step_s2_construct_partial_state_interface.py

class StepS2ConstructPartialStateInterface:
    """
    Contract-only interface for Step S2: Construct BernoulliState (partial).

    This step creates the initial BernoulliState (the Sovereign Container)
    using the validated input from S1. All fields that are present in the
    input are copied directly into the state. The single missing primary
    variable, as well as all diagnostic and execution-derived fields
    (energy, energy_imbalance, p_min, p_max, v_min, v_max), are populated
    with an explicit UNFILLED sentinel.

    S2 performs no computation, no inference, no type checking, and no
    mutation of values. It does not attempt to solve the missing variable
    or compute any derived quantities. Its sole purpose is to produce a
    structurally complete BernoulliState instance in which every field
    exists, but only the known fields contain real values.

    This partial state becomes the input to all subsequent computational
    steps (S3–S5).
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # The list of strictly permitted members defined by the Constitution
        ALLOWED_MEMBERS = {"construct_partial_state"}
        
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

    def construct_partial_state(self, validated_input_dict, missing_variable_name, unfilled_sentinel):
        """
        Inputs:
            validated_input_dict: dict
                The validated input dictionary returned by S1.

            missing_variable_name: str
                The identity of the single missing primary variable determined by S1.

            unfilled_sentinel:
                A project-defined sentinel object used to mark fields that are
                intentionally unfilled at this stage.

        Returns:
            bernoulli_state_instance:
                A BernoulliState object (Sovereign Container) with:
                - all known primary fields populated with real values,
                - the missing primary variable set to the sentinel,
                - all diagnostic and execution-derived fields (energy,
                  energy_imbalance, p_min, p_max, v_min, v_max) set to the sentinel.

        This method performs no computation and no inference.
        """
        raise NotImplementedError