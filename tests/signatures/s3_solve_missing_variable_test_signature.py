class S3SolveMissingVariableTestSignature:
    """
    Contract‑level signature for S3 – Solve Missing Bernoulli Primary Variable.

    This signature defines the REQUIRED test signatures for the S3 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S3 PURPOSE:
        - Receive the partial BernoulliState from S2 (exactly one primary variable UNFILLED).
        - Solve for the missing primary variable using the appropriate rearranged
          form of Bernoulli’s equation.
        - Support all 7 missing‑variable cases:
              p1, p2, v1, v2, h1, h2, rho.
        - Produce a NEW BernoulliState with the missing variable populated.

    S3 MUST NOT:
        - Compute energy or energy_imbalance (S4’s responsibility).
        - Compute constraint envelopes (S5’s responsibility).
        - Modify or mutate the input state.
        - Perform classification or missing‑field counting (S0/S1 responsibility).
        - Accept more than one missing primary variable.
        - Infer or validate any diagnostic fields.

    SCOPE OF TEST SIGNATURES:
        These signatures cover ONLY the computational responsibilities of S3:
            - correct Bernoulli rearrangements,
            - correct handling of radicands and sign conventions,
            - correct positivity constraints (e.g., density),
            - structural invariants (immutability, dummy alignment).
        No physics ranges, no scenario logic, and no validation logic may appear here.
    """

    # ---------------------------------------------------------
    # Missing‑variable solves (core responsibility)
    # ---------------------------------------------------------

    def test_solves_missing_p1(self):
        """S3 must correctly solve for p1 using Bernoulli."""
        raise NotImplementedError

    def test_solves_missing_p2(self):
        """S3 must correctly solve for p2 using Bernoulli."""
        raise NotImplementedError

    def test_solves_missing_v1(self):
        """S3 must correctly solve for v1, including correct sqrt handling."""
        raise NotImplementedError

    def test_solves_missing_v2(self):
        """S3 must correctly solve for v2, including correct sqrt handling."""
        raise NotImplementedError

    def test_solves_missing_h1(self):
        """S3 must correctly solve for h1."""
        raise NotImplementedError

    def test_solves_missing_h2(self):
        """S3 must correctly solve for h2."""
        raise NotImplementedError

    def test_solves_missing_rho(self):
        """S3 must correctly solve for rho and reject negative density solutions."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Physics & math correctness
    # ---------------------------------------------------------

    def test_rejects_negative_radicand(self):
        """Velocity solves must reject negative radicands (non‑physical)."""
        raise NotImplementedError

    def test_rejects_negative_density_solution(self):
        """Density solves must reject negative rho results."""
        raise NotImplementedError

    def test_correct_sign_conventions(self):
        """S3 must apply Bernoulli with correct sign conventions for p, h, v."""
        raise NotImplementedError

    def test_correct_use_of_g_and_rho(self):
        """S3 must use g and rho consistently in all rearrangements."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

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