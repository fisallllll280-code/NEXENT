from nexent.engineering.formal_execution import FormalExecution
from nexent.engineering.lifecycle import Phase

def test_full_linear_execution():
    run=FormalExecution("NEXENT-TEST")
    for phase in list(Phase)[:-1]:
        assert run.phase is phase
        a=run.emit(phase.value.lower()+"-01","phase-artifact",{"phase":phase.value})
        run.advance(a.artifact_id,approved=phase in {Phase.GOVERNANCE,Phase.RELEASE})
    assert run.phase is Phase.EVOLUTION
    assert run.manifest()["complete"] is True

def test_phase_cannot_consume_foreign_artifact():
    run=FormalExecution("NEXENT-TEST-2")
    a=run.emit("req-01","requirements",{"x":1})
    run.advance(a.artifact_id)
    b=run.emit("model-01","model",{"x":2})
    run.advance(b.artifact_id)
    assert run.phase is Phase.ARCHITECTURE

def test_execution_is_blocked_until_release():
    assert FormalExecution("NEXENT-TEST-3").execute_ready() is False
