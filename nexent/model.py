from __future__ import annotations
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import Any, Callable
import hashlib, json

def canonical(value: Any) -> str:
    if is_dataclass(value):
        value = asdict(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()

@dataclass(frozen=True)
class EntitySpec:
    id: str
    kind: str
    domain: str
    provides: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Capability:
    id: str
    version: str
    description: str
    handler: Callable[[dict[str, Any]], Any]
    constraints: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Intent:
    id: str
    actor: str
    objective: str
    capability: str
    payload: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionResult:
    execution_id: str
    status: str
    output: Any = None
    evidence_id: str | None = None
    event_ids: list[str] = field(default_factory=list)
    reason: str | None = None
    def public(self) -> dict[str, Any]:
        return asdict(self)
