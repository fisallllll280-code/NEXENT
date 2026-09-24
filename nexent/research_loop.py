from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class ResearchStage(str, Enum):
    OBSERVE = "OBSERVE"
    FRONTIER = "FRONTIER"
    HYPOTHESIS = "HYPOTHESIS"
    CANDIDATE = "CANDIDATE"
    SIMULATION = "SIMULATION"
    ATTACK = "ATTACK"
    PROOF = "PROOF"
    GOVERNANCE = "GOVERNANCE"
    ADOPTION = "ADOPTION"


@dataclass(frozen=True)
class ResearchRecord:
    stage: ResearchStage
    subject_id: str
    evidence: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


class ResearchLoop:
    """Deterministic state machine for NEXENT's governed research loop."""

    ORDER = (
        ResearchStage.OBSERVE,
        ResearchStage.FRONTIER,
        ResearchStage.HYPOTHESIS,
        ResearchStage.CANDIDATE,
        ResearchStage.SIMULATION,
        ResearchStage.ATTACK,
        ResearchStage.PROOF,
        ResearchStage.GOVERNANCE,
        ResearchStage.ADOPTION,
    )

    def next_stage(self, current: ResearchStage) -> ResearchStage:
        index = self.ORDER.index(current)
        if index + 1 >= len(self.ORDER):
            raise ValueError("research loop is already at terminal stage")
        return self.ORDER[index + 1]

    def transition(self, record: ResearchRecord, target: ResearchStage) -> ResearchRecord:
        expected = self.next_stage(record.stage)
        if target is not expected:
            raise ValueError(f"invalid transition: {record.stage} -> {target}; expected {expected}")
        return ResearchRecord(target, record.subject_id, record.evidence, record.notes)

    @staticmethod
    def is_authorized(record: ResearchRecord, governance_decision: Mapping[str, Any]) -> bool:
        # NEXENT never manufactures authority.
        return record.stage is ResearchStage.GOVERNANCE and governance_decision.get("approved") is True
