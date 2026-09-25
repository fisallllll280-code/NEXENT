from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .model_fabric import ModelFabric, ModelReply


class MindRole(str, Enum):
    CAUSAL = "causal"
    SYSTEM = "system"
    RISK = "risk"
    SECURITY = "security"
    ECONOMIC = "economic"
    DOMAIN = "domain"
    ADVERSARIAL = "adversarial"
    VERIFICATION = "verification"
    SYNTHESIS = "synthesis"


ROLE_INSTRUCTIONS = {
    MindRole.CAUSAL.value: "Trace causes, mechanisms, dependencies, feedback loops, and counterfactual consequences. Separate observed facts from assumptions.",
    MindRole.SYSTEM.value: "Decompose the problem as a system: components, interfaces, states, events, capabilities, constraints, resources, and lifecycle.",
    MindRole.RISK.value: "Search for failure modes, tail risks, operational hazards, uncertainty, hidden dependencies, and blast radius.",
    MindRole.SECURITY.value: "Model authority, trust boundaries, provenance, attack surfaces, abuse paths, privacy, integrity, and containment.",
    MindRole.ECONOMIC.value: "Analyze resource use, incentives, cost surfaces, scalability, opportunity costs, and value creation without inventing numbers.",
    MindRole.DOMAIN.value: "Act as a domain engineering specialist. Identify scientific or technical principles, constraints, standards, and missing expertise.",
    MindRole.ADVERSARIAL.value: "Try to break the candidate. Produce the strongest contradiction, edge case, adversarial condition, or alternative explanation.",
    MindRole.VERIFICATION.value: "Turn claims into testable predicates, invariants, evidence requirements, reproducibility checks, and proof obligations.",
    MindRole.SYNTHESIS.value: "Synthesize competing views into a candidate architecture. Preserve disagreements and uncertainty instead of hiding them.",
}


@dataclass(frozen=True)
class CouncilResult:
    problem: str
    replies: tuple[ModelReply, ...]
    synthesis: ModelReply | None
    roles: tuple[str, ...]

    def public(self) -> dict:
        return {
            "problem": self.problem,
            "roles": list(self.roles),
            "minds": [reply.public() for reply in self.replies],
            "synthesis": self.synthesis.public() if self.synthesis else None,
        }


class MultiMindCouncil:
    """Runs explicit, role-separated reasoning passes and one synthesis pass."""

    def __init__(self, fabric: ModelFabric | None = None, max_workers: int = 8) -> None:
        self.fabric = fabric or ModelFabric()
        self.max_workers = max_workers

    def deliberate(self, problem: str, roles: Iterable[str] | None = None) -> CouncilResult:
        selected = tuple(dict.fromkeys(roles or ROLE_INSTRUCTIONS.keys()))
        invalid = [role for role in selected if role not in ROLE_INSTRUCTIONS]
        if invalid:
            raise ValueError(f"unknown mind roles: {invalid}")
        if not problem.strip():
            raise ValueError("problem cannot be empty")

        replies: dict[str, ModelReply] = {}

        def run(role: str) -> tuple[str, ModelReply]:
            reply = self.fabric.complete(
                role=role,
                instructions=ROLE_INSTRUCTIONS[role],
                prompt=problem,
            )
            return role, reply

        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(selected) or 1)) as pool:
            futures = [pool.submit(run, role) for role in selected]
            for future in as_completed(futures):
                role, reply = future.result()
                replies[role] = reply

        ordered = tuple(replies[role] for role in selected)
        usable = [reply for reply in ordered if reply.status == "COMPLETED" and reply.text.strip()]

        synthesis: ModelReply | None = None
        if usable:
            dossier = "\n\n".join(
                f"[{reply.role.upper()}]\n{reply.text}" for reply in usable
            )
            synthesis = self.fabric.complete(
                role=MindRole.SYNTHESIS.value,
                instructions=ROLE_INSTRUCTIONS[MindRole.SYNTHESIS.value],
                prompt=f"Problem:\n{problem}\n\nIndependent reasoning dossier:\n{dossier}",
            )

        return CouncilResult(problem, ordered, synthesis, selected)
