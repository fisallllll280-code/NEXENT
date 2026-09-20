from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .canonical import InnovationRecord, RecordStatus, SystemGenome, NEXENTUIR, fingerprint


class IndexKind(str, Enum):
    MASTER_ENTITY="master_entity"; SYSTEM="system"; SUBSYSTEM="subsystem"; MECHANISM="mechanism"
    FORMULA="formula"; ALGORITHM="algorithm"; LANGUAGE="language"; SYNTAX="syntax"; SEMANTIC="semantic"
    AST="ast"; IR="ir"; RUNTIME="runtime"; KERNEL="kernel"; EVENT="event"; STATE="state"
    CONTRACT="contract"; CAPABILITY="capability"; AUTHORITY="authority"; GOVERNANCE="governance"
    EVIDENCE="evidence"; VERIFICATION="verification"; PROOF="proof"; MEMORY="memory"; SIMULATION="simulation"
    GENOME="genome"; GENERATION="generation"; EVOLUTION="evolution"; PROJECT="project"; REPOSITORY="repository"
    LIBRARY="library"; FILE="file"; VISUAL="visual"; DEPENDENCY="dependency"; LINEAGE="lineage"
    LEGACY_CANONICAL="legacy_canonical"; CANONICAL_IMPLEMENTATION="canonical_implementation"
    IMPLEMENTATION_PROOF="implementation_proof"; PROOF_EVIDENCE="proof_evidence"


@dataclass(frozen=True)
class MasterEntity:
    entity_id: str
    entity_type: str
    name: str
    status: RecordStatus
    definition: str=""
    provenance: tuple[str,...]=()
    relations: tuple[str,...]=()
    evidence: tuple[str,...]=()
    metadata: dict[str,Any]=field(default_factory=dict)

    @property
    def fingerprint(self) -> str:
        return fingerprint({"entity_id":self.entity_id,"entity_type":self.entity_type,"name":self.name,
                            "status":self.status.value,"definition":self.definition,
                            "provenance":self.provenance,"relations":self.relations,
                            "evidence":self.evidence,"metadata":self.metadata})


class MasterRegistry:
    """Deterministic master entity store plus typed cross-indexes."""
    def __init__(self) -> None:
        self._entities: dict[str,MasterEntity]={}
        self._indexes: dict[IndexKind,dict[str,str]]={kind:{} for kind in IndexKind}

    def register(self, entity: MasterEntity, indexes: tuple[IndexKind,...]=()) -> str:
        if entity.entity_id in self._entities: raise ValueError(f"duplicate entity: {entity.entity_id}")
        self._entities[entity.entity_id]=entity
        self._indexes[IndexKind.MASTER_ENTITY].setdefault(entity.name.casefold(),entity.entity_id)
        for kind in indexes:
            key=entity.name.casefold()
            if key in self._indexes[kind]: raise ValueError(f"duplicate {kind.value} index key: {entity.name}")
            self._indexes[kind][key]=entity.entity_id
        return entity.entity_id

    def register_genome(self, genome: SystemGenome) -> str:
        return self.register(MasterEntity(genome.genome_id,"SYSTEM_GENOME",genome.identity,
            RecordStatus.FORMULATED,genome.purpose,genome.history,(),genome.evidence,genome.canonical_form()),
            (IndexKind.SYSTEM,IndexKind.GENOME))

    def register_innovation(self, innovation: InnovationRecord) -> str:
        return self.register(MasterEntity(innovation.canonical_id,"INNOVATION",innovation.name,
            innovation.status,innovation.definition,(innovation.origin,),
            innovation.dependencies+innovation.derived_from,innovation.evidence,
            {"family":innovation.family,"kind":innovation.kind,"implementation":innovation.implementation,
             "tests":innovation.tests,"limitations":innovation.limitations}), ())

    def register_uir(self, uir: NEXENTUIR) -> str:
        entity_id="UIR-"+uir.fingerprint[:32]
        return self.register(MasterEntity(entity_id,"UIR",f"UIR:{uir.version}",
            RecordStatus.FORMULATED,"Canonical one-model representation boundary.",metadata=uir.to_dict()),
            (IndexKind.IR,))

    def get(self, entity_id: str) -> MasterEntity: return self._entities[entity_id]
    def find(self, kind: IndexKind, name: str) -> MasterEntity:
        return self._entities[self._indexes[kind][name.casefold()]]
    def all(self) -> tuple[MasterEntity,...]: return tuple(self._entities[k] for k in sorted(self._entities))
    def index(self, kind: IndexKind) -> tuple[str,...]: return tuple(sorted(self._indexes[kind]))
    def manifest(self) -> dict[str,Any]:
        return {"entities":[e.__dict__ for e in self.all()],
                "indexes":{kind.value:self.index(kind) for kind in IndexKind}}
