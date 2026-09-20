from nexent.engineering.formal_execution import FormalExecution
from nexent.engineering.lifecycle import Phase

def test_end_to_end_requirement_to_operation():
    run=FormalExecution("E2E-001")
    artifacts={
        Phase.REQUIREMENTS:"requirements",
        Phase.MODEL:"model",
        Phase.ARCHITECTURE:"architecture",
        Phase.CONTRACTS:"contracts",
        Phase.IR:"ir",
        Phase.IMPLEMENTATION:"implementation",
        Phase.VERIFICATION:"verification",
        Phase.VALIDATION:"validation",
        Phase.EVIDENCE:"evidence",
        Phase.GOVERNANCE:"governance",
        Phase.RELEASE:"release",
        Phase.OPERATION:"operation",
    }
    for phase in list(Phase)[:-1]:
        aid=phase.value.lower()+"-e2e"
        run.emit(aid,artifacts[phase],{"phase":phase.value,"system":"E2E-001"})
        run.advance(aid,approved=phase in {Phase.GOVERNANCE,Phase.RELEASE})
    assert run.phase is Phase.EVOLUTION
    assert run.execute_ready() is True
    assert len(run.records)==12

def test_zero_bypass():
    run=FormalExecution("E2E-002")
    req=run.emit("req","requirements",{"r":"R1"})
    try:
        run.advance("missing")
        assert False
    except ValueError:
        pass
    run.advance(req.artifact_id)
    assert run.phase is Phase.MODEL
