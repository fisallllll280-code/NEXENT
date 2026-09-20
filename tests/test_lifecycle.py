import pytest
from nexent.engineering.lifecycle import LinearEngineeringLifecycle, Phase

def test_lifecycle_is_strictly_linear():
    l=LinearEngineeringLifecycle("SYS-1")
    assert l.state.current is Phase.REQUIREMENTS
    with pytest.raises(PermissionError): l.advance()
    for expected in list(Phase)[:-1]:
        assert l.state.current is expected
        l.advance(verified=True, approved=expected in {Phase.GOVERNANCE,Phase.RELEASE})
    assert l.state.current is Phase.EVOLUTION

def test_release_requires_approval():
    l=LinearEngineeringLifecycle("SYS-2")
    for phase in list(Phase)[:9]:
        assert l.state.current is phase
        l.advance(verified=True)
    assert l.state.current is Phase.GOVERNANCE
    with pytest.raises(PermissionError): l.advance(verified=True, approved=False)

def test_manifest_is_deterministic_shape():
    l=LinearEngineeringLifecycle("SYS-3")
    l.advance(verified=True)
    assert l.manifest()["linear"] is True
    assert l.manifest()["completed"] == ["REQUIREMENTS"]
