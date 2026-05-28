class ExcessFieldValidationTestSignature:
    """
    Contract‑level signature for excess‑field validation tests.
    Ensures that:
    - No extra fields appear in the input schema.
    - No extra fields appear in the output schema.
    - No field outside BernoulliStateInterface is permitted.
    No logic or assertions here.
    """

    def test_input_has_no_extra_fields(self):
        """
        Validate that the input schema instance contains only the Bernoulli
        primary variables defined in the input schema and present in
        BernoulliStateInterface: p1, p2, v1, v2, h1, h2, rho.
        Any additional or convenience field must cause immediate failure.
        """
        raise NotImplementedError

    def test_output_has_no_extra_fields(self):
        """
        Validate that the output schema instance contains only the fields
        defined in the output schema and BernoulliStateInterface. This includes
        all primary variables, energy bookkeeping fields, and the S5
        constraint‑export fields: p_min, p_max, v_min, v_max.
        Any additional or convenience field must cause immediate failure.
        """
        raise NotImplementedError

    def test_state_interface_allows_no_undefined_fields(self):
        """
        Validate that BernoulliStateInterface defines the complete and exclusive
        set of allowed fields. No undefined field (including removed fields such
        as delta_h or delta_v) may appear in any state instance. Any field not
        present in the interface must be rejected by the validation layer.
        """
        raise NotImplementedError