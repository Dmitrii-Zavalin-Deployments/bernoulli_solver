class S1ExactlyOneMissingTestSignature:
    """
    Contract‑level signature for S1 – Exactly‑One‑Missing validation.

    This signature defines the REQUIRED test scenarios for the S1 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S1 PURPOSE:
        - Receive the classification result from S0.
        - Verify that EXACTLY ONE primary variable is missing.
        - Reject:
            * zero missing
            * two or more missing
            * missing diagnostic fields (diagnostic fields must be ignored)
        - Produce a validated state for S2.

    S1 MUST NOT:
        - Compute any values.
        - Infer the missing variable.
        - Modify or mutate the input.
        - Perform Bernoulli math.
        - Validate energy or constraints.

    GLOBAL 4.1 TEST CATEGORIES APPLIED TO S1:

        Sensitivity Gates:
            - S1 must accept all valid engineering ranges for p, v, h, rho.
            - Zero/low velocities must not affect missing‑field logic.
            - Extreme but admissible values must not affect missing‑field logic.
            - Non‑numeric or NaN values must be rejected BEFORE S1 (S0 territory),
              but S1 must still reject them if they slip through.

        Physics & Math Gates:
            - S1 performs NO physics.
            - S1 must correctly count missing primary variables.
            - S1 must ignore diagnostic fields when counting missing variables.
            - S1 must not perform Bernoulli rearrangements or energy checks.

        Consistency Gates:
            - Deterministic, analytically verifiable profiles must pass through S1 unchanged.
            - S1 must not validate correctness of such profiles.
            - S1 must enforce ONLY the exactly‑one‑missing invariant.
    """

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

    def test_ignores_missing_diagnostic_fields(self):
        """
        S1 must ignore missing diagnostic/derived fields when counting missing variables:
            energy, energy_imbalance, p_min, p_max, v_min, v_max.
        """
        raise NotImplementedError

    def test_rejects_non_numeric_primary_values(self):
        """
        If non-numeric values slip past S0 (should not happen), S1 must still reject them.
        """
        raise NotImplementedError

    def test_zero_and_low_velocity_do_not_affect_missing_logic(self):
        """
        v1 = 0 or v2 = 0 must not cause S1 to misclassify missing fields.
        """
        raise NotImplementedError

    def test_extreme_but_valid_ranges_do_not_affect_missing_logic(self):
        """
        Extreme but physically admissible values must not affect S1's missing-field logic.
        """
        raise NotImplementedError

    def test_no_computation_occurs(self):
        """
        S1 must NOT compute:
            - the missing variable
            - energy or energy_imbalance
            - constraint envelopes
            - any Bernoulli rearrangement
        """
        raise NotImplementedError

    def test_consistency_passthrough(self):
        """
        Deterministic, analytically verifiable profiles (formerly MMS) must pass through S1 unchanged.
        S1 must not validate their correctness or perform physics.
        """
        raise NotImplementedError

    def test_input_immutability(self):
        """S1 must not mutate the input structure."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S1 output must match the frozen dummy structure for:
            - missing-field flags
            - classification structure
            - presence/absence semantics
        """
        raise NotImplementedError