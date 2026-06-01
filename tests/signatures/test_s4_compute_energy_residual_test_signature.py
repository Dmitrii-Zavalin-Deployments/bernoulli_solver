class S4ComputeEnergyResidualTestSignature:
    """
    Contract‑level signature for S4 – Compute Bernoulli Energy and Residual.

    This signature defines the REQUIRED test signatures for the S4 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S4 PURPOSE:
        - Receive the fully populated BernoulliState from S3.
        - Compute the Bernoulli energy terms:
              E1 = p1 + 0.5 * rho * v1^2 + rho * g * h1
              E2 = p2 + 0.5 * rho * v2^2 + rho * g * h2
        - Compute the diagnostic:
              energy_imbalance = E1 - E2
        - Produce a NEW BernoulliState with these diagnostic fields populated.

    S4 MUST NOT:
        - Modify or mutate the input state.
        - Solve any missing variable (S3’s responsibility).
        - Compute constraint envelopes (S5’s responsibility).
        - Validate types, ranges, or physical plausibility.
        - Infer or modify any primary variables.

    SCOPE OF TEST SIGNATURES:
        These signatures cover ONLY:
            - correct computation of E1 and E2,
            - correct computation of energy_imbalance,
            - structural invariants (immutability, dummy alignment).
        No physics ranges, no scenario logic, and no validation logic may appear here.
    """

    # ---------------------------------------------------------
    # Energy computation
    # ---------------------------------------------------------

    def test_computes_correct_E1(self):
        """S4 must compute E1 correctly from p1, v1, h1, rho, and g."""
        raise NotImplementedError

    def test_computes_correct_E2(self):
        """S4 must compute E2 correctly from p2, v2, h2, rho, and g."""
        raise NotImplementedError

    def test_computes_correct_energy_imbalance(self):
        """S4 must compute energy_imbalance = E1 - E2 correctly."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

    def test_input_immutability(self):
        """S4 must not mutate the input state."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S4 output must match the frozen dummy structure for:
            - energy = [E1, E2],
            - energy_imbalance,
            - correct field ordering,
            - UNFILLED semantics for all non‑S4 fields.
        """
        raise NotImplementedError