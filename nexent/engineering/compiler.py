from __future__ import annotations
from dataclasses import dataclass
import json
from .core import SystemContract
from ..model import digest

@dataclass(frozen=True)
class CompiledArtifact:
    contract_id: str
    language: str
    ast: dict
    ir: dict
    source: str
    fingerprint: str

class EngineeringCompiler:
    """Deterministic contract -> AST -> IR -> source compiler; it never delegates compilation to an LLM."""
    def compile(self, contract: SystemContract, language: str = "nexent-ir") -> CompiledArtifact:
        ast={"node":"System","id":contract.system_id,"name":contract.name,
             "purpose":contract.purpose,"inputs":list(contract.inputs),
             "outputs":list(contract.outputs),"constraints":dict(contract.constraints),
             "invariants":list(contract.invariants)}
        ir={"op":"SYSTEM","contract_id":contract.canonical_id,
            "inputs":list(contract.inputs),"outputs":list(contract.outputs),
            "constraints":dict(contract.constraints),"invariants":list(contract.invariants)}
        source=json.dumps(ir, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return CompiledArtifact(contract.canonical_id,language,ast,ir,source,digest({"ast":ast,"ir":ir,"language":language}))
