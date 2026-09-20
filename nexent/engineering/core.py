from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping
import hashlib, json

def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()

class VerificationStatus(str, Enum):
    ASSERTED="ASSERTED"; DESIGNED="DESIGNED"; IMPLEMENTED="IMPLEMENTED"; TESTED="TESTED"; VERIFIED="VERIFIED"; APPROVED="APPROVED"

@dataclass(frozen=True)
class SystemContract:
    system_id: str
    name: str
    purpose: str
    inputs: tuple[str,...]=()
    outputs: tuple[str,...]=()
    constraints: Mapping[str,Any]=field(default_factory=dict)
    assumptions: tuple[str,...]=()
    dependencies: tuple[str,...]=()
    invariants: tuple[str,...]=()
    def __post_init__(self):
        if not self.system_id or not self.name or not self.purpose: raise ValueError("system_id, name, and purpose are required")
    def canonical(self):
        return {"system_id":self.system_id,"name":self.name,"purpose":self.purpose,"inputs":list(self.inputs),"outputs":list(self.outputs),"constraints":dict(self.constraints),"assumptions":list(self.assumptions),"dependencies":list(self.dependencies),"invariants":list(self.invariants)}
    @property
    def canonical_id(self): return "CID-"+_digest(self.canonical())[:32]

@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    kind: str
    claim: str
    content: Any
    assumptions: tuple[str,...]=()
    evidence: tuple[str,...]=()
    provenance: tuple[str,...]=()
    status: VerificationStatus=VerificationStatus.DESIGNED
    @property
    def content_hash(self): return _digest(self.content)
    def proof_ready(self): return bool(self.claim and self.evidence and self.provenance)

@dataclass(frozen=True)
class ExecutionPlan:
    contract_id: str
    steps: tuple[str,...]
    artifacts: tuple[str,...]
    executable: bool

class EngineeringSystem:
    def __init__(self):
        self.contracts={}; self.artifacts={}; self.handlers={}
    def register_contract(self, contract):
        cid=contract.canonical_id
        if cid in self.contracts: raise ValueError(f"duplicate canonical contract: {cid}")
        self.contracts[cid]=contract; return cid
    def register_handler(self, contract_id: str, handler: Callable[[dict[str,Any]],Any]):
        if contract_id not in self.contracts: raise KeyError(contract_id)
        self.handlers[contract_id]=handler
    def add_artifact(self, artifact):
        if artifact.artifact_id in self.artifacts: raise ValueError(f"duplicate artifact: {artifact.artifact_id}")
        self.artifacts[artifact.artifact_id]=artifact
    def plan(self, contract_id):
        contract=self.contracts[contract_id]
        handler_ready=contract_id in self.handlers
        evidence_ready=any(a.proof_ready() and a.status in {VerificationStatus.TESTED,VerificationStatus.VERIFIED,VerificationStatus.APPROVED} for a in self.artifacts.values())
        return ExecutionPlan(contract_id,("VALIDATE_CONTRACT","RESOLVE_DEPENDENCIES","CHECK_EVIDENCE","AUTHORIZE","EXECUTE","RECORD"),tuple(sorted(self.artifacts)),handler_ready and evidence_ready)
    def execute(self, contract_id, payload, *, authorized=False):
        plan=self.plan(contract_id)
        if not plan.executable: raise PermissionError("execution blocked: implementation/evidence prerequisites are incomplete")
        if not authorized: raise PermissionError("execution requires explicit authorization")
        contract=self.contracts[contract_id]
        missing=[name for name in contract.inputs if name not in payload]
        if missing: raise ValueError(f"missing required inputs: {missing}")
        return self.handlers[contract_id](dict(payload))
    def manifest(self):
        return {"contracts":[{**c.canonical(),"canonical_id":cid} for cid,c in sorted(self.contracts.items())],"artifacts":[{"artifact_id":a.artifact_id,"kind":a.kind,"content_hash":a.content_hash,"status":a.status.value,"proof_ready":a.proof_ready()} for a in sorted(self.artifacts.values(),key=lambda x:x.artifact_id)]}
