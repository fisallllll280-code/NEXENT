from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from .kernel import NexentKernel
from .engineering import EngineeringRuntime, EngineeringTask, MultiMindCoordinator, NEXENTEngineeringOntology, ContradictionEngine, SystemContract, Artifact
from .agents.registry import AgentRegistry
from .portfolio import Portfolio
from .physics import PhysicsEngine
from .van import VANDesign
from .canonical import Nexus, SystemGenome, NEXENTUIR, InnovationRecord
from .languages import NativeLanguageRegistry, proposed_nxl_registry
from .archive import ArchiveReconstructor

@dataclass(frozen=True)
class SystemSnapshot:
    kernel: dict[str, Any]
    engineering: dict[str, Any]
    agents: tuple[str, ...]
    neo_records: int
    ledger_valid: bool

class NEXENTSystem:
    """Integrated composition root for NEXENT subsystems."""
    def __init__(self, ledger_path: str | None = None) -> None:
        self.kernel = NexentKernel(ledger_path)
        self.agents = AgentRegistry()
        self.coordinator = MultiMindCoordinator(self.agents)
        self.neo = NEXENTEngineeringOntology()
        self.contradictions = ContradictionEngine()
        self.engineering = EngineeringRuntime(self.kernel.ledger)
        self.physics = PhysicsEngine()
        self.portfolios: dict[str, Portfolio] = {}
        self.visuals: dict[str, VANDesign] = {}
        self.nexus = Nexus()
        self.languages: NativeLanguageRegistry = proposed_nxl_registry()
        self.archive = ArchiveReconstructor()
        self.innovations: dict[str, InnovationRecord] = {}

    def register_contract(self, contract: SystemContract) -> str:
        cid = self.engineering.system.register_contract(contract)
        self.neo.register_contract(contract)
        self.kernel.ledger.append("NEO_CONTRACT_REGISTERED", "SYSTEM", contract.system_id, {"canonical_id": cid})
        return cid

    def register_handler(self, contract_id: str, handler: Callable[[dict[str, Any]], Any]) -> None:
        self.engineering.system.register_handler(contract_id, handler)
        self.kernel.ledger.append("ENGINEERING_HANDLER_REGISTERED", "SYSTEM", contract_id, {})

    def attach_artifact(self, system_id: str, artifact: Artifact) -> None:
        self.engineering.attach_evidence(artifact, actor="SYSTEM")
        self.neo.bind_artifact(system_id, artifact)

    def route(self, task: EngineeringTask):
        result = self.coordinator.route(task)
        self.kernel.ledger.append("MULTIMIND_ROUTED", "SYSTEM", task.task_id, {
            "selected_agents": list(result.selected_agents),
            "unresolved": list(result.unresolved_capabilities),
            "executable": result.executable,
        })
        return result

    def run(self, contract_id: str, payload: dict[str, Any], *, authorized: bool = False, actor: str = "SYSTEM"):
        return self.engineering.run(contract_id, payload, authorized=authorized, actor=actor)

    def create_portfolio(self, portfolio_id: str, currency: str) -> Portfolio:
        if portfolio_id in self.portfolios:
            raise ValueError(f"portfolio already exists: {portfolio_id}")
        portfolio = Portfolio(portfolio_id, currency)
        self.portfolios[portfolio_id] = portfolio
        self.kernel.ledger.append("PORTFOLIO_CREATED", "SYSTEM", portfolio_id, {"currency": portfolio.currency})
        return portfolio

    def register_visual(self, design: VANDesign) -> None:
        if design.name in self.visuals:
            raise ValueError(f"visual design already exists: {design.name}")
        self.visuals[design.name] = design
        self.kernel.ledger.append("VAN_DESIGN_REGISTERED", "SYSTEM", design.name, design.to_dict())

    def register_innovation(self, innovation: InnovationRecord) -> str:
        if innovation.canonical_id in self.innovations:
            raise ValueError(f"innovation already exists: {innovation.canonical_id}")
        self.innovations[innovation.canonical_id] = innovation
        self.kernel.ledger.append("INNOVATION_REGISTERED", "SYSTEM", innovation.canonical_id, {"name": innovation.name, "status": innovation.status.value})
        return innovation.canonical_id

    def snapshot(self) -> SystemSnapshot:
        return SystemSnapshot(
            kernel=self.kernel.status(),
            engineering=self.engineering.system.manifest(),
            agents=tuple(a.agent_id for a in self.agents.all()),
            neo_records=len(self.neo.records),
            ledger_valid=self.kernel.ledger.verify(),
        )
