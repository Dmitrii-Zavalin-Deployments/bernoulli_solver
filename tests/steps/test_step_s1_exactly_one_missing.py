import pytest
from src.steps.step_s1_exactly_one_missing import StepS1ExactlyOneMissing, ValidationError
from tests.signatures.s1_exactly_one_missing_test_signature import S1ExactlyOneMissingTestSignature
from tests.dummies.dummy_bernoulli_state import BernoulliStateDummy

class TestStepS1ExactlyOneMissing(S1ExactlyOneMissingTestSignature):
    """
    Implementation of the S1 exactly-one-missing contract.
    """

    def setup_method(self):
        self.s1 = StepS1ExactlyOneMissing()

    # ---------------------------------------------------------
    # Core invariant: exactly one primary variable is missing
    # ---------------------------------------------------------

    def test_accepts_exactly_one_missing_primary(self):
        """S1 must accept states where exactly one primary variable is missing."""
        dummy = BernoulliStateDummy()
        # Remove exactly one
        del dummy['p1']
        
        result_dict, missing_var = self.s1.enforce_exactly_one_missing(dummy)
        assert missing_var == 'p1'

    def test_rejects_zero_missing_primary(self):
        """S1 must reject states where no primary variable is missing."""
        dummy = BernoulliStateDummy()
        
        # NOTE: If your implementation allows identity/round-trip (0 missing), 
        # this will fail. Adjust this assertion if identity-path is required.
        with pytest.raises(ValidationError):
            self.s1.enforce_exactly_one_missing(dummy)

    def test_rejects_two_missing_primary(self):
        """S1 must reject states where two primary variables are missing."""
        dummy = BernoulliStateDummy()
        del dummy['p1']
        del dummy['p2']
        
        with pytest.raises(ValidationError, match="Too many missing variables"):
            self.s1.enforce_exactly_one_missing(dummy)

    def test_rejects_three_or_more_missing_primary(self):
        """S1 must reject states where three or more primary variables are missing."""
        dummy = BernoulliStateDummy()
        del dummy['p1']
        del dummy['p2']
        del dummy['v1']
        
        with pytest.raises(ValidationError, match="Too many missing variables"):
            self.s1.enforce_exactly_one_missing(dummy)

    # ---------------------------------------------------------
    # Diagnostic fields must be ignored when counting missing
    # ---------------------------------------------------------

    def test_ignores_missing_diagnostic_fields(self):
        """
        S1 must ignore missing diagnostic/derived fields when counting missing variables:
            energy, energy_imbalance, p_min, p_max, v_min, v_max.
        """
        dummy = BernoulliStateDummy()
        # Ensure diagnostics are missing
        dummy.energy = None 
        
        # Should still succeed (0 missing primaries)
        # Note: Depending on your strictness, you might change this test 
        # to ensure it doesn't count diagnostic 'None' as a 'missing variable'.
        try:
            self.s1.enforce_exactly_one_missing(dummy)
        except ValidationError:
            pytest.fail("S1 raised ValidationError despite only diagnostics being missing.")

    # ---------------------------------------------------------
    # Structural invariants
    # ---------------------------------------------------------

    def test_input_immutability(self):
        """S1 must not mutate the input structure."""
        dummy = BernoulliStateDummy()
        del dummy['p1']
        
        # Create a shallow copy to compare against
        original_keys = set(dummy.keys())
        
        self.s1.enforce_exactly_one_missing(dummy)
        
        # Verify keys haven't changed (assuming mutation might happen via dict updates)
        assert set(dummy.keys()) == original_keys

    def test_frozen_dummy_alignment(self):
        """
        S1 output must match the frozen dummy structure.
        """
        dummy = BernoulliStateDummy()
        del dummy['p1']
        
        result_dict, missing_var = self.s1.enforce_exactly_one_missing(dummy)
        
        # Verify it returns the identity of the missing variable
        assert missing_var == 'p1'
        # Verify the returned dict is structurally the same as the input
        assert 'p1' not in result_dict