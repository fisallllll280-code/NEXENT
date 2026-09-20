from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .lifecycle import LinearEngineeringLifecycle, Phase
from .pipeline import Artifact

@dataclass(frozen=True)
class PhaseRecord:
    phase: Phase
    artifact_ids: tuple[str,...]
    artifact_digests: tuple[str,...]

class FormalExecution:
    """Single control-plane facade for the complete NEXENT linear engineering flow."""
    def __init__(self, system_id: str):
        self.lifecycle=LinearEngineeringLifecycle(system_id)
        self.artifacts: dict[str,Artifact]={}
        self.records: list[PhaseRecord]=[]

    @property
    def phase(self): return self.lifecycle.state.current

    def emit(self, artifact_id: str, kind: str, content: Mapping[str,Any]) -> Artifact:
        if artifact_id in self.artifacts: raise ValueError(f"duplicate artifact: {artifact_id}")
        artifact=Artifact.create(artifact_id,kind,self.phase,content)
        self.artifacts[artifact_id]=artifact
        return artifact

    def advance(self, *artifact_ids: str, approved: bool=False):
        if not artifact_ids: raise ValueError(f"{self.phase.value}: at least one artifact is required")
        missing=[a for a in artifact_ids if a not in self.artifacts]
        if missing: raise ValueError(f"unknown artifacts: {missing}")
        wrong=[a for a in artifact_ids if self.artifacts[a].phase is not self.phase]
        if wrong: raise ValueError(f"artifacts belong to another phase: {wrong}")
        ids=tuple(sorted(artifact_ids))
        self.lifecycle.advance(verified=True,approved=approved,artifact_ids=ids)
        self.records.append(PhaseRecord(self.lifecycle.state.completed[-1],ids,
                                        tuple(self.artifacts[a].digest for a in ids)))
        return self.phase

    def execute_ready(self):
        return self.lifecycle.can_execute()

    def manifest(self) -> dict[str,Any]:
        return {"schema":"NEXENT-FORMAL-EXECUTION-1","system_id":self.lifecycle.state.system_id,
                "current_phase":self.phase.value,"linear":True,
                "complete":self.phase is Phase.EVOLUTION,"executable":self.execute_ready(),
                "records":[{"phase":r.phase.value,"artifact_ids":list(r.artifact_ids),
                            "artifact_digests":list(r.artifact_digests)} for r in self.records],
                "artifact_count":len(self.artifacts),"lifecycle":self.lifecycle.manifest()}
