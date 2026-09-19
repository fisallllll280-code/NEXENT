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
