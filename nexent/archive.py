from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum
from typing import Any,Iterable

class ArchiveClass(str,Enum):
    REPOSITORY="REPOSITORY"; FOLDER="FOLDER"; FILE="FILE"; SPECIFICATION="SPECIFICATION"; CODE="CODE"
    EXPERIMENT="EXPERIMENT"; DIAGRAM="DIAGRAM"; LANGUAGE="LANGUAGE"; ALGORITHM="ALGORITHM"; PROTOCOL="PROTOCOL"
    INNOVATION="INNOVATION"; DECISION="DECISION"; TEST="TEST"; RESULT="RESULT"
class ReconstructionStatus(str,Enum):
    RESTORED="RESTORED"; CANONICAL="CANONICAL"; DERIVED="DERIVED"; PROPOSED="PROPOSED"; CONFLICT="CONFLICT"; DUPLICATE="DUPLICATE"

@dataclass(frozen=True)
class ArchiveRecord:
    record_id:str; source:str; classification:ArchiveClass; title:str; content_hash:str; status:ReconstructionStatus
    aliases:tuple[str,...]=(); derived_from:tuple[str,...]=(); conflicts:tuple[str,...]=(); metadata:dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True)
class ReconstructionResult:
    restored:tuple[ArchiveRecord,...]; canonical:tuple[ArchiveRecord,...]; derived:tuple[ArchiveRecord,...]
    proposed:tuple[ArchiveRecord,...]; conflicts:tuple[ArchiveRecord,...]; duplicates:tuple[ArchiveRecord,...]

class ArchiveReconstructor:
    def __init__(self,records:Iterable[ArchiveRecord]=()): self.records=list(records)
    def add(self,record): self.records.append(record)
    def classify(self):
        groups={}
        for r in self.records: groups.setdefault((r.title.casefold(),r.content_hash),[]).append(r)
        dup=tuple(r for g in groups.values() if len(g)>1 for r in g[1:])
        did={r.record_id for r in dup}; b={s:[] for s in ReconstructionStatus}
        for r in self.records: b[ReconstructionStatus.DUPLICATE if r.record_id in did else r.status].append(r)
        return ReconstructionResult(tuple(b[ReconstructionStatus.RESTORED]),tuple(b[ReconstructionStatus.CANONICAL]),
        tuple(b[ReconstructionStatus.DERIVED]),tuple(b[ReconstructionStatus.PROPOSED]),
        tuple(b[ReconstructionStatus.CONFLICT]),dup)
