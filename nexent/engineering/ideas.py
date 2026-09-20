from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class EngineeringHypothesis:
    idea_id: str
    claim: str
    variables: tuple[str, ...]
    equations: tuple[str, ...] = ()
    constraints: Mapping[str, Any] = field(default_factory=dict)
    falsifiers: tuple[str, ...] = ()
    def __post_init__(self):
        if not self.idea_id or not self.claim: raise ValueError("idea_id and claim are required")
        if not self.falsifiers: raise ValueError("at least one falsifier/test condition is required")
    def engineering_path(self):
        return ("HYPOTHESIS","FORMALIZE","BOUND","SIMULATE","PROTOTYPE","MEASURE","FALSIFY_OR_SUPPORT","VERIFY","DEPLOY")
