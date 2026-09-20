from nexent.canonical import InnovationRecord, RecordStatus, SystemGenome, NEXENTUIR
from nexent.master_registry import IndexKind, MasterRegistry

def test_master_registry_preserves_status_and_indexes():
    registry=MasterRegistry()
    genome=SystemGenome("NEXENT","canonical engineering fabric",history=("RESTORED:archive",))
    gid=registry.register_genome(genome)
    assert registry.get(gid).status is RecordStatus.FORMULATED
    assert registry.find(IndexKind.SYSTEM,"NEXENT").entity_id==gid
    innovation=InnovationRecord.create("Proof-Carrying Artifact","mechanism","proof",
        "artifact carries claim, evidence and verification state","NEXENT",status=RecordStatus.PROPOSED)
    iid=registry.register_innovation(innovation)
    assert registry.get(iid).status is RecordStatus.PROPOSED
    assert registry.find(IndexKind.MASTER_ENTITY,"Proof-Carrying Artifact").entity_id==iid

def test_uir_is_indexed_as_ir():
    registry=MasterRegistry()
    uir=NEXENTUIR("1",{"meaning":"x"},{"identity":"x"})
    uid=registry.register_uir(uir)
    assert registry.find(IndexKind.IR,"UIR:1").entity_id==uid
