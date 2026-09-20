from __future__ import annotations
from typing import Callable, Any
from .ledger import EventLedger

class ReplayEngine:
    def verify(self, ledger: EventLedger) -> dict:
        valid=ledger.verify()
        return {"valid":valid,"event_count":len(ledger.events),
                "head":ledger.events[-1].hash if ledger.events else "GENESIS"}

    def replay(self, ledger: EventLedger, reducer: Callable[[Any, dict], Any], initial: Any) -> Any:
        if not ledger.verify():
            raise ValueError("cannot replay an invalid ledger")
        state=initial
        for event in ledger.events:
            state=reducer(state,event.__dict__.copy())
        return state

    def entity_events(self, ledger: EventLedger, entity: str) -> tuple:
        if not ledger.verify():
            raise ValueError("cannot query an invalid ledger")
        return tuple(e for e in ledger.events if e.entity == entity)
