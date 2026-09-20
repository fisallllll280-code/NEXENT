from nexent.safety.containment import Boundary, ContainmentEngine, FailureMode, SafetyState

def test_verified_transition_inside_boundary_is_allowed():
    engine = ContainmentEngine([Boundary("kernel", ("replay",), ("append_only",))])
    result = engine.evaluate("kernel", ["replay"], ["append_only"], True)
    assert result.allowed is True
    assert result.state is SafetyState.NORMAL
    assert result.failures == ()

def test_boundary_breach_is_quarantined():
    engine = ContainmentEngine([Boundary("kernel", ("replay",), ("append_only",))])
    result = engine.evaluate("kernel", ["deployment"], ["append_only"], True)
    assert result.allowed is False
    assert result.state is SafetyState.QUARANTINED
    assert FailureMode.BOUNDARY_BREACH in result.failures

def test_unknown_or_unverified_change_fails_closed():
    engine = ContainmentEngine([])
    result = engine.evaluate("unknown", ["anything"], [], False)
    assert result.allowed is False
    assert result.state is SafetyState.QUARANTINED
    assert FailureMode.UNKNOWN_DEPENDENCY in result.failures
    assert FailureMode.UNVERIFIED_CHANGE in result.failures
