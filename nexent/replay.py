from __future__ import annotations
from .ledger import EventLedger

class ReplayEngine:
    def verify(self, ledger: EventLedger) -> dict:
        valid=ledger.verify()
        return {"valid":valid,"event_count":len(ledger.events),
                "head":ledger.events[-1].hash if ledger.events else "GENESIS"}
