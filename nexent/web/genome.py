from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..model import digest


@dataclass
class WebObject:
    object_id: str
    object_type: str
    name: str
    meaning: str
    state: dict[str, Any] = field(default_factory=dict)
    capabilities: tuple[str, ...] = ()
    properties: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        object_type: str,
        name: str,
        meaning: str,
        *,
        state: dict[str, Any] | None = None,
        capabilities: tuple[str, ...] = (),
        properties: dict[str, Any] | None = None,
        provenance: dict[str, Any] | None = None,
    ) -> "WebObject":
        seed = {
            "object_type": object_type,
            "name": name,
            "meaning": meaning,
            "state": state or {},
            "capabilities": capabilities,
            "properties": properties or {},
            "provenance": provenance or {},
        }
        return cls(
            object_id="WO-" + digest(seed)[:24],
            object_type=object_type,
            name=name,
            meaning=meaning,
            state=dict(state or {}),
            capabilities=tuple(capabilities),
            properties=dict(properties or {}),
            provenance=dict(provenance or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "object_type": self.object_type,
            "name": self.name,
            "meaning": self.meaning,
            "state": dict(self.state),
            "capabilities": list(self.capabilities),
            "properties": dict(self.properties),
            "provenance": dict(self.provenance),
        }


@dataclass(frozen=True)
class WebAction:
    action_id: str
    name: str
    description: str
    capability: str
    risk: str = "low"
    requires_confirmation: bool = False

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        capability: str,
        *,
        risk: str = "low",
        requires_confirmation: bool = False,
    ) -> "WebAction":
        seed = {
            "name": name,
            "description": description,
            "capability": capability,
            "risk": risk,
            "requires_confirmation": requires_confirmation,
        }
        return cls(
            action_id="WA-" + digest(seed)[:20],
            name=name,
            description=description,
            capability=capability,
            risk=risk,
            requires_confirmation=requires_confirmation,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "name": self.name,
            "description": self.description,
            "capability": self.capability,
            "risk": self.risk,
            "requires_confirmation": self.requires_confirmation,
        }


@dataclass
class WebWorld:
    world_id: str
    intent_id: str
    objective: str
    actor: str
    objects: dict[str, WebObject] = field(default_factory=dict)
    relations: list[dict[str, Any]] = field(default_factory=list)
    actions: dict[str, WebAction] = field(default_factory=dict)
    memory: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, *, intent_id: str, objective: str, actor: str, context: dict[str, Any]) -> "WebWorld":
        seed = {
            "intent_id": intent_id,
            "objective": objective,
            "actor": actor,
            "context": context,
        }
        return cls(
            world_id="WW-" + digest(seed)[:24],
            intent_id=intent_id,
            objective=objective,
            actor=actor,
            metadata={"context": dict(context), "model": "nexent-web-genome-v1"},
        )

    def add_object(self, obj: WebObject) -> None:
        self.objects[obj.object_id] = obj

    def add_relation(self, source: str, target: str, relation: str, **conditions: Any) -> None:
        self.relations.append({
            "source": source,
            "target": target,
            "relation": relation,
            "conditions": conditions,
        })

    def add_action(self, action: WebAction) -> None:
        self.actions[action.action_id] = action

    def remember(self, entry: dict[str, Any]) -> None:
        self.memory.append(dict(entry))

    def to_dict(self) -> dict[str, Any]:
        return {
            "world_id": self.world_id,
            "intent_id": self.intent_id,
            "objective": self.objective,
            "actor": self.actor,
            "objects": [obj.to_dict() for obj in self.objects.values()],
            "relations": list(self.relations),
            "actions": [action.to_dict() for action in self.actions.values()],
            "memory": list(self.memory),
            "metadata": dict(self.metadata),
        }
