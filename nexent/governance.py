from __future__ import annotations
from dataclasses import dataclass
from .model import Intent, Capability

@dataclass(frozen=True)
class Decision:
    allowed: bool
    code: str
    reason: str

class Constitution:
    def __init__(self) -> None:
        self.denied_capabilities: set[str] = set()
        self.required_fields: dict[str, set[str]] = {}

    def require(self, capability: str, *fields: str) -> None:
        self.required_fields[capability] = set(fields)

    def deny(self, capability: str) -> None:
        self.denied_capabilities.add(capability)

    def evaluate(self, intent: Intent, capability: Capability) -> Decision:
        if capability.id in self.denied_capabilities:
            return Decision(False, "CAPABILITY_DENIED", capability.id)
        missing = sorted(self.required_fields.get(capability.id, set()) - set(intent.payload))
        if missing:
            return Decision(False, "MISSING_INPUT", ",".join(missing))
        return Decision(True, "ALLOW", "constitutional checks passed")
