# step_filled_unfilled_classifier_interface.py

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

    Its sole purpose is to determine which Bernoulli variables are present
    in the input and which are absent, so that the validation steps (S1–S3)
    and the Schema–State Mapping step (S4) can operate deterministically.
    """

    def classify_filled_and_unfilled(self, input_schema_instance):
        """
        Given an input schema instance, return two sets:

        filled_fields:
            All Bernoulli variables that appear in the input. These fields
            are structurally present and eligible for type validation.

        unfilled_fields:
            The single missing Bernoulli variable (which the solver must
            compute), plus the diagnostic fields 'energy' and
            'energy_imbalance', which are always unfilled at the start of
            the Minimal Step Chain.

        Returns:
            filled_fields: Set[str]
            unfilled_fields: Set[str]
        """
        raise NotImplementedError
