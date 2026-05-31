import pytest
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

from src.interfaces.step_interfaces.step_s0_filled_unfilled_classifier_interface import FilledUnfilledClassifierInterface
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface
from src.interfaces.step_interfaces.step_s2_construct_partial_state_interface import StepS2ConstructPartialStateInterface
from src.interfaces.step_interfaces.step_s3_solve_missing_variable_interface import StepS3SolveMissingVariableInterface
from src.interfaces.step_interfaces.step_s4_compute_energy_residual_interface import StepS4ComputeEnergyResidualInterface
from src.interfaces.step_interfaces.step_s5_compute_min_max_constraints_interface import StepS5ComputeMinMaxConstraintsInterface

# --- Concrete Implementations for Coverage ---

class ConcreteS0(FilledUnfilledClassifierInterface):
    def classify_filled_and_unfilled(self, state): return None

class ConcreteS1(StepS1ExactlyOneMissingInterface):
    def enforce_exactly_one_missing(self, state): return None

class ConcreteS2(StepS2ConstructPartialStateInterface):
    def construct_partial_state(self, state, var_name, value): return None

class ConcreteS3(StepS3SolveMissingVariableInterface):
    def solve_missing_variable(self, state, config): return None

class ConcreteS4(StepS4ComputeEnergyResidualInterface):
    def compute_energy_and_residual(self, state, config): return None

class ConcreteS5(StepS5ComputeMinMaxConstraintsInterface):
    def compute_min_max_constraints(self, state, config): return None

# --- Fixtures ---

@pytest.fixture
def dummy_state():
    return BernoulliStateDummy()

# --- Contract Tests (Verifying Interfaces Raise Error) ---

def test_s0_interface_contract(dummy_state):
    interface = FilledUnfilledClassifierInterface()
    with pytest.raises(NotImplementedError):
        interface.classify_filled_and_unfilled(dummy_state)

def test_s1_interface_contract(dummy_state):
    interface = StepS1ExactlyOneMissingInterface()
    with pytest.raises(NotImplementedError):
        # We pass the dummy directly. This ensures the interface 
        # is capable of accepting the expected object type.
        interface.enforce_exactly_one_missing(dummy_state)

def test_s2_interface_contract(dummy_state):
    interface = StepS2ConstructPartialStateInterface()
    with pytest.raises(NotImplementedError):
        interface.construct_partial_state(dummy_state, "p1", 1.0)

def test_s3_interface_contract(dummy_state):
    interface = StepS3SolveMissingVariableInterface()
    with pytest.raises(NotImplementedError):
        interface.solve_missing_variable(dummy_state, None)

def test_s4_interface_contract(dummy_state):
    interface = StepS4ComputeEnergyResidualInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_energy_and_residual(dummy_state, None)

def test_s5_interface_contract(dummy_state):
    interface = StepS5ComputeMinMaxConstraintsInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_min_max_constraints(dummy_state, None)

# --- Concrete Usage Tests (Achieving 100% Coverage) ---

def test_concrete_implementations_run(dummy_state):
    # This forces execution of all lines in the interface files, including __init__
    assert ConcreteS0().classify_filled_and_unfilled(dummy_state) is None
    assert ConcreteS1().enforce_exactly_one_missing(dummy_state) is None
    assert ConcreteS2().construct_partial_state(dummy_state, "p1", 1.0) is None
    assert ConcreteS3().solve_missing_variable(dummy_state, None) is None
    assert ConcreteS4().compute_energy_and_residual(dummy_state, None) is None
    assert ConcreteS5().compute_min_max_constraints(dummy_state, None) is None