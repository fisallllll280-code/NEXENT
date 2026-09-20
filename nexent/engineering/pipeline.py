from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping
from .lifecycle import LinearEngineeringLifecycle, Phase

@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    kind: str
    phase: Phase
    content: Mapping[str, Any]
    digest: str

    @staticmethod
    def create(artifact_id: str, kind: str, phase: Phase, content: Mapping[str, Any]) -> "Artifact":
        canonical=json.dumps(content, sort_keys=True, separators=(",",":"), ensure_ascii=False)
        return Artifact(artifact_id, kind, phase, content, sha256(canonical.encode()).hexdigest())

@dataclass
class EngineeringRun:
    system_id: str
    lifecycle: LinearEngineeringLifecycle = field(init=False)
    artifacts: dict[str,Artifact] = field(default_factory=dict)

    def __post_init__(self):
        self.lifecycle=LinearEngineeringLifecycle(self.system_id)

    def emit(self, artifact_id: str, kind: str, content: Mapping[str,Any]) -> Artifact:
        phase=self.lifecycle.state.current
        a=Artifact.create(artifact_id,kind,phase,content)
        self.artifacts[artifact_id]=a
        return a

    def gate(self, *artifact_ids: str, approved: bool=False):
        missing=[x for x in artifact_ids if x not in self.artifacts]
        if missing: raise ValueError(f"missing artifacts: {missing}")
        return self.lifecycle.advance(verified=True,approved=approved,artifact_ids=tuple(artifact_ids))

    def manifest(self) -> dict[str,Any]:
        return {
            "schema":"NEXENT-ENGINEERING-RUN-1",
            "system_id":self.system_id,
            "phase":self.lifecycle.state.current.value,
            "linear":True,
            "artifacts":{k:{"kind":v.kind,"phase":v.phase.value,"digest":v.digest}
                         for k,v in sorted(self.artifacts.items())},
            "lifecycle":self.lifecycle.manifest(),
        }

    def ready_for_execution(self) -> bool:
        return self.lifecycle.can_execute()
