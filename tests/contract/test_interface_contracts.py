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

# ==============================================================================
# 1. CONTRACT TESTS (Verifying NotImplementedError on Valid Instances)
# ==============================================================================

def test_s0_interface_contract(dummy_state):
    interface = FilledUnfilledClassifierInterface()
    with pytest.raises(NotImplementedError):
        interface.classify_filled_and_unfilled(dummy_state)

def test_s1_interface_contract(dummy_state):
    interface = StepS1ExactlyOneMissingInterface()
    with pytest.raises(NotImplementedError):
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


# ==============================================================================
# 2. CONSTITUTION VIOLATION TESTS (Forces 100% Line Coverage on TypeErrors)
# ==============================================================================
# These tests dynamically create an illegal subclass containing an unauthorized 
# attribute, forcing the validation loops to execute the missing error-raising lines.

def test_s0_constitution_violation():
    with pytest.raises(TypeError, match="CONSTITUTION VIOLATION"):
        type("BadS0", (FilledUnfilledClassifierInterface,), {"forbidden_custom_member": True})

def test_s1_constitution_violation():
    with pytest.raises(TypeError, match="CONSTITUTION VIOLATION"):
        type("BadS1", (StepS1ExactlyOneMissingInterface,), {"forbidden_custom_member": True})

def test_s2_constitution_violation():
    with pytest.raises(TypeError, match="CONSTITUTION VIOLATION"):
        type("BadS2", (StepS2ConstructPartialStateInterface,), {"forbidden_custom_member": True})

def test_s3_constitution_violation():
    with pytest.raises(TypeError, match="CONSTITUTION VIOLATION"):
        type("BadS3", (StepS3SolveMissingVariableInterface,), {"forbidden_custom_member": True})

def test_s4_constitution_violation():
    with pytest.raises(TypeError, match="CONSTITUTION VIOLATION"):
        type("BadS4", (StepS4ComputeEnergyResidualInterface,), {"forbidden_custom_member": True})

def test_s5_constitution_violation():
    with pytest.raises(TypeError, match="CONSTITUTION VIOLATION"):
        type("BadS5", (StepS5ComputeMinMaxConstraintsInterface,), {"forbidden_custom_member": True})