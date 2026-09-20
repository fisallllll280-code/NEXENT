from nexent.engineering import Artifact, EngineeringSystem, SystemContract, VerificationStatus

def test_contract_to_executable_plan_requires_evidence_and_handler():
    s=EngineeringSystem(); c=SystemContract(system_id="SYS-001",name="adder",purpose="add values",inputs=("a","b"),outputs=("sum",),invariants=("sum=a+b",)); cid=s.register_contract(c)
    assert not s.plan(cid).executable
    s.register_handler(cid,lambda p: {"sum":p["a"]+p["b"]})
    s.add_artifact(Artifact("TEST-001","test","adder is correct",{"case":"2+3=5"},evidence=("test-run-001",),provenance=("tests/test_engineering.py",),status=VerificationStatus.TESTED))
    assert s.plan(cid).executable
    assert s.execute(cid,{"a":2,"b":3},authorized=True)=={"sum":5}

def test_execution_requires_authorization():
    s=EngineeringSystem(); cid=s.register_contract(SystemContract(system_id="SYS-002",name="noop",purpose="bounded action",inputs=("x",))); s.register_handler(cid,lambda p:p["x"])
    s.add_artifact(Artifact("TEST-002","test","bounded",True,evidence=("evidence",),provenance=("test",),status=VerificationStatus.VERIFIED))
    try: s.execute(cid,{"x":1})
    except PermissionError as e: assert "authorization" in str(e)
    else: raise AssertionError("execution should require authorization")
