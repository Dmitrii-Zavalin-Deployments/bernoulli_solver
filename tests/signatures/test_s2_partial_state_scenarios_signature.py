class S2PartialStateTestSignature:
    """
    Contract‑level signature for S2 – Partial State Construction.

    This signature defines the REQUIRED test scenarios for the S2 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S2 PURPOSE:
        - Receive the validated S1 output (exactly one primary variable missing).
        - Construct a BernoulliState where:
            * all known primary variables are copied exactly,
            * the missing primary variable is marked UNFILLED,
            * all diagnostic/derived fields are set to UNFILLED,
            * no computation is performed.
        - Produce a clean, deterministic state for S3.

    S2 MUST NOT:
        - Compute the missing variable.
        - Compute energy or energy_imbalance.
        - Compute constraint envelopes.
        - Perform Bernoulli math.
        - Mutate the input.
        - Infer or validate physics.

    GLOBAL 4.1 TEST CATEGORIES APPLIED TO S2:

        Sensitivity Gates:
            - S2 must accept all valid engineering ranges for p, v, h, rho.
            - Zero/low velocities must not affect partial-state construction.
            - Extreme but admissible values must not affect copying behavior.
            - Non-numeric or NaN values should already be rejected in S0/S1,
              but S2 must still reject them if they slip through.

        Physics & Math Gates:
            - S2 performs NO physics.
            - S2 must correctly propagate known primary variables.
            - S2 must correctly mark exactly one primary variable as UNFILLED.
            - S2 must set ALL diagnostic/derived fields to UNFILLED.
            - S2 must not perform any Bernoulli rearrangement.

        Consistency Gates:
            - Deterministic, analytically verifiable profiles must pass through S2 unchanged.
            - S2 must not compute or validate correctness of such profiles.
            - S2 must only construct the partial state.
    """

    def test_copies_all_known_primary_variables(self):
        """S2 must copy all known primary variables exactly, without modification."""
        raise NotImplementedError

    def test_marks_missing_primary_as_unfilled(self):
        """S2 must mark the single missing primary variable as UNFILLED."""
        raise NotImplementedError

    def test_sets_all_diagnostic_fields_unfilled(self):
        """
        S2 must set all diagnostic/derived fields to UNFILLED:
            energy, energy_imbalance,
            p_min, p_max, v_min, v_max.
        """
        raise NotImplementedError

    def test_rejects_non_numeric_primary_values(self):
        """
        If non-numeric values slip past S0/S1, S2 must still reject them.
        """
        raise NotImplementedError

    def test_zero_and_low_velocity_do_not_affect_partial_state(self):
        """
        v1 = 0 or v2 = 0 must not affect S2's partial-state construction.
        """
        raise NotImplementedError

    def test_extreme_but_valid_ranges_do_not_affect_partial_state(self):
        """
        Extreme but physically admissible values must not affect S2's copying logic.
        """
        raise NotImplementedError

    def test_no_computation_occurs(self):
        """
        S2 must NOT compute:
            - the missing variable,
            - energy or energy_imbalance,
            - constraint envelopes,
            - any Bernoulli rearrangement.
        """
        raise NotImplementedError

    def test_consistency_passthrough(self):
        """
        Deterministic, analytically verifiable profiles (formerly MMS) must pass
        through S2 unchanged for known fields. S2 must not compute or validate
        correctness of such profiles.
        """
        raise NotImplementedError

    def test_input_immutability(self):
        """S2 must not mutate the input structure."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S2 output must match the frozen dummy structure for:
            - UNFILLED markers,
            - field ordering,
            - presence/absence semantics.
        """
        raise NotImplementedError