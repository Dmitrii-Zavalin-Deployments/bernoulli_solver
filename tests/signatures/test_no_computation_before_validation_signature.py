class NoComputationBeforeValidationTestSignature:
    """
    Contract‑level signature ensuring that no computation is allowed
    before all contract‑validation tests pass.
    Validation is a mandatory pre‑execution gate.
    No logic or assertions here.
    """

    def test_solver_refuses_execution_if_validation_fails(self):
        """
        Validate that the solver refuses to execute any step of the
        Minimal Step Chain when validation has not passed or has failed.
        """
        raise NotImplementedError

    def test_solver_requires_successful_validation_before_execution(self):
        """
        Validate that the solver may only begin execution after all
        contract‑validation checks have succeeded.
        """
        raise NotImplementedError

    def test_no_partial_or_intermediate_execution_allowed(self):
        """
        Validate that the solver cannot execute partial steps, preview
        steps, or internal computations before validation succeeds.
        """
        raise NotImplementedError

    def test_validation_gate_is_global_and_non_bypassable(self):
        """
        Validate that the validation gate cannot be bypassed by direct
        calls, internal methods, or step‑level execution attempts.
        """
        raise NotImplementedError