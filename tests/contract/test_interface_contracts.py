import pytest
from src.interfaces.step_interfaces.step_s0_filled_unfilled_classifier_interface import FilledUnfilledClassifierInterface
from src.interfaces.step_interfaces.step_s1_exactly_one_missing_interface import StepS1ExactlyOneMissingInterface
from src.interfaces.step_interfaces.step_s2_construct_partial_state_interface import StepS2ConstructPartialStateInterface
from src.interfaces.step_interfaces.step_s3_solve_missing_variable_interface import StepS3SolveMissingVariableInterface
from src.interfaces.step_interfaces.step_s4_compute_energy_residual_interface import StepS4ComputeEnergyResidualInterface
from src.interfaces.step_interfaces.step_s5_compute_min_max_constraints_interface import StepS5ComputeMinMaxConstraintsInterface

def test_s0_interface_contract():
    interface = FilledUnfilledClassifierInterface()
    with pytest.raises(NotImplementedError):
        interface.classify_filled_and_unfilled(None)

def test_s1_interface_contract():
    interface = StepS1ExactlyOneMissingInterface()
    with pytest.raises(NotImplementedError):
        interface.enforce_exactly_one_missing({})

def test_s2_interface_contract():
    interface = StepS2ConstructPartialStateInterface()
    with pytest.raises(NotImplementedError):
        interface.construct_partial_state({}, "", None)

def test_s3_interface_contract():
    interface = StepS3SolveMissingVariableInterface()
    with pytest.raises(NotImplementedError):
        interface.solve_missing_variable(None, None)

def test_s4_interface_contract():
    interface = StepS4ComputeEnergyResidualInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_energy_and_residual(None, None)

def test_s5_interface_contract():
    interface = StepS5ComputeMinMaxConstraintsInterface()
    with pytest.raises(NotImplementedError):
        interface.compute_min_max_constraints(None, None)