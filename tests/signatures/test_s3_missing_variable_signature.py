class S3MissingVariableTestSignature:
    """
    Contract‑level signature for S3 – Missing‑Variable Solver.

    This signature defines the REQUIRED test scenarios for the S3 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S3 PURPOSE:
        - Receive the partial state from S2 (exactly one primary variable UNFILLED).
        - Solve for the missing primary variable using the Bernoulli equation:
              p + ρ g h + ½ ρ v² = constant
        - Support all 7 missing‑variable cases:
              missing p1, p2, v1, v2, h1, h2, or rho
        - Produce a fully populated BernoulliState for S4.

    S3 MUST NOT:
        - Compute energy or energy_imbalance (S4’s job).
        - Compute constraint envelopes (S5’s job).
        - Modify or mutate the input.
        - Perform classification or missing‑field counting (S0/S1’s job).
        - Accept more than one missing primary variable.

    GLOBAL 4.1 TEST CATEGORIES APPLIED TO S3:

        Sensitivity gates:
            - S3 must solve correctly across valid engineering ranges for p, v, h, rho.
            - Zero/low velocities must be handled without instability.
            - Extreme but admissible pressures/elevations must not break the solver.
            - Non‑numeric or NaN values should already be rejected in S0/S1/S2,
              but S3 must still reject them if they slip through.

        Physics & math gates:
            - Correct Bernoulli rearrangements for all 7 missing‑variable cases.
            - Correct sign conventions for p, h, v.
            - Correct use of g and rho.
            - Correct handling of square roots in velocity solves.
            - Reject negative radicands (non‑physical).
            - Reject negative density solutions.
            - No energy or envelope computations.

        MMS gates:
            - Manufactured solutions must be solved exactly (within tolerance).
            - MMS profiles must produce the known missing variable.
            - MMS correctness must be validated by S4, not S3.
    """

    # -------------------------
    # Missing-variable cases
    # -------------------------

    def test_solves_missing_p1(self):
        """S3 must correctly solve for p1 using Bernoulli."""
        raise NotImplementedError

    def test_solves_missing_p2(self):
        """S3 must correctly solve for p2 using Bernoulli."""
        raise NotImplementedError

    def test_solves_missing_v1(self):
        """S3 must correctly solve for v1, including sqrt handling."""
        raise NotImplementedError

    def test_solves_missing_v2(self):
        """S3 must correctly solve for v2, including sqrt handling."""
        raise NotImplementedError

    def test_solves_missing_h1(self):
        """S3 must correctly solve for h1."""
        raise NotImplementedError

    def test_solves_missing_h2(self):
        """S3 must correctly solve for h2."""
        raise NotImplementedError

    def test_solves_missing_rho(self):
        """S3 must correctly solve for rho and reject negative solutions."""
        raise NotImplementedError

    # -------------------------
    # Sensitivity gates
    # -------------------------

    def test_zero_and_low_velocity_handling(self):
        """S3 must remain stable when v1 or v2 is zero or near zero."""
        raise NotImplementedError

    def test_extreme_but_valid_ranges(self):
        """S3 must solve correctly for extreme but physically admissible p, v, h, rho."""
        raise NotImplementedError

    def test_rejects_non_numeric_values(self):
        """If non-numeric values slip through earlier steps, S3 must reject them."""
        raise NotImplementedError

    # -------------------------
    # Physics & math gates
    # -------------------------

    def test_correct_sign_conventions(self):
        """S3 must apply Bernoulli with correct sign conventions for p, h, v."""
        raise NotImplementedError

    def test_correct_use_of_g_and_rho(self):
        """S3 must use g and rho consistently in all rearrangements."""
        raise NotImplementedError

    def test_rejects_negative_radicand(self):
        """Velocity solves must reject negative radicands (non-physical)."""
        raise NotImplementedError

    def test_rejects_negative_density_solution(self):
        """Density solves must reject negative rho results."""
        raise NotImplementedError

    def test_no_energy_or_envelope_computation(self):
        """S3 must NOT compute energy, energy_imbalance, or constraint envelopes."""
        raise NotImplementedError

    # -------------------------
    # MMS gates
    # -------------------------

    def test_mms_exact_solution(self):
        """
        S3 must recover the exact missing variable for MMS profiles
        (within numerical tolerance).
        """
        raise NotImplementedError

    def test_mms_passthrough_for_known_fields(self):
        """Known MMS fields must pass through unchanged."""
        raise NotImplementedError

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self):
        """S3 must not mutate the input partial state."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S3 output must match the frozen dummy structure for:
            - fully populated primary variables,
            - UNFILLED diagnostic fields,
            - correct field ordering.
        """
        raise NotImplementedError