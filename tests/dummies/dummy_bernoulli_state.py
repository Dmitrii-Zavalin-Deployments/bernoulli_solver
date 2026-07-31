import copy

from src.interfaces.bernoulli_state_interface import BernoulliStateInterface


class BernoulliStateDummy(dict, BernoulliStateInterface):
    def __init__(self):
        # 1. Initialize only primary variables into the dict
        # This satisfies the 'StepS1ExactlyOneMissing' validator
        super().__init__({
            'p1': 1.0, 'p2': 1.0, 'v1': 1.0, 'v2': 1.0,
            'h1': 1.0, 'h2': 1.0, 'rho': 1.0
        })
        
        # 2. Store extra fields as instance attributes (not dict keys)
        self.energy = [0.0, 0.0]
        self.energy_imbalance = 0.0
        
        # New structure per Sovereign Container schema
        self.initial_conditions = {
            "velocity": [1.0, 0.0, 0.0], 
            "pressure": 1.0
        }
        self.physical_constraints = {
            "min_pressure": 0.0, 
            "max_pressure": 0.0,
            "min_velocity": 0.0, 
            "max_velocity": 0.0
        }

    def __getattr__(self, name):
        """Bridges dictionary keys to object attributes for S3 compatibility."""
        if name in self:
            return self[name]
        # If an expected primary field was deleted for S1 compliance, 
        # return NaN so that S3's math.isnan(getattr(...)) detects it perfectly.
        if name in {'p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho'}:
            return float('nan')
        raise AttributeError(f"'BernoulliStateDummy' object has no attribute '{name}'")

    def override(self, **kwargs):
        """Overrides primary fields in dict, others in attributes."""
        primary_fields = {'p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho'}
        for key, value in kwargs.items():
            if key in primary_fields:
                self[key] = value
            else:
                setattr(self, key, value)
        return self

    def get_s1_compliant_state(self, missing_key="h1"):
        """Removes the specified key to satisfy S1 gatekeeper requirements."""
        state_copy = copy.deepcopy(self)
        if missing_key in state_copy:
            del state_copy[missing_key]
        return state_copy
