class S4EnergyDiagnosticsTestSignature:
    """
    Contract‑level signature for S4 – Energy Diagnostics.

    This signature defines the REQUIRED test scenarios for the S4 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S4 PURPOSE:
        - Receive the fully populated state from S3.
        - Compute:
              E1 = p1 + rho * g * h1 + 0.5 * rho * v1^2
              E2 = p2 + rho * g * h2 + 0.5 * rho * v2^2
        - Compute:
              energy_imbalance = E2 - E1
        - Validate energy consistency within tolerance.
        - Produce a state ready for S5.

    S4 MUST NOT:
        - Modify or mutate the input.
        - Solve missing variables (S3’s job).
        - Compute constraint envelopes (S5’s job).
        - Perform classification or missing‑field counting.

    GLOBAL 4.1 TEST CATEGORIES APPLIED TO S4:

        Sensitivity Gates:
            - S4 must compute energy correctly across valid engineering ranges.
            - Zero/low velocities must not cause instability.
            - Extreme but admissible pressures/elevations must not break energy computation.
            - Non‑numeric or NaN values should already be rejected in S0–S3,
              but S4 must still reject them if they slip through.

        Physics & Math Gates:
            - Correct Bernoulli energy expressions for E1 and E2.
            - Correct use of g and rho.
            - Correct sign conventions.
            - Correct energy_imbalance computation.
            - Enforce energy‑balance tolerance.
            - No constraint envelope computation.

        Consistency Gates:
            - Deterministic, analytically verifiable profiles must produce the known
              energy imbalance (often zero) within tolerance.
            - Known fields must pass through unchanged.
            - S4 validates consistency but does not modify physics inputs.
    """

    # -------------------------
    # Core energy computations
    # -------------------------

    def test_computes_E1_correctly(self):
        """S4 must compute E1 = p1 + rho*g*h1 + 0.5*rho*v1^2 correctly."""
        raise NotImplementedError

    def test_computes_E2_correctly(self):
        """S4 must compute E2 = p2 + rho*g*h2 + 0.5*rho*v2^2 correctly."""
        raise NotImplementedError

    def test_computes_energy_imbalance_correctly(self):
        """S4 must compute energy_imbalance = E2 - E1 correctly."""
        raise NotImplementedError

    # -------------------------
    # Sensitivity gates
    # -------------------------

    def test_zero_and_low_velocity_handling(self):
        """S4 must remain stable when v1 or v2 is zero or near zero."""
        raise NotImplementedError

    def test_extreme_but_valid_ranges(self):
        """S4 must compute energy correctly for extreme but admissible p, v, h, rho."""
        raise NotImplementedError

    def test_rejects_non_numeric_values(self):
        """If non-numeric values slip through earlier steps, S4 must reject them."""
        raise NotImplementedError

    # -------------------------
    # Physics & math gates
    # -------------------------

    def test_correct_use_of_g_and_rho(self):
        """S4 must use g and rho consistently in all energy computations."""
        raise NotImplementedError

    def test_correct_sign_conventions(self):
        """S4 must apply correct sign conventions for p, h, v in energy formulas."""
        raise NotImplementedError

    def test_energy_balance_tolerance(self):
        """
        S4 must enforce the energy‑balance tolerance:
            |energy_imbalance| <= tolerance
        """
        raise NotImplementedError

    def test_no_constraint_envelope_computation(self):
        """S4 must NOT compute p_min, p_max, v_min, v_max, or any S5 outputs."""
        raise NotImplementedError

    # -------------------------
    # Consistency gates
    # -------------------------

    def test_consistency_energy_behavior(self):
        """
        Deterministic, analytically verifiable profiles (formerly MMS) must produce
        the known energy imbalance (usually zero) within numerical tolerance.
        """
        raise NotImplementedError

    def test_consistency_passthrough_for_known_fields(self):
        """Known deterministic fields must pass through unchanged."""
        raise NotImplementedError

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self):
        """S4 must not mutate the input state."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S4 output must match the frozen dummy structure for:
            - E1, E2, energy_imbalance fields,
            - UNFILLED constraint fields,
            - correct field ordering.
        """
        raise NotImplementedError