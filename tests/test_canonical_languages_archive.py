from nexent.archive import *
from nexent.canonical import *
from nexent.languages import *

def test_genome_nexus_and_algebra():
    g=SystemGenome("S-1","organize",capabilities=("index",)); assert g.genome_id.startswith("GEN-")
    n=Nexus(); n.link(NexusRelation("A","B","depends_on","dependency")); n.link(NexusRelation("B","C","supports","evidence"))
    assert n.impact("A")==("B",); assert diff({"x":1},{"x":2})=={"x":{"left":1,"right":2}}

def test_language_family_is_proposed():
    r=proposed_nxl_registry(); assert len(r.all())==9; assert all(x.status is LanguageStatus.PROPOSED for x in r.all())

def test_archive_conservative_duplicate():
    a=ArchiveRecord("R1","old/a",ArchiveClass.INNOVATION,"X","h1",ReconstructionStatus.RESTORED)
    b=ArchiveRecord("R2","old/b",ArchiveClass.INNOVATION,"X","h1",ReconstructionStatus.RESTORED)
    c=ArchiveRecord("R3","new",ArchiveClass.INNOVATION,"Y","h2",ReconstructionStatus.PROPOSED)
    r=ArchiveReconstructor([a,b,c]).classify(); assert r.restored==(a,); assert r.duplicates==(b,); assert r.proposed==(c,)
