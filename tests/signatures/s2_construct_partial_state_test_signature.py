class S2PartialStateEdgeCasesTestSignature:
    """
    Contract‑level signature for S2 – Partial State Construction (Edge‑Case Tests Only).

    This signature defines the REQUIRED edge‑case test scenarios for the S2 step,
    corresponding to Phase 4.2 Per‑step Edge Cases.

    These tests focus on malformed inputs, degenerate states, pathological
    configurations, and precision‑sensitive behaviour. They are distinct from the
    4.1 scenario tests.

    S2 EDGE‑CASE PURPOSE:
        - Validate S2 behaviour under malformed, extreme, or degenerate inputs.
        - Ensure S2 rejects invalid states without performing computation.
        - Ensure S2 remains deterministic and predictable near edge boundaries.

    S2 MUST NOT:
        - Compute the missing variable.
        - Compute energy or energy_imbalance.
        - Compute constraint envelopes.
        - Mutate the input.
        - Infer or validate physics.

    GLOBAL 4.2 EDGE‑CASE CATEGORIES APPLIED TO S2:

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
            - Any situation where partial‑state construction must remain predictable
              and analytically verifiable despite edge‑case behaviour.
    """

    # -------------------------
    # Sensitivity edge cases
    # -------------------------

    def test_rejects_negative_pressures(self):
        """S2 must reject states containing negative pressures."""
        raise NotImplementedError

    def test_rejects_extreme_velocities(self):
        """S2 must reject velocities far outside engineering plausibility."""
        raise NotImplementedError

    def test_handles_tiny_delta_h_or_v(self):
        """S2 must still construct a partial state when Δh or Δv is extremely small."""
        raise NotImplementedError

    def test_rejects_malformed_input_structures(self):
        """S2 must reject malformed inputs: wrong types, wrong shapes, missing keys."""
        raise NotImplementedError

    def test_rejects_missing_required_fields(self):
        """S2 must reject states missing required primary variables."""
        raise NotImplementedError

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self):
        """S2 must not mis-handle v1=0 or v2=0 when constructing the partial state."""
        raise NotImplementedError

    def test_equal_pressures(self):
        """S2 must correctly propagate fields when p1 == p2."""
        raise NotImplementedError

    def test_flat_line_delta_h_zero(self):
        """S2 must correctly propagate fields when h1 == h2 (Δh = 0)."""
        raise NotImplementedError

    def test_other_degenerate_configurations(self):
        """S2 must behave correctly under other degenerate but admissible configurations."""
        raise NotImplementedError

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self):
        """S2 must remain deterministic when inputs contain tiny floating‑point drift."""
        raise NotImplementedError

    def test_near_cancellation_scenarios(self):
        """S2 must correctly propagate fields when values nearly cancel (p1≈p2, h1≈h2)."""
        raise NotImplementedError

    def test_predictable_behavior_under_edge_conditions(self):
        """
        S2 must remain predictable and analytically verifiable even when constructing
        a partial state near pathological boundaries.
        """
        raise NotImplementedError

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability(self):
        """S2 must not mutate the input structure under any edge‑case condition."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S2 output must match the frozen dummy structure even for edge‑case inputs:
            - UNFILLED markers,
            - field ordering,
            - presence/absence semantics.
        """
        raise NotImplementedError