from nexent.agents.registry import AgentProfile, AgentRegistry, AgentStatus
from nexent.engineering import Artifact, ConflictKind, ContradictionEngine, EngineeringTask, MultiMindCoordinator, NEXENTEngineeringOntology, SystemContract, VerificationStatus

def test_coordinator_routes_capability():
    registry = AgentRegistry()
    registry.register(AgentProfile("MATH", "MATHEMATICS", "formal models", capabilities=("math",), status=AgentStatus.ACTIVE))
    result = MultiMindCoordinator(registry).route(EngineeringTask("T1", ("math",)))
    assert result.executable
    assert result.selected_agents == ("MATH",)

def test_neo_binds_artifact():
    contract = SystemContract("S1", "system", "purpose")
    artifact = Artifact("A1", "proof", "claim", {"x": 1}, evidence=("E1",), provenance=("P1",), status=VerificationStatus.VERIFIED)
    neo = NEXENTEngineeringOntology()
    neo.register_contract(contract)
    record = neo.bind_artifact("S1", artifact)
    assert record.linked_artifacts == ("A1",)
    assert record.evidence == ("E1",)

def test_contradiction_engine_records_conflict():
    a = Artifact("A", "model", "claim A", {"x": 1}, evidence=("E1",), provenance=("P1",))
    b = Artifact("B", "model", "claim B", {"x": 2}, evidence=("E2",), provenance=("P2",))
    conflicts = ContradictionEngine().compare(a, b)
    assert {c.kind for c in conflicts} == {ConflictKind.SEMANTIC, ConflictKind.CONSTRAINT, ConflictKind.EVIDENCE, ConflictKind.DEPENDENCY}
