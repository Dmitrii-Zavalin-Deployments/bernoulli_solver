class PresenceValidationTestSignature:
    """
    Contract‑level signature for presence‑validation tests.
    Ensures that:
    - Input has exactly one missing Bernoulli variable.
    - Output has all required fields with no omissions.
    No logic or assertions here.
    """

    def test_input_has_exactly_one_missing_variable(self):
        """
        Validate that the input schema instance contains exactly one
        missing Bernoulli variable. Zero, two, or more missing fields
        must cause immediate failure.
        """
        raise NotImplementedError

    def test_output_has_all_required_fields(self):
        """
        Validate that the output schema instance contains all required
        fields defined in BernoulliStateInterface, with no omissions.
        """
        raise NotImplementedError

    def test_no_optional_or_missing_fields_allowed(self):
        """
        Validate that neither the input nor the output contains optional,
        undefined, or partially missing fields. Presence rules must be strict.
        """
        raise NotImplementedError