from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .core import SystemContract, Artifact

@dataclass(frozen=True)
class NEORecord:
    record_id: str
    kind: str
    canonical_id: str
    definition: dict[str, Any]
    linked_artifacts: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()

class NEXENTEngineeringOntology:
    """Canonical semantic index connecting contracts, artifacts, evidence and provenance."""
    def __init__(self) -> None:
        self.records: dict[str, NEORecord] = {}

    def register_contract(self, contract: SystemContract) -> NEORecord:
        record = NEORecord(
            record_id=contract.system_id,
            kind="SYSTEM_CONTRACT",
            canonical_id=contract.canonical_id,
            definition=contract.canonical(),
        )
        existing = self.records.get(record.record_id)
        if existing and existing != record:
            raise ValueError(f"NEO identity collision: {record.record_id}")
        self.records[record.record_id] = record
        return record

    def bind_artifact(self, system_id: str, artifact: Artifact) -> NEORecord:
        record = self.records[system_id]
        updated = NEORecord(record.record_id, record.kind, record.canonical_id,
                            record.definition,
                            tuple(sorted(set(record.linked_artifacts) | {artifact.artifact_id})),
                            tuple(sorted(set(record.evidence) | set(artifact.evidence))),
                            tuple(sorted(set(record.provenance) | set(artifact.provenance))))
        self.records[system_id] = updated
        return updated

    def get(self, system_id: str) -> NEORecord:
        return self.records[system_id]

    def manifest(self) -> tuple[NEORecord, ...]:
        return tuple(self.records[k] for k in sorted(self.records))
