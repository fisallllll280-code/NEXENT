from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import hashlib, json, uuid
from .clock import LogicalClock

def _canon(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

@dataclass(frozen=True)
class Event:
    id: str
    seq: int
    type: str
    actor: str
    entity: str
    payload: dict[str, Any]
    previous_hash: str
    hash: str

class EventLedger:
    def __init__(self) -> None:
        self.clock = LogicalClock()
        self.events: list[Event] = []

    def append(self, event_type: str, actor: str, entity: str, payload: dict[str, Any]) -> Event:
        seq = self.clock.tick()
        previous = self.events[-1].hash if self.events else "GENESIS"
        event_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"nexent:event:{seq}:{event_type}:{entity}"))
        body = {"id":event_id,"seq":seq,"type":event_type,"actor":actor,"entity":entity,
                "payload":payload,"previous_hash":previous}
        event_hash = hashlib.sha256(_canon(body).encode()).hexdigest()
        event = Event(hash=event_hash, **body)
        self.events.append(event)
        return event

    def verify(self) -> bool:
        previous = "GENESIS"
        for event in self.events:
            body = {"id":event.id,"seq":event.seq,"type":event.type,"actor":event.actor,
                    "entity":event.entity,"payload":event.payload,"previous_hash":event.previous_hash}
            if event.previous_hash != previous:
                return False
            if hashlib.sha256(_canon(body).encode()).hexdigest() != event.hash:
                return False
            previous = event.hash
        return True

    def export(self) -> list[dict[str, Any]]:
        return [asdict(e) for e in self.events]
