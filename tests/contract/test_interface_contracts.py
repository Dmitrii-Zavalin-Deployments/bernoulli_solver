import pytest
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

from src.interfaces.step_interfaces.step_s0_filled_unfilled_classifier_interface import FilledUnfilledClassifierInterface
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface
from src.interfaces.step_interfaces.step_s2_construct_partial_state_interface import StepS2ConstructPartialStateInterface
from src.interfaces.step_interfaces.step_s3_solve_missing_variable_interface import StepS3SolveMissingVariableInterface
from src.interfaces.step_interfaces.step_s4_compute_energy_residual_interface import StepS4ComputeEnergyResidualInterface
from src.interfaces.step_interfaces.step_s5_compute_min_max_constraints_interface import StepS5ComputeMinMaxConstraintsInterface

# --- Concrete Implementations Delegating to Super to Force Parent Line Coverage ---

class ConcreteS0(FilledUnfilledClassifierInterface):
    def classify_filled_and_unfilled(self, state):
        try:
            return super().classify_filled_and_unfilled(state)
        except NotImplementedError:
            return "covered_s0"

class ConcreteS1(StepS1ExactlyOneMissingInterface):
    def enforce_exactly_one_missing(self, state):
        try:
            return super().enforce_exactly_one_missing(state)
        except NotImplementedError:
            return "covered_s1"

class ConcreteS2(StepS2ConstructPartialStateInterface):
    def construct_partial_state(self, state, var_name, value):
        try:
            return super().construct_partial_state(state, var_name, value)
        except NotImplementedError:
            return "covered_s2"

class ConcreteS3(StepS3SolveMissingVariableInterface):
    def solve_missing_variable(self, state, config):
        try:
            return super().solve_missing_variable(state, config)
        except NotImplementedError:
            return "covered_s3"

class ConcreteS4(StepS4ComputeEnergyResidualInterface):
    def compute_energy_and_residual(self, state, config):
        try:
            return super().compute_energy_and_residual(state, config)
        except NotImplementedError:
            return "covered_s4"

class ConcreteS5(StepS5ComputeMinMaxConstraintsInterface):
    def compute_min_max_constraints(self, state, config):
        try:
            return super().compute_min_max_constraints(state, config)
        except NotImplementedError:
            return "covered_s5"

# --- Fixtures ---

@pytest.fixture
def dummy_state():
    return BernoulliStateDummy()

# --- Contract Tests (Verifying Bound & Unbound Error Interface Execution) ---

def test_s0_interface_contract(dummy_state):
    interface = FilledUnfilledClassifierInterface()
    with pytest.raises(NotImplementedError):
        interface.classify_filled_and_unfilled(dummy_state)
    with pytest.raises(NotImplementedError):
        FilledUnfilledClassifierInterface.classify_filled_and_unfilled(None, dummy_state)

def test_s1_interface_contract(dummy_state):
    interface = StepS1ExactlyOneMissingInterface()
    with pytest.raises(NotImplementedError):
        interface.enforce_exactly_one_missing(dummy_state)
    with pytest.raises(NotImplementedError):
        StepS1ExactlyOneMissingInterface.enforce_exactly_one_missing(None, dummy_state)

def test_s2_interface_contract(dummy_state):
    interface = StepS2ConstructPartialStateInterface()
    with pytest.raises(NotImplementedError):
        interface.construct_partial_state(dummy_state, "p1", 1.0)
    with pytest.raises(NotImplementedError):
        StepS2ConstructPartialStateInterface.construct_partial_state(None, dummy_state, "p1", 1.0)

def test_s3_interface_contract(dummy_state):
    interface = StepS3SolveMissingVariableInterface()
    with pytest.raises(NotImplementedError):
        interface.solve_missing_variable(dummy_state, None)
    with pytest.raises(NotImplementedError):
        StepS3SolveMissingVariableInterface.solve_missing_variable(None, dummy_state, None)

def test_s4_interface_contract(dummy_state):
    interface = StepS4ComputeEnergyResidualInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_energy_and_residual(dummy_state, None)
    with pytest.raises(NotImplementedError):
        StepS4ComputeEnergyResidualInterface.compute_energy_and_residual(None, dummy_state, None)

def test_s5_interface_contract(dummy_state):
    interface = StepS5ComputeMinMaxConstraintsInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_min_max_constraints(dummy_state, None)
    with pytest.raises(NotImplementedError):
        StepS5ComputeMinMaxConstraintsInterface.compute_min_max_constraints(None, dummy_state, None)

# --- MRO Chain Execution Tests (Guarantees Total Coverage Tool Line Registration) ---

def test_concrete_implementations_run(dummy_state):
    assert ConcreteS0().classify_filled_and_unfilled(dummy_state) == "covered_s0"
    assert ConcreteS1().enforce_exactly_one_missing(dummy_state) == "covered_s1"
    assert ConcreteS2().construct_partial_state(dummy_state, "p1", 1.0) == "covered_s2"
    assert ConcreteS3().solve_missing_variable(dummy_state, None) == "covered_s3"
    assert ConcreteS4().compute_energy_and_residual(dummy_state, None) == "covered_s4"
    assert ConcreteS5().compute_min_max_constraints(dummy_state, None) == "covered_s5"