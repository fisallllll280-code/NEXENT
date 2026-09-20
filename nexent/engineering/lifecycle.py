from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any

class Phase(str, Enum):
    REQUIREMENTS="REQUIREMENTS"; MODEL="MODEL"; ARCHITECTURE="ARCHITECTURE"; CONTRACTS="CONTRACTS"
    IR="IR"; IMPLEMENTATION="IMPLEMENTATION"; VERIFICATION="VERIFICATION"; VALIDATION="VALIDATION"
    EVIDENCE="EVIDENCE"; GOVERNANCE="GOVERNANCE"; RELEASE="RELEASE"; OPERATION="OPERATION"; EVOLUTION="EVOLUTION"

ORDER=tuple(Phase)

@dataclass(frozen=True)
class Gate:
    phase: Phase
    artifact_ids: tuple[str,...]=()
    verified: bool=False
    approved: bool=False

@dataclass(frozen=True)
class EngineeringState:
    system_id: str
    current: Phase
    completed: tuple[Phase,...]=()
    gates: tuple[Gate,...]=()

class LinearEngineeringLifecycle:
    """Formal monotonic lifecycle. Backward transitions and gate skipping are rejected."""
    def __init__(self, system_id: str):
        if not system_id: raise ValueError("system_id is required")
        self.state=EngineeringState(system_id,Phase.REQUIREMENTS)

    @staticmethod
    def next_phase(phase: Phase):
        i=ORDER.index(phase)
        return ORDER[i+1] if i+1 < len(ORDER) else None

    def close_gate(self, *, artifact_ids=(), verified=False, approved=False):
        if not verified: raise PermissionError(f"{self.state.current.value}: verification gate is not closed")
        if self.state.current in {Phase.GOVERNANCE,Phase.RELEASE} and not approved:
            raise PermissionError(f"{self.state.current.value}: approval is required")
        gate=Gate(self.state.current,tuple(sorted(artifact_ids)),verified,approved)
        self.state=EngineeringState(self.state.system_id,self.state.current,
                                    self.state.completed+(self.state.current,),
                                    self.state.gates+(gate,))
        return self.state

    def advance(self, *, verified=False, approved=False, artifact_ids=()):
        self.close_gate(artifact_ids=artifact_ids,verified=verified,approved=approved)
        nxt=self.next_phase(self.state.current)
        if nxt is not None:
            self.state=EngineeringState(self.state.system_id,nxt,self.state.completed,self.state.gates)
        return self.state

    def can_execute(self):
        return self.state.current in {Phase.RELEASE,Phase.OPERATION} and bool(self.state.completed)

    def manifest(self) -> dict[str,Any]:
        return {"system_id":self.state.system_id,"current_phase":self.state.current.value,
                "completed":[p.value for p in self.state.completed],
                "gates":[{"phase":g.phase.value,"artifact_ids":list(g.artifact_ids),
                          "verified":g.verified,"approved":g.approved} for g in self.state.gates],
                "linear":True}
