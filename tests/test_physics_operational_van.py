from decimal import Decimal
from nexent.physics import PhysicalState,PhysicsScenario,Vector3,simulate
from nexent.operational import OperationalRecord,RecordKind
from nexent.van import VANDesign

def test_physics():
    s=PhysicalState(Vector3.from_values(0,0,0),Vector3.from_values(0,0,0),2)
    r=simulate(PhysicsScenario(s,(Vector3.from_values(2,0,0),),Decimal("0.5")))
    assert r.velocity.x==Decimal("0.5"); assert r.position.x==Decimal("0.25")
def test_record(): assert len(OperationalRecord(RecordKind.COMPUTATION,{"v":42},"test").digest)==64
def test_van(): assert "graph" in VANDesign("NEXENT",(1440,900),("graph",),{},{}).to_dict()["components"]
