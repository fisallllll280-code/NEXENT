from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any

class ConflictKind(str, Enum):
    SEMANTIC = "SEMANTIC"
    CONSTRAINT = "CONSTRAINT"
    EVIDENCE = "EVIDENCE"
    DEPENDENCY = "DEPENDENCY"

@dataclass(frozen=True)
class Conflict:
    left_id: str
    right_id: str
    kind: ConflictKind
    reason: str
    severity: str = "REVIEW"

class ContradictionEngine:
    def compare(self, left: Any, right: Any) -> tuple[Conflict, ...]:
        conflicts: list[Conflict] = []
        if getattr(left, "claim", None) and getattr(right, "claim", None) and left.claim != right.claim:
            conflicts.append(Conflict(left.artifact_id, right.artifact_id, ConflictKind.SEMANTIC, "claims differ"))
        lc, rc = getattr(left, "content", None), getattr(right, "content", None)
        if isinstance(lc, dict) and isinstance(rc, dict):
            for key in sorted(set(lc) & set(rc)):
                if lc[key] != rc[key]:
                    conflicts.append(Conflict(left.artifact_id, right.artifact_id, ConflictKind.CONSTRAINT, f"content conflict at {key}"))
        le, re = set(getattr(left, "evidence", ())), set(getattr(right, "evidence", ()))
        if le and re and le.isdisjoint(re):
            conflicts.append(Conflict(left.artifact_id, right.artifact_id, ConflictKind.EVIDENCE, "evidence sets are disjoint"))
        ld, rd = set(getattr(left, "provenance", ())), set(getattr(right, "provenance", ()))
        if ld and rd and ld.isdisjoint(rd):
            conflicts.append(Conflict(left.artifact_id, right.artifact_id, ConflictKind.DEPENDENCY, "provenance sets are disjoint"))
        return tuple(conflicts)
