import pytest
from nexent.engineering.pipeline import EngineeringRun
from nexent.engineering.lifecycle import Phase

def test_pipeline_requires_real_artifacts():
    r=EngineeringRun("NEXENT-CORE")
    with pytest.raises(ValueError): r.gate("missing")
    assert r.lifecycle.state.current is Phase.REQUIREMENTS

def test_pipeline_advances_only_through_current_phase():
    r=EngineeringRun("NEXENT-CORE")
    for phase in list(Phase)[:10]:
        a=r.emit(f"{phase.value.lower()}-001", "engineering-artifact", {})
        r.gate(a.artifact_id, approved=phase is Phase.GOVERNANCE)
    assert r.lifecycle.state.current is Phase.RELEASE
    assert not r.ready_for_execution()
    r.gate("release-001", approved=True)
    assert r.lifecycle.state.current is Phase.OPERATION
    assert r.ready_for_execution()

def test_artifact_digest_is_stable():
    r=EngineeringRun("X")
    a=r.emit("a","model",{"b":2,"a":1})
    r2=EngineeringRun("X")
    b=r2.emit("a","model",{"a":1,"b":2})
    assert a.digest==b.digest
