from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from ..agents.registry import AgentProfile, AgentRegistry

@dataclass(frozen=True)
class EngineeringTask:
    task_id: str
    required_capabilities: tuple[str, ...] = ()
    required_outputs: tuple[str, ...] = ()
    authorized_agents: tuple[str, ...] = ()

@dataclass(frozen=True)
class CoordinationResult:
    task_id: str
    selected_agents: tuple[str, ...]
    unresolved_capabilities: tuple[str, ...]
    dependency_errors: tuple[str, ...]
    executable: bool

class MultiMindCoordinator:
    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self.registry = registry or AgentRegistry()

    def route(self, task: EngineeringTask) -> CoordinationResult:
        dependency_errors = self.registry.validate_dependencies()
        candidates: list[AgentProfile] = []
        for capability in task.required_capabilities:
            matches = self.registry.by_capability(capability)
            if task.authorized_agents:
                matches = tuple(a for a in matches if a.agent_id in task.authorized_agents)
            if matches:
                candidates.append(matches[0])
        selected = {a.agent_id for a in candidates}
        unresolved = tuple(sorted(set(task.required_capabilities) - {
            capability for capability in task.required_capabilities
            if any(capability in a.capabilities for a in candidates)
        }))
        return CoordinationResult(task.task_id, tuple(sorted(selected)), unresolved,
                                   tuple(dependency_errors), not unresolved and not dependency_errors)

    def require_executable(self, task: EngineeringTask) -> CoordinationResult:
        result = self.route(task)
        if not result.executable:
            raise PermissionError(
                f"coordination blocked: unresolved={result.unresolved_capabilities}, "
                f"dependencies={result.dependency_errors}"
            )
        return result
