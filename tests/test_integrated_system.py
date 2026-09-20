from nexent.system import NEXENTSystem
from nexent.agents.registry import AgentProfile, AgentStatus
from nexent.engineering import Artifact, EngineeringTask, SystemContract, VerificationStatus
from nexent.van import VANDesign

def test_integrated_system_routes_binds_and_runs():
    system = NEXENTSystem()
    system.agents.register(AgentProfile("ENG", "ENGINEER", "build", capabilities=("implementation",), status=AgentStatus.ACTIVE))
    assert system.route(EngineeringTask("T1", ("implementation",))).executable
    contract = SystemContract("S1", "adder", "add values", inputs=("a", "b"), outputs=("sum",))
    cid = system.register_contract(contract)
    system.register_handler(cid, lambda p: p["a"] + p["b"])
    artifact = Artifact("A1", "test-proof", "adder verified", {"example": 5}, evidence=("test:adder",), provenance=("tests/test_integrated_system.py",), status=VerificationStatus.VERIFIED)
    system.attach_artifact("S1", artifact)
    result = system.run(cid, {"a": 2, "b": 3}, authorized=True, actor="test")
    assert result.status == "COMPLETED" and result.output == 5
    system.register_visual(VANDesign("adder", (800, 600), ("input", "result"), {}, {}))
    assert system.snapshot().ledger_valid
