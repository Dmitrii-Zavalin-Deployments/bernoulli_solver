# step_s5_compute_min_max_constraints_interface.py

class StepS5ComputeMinMaxConstraintsInterface:
    """
    Contract-only interface for Step S5: Compute the Bernoulli-derived
    physical constraint envelopes required by the Navier–Stokes solver.

    S5 does NOT use pure min/max of p1, p2, v1, v2. Instead, it constructs
    *loose but truthful* physical bounds using four independent looseness
    coefficients supplied in SolverConfig:

        k_v_min, k_v_max, k_p_min, k_p_max

    These coefficients allow the developer to tune the constraint envelope
    to minimize false positives and false negatives in Navier–Stokes.

    PHYSICS THEORY & NAVIER-STOKES INTEGRATION:
    The constraint envelopes calculated here define a 'Numerical Sandbox' 
    essential for CFD stability:
    
    1. Boundary Layer Displacement (v_max): 
       Accounts for effective area reduction in pipes, allowing core flow 
       acceleration without hitting artificial ceiling bounds.
       
    2. Turbulent Recirculation (v_min): 
       **Critical for Stability.** By allowing negative velocity components 
       (eddies/vortices), we prevent numerical crashes in geometries with 
       expansions or obstacles.
       
    3. Startup Transients/Water Hammer (p_max): 
       Provides a pressure buffer to absorb the high-frequency numerical 
       shockwaves inherent in transient CFD initialization.
       
    4. Venturi & Bernoulli Effects (p_min): 
       Ensures adequate headroom for pressure drops during flow acceleration 
       through constrictions, preventing premature numerical clamping.

    S5 computes:

        # Characteristic scales
        V_char = max(|v1|, |v2|)
        P_low  = min(p1, p2)
        P_high = max(p1, p2)
        p_scale = max(0.5 * rho * V_char^2, |p1 - p2|)

        v_min = -V_char * (1.0 + k_v_min)
        v_max =  V_char * (1.0 + k_v_max)
        p_min = P_low  - p_scale * (1.0 + k_p_min)
        p_max = P_high + p_scale * (1.0 + k_p_max)

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

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # The list of strictly permitted members defined by the Constitution
        ALLOWED_MEMBERS = {"compute_min_max_constraints"}
        
        # Inspect the subclass members to ensure no 'unauthorized' logic is injected
        for name in cls.__dict__:
            # Skip dunder methods (e.g., __init__, __doc__)
            if name.startswith("__"):
                continue
                
            # If a member is defined that isn't explicitly in the contract, block it
            if name not in ALLOWED_MEMBERS:
                raise TypeError(
                    f"CONSTITUTION VIOLATION: Subclass '{cls.__name__}' is strictly "
                    f"prohibited from defining custom member '{name}'. "
                    f"Allowed interface members are: {ALLOWED_MEMBERS}"
                )

    def compute_min_max_constraints(self, state_with_energy, config):
        """
        Inputs:
            state_with_energy: BernoulliState
                The state produced by S4, containing all primary variables
                and diagnostic energy fields.

            config: SolverConfig
                Must contain: k_v_min, k_v_max, k_p_min, k_p_max.
                No defaults are assumed.

        Returns:
            new_state: BernoulliState
                A new state with p_min, p_max, v_min, v_max computed
                using the logic defined in the Physics Theory header.

        This method performs no mutation of the input state.
        """
        raise NotImplementedError