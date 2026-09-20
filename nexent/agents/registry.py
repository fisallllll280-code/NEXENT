from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

class AgentStatus(str, Enum):
    DESIGN = "DESIGN"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

@dataclass(frozen=True)
class AgentProfile:
    agent_id: str
    role: str
    mission: str
    capabilities: tuple[str, ...] = ()
    consumes: tuple[str, ...] = ()
    produces: tuple[str, ...] = ()
    requires_agents: tuple[str, ...] = ()
    status: AgentStatus = AgentStatus.DESIGN
    autonomy_level: str = "A0"

    def __post_init__(self) -> None:
        if not self.agent_id or not self.role or not self.mission:
            raise ValueError("agent_id, role, and mission are required")
        if self.autonomy_level not in {"A0", "A1", "A2", "A3", "A4", "A5"}:
            raise ValueError("invalid autonomy level")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("duplicate capabilities")

@dataclass
class AgentRegistry:
    _agents: dict[str, AgentProfile] = field(default_factory=dict)

    def register(self, agent: AgentProfile) -> AgentProfile:
        if agent.agent_id in self._agents:
            raise ValueError(f"agent already registered: {agent.agent_id}")
        self._agents[agent.agent_id] = agent
        return agent

    def get(self, agent_id: str) -> AgentProfile:
        return self._agents[agent_id]

    def all(self) -> tuple[AgentProfile, ...]:
        return tuple(self._agents[k] for k in sorted(self._agents))

    def by_capability(self, capability: str) -> tuple[AgentProfile, ...]:
        return tuple(a for a in self.all() if capability in a.capabilities)

    def validate_dependencies(self) -> tuple[str, ...]:
        errors: list[str] = []
        for agent in self.all():
            for dependency in agent.requires_agents:
                if dependency not in self._agents:
                    errors.append(f"{agent.agent_id}: missing dependency {dependency}")
        return tuple(errors)

    def require_capabilities(self, agent_ids: Iterable[str], capabilities: Iterable[str]) -> None:
        required = set(capabilities)
        for agent_id in agent_ids:
            agent = self.get(agent_id)
            missing = required.difference(agent.capabilities)
            if missing:
                raise PermissionError(f"{agent_id}: missing capabilities {sorted(missing)}")
