class TypeValidationTestSignature:
    """
    Contract‑level signature for type‑validation tests.
    Ensures that all schema fields match the types declared
    in BernoulliStateInterface. No logic or assertions here.
    """

    def test_input_schema_field_types(self):
        """
        Validate that every field in the input schema has the exact
        type declared in BernoulliStateInterface.
        Any mismatch must cause immediate failure.
        """
        raise NotImplementedError

    def test_output_schema_field_types(self):
        """
        Validate that every field in the output schema has the exact
        type declared in BernoulliStateInterface.
        Any mismatch must cause immediate failure.
        """
        raise NotImplementedError

    def test_state_interface_type_completeness(self):
        """
        Validate that BernoulliStateInterface declares all required
        fields with explicit types and that no field is missing.
        """
        raise NotImplementedError