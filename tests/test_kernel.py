from nexent import NexentKernel
from nexent.model import EntitySpec, Capability, Intent

def kernel():
    k=NexentKernel()
    k.register_entity(EntitySpec("kernel","kernel","core",("execute",),()))
    k.register_capability(Capability("sum","1.0","sum",lambda p:int(p["a"])+int(p["b"])))
    return k

def test_execution_produces_evidence_and_valid_ledger():
    k=kernel()
    r=k.execute(Intent("i1","user","sum","sum",{"a":"2","b":"3"}))
    assert r.status=="COMPLETED"
    assert r.output==5
    assert r.evidence_id in k.evidence
    assert k.ledger.verify()

def test_policy_rejects_missing_required_input():
    k=kernel()
    k.constitution.require("sum","a","b")
    r=k.execute(Intent("i2","user","sum","sum",{"a":"2"}))
    assert r.status=="REJECTED"
    assert r.reason=="a,b"

def test_graph_validation():
    k=kernel()
    k.register_entity(EntitySpec("broken","component","x",(),("missing",)))
    assert k.validate()
