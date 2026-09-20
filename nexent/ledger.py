from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import hashlib, json, uuid
from pathlib import Path
from .clock import LogicalClock

def _canon(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)

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
    def __init__(self, path: str | Path | None = None, *, load: bool = True) -> None:
        self.clock = LogicalClock()
        self.events: list[Event] = []
        self.path = Path(path) if path is not None else None
        if self.path is not None and load and self.path.exists():
            self._load()

    def append(self, event_type: str, actor: str, entity: str, payload: dict[str, Any]) -> Event:
        seq = len(self.events) + 1
        self.clock.tick()
        previous = self.events[-1].hash if self.events else "GENESIS"
        event_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"nexent:event:{seq}:{event_type}:{entity}"))
        body = {"id":event_id,"seq":seq,"type":event_type,"actor":actor,"entity":entity,
                "payload":payload,"previous_hash":previous}
        event_hash = hashlib.sha256(_canon(body).encode()).hexdigest()
        event = Event(hash=event_hash, **body)
        self.events.append(event)
        self._persist(event)
        return event

    def _persist(self, event: Event) -> None:
        if self.path is None: return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(_canon(asdict(event)) + "\n")

    def _load(self) -> None:
        loaded: list[Event] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                data=json.loads(line)
                loaded.append(Event(**data))
        self.events=loaded
        if not self.verify():
            raise ValueError("ledger persistence failed integrity verification")
        for _ in loaded: self.clock.tick()

    def verify(self) -> bool:
        previous = "GENESIS"
        expected_seq = 1
        for event in self.events:
            body = {"id":event.id,"seq":event.seq,"type":event.type,"actor":event.actor,
                    "entity":event.entity,"payload":event.payload,"previous_hash":event.previous_hash}
            if event.seq != expected_seq or event.previous_hash != previous:
                return False
            if hashlib.sha256(_canon(body).encode()).hexdigest() != event.hash:
                return False
            previous = event.hash
            expected_seq += 1
        return True

    def export(self) -> list[dict[str, Any]]:
        return [asdict(e) for e in self.events]
