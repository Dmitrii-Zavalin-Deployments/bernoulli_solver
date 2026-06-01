class S4EnergyDiagnosticsEdgeCasesTestSignature:
    """
    Contract‑level signature for S4 – Energy Diagnostics (Edge‑Case Tests Only).

    This signature defines the REQUIRED edge‑case test scenarios for the S4 step,
    corresponding to Phase 4.2 Per‑step Edge Cases.

    These tests focus on malformed inputs, degenerate states, pathological
    configurations, and precision‑sensitive behaviour. They are distinct from the
    4.1 scenario tests.

    S4 EDGE‑CASE PURPOSE:
        - Validate S4 behaviour under malformed, extreme, or degenerate inputs.
        - Ensure S4 rejects invalid states without producing energy values.
        - Ensure S4 remains numerically stable and predictable near edge boundaries.

    S4 MUST NOT:
        - Modify or mutate the input.
        - Solve missing variables (S3’s job).
        - Compute constraint envelopes (S5’s job).
        - Perform classification or missing‑field counting.

    GLOBAL 4.2 EDGE‑CASE CATEGORIES APPLIED TO S4:

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
            - Energy expressions near cancellation.

        Consistency Gates:
            - Precision drift in residuals.
            - Near‑cancellation scenarios.
            - Any situation where energy computation must remain predictable
              and analytically verifiable despite edge‑case behaviour.
    """

    # -------------------------
    # Sensitivity edge cases
    # -------------------------

    def test_rejects_negative_pressures(self):
        """S4 must reject states containing negative pressures."""
        raise NotImplementedError

    def test_rejects_extreme_velocities(self):
        """S4 must reject velocities far outside engineering plausibility."""
        raise NotImplementedError

    def test_handles_tiny_delta_h_or_v(self):
        """S4 must remain stable when Δh or Δv is extremely small."""
        raise NotImplementedError

    def test_rejects_malformed_input_structures(self):
        """S4 must reject malformed inputs: wrong types, wrong shapes, missing keys."""
        raise NotImplementedError

    def test_rejects_missing_required_fields(self):
        """S4 must reject states missing required primary variables."""
        raise NotImplementedError

    # -------------------------
    # Physics & math edge cases
    # -------------------------

    def test_zero_velocity_station(self):
        """S4 must compute energy correctly when v1=0 or v2=0 without instability."""
        raise NotImplementedError

    def test_equal_pressures(self):
        """S4 must compute E1/E2 correctly when p1 == p2."""
        raise NotImplementedError

    def test_flat_line_delta_h_zero(self):
        """S4 must compute E1/E2 correctly when h1 == h2 (Δh = 0)."""
        raise NotImplementedError

    def test_other_degenerate_configurations(self):
        """S4 must behave correctly under other degenerate but admissible configurations."""
        raise NotImplementedError

    def test_energy_near_cancellation(self):
        """S4 must handle E2 ≈ E1 without producing unstable energy_imbalance values."""
        raise NotImplementedError

    # -------------------------
    # Consistency edge cases
    # -------------------------

    def test_precision_drift_in_inputs(self):
        """S4 must remain deterministic when inputs contain tiny floating‑point drift."""
        raise NotImplementedError

    def test_near_cancellation_scenarios(self):
        """S4 must compute energy correctly when values nearly cancel (p1≈p2, h1≈h2, v1≈v2)."""
        raise NotImplementedError

    def test_predictable_behavior_under_edge_conditions(self):
        """
        S4 must remain predictable and analytically verifiable even when computing
        energy near pathological boundaries.
        """
        raise NotImplementedError

    # -------------------------
    # Structural invariants
    # -------------------------

    def test_input_immutability_under_edge_cases(self):
        """S4 must not mutate the input state under any edge‑case condition."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """
        S4 output must match the frozen dummy structure even for edge‑case inputs:
            - E1, E2, energy_imbalance fields,
            - UNFILLED constraint fields,
            - correct field ordering.
        """
        raise NotImplementedError