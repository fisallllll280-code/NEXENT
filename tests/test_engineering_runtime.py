from nexent.engineering import Artifact, EngineeringHypothesis, EngineeringRuntime, SystemContract, VerificationStatus

def test_runtime():
    rt=EngineeringRuntime(); cid=rt.deploy(SystemContract("SYS-RUN","adder","bounded addition",inputs=("a","b")),lambda p:p["a"]+p["b"])
    rt.attach_evidence(Artifact("EV-RUN","test","addition tested",{"case":"2+3"},evidence=("run",),provenance=("test",),status=VerificationStatus.VERIFIED))
    result=rt.run(cid,{"a":2,"b":3},authorized=True)
    assert result.status=="COMPLETED" and result.output==5 and rt.ledger.verify()

def test_falsifiable():
    h=EngineeringHypothesis("H-1","new mechanism",("x","t"),equations=("x(t+1)=F(x(t))",),falsifiers=("measurement violates bound",))
    assert h.engineering_path()[-1]=="DEPLOY"
