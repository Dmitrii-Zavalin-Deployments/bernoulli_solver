class S1ExactlyOneMissingEdgeCasesTestSignature:
    """
    Contract‑level signature for S1 – Exactly‑One‑Missing (Edge‑Case Tests Only).

    This signature defines the REQUIRED edge‑case test scenarios for the S1 step,
    corresponding to Phase 4.2 Per‑step Edge Cases.

    These tests focus on malformed inputs, degenerate states, pathological
    configurations, and precision‑sensitive behaviour. They are distinct from the
    4.1 scenario tests.

    S1 EDGE‑CASE PURPOSE:
        - Validate S1 behaviour under malformed, extreme, or degenerate inputs.
        - Ensure S1 rejects invalid structures without performing computation.
        - Ensure S1 remains deterministic and predictable near edge boundaries.

    S1 MUST NOT:
        - Compute any values.
        - Infer the missing variable.
        - Mutate input.
        - Perform Bernoulli math.
        - Validate energy or constraints.

    GLOBAL 4.2 EDGE‑CASE CATEGORIES APPLIED TO S1:

        Sensitivity Gates:
            - Negative pressures.
            - Extreme velocities.
            - Tiny Δh or Δv (degenerate geometry).
            - Malformed inputs (wrong types, wrong shapes).
            - Missing fields.

        Physics & Math Gates:
            - Zero velocity at one station.
            - Equal pressures.
            - Flat‑line cases (Δh = 0).
            - Other degenerate configurations.

        Consistency Gates:
            - Precision drift in residuals.
            - Near‑cancellation scenarios.
            - Any situation where missing‑field logic must remain predictable
              and analytically verifiable despite edge‑case behaviour.
    """

    # -------------------------
    # Sensitivity edge cases
    # -------------------------

    def test_rejects_negative_pressures(self):
        """S1 must reject states containing negative pressures."""
        raise NotImplementedError

    def test_rejects_extreme_velocities(self):
        """S1 must reject states containing velocities far outside engineering plausibility."""
        raise NotImplementedError

    def test_handles_tiny_delta_h_or_v(self):
        """S1 must still correctly count missing fields when Δh or Δv is extremely small."""
        raise NotImplementedError

    def test_rejects_malformed_input_structures(self):
        """S1 must reject malformed inputs: wrong types, wrong shapes, missing keys."""
        raise NotImplementedError

    def test_rejects_missing_required_fields(self):
        """S1 must reject states missing required primary variables."""
        raise NotImplementedError

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self):
        """S1 must not misclassify missing fields when v1=0 or v2=0."""
        raise NotImplementedError

    def test_equal_pressures(self):
        """S1 must not misclassify missing fields when p1 == p2."""
        raise NotImplementedError

    def test_flat_line_delta_h_zero(self):
        """S1 must not misclassify missing fields when h1 == h2 (Δh = 0)."""
        raise NotImplementedError

    def test_other_degenerate_configurations(self):
        """S1 must behave correctly under other degenerate but admissible configurations."""
        raise NotImplementedError

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self):
        """S1 must remain deterministic when inputs contain tiny floating‑point drift."""
        raise NotImplementedError

    def test_near_cancellation_scenarios(self):
        """S1 must correctly count missing fields when values nearly cancel (p1≈p2, h1≈h2)."""
        raise NotImplementedError

    def test_predictable_behavior_under_edge_conditions(self):
        """
        S1 must remain predictable and analytically verifiable even when inputs
        are near pathological boundaries.
        """
        raise NotImplementedError

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self):
        """S1 must not mutate the input structure under any edge‑case condition."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """S1 output must match the frozen dummy structure even for edge‑case inputs."""
        raise NotImplementedError