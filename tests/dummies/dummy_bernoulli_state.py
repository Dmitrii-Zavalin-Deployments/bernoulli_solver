from src.interfaces.bernoulli_state_interface import BernoulliStateInterface

class BernoulliStateDummy(BernoulliStateInterface):
    def __init__(self, **kwargs):
        # Initialize with provided values, default to 0.0 if not provided
        for field in ['p1', 'p2', 'v1', 'v2', 'h1', 'h2', 'rho', 'energy_imbalance', 
                      'p_min', 'p_max', 'v_min', 'v_max']:
            setattr(self, field, kwargs.get(field, 0.0))
        self.energy = kwargs.get('energy', [0.0, 0.0])
