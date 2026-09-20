from __future__ import annotations
import uuid
from .model import EntitySpec, Capability, Intent, ExecutionResult
from .ledger import EventLedger
from .graph import SystemGraph
from .governance import Constitution
from .proof import ProofEngine, Evidence
from .evolution import EvolutionEngine

class NexentKernel:
    def __init__(self, ledger_path: str | None = None) -> None:
        self.graph=SystemGraph()
        self.ledger=EventLedger(ledger_path)
        self.constitution=Constitution()
        self.proof=ProofEngine()
        self.evolution=EvolutionEngine()
        self.capabilities: dict[str, Capability] = {}
        self.evidence: dict[str, Evidence] = {}

    def register_entity(self, spec: EntitySpec) -> None:
        self.graph.register(spec)
        self.ledger.append("ENTITY_REGISTERED","SYSTEM",spec.id,{"kind":spec.kind,"domain":spec.domain})

    def register_capability(self, capability: Capability) -> None:
        if capability.id in self.capabilities: raise ValueError("duplicate capability")
        self.capabilities[capability.id]=capability
        self.ledger.append("CAPABILITY_REGISTERED","SYSTEM",capability.id,{"version":capability.version})

    def validate(self) -> list[str]:
        errors=self.graph.validate()
        self.ledger.append("GRAPH_VALIDATED","SYSTEM","graph",{"errors":errors})
        return errors

    def execute(self, intent: Intent) -> ExecutionResult:
        execution_id="EX-"+uuid.uuid4().hex[:20]
        trace=[]
        self.ledger.append("INTENT_ACCEPTED",intent.actor,intent.id,{"objective":intent.objective,"capability":intent.capability})
        graph_errors=self.graph.validate()
        if graph_errors:
            self.ledger.append("EXECUTION_REJECTED","SYSTEM",execution_id,{"reason":"INVALID_GRAPH","errors":graph_errors})
            return ExecutionResult(execution_id,"REJECTED",reason="INVALID_GRAPH")
        cap=self.capabilities.get(intent.capability)
        if not cap:
            self.ledger.append("EXECUTION_REJECTED","SYSTEM",execution_id,{"reason":"UNKNOWN_CAPABILITY"})
            return ExecutionResult(execution_id,"REJECTED",reason="UNKNOWN_CAPABILITY")
        decision=self.constitution.evaluate(intent,cap)
        self.ledger.append("POLICY_DECISION","SYSTEM",execution_id,{"allowed":decision.allowed,"code":decision.code})
        trace.append(decision.code)
        if not decision.allowed:
            self.ledger.append("EXECUTION_REJECTED","SYSTEM",execution_id,{"reason":decision.code})
            return ExecutionResult(execution_id,"REJECTED",reason=decision.reason)
        self.ledger.append("EXECUTION_STARTED",intent.actor,execution_id,{"capability":cap.id})
        trace.append("EXECUTION_STARTED")
        try:
            output=cap.handler(dict(intent.payload))
            self.ledger.append("EXECUTION_COMPLETED",intent.actor,execution_id,{"output":output})
            trace.append("EXECUTION_COMPLETED")
            ev=self.proof.build(execution_id,intent,output,self.ledger.events[-1].hash,cap.id,decision.code,trace)
            self.evidence[ev.id]=ev
            self.ledger.append("EVIDENCE_BOUND","SYSTEM",execution_id,{"evidence_id":ev.id,"output_hash":ev.output_hash})
            return ExecutionResult(execution_id,"COMPLETED",output,ev.id,[e.id for e in self.ledger.events])
        except Exception as exc:
            self.ledger.append("EXECUTION_FAILED",intent.actor,execution_id,{"error":type(exc).__name__,"message":str(exc)})
            return ExecutionResult(execution_id,"FAILED",reason=str(exc),event_ids=[e.id for e in self.ledger.events])

    def status(self) -> dict:
        return {"entities":len(self.graph.entities),"capabilities":len(self.capabilities),
                "events":len(self.ledger.events),"evidence":len(self.evidence),
                "ledger_valid":self.ledger.verify(),"graph_errors":self.graph.validate()}
