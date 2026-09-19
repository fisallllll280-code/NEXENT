from __future__ import annotations
from dataclasses import dataclass
from .model import Intent, digest

@dataclass(frozen=True)
class VIR:
    intent_id: str
    actor: str
    objective: str
    capability: str
    payload: dict
    constraints: dict
    fingerprint: str

class IRBuilder:
    def lower(self, intent: Intent) -> VIR:
        raw={"id":intent.id,"actor":intent.actor,"objective":intent.objective,
             "capability":intent.capability,"payload":intent.payload,"constraints":intent.constraints}
        return VIR(intent.id,intent.actor,intent.objective,intent.capability,
                   dict(intent.payload),dict(intent.constraints),digest(raw))
