from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from .core import EngineeringSystem, SystemContract, Artifact
from ..ledger import EventLedger

@dataclass(frozen=True)
class RuntimeResult:
    execution_id: str
    status: str
    output: Any = None
    reason: str | None = None

class EngineeringRuntime:
    def __init__(self, engine=None, ledger=None):
        self.engine = engine or EngineeringSystem()
        self.ledger = ledger or EventLedger()

    def deploy(self, contract: SystemContract, handler: Callable[[dict[str, Any]], Any], *, actor="ENGINEERING_RUNTIME"):
        cid = self.engine.register_contract(contract)
        self.engine.register_handler(cid, handler)
        self.ledger.append("ENGINEERING_DEPLOYED", actor, cid, {"canonical_id": cid, "system_id": contract.system_id})
        return cid

    def attach_evidence(self, artifact: Artifact, *, actor="VERIFIER"):
        self.engine.add_artifact(artifact)
        self.ledger.append("ENGINEERING_EVIDENCE_ATTACHED", actor, artifact.artifact_id, {"status": artifact.status.value, "content_hash": artifact.content_hash})

    def run(self, contract_id, payload, *, authorized=False, actor="EXECUTOR"):
        execution_id=self.ledger.append("ENGINEERING_EXECUTION_REQUESTED", actor, contract_id, {"authorized":authorized}).id
        plan=self.engine.plan(contract_id)
        self.ledger.append("ENGINEERING_PLAN", actor, contract_id, {"executable":plan.executable,"steps":plan.steps})
        try:
            output=self.engine.execute(contract_id,payload,authorized=authorized)
        except Exception as exc:
            self.ledger.append("ENGINEERING_EXECUTION_REJECTED",actor,contract_id,{"execution_id":execution_id,"error":type(exc).__name__,"reason":str(exc)})
            return RuntimeResult(execution_id,"REJECTED",reason=str(exc))
        self.ledger.append("ENGINEERING_EXECUTION_COMPLETED",actor,contract_id,{"execution_id":execution_id,"output":output})
        return RuntimeResult(execution_id,"COMPLETED",output=output)
