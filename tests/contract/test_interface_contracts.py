import pytest
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

from src.interfaces.step_interfaces.step_s0_filled_unfilled_classifier_interface import FilledUnfilledClassifierInterface
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface
from src.interfaces.step_interfaces.step_s2_construct_partial_state_interface import StepS2ConstructPartialStateInterface
from src.interfaces.step_interfaces.step_s3_solve_missing_variable_interface import StepS3SolveMissingVariableInterface
from src.interfaces.step_interfaces.step_s4_compute_energy_residual_interface import StepS4ComputeEnergyResidualInterface
from src.interfaces.step_interfaces.step_s5_compute_min_max_constraints_interface import StepS5ComputeMinMaxConstraintsInterface

@pytest.fixture
def dummy_state():
    return BernoulliStateDummy()

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
        interface.solve_missing_variable(dummy_state, None) # Assuming None is config

def test_s4_interface_contract(dummy_state):
    interface = StepS4ComputeEnergyResidualInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_energy_and_residual(dummy_state, None)

def test_s5_interface_contract(dummy_state):
    interface = StepS5ComputeMinMaxConstraintsInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_min_max_constraints(dummy_state, None)