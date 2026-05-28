class PresenceValidationTestSignature:
    """
    Contract‑level signature for presence‑validation tests.
    Ensures that:
    - Input has exactly one missing Bernoulli primary variable.
    - Output has all required fields with no omissions.
    No logic or assertions here.
    """

    def test_input_has_exactly_one_missing_variable(self):
        """
        Validate that the input schema instance contains exactly one
        missing Bernoulli primary variable:
        p1, p2, v1, v2, h1, h2, rho.
        Zero, two, or more missing fields must cause immediate failure.
        """
        raise NotImplementedError

    def test_output_has_all_required_fields(self):
        """
        Validate that the output schema instance contains all required
        fields defined in BernoulliStateInterface. This includes all
        primary variables, energy bookkeeping fields, and the S5
        constraint‑export fields: p_min, p_max, v_min, v_max.
        No omissions are permitted.
        """
        raise NotImplementedError

    def test_no_optional_or_missing_fields_allowed(self):
        """
        Validate that neither the input nor the output contains optional,
        undefined, or partially missing fields. Presence rules must be
        strict: only the single missing input variable is allowed, and
        the output must be fully populated with no exceptions.
        """
        raise NotImplementedError