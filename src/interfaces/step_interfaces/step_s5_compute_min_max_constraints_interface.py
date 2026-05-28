# step_s5_compute_min_max_constraints_interface.py

class StepS5ComputeMinMaxConstraintsInterface:
    """
    Contract-only interface for Step S5: Compute the Bernoulli-derived
    physical constraint envelopes required by the Navier–Stokes solver.

    Unlike earlier versions, S5 does NOT use pure min/max of p1, p2, v1, v2.
    Instead, it constructs *loose but truthful* physical bounds using
    four independent looseness coefficients supplied in SolverConfig:

        k_v_min, k_v_max, k_p_min, k_p_max

    These coefficients allow the developer to tune the constraint envelope
    to minimize false positives and false negatives in Navier–Stokes.
    All four must be explicitly provided; no defaults or symmetry are assumed.

    S5 computes:

        # Characteristic scales
        V_char = max(|v1|, |v2|)
        P_low  = min(p1, p2)
        P_high = max(p1, p2)
        ΔP     = |p1 - p2|

        # Velocity envelope
        v_min = -k_v_min * V_char
        v_max =  k_v_max * V_char

        # Pressure envelope
        p_min = P_low  - k_p_min * ΔP
        p_max = P_high + k_p_max * ΔP

    Purpose:
        - Provide Navier–Stokes with hard physical envelopes that are
          conservative enough to never cut valid flows, yet strict enough
          to eliminate non-physical or numerically explosive states.
        - Serve as the export layer of the Bernoulli pipeline.
        - Allow industrial-level tuning for complex geometries.

    S5 does NOT:
        - compute energy or energy_imbalance (S4),
        - solve any missing variable (S3),
        - modify primary variables,
        - perform validation or inference,
        - mutate the input state.

    S5 returns a NEW BernoulliState instance with the fields:
        p_min: float
        p_max: float
        v_min: float
        v_max: float
    populated, while all other fields remain unchanged.
    """

    def compute_min_max_constraints(self, state_with_energy, config):
        """
        Inputs:
            state_with_energy: BernoulliState
                The state produced by S4, containing all primary variables
                and diagnostic energy fields.

            config: SolverConfig
                Must contain:
                    k_v_min, k_v_max, k_p_min, k_p_max
                No defaults are assumed.

        Returns:
            new_state: BernoulliState
                A new state with:
                    - p_min
                    - p_max
                    - v_min
                    - v_max
                computed and populated using the four independent
                looseness coefficients.

        This method performs no mutation of the input state.
        """
        raise NotImplementedError