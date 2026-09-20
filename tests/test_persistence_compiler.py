from nexent.ledger import EventLedger
from nexent.replay import ReplayEngine
from nexent.engineering.compiler import EngineeringCompiler
from nexent.engineering import SystemContract

def test_persistent_ledger_and_replay(tmp_path):
    path=tmp_path/"events.jsonl"
    ledger=EventLedger(path)
    ledger.append("A","T","E",{"x":1})
    ledger.append("B","T","E",{"x":2})
    restored=EventLedger(path)
    assert restored.verify()
    assert ReplayEngine().entity_events(restored,"E")[1].payload["x"] == 2

def test_compiler_is_deterministic():
    c=SystemContract("S","demo","test",inputs=("x",),outputs=("y",),invariants=("field:y=2",))
    compiler=EngineeringCompiler()
    a=compiler.compile(c)
    b=compiler.compile(c)
    assert a.fingerprint == b.fingerprint
    assert a.ast["id"] == "S"
