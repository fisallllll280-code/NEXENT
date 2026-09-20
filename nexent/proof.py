from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .model import digest

@dataclass(frozen=True)
class Evidence:
    id: str
    execution_id: str
    input_hash: str
    output_hash: str
    ledger_head: str
    capability: str
    policy_code: str
    trace: tuple[str, ...]
    def verify_shape(self) -> bool:
        return all((self.id,self.execution_id,self.input_hash,self.output_hash,self.capability,self.policy_code))

class ProofEngine:
    def build(self, execution_id: str, intent: Any, output: Any, ledger_head: str,
              capability: str, policy_code: str, trace: list[str]) -> Evidence:
        return Evidence("EV-"+digest({"execution":execution_id,"out":output})[:20],execution_id,
                         digest(intent),digest(output),ledger_head,capability,policy_code,tuple(trace))

    def verify(self, evidence: Evidence, intent: Any, output: Any, ledger_head: str | None = None) -> bool:
        if not evidence.verify_shape(): return False
        if evidence.input_hash != digest(intent) or evidence.output_hash != digest(output): return False
        return ledger_head is None or evidence.ledger_head == ledger_head

    def verify_invariants(self, state: dict[str, Any], invariants: tuple[str, ...]) -> tuple[str, ...]:
        failures=[]
        for invariant in invariants:
            if invariant.startswith("field:") and "=" in invariant:
                field, expected=invariant[6:].split("=",1)
                if str(state.get(field)) != expected: failures.append(invariant)
            elif invariant not in state.get("_verified_invariants", ()):
                failures.append(invariant)
        return tuple(failures)
