class S0ClassificationTestSignature:
    """
    Contract‑level signature for S0 – Classification.

    This signature defines the REQUIRED test scenarios for the S0 step.
    It does NOT contain implementations. Each method represents a test
    that MUST be implemented during Phase 5.

    S0 PURPOSE:
        - Accept raw input and classify fields into:
            * primary variables: p1, p2, v1, v2, h1, h2, rho
            * diagnostic/derived fields: energy, energy_imbalance,
              p_min, p_max, v_min, v_max
        - Detect missing fields.
        - Detect excess/unexpected fields.
        - Produce a classification result consumed by S1.

    S0 MUST NOT:
        - Perform any computation.
        - Infer any values.
        - Mutate input.
        - Validate Bernoulli identities.
        - Perform numeric work.

    GLOBAL 4.1 TEST CATEGORIES APPLIED TO S0:

        Sensitivity Gates:
            - Valid engineering ranges for p, v, h, rho.
            - Zero/low velocities.
            - Extreme but physically admissible values.
            - Reject NaN, None, non-numeric, negative density.

        Physics & Math Gates:
            - Correct classification of all primary variables.
            - Correct classification of diagnostic fields.
            - Reject any field outside the Sovereign Container.
            - No Bernoulli math performed.

        Consistency Gates:
            - Accept deterministic, analytically verifiable profiles
              without modification.
            - Do not compute or validate any step-level correctness.
            - Preserve input structure and ordering.
    """

    def test_accepts_all_primary_fields(self):
        """S0 must accept and correctly classify all seven primary variables."""
        raise NotImplementedError

    def test_rejects_missing_primary_fields(self):
        """S0 must detect missing primary variables and must not infer them."""
        raise NotImplementedError

    def test_rejects_excess_fields(self):
        """S0 must reject any field not in the Sovereign Container."""
        raise NotImplementedError

    def test_rejects_non_numeric_values(self):
        """S0 must reject non-numeric values: strings, lists, dicts, None, NaN."""
        raise NotImplementedError

    def test_rejects_negative_or_zero_density(self):
        """Density must be positive; S0 must reject zero or negative rho."""
        raise NotImplementedError

    def test_accepts_zero_and_low_velocity(self):
        """S0 must accept v1 = 0 or v2 = 0 as physically valid."""
        raise NotImplementedError

    def test_accepts_extreme_but_valid_ranges(self):
        """S0 must accept extreme but physically admissible p, v, h, rho."""
        raise NotImplementedError

    def test_no_computation_occurs(self):
        """
        S0 must NOT compute:
            - energy
            - energy_imbalance
            - p_min, p_max
            - v_min, v_max
            - any Bernoulli rearrangement
        """
        raise NotImplementedError

    def test_classifies_diagnostic_fields(self):
        """S0 must classify diagnostic fields but must not compute them."""
        raise NotImplementedError

    def test_consistency_passthrough(self):
        """
        S0 must accept deterministic, analytically verifiable profiles
        (formerly MMS) without modification or validation.
        """
        raise NotImplementedError

    def test_input_immutability(self):
        """S0 must not mutate the input structure."""
        raise NotImplementedError

    def test_frozen_dummy_alignment(self):
        """S0 output must match the frozen dummy structure exactly."""
        raise NotImplementedError