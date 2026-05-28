# step_s0_filled_unfilled_classifier_interface.py

class FilledUnfilledClassifierInterface:
    """
    Contract-only interface for classifying Bernoulli input fields into
    'filled' and 'unfilled' categories before any validation or container
    construction occurs.

    This step is purely structural. It does not:
    - perform validation,
    - assign defaults or nulls,
    - create or partially create the Sovereign Container,
    - mutate state,
    - or inspect types.

    Its sole purpose is to determine which Bernoulli primary variables are
    present in the input and which are absent, so that the validation steps
    (S1) and the Schema–State Mapping step can operate deterministically.
    """

    def classify_filled_and_unfilled(self, input_schema_instance):
        """
        Given an input schema instance, return two sets:

        filled_fields:
            All Bernoulli primary variables that appear in the input:
            p1, p2, v1, v2, h1, h2, rho.
            These fields are structurally present and eligible for type validation.

        unfilled_fields:
            The single missing Bernoulli primary variable (which the solver must
            compute), plus all diagnostic and execution-derived fields:
            'energy', 'energy_imbalance',
            'p_min', 'p_max', 'v_min', 'v_max'.
            These fields are always unfilled at the start of the Minimal Step Chain.

        Returns:
            filled_fields: Set[str]
            unfilled_fields: Set[str]
        """
        raise NotImplementedError