class S1ExactlyOneMissingTestSignature:
    """
    Contract‑level signature for S1 – Exactly‑One‑Missing validation.

    This signature defines the REQUIRED test signatures for the S1 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S1 PURPOSE:
        - Receive the classification result from S0.
        - Verify that EXACTLY ONE primary variable is missing.
        - Reject:
            * zero missing
            * two or more missing
            * missing diagnostic fields (diagnostic fields must be ignored)
        - Produce a validated input dictionary and the identity of the
          missing primary variable for S2.

    S1 MUST NOT:
        - Compute any values.
        - Infer the missing variable.
        - Modify or mutate the input.
        - Perform Bernoulli math.
        - Validate energy, envelopes, or any diagnostic fields.
        - Inspect numerical ranges or perform physics.

    SCOPE OF TEST SIGNATURES:
        These signatures cover ONLY the structural responsibilities of S1.
        No physics, no sensitivity ranges, no numerical behaviour, and no
        scenario/edge‑case logic beyond the exactly‑one‑missing invariant
        may be included.
    """

    # ---------------------------------------------------------
    # Core invariant: exactly one primary variable is missing
    # ---------------------------------------------------------

    def test_accepts_exactly_one_missing_primary(self):
        """S1 must accept states where exactly one primary variable is missing."""
        raise NotImplementedError

    def test_rejects_zero_missing_primary(self):
        """S1 must reject states where no primary variable is missing."""
        raise NotImplementedError

    def test_rejects_two_missing_primary(self):
        """S1 must reject states where two primary variables are missing."""
        raise NotImplementedError

    def test_rejects_three_or_more_missing_primary(self):
        """S1 must reject states where three or more primary variables are missing."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Diagnostic fields must be ignored when counting missing
    # ---------------------------------------------------------

    def test_ignores_missing_diagnostic_fields(self):
        """
        S1 must ignore missing diagnostic/derived fields when counting missing variables:
            energy, energy_imbalance, p_min, p_max, v_min, v_max.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

    def test_input_immutability(self):
        """S1 must not mutate the input structure."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S1 output must match the frozen dummy structure for:
            - missing‑field flags,
            - classification structure,
            - presence/absence semantics.
        """
        raise NotImplementedError