from nexent.engineering.formal_execution import FormalExecution
from nexent.engineering.lifecycle import Phase

def test_e2e_reaches_evolution_without_bypass():
    run=FormalExecution("E2E-DRY-RUN")
    for phase in list(Phase)[:-1]:
        artifact=run.emit(
            f"{phase.value.lower()}-001",
            phase.value.lower(),
            {"phase":phase.value,"sequence":list(Phase).index(phase)},
        )
        run.advance(artifact.artifact_id,approved=phase in {Phase.GOVERNANCE,Phase.RELEASE})
    assert run.phase is Phase.EVOLUTION
    assert run.manifest()["complete"] is True

def test_direct_implementation_bypass_is_rejected():
    run=FormalExecution("E2E-BYPASS")
    artifact=run.emit("requirements-001","requirements",{"x":"required"})
    try:
        run.advance("implementation-001")
    except ValueError:
        pass
    else:
        raise AssertionError("bypass must be rejected")
    assert run.phase is Phase.REQUIREMENTS
