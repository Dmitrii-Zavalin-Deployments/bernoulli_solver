class TypeValidationTestSignature:
    """
    Contract‑level signature for type‑validation tests.
    Ensures that all schema fields match the types declared
    in BernoulliStateInterface. No logic or assertions here.
    """

    def test_input_schema_field_types(self):
        """
        Validate that every field in the input schema has the exact
        type declared in BernoulliStateInterface. The input schema
        includes only the Bernoulli primary variables:
        p1, p2, v1, v2, h1, h2, rho.
        Any mismatch must cause immediate failure.
        """
        raise NotImplementedError

    def test_output_schema_field_types(self):
        """
        Validate that every field in the output schema has the exact
        type declared in BernoulliStateInterface. The output schema
        includes all primary variables, energy bookkeeping fields,
        and the S5 constraint‑export fields:
        p_min, p_max, v_min, v_max.
        Any mismatch must cause immediate failure.
        """
        raise NotImplementedError

    def test_state_interface_type_completeness(self):
        """
        Validate that BernoulliStateInterface declares all required
        fields with explicit types and that no field is missing.
        This includes the S5 constraint‑export fields and excludes
        any removed or convenience fields such as delta_h or delta_v.
        """
        raise NotImplementedError