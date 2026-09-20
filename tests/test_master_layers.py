from pathlib import Path
from nexent.canonical import InnovationRecord, RecordStatus
from nexent.system import NEXENTSystem

def test_integrated_system_exposes_canonical_layers(tmp_path):
    system=NEXENTSystem(str(tmp_path/"events.jsonl"))
    assert len(system.languages.all())==9
    innovation=InnovationRecord.create("Archive Reconstruction","fabric","archive","conservative reconstruction","NEXENT")
    assert system.register_innovation(innovation)==innovation.canonical_id
    assert system.kernel.ledger.verify()
    assert Path(tmp_path/"events.jsonl").exists()
