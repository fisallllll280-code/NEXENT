from __future__ import annotations
from dataclasses import dataclass, field
from .model import digest

@dataclass
class EvolutionProposal:
    id: str
    trigger: str
    hypothesis: str
    changes: list[str]
    status: str = "PROPOSED"
    evidence: list[str] = field(default_factory=list)

class EvolutionEngine:
    def propose(self, trigger: str, hypothesis: str, changes: list[str]) -> EvolutionProposal:
        pid="EP-"+digest({"trigger":trigger,"hypothesis":hypothesis,"changes":changes})[:20]
        return EvolutionProposal(pid,trigger,hypothesis,changes)
    def approve(self, proposal: EvolutionProposal) -> None:
        proposal.status="APPROVED"
    def deploy(self, proposal: EvolutionProposal) -> None:
        if proposal.status != "APPROVED":
            raise PermissionError("evolution requires explicit approval")
        proposal.status="DEPLOYED"
