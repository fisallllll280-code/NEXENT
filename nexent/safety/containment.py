"""Fail-closed containment primitives for NEXENT.

This layer is intentionally independent of LLMs and application policy.
It computes whether a proposed transition stays inside declared safety
boundaries and produces a deterministic decision artifact. It does not
perform deployment or grant authority.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from ..model import digest

class SafetyState(str, Enum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    QUARANTINED = "quarantined"
    HALTED = "halted"

class FailureMode(str, Enum):
    UNKNOWN_DEPENDENCY = "unknown_dependency"
    BOUNDARY_BREACH = "boundary_breach"
    INVARIANT_RISK = "invariant_risk"
    UNVERIFIED_CHANGE = "unverified_change"

@dataclass(frozen=True)
class Boundary:
    source: str
    allowed_targets: tuple[str, ...] = ()
    required_invariants: tuple[str, ...] = ()

@dataclass(frozen=True)
class ContainmentDecision:
    allowed: bool
    state: SafetyState
    failures: tuple[FailureMode, ...]
    affected: tuple[str, ...]
    digest: str

class ContainmentEngine:
    """Evaluate transitions with fail-closed semantics."""

    def __init__(self, boundaries: tuple[Boundary, ...] | list[Boundary]):
        self.boundaries = {b.source: b for b in boundaries}

    def evaluate(
        self,
        source: str,
        targets: tuple[str, ...] | list[str],
        supplied_invariants: tuple[str, ...] | list[str],
        verified: bool,
    ) -> ContainmentDecision:
        target_set = tuple(sorted(set(targets)))
        invariant_set = set(supplied_invariants)
        failures: list[FailureMode] = []
        boundary = self.boundaries.get(source)
        if boundary is None:
            failures.append(FailureMode.UNKNOWN_DEPENDENCY)
        else:
            allowed = set(boundary.allowed_targets)
            if any(t not in allowed for t in target_set):
                failures.append(FailureMode.BOUNDARY_BREACH)
            if any(i not in invariant_set for i in boundary.required_invariants):
                failures.append(FailureMode.INVARIANT_RISK)
        if not verified:
            failures.append(FailureMode.UNVERIFIED_CHANGE)
        ordered = tuple(dict.fromkeys(failures))
        allowed = not ordered
        state = SafetyState.NORMAL if allowed else SafetyState.QUARANTINED
        payload = {
            "source": source,
            "targets": target_set,
            "invariants": tuple(sorted(invariant_set)),
            "verified": verified,
            "failures": tuple(f.value for f in ordered),
            "state": state.value,
        }
        return ContainmentDecision(
            allowed=allowed,
            state=state,
            failures=ordered,
            affected=target_set,
            digest="SC-" + digest(payload)[:20],
        )

__all__ = ["Boundary", "ContainmentDecision", "ContainmentEngine", "FailureMode", "SafetyState"]
