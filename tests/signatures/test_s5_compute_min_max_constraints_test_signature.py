class S5ComputeMinMaxConstraintsTestSignature:
    """
    Contract‑level signature for S5 – Compute Constraint Envelopes.

    This signature defines the REQUIRED test signatures for the S5 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S5 PURPOSE:
        - Receive the BernoulliState produced by S4 (with energy diagnostics).
        - Compute the physical constraint envelopes:
              v_min, v_max, p_min, p_max
          using the four looseness coefficients:
              k_v_min, k_v_max, k_p_min, k_p_max.
        - Produce a NEW BernoulliState with these envelope fields populated.

    S5 MUST NOT:
        - Modify or mutate the input state.
        - Solve any missing variable (S3’s responsibility).
        - Compute energy or energy_imbalance (S4’s responsibility).
        - Validate types, ranges, or physical plausibility.
        - Infer or modify any primary variables.

    SCOPE OF TEST SIGNATURES:
        These signatures cover ONLY:
            - correct computation of v_min, v_max, p_min, p_max,
            - correct use of looseness coefficients,
            - structural invariants (immutability, dummy alignment).
        No physics ranges, no scenario logic, and no validation logic may appear here.
    """

    # ---------------------------------------------------------
    # Envelope computation
    # ---------------------------------------------------------

    def test_computes_correct_v_min(self):
        """S5 must compute v_min = -k_v_min * max(|v1|, |v2|)."""
        raise NotImplementedError

    def test_computes_correct_v_max(self):
        """S5 must compute v_max =  k_v_max * max(|v1|, |v2|)."""
        raise NotImplementedError

    def test_computes_correct_p_min(self):
        """S5 must compute p_min = min(p1, p2) - k_p_min * |p1 - p2|."""
        raise NotImplementedError

    def test_computes_correct_p_max(self):
        """S5 must compute p_max = max(p1, p2) + k_p_max * |p1 - p2|."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

    def test_input_immutability(self):
        """S5 must not mutate the input state."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S5 output must match the frozen dummy structure for:
            - p_min, p_max, v_min, v_max,
            - correct field ordering,
            - UNFILLED semantics for all non‑S5 fields.
        """
        raise NotImplementedError