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
        self.p_min = 0.0
        self.p_max = 0.0
        self.v_min = 0.0
        self.v_max = 0.0

    def override(self, **kwargs):
        """Overrides primary fields in dict, others in attributes."""
        primary_fields = {'p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho'}
        for key, value in kwargs.items():
            if key in primary_fields:
                self[key] = value
            else:
                setattr(self, key, value)
        return self

    def get_s1_compliant_state(self):
        """
        Returns a copy of this state with exactly one primary variable removed.
        Does not mutate the original object.
        """
        state_copy = copy.deepcopy(self)
        # Remove 'p1' to satisfy the S1 requirement
        if "p1" in state_copy:
            del state_copy["p1"]
        return state_copy
