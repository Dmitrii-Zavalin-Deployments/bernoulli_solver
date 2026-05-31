from src.interfaces.bernoulli_state_interface import BernoulliStateInterface

class BernoulliStateDummy(dict, BernoulliStateInterface):
    def __init__(self):
        # Set all interface defaults immediately using dict's constructor
        super().__init__({
            'p1': 1.0, 'p2': 1.0, 'v1': 1.0, 'v2': 1.0,
            'h1': 1.0, 'h2': 1.0, 'rho': 1.0,
            'energy': [0.0, 0.0], 'energy_imbalance': 0.0,
            'p_min': 0.0, 'p_max': 0.0, 'v_min': 0.0, 'v_max': 0.0
        })

    def override(self, **kwargs):
        """Allows overriding specific fields while maintaining object identity."""
        self.update(kwargs)
        return self
