from __future__ import annotations

import uuid
from typing import Any

from ..kernel import NexentKernel
from ..model import Capability, EntitySpec, Intent
from .catalog import catalog
from .genome import WebAction, WebObject, WebWorld


class WebRuntime:
    """Governed runtime for NEXENT's intent-first web.

    This is a deterministic foundation. An external AI/LLM can be attached
    through the capability boundary, but the runtime never treats model output
    as authority by default.
    """

    def __init__(self, ledger_path: str | None = None) -> None:
        self.kernel = NexentKernel(ledger_path)
        self.worlds: dict[str, WebWorld] = {}
        self.intent_to_world: dict[str, str] = {}
        self._register_core()
        self.ai_adapter: Any | None = None

    def _register_core(self) -> None:
        self.kernel.register_entity(EntitySpec(
            "nexent.web",
            "web-runtime",
            "web",
            ("intent", "world", "action", "memory", "evidence"),
        ))
        self.kernel.register_capability(Capability(
            "web.world.create",
            "1.0",
            "Create a deterministic web world from an intent.",
            self._handle_world_create,
        ))
        self.kernel.register_capability(Capability(
            "web.world.inspect",
            "1.0",
            "Inspect a web world.",
            self._handle_world_inspect,
        ))
        self.kernel.register_capability(Capability(
            "web.world.remember",
            "1.0",
            "Store a structured memory entry in a web world.",
            self._handle_world_remember,
        ))
        self.kernel.register_capability(Capability(
            "web.world.derive",
            "1.0",
            "Derive a semantic object from world context without side effects.",
            self._handle_world_derive,
        ))
        self.kernel.constitution.require("web.world.create", "objective")
        self.kernel.constitution.require("web.world.inspect", "world_id")
        self.kernel.constitution.require("web.world.remember", "world_id", "content")
        self.kernel.constitution.require("web.world.derive", "world_id", "content")

    def register_ai_adapter(self, adapter: Any) -> None:
        """Register an AI adapter; it remains subordinate to capabilities/governance."""
        if not callable(getattr(adapter, "plan", None)):
            raise TypeError("AI adapter must expose callable plan(context)")
        self.ai_adapter = adapter
        self.kernel.ledger.append("AI_ADAPTER_REGISTERED", "SYSTEM", "nexent.web", {
            "adapter": type(adapter).__name__,
        })

    @property
    def capabilities(self) -> dict[str, Capability]:
        return dict(self.kernel.capabilities)

    def start_intent(
        self,
        objective: str,
        *,
        actor: str = "WEB_USER",
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        objective = objective.strip()
        if not objective:
            raise ValueError("objective must not be empty")
        context = dict(context or {})
        intent_id = "INT-" + uuid.uuid5(
            uuid.NAMESPACE_URL,
            "nexent:web:intent:" + objective + ":" + repr(sorted(context.items())),
        ).hex[:24]
        intent = Intent(
            id=intent_id,
            actor=actor,
            objective=objective,
            capability="web.world.create",
            payload={"objective": objective, "context": context, "actor": actor, "intent_id": intent_id},
        )
        result = self.kernel.execute(intent)
        return {
            "intent": {
                "id": intent.id,
                "actor": intent.actor,
                "objective": intent.objective,
                "context": context,
            },
            "result": result.public(),
            "world": self.worlds.get(result.output.get("world_id")) if result.status == "COMPLETED" else None,
        } | {
            "world": self.worlds[result.output["world_id"]].to_dict()
            if result.status == "COMPLETED" and result.output["world_id"] in self.worlds
            else None
        }

    def _handle_world_create(self, payload: dict[str, Any]) -> dict[str, Any]:
        objective = str(payload["objective"]).strip()
        context = dict(payload.get("context", {}))
        actor = str(payload.get("actor", "WEB_USER"))
        intent_id = str(payload.get("intent_id") or "INT-INTERNAL")

        world = WebWorld.create(
            intent_id=intent_id,
            objective=objective,
            actor=actor,
            context=context,
        )
        intent_obj = WebObject.create(
            "intent",
            "Active Intent",
            objective,
            state={"status": "active"},
            capabilities=("inspect", "remember", "derive"),
            properties={"intent_id": intent_id},
            provenance={"source": "nexent.intent"},
        )
        context_obj = WebObject.create(
            "context",
            "Intent Context",
            "Structured context carried by the intent.",
            state={"fields": sorted(context)},
            properties=context,
            provenance={"intent_id": intent_id},
        )
        knowledge_obj = WebObject.create(
            "knowledge-space",
            "Knowledge Space",
            "A semantic container for discoveries related to the intent.",
            capabilities=("inspect", "derive"),
            provenance={"world_id": world.world_id},
        )
        world.add_object(intent_obj)
        world.add_object(context_obj)
        world.add_object(knowledge_obj)
        world.add_relation(intent_obj.object_id, context_obj.object_id, "has-context")
        world.add_relation(intent_obj.object_id, knowledge_obj.object_id, "opens-knowledge-space")

        world.add_action(WebAction.create(
            "inspect",
            "Read the current world state.",
            "web.world.inspect",
        ))
        world.add_action(WebAction.create(
            "remember",
            "Add structured memory to the world.",
            "web.world.remember",
        ))
        world.add_action(WebAction.create(
            "derive",
            "Derive a new semantic object from supplied content.",
            "web.world.derive",
        ))

        self.worlds[world.world_id] = world
        self.intent_to_world[intent_id] = world.world_id
        self.kernel.ledger.append("WEB_WORLD_CREATED", actor, world.world_id, {
            "intent_id": intent_id,
            "object_count": len(world.objects),
            "action_count": len(world.actions),
        })
        return {"world_id": world.world_id, "intent_id": intent_id}

    def _handle_world_inspect(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.get_world(str(payload["world_id"]))

    def _handle_world_remember(self, payload: dict[str, Any]) -> dict[str, Any]:
        world = self._require_world(str(payload["world_id"]))
        entry = {
            "content": str(payload["content"]),
            "actor": str(payload.get("actor", "WEB_USER")),
            "kind": str(payload.get("kind", "episodic")),
            "intent_id": world.intent_id,
        }
        world.remember(entry)
        self.kernel.ledger.append("WEB_MEMORY_ADDED", entry["actor"], world.world_id, entry)
        return {"world_id": world.world_id, "memory_count": len(world.memory), "entry": entry}

    def _handle_world_derive(self, payload: dict[str, Any]) -> dict[str, Any]:
        world = self._require_world(str(payload["world_id"]))
        content = str(payload["content"]).strip()
        obj = WebObject.create(
            "derived-knowledge",
            "Derived Object",
            content,
            properties={"source_text": content},
            provenance={"world_id": world.world_id, "method": "deterministic-derivation"},
        )
        world.add_object(obj)
        world.add_relation(
            next(iter(world.objects)),
            obj.object_id,
            "derived",
        )
        self.kernel.ledger.append("WEB_OBJECT_DERIVED", str(payload.get("actor", "WEB_USER")), obj.object_id, {
            "world_id": world.world_id,
            "content_digest": obj.object_id,
        })
        return {"world_id": world.world_id, "object": obj.to_dict()}

    def execute_action(
        self,
        world_id: str,
        action_id: str,
        *,
        actor: str = "WEB_USER",
        input_data: dict[str, Any] | None = None,
        confirm: bool = False,
    ) -> dict[str, Any]:
        world = self._require_world(world_id)
        action = world.actions.get(action_id)
        if action is None:
            raise KeyError("unknown web action")
        if action.requires_confirmation and not confirm:
            raise PermissionError("action requires explicit confirmation")
        payload = dict(input_data or {})
        payload["world_id"] = world_id
        payload["actor"] = actor
        intent = Intent(
            id=f"{world.intent_id}:{action.action_id}",
            actor=actor,
            objective=action.description,
            capability=action.capability,
            payload=payload,
        )
        result = self.kernel.execute(intent)
        return {
            "action": action.to_dict(),
            "result": result.public(),
            "evidence": self.kernel.evidence[result.evidence_id].__dict__
            if result.evidence_id and result.evidence_id in self.kernel.evidence
            else None,
        }

    def remember(self, world_id: str, content: str, *, actor: str = "WEB_USER", kind: str = "episodic") -> dict[str, Any]:
        action = next(a for a in self.worlds[world_id].actions.values() if a.capability == "web.world.remember")
        return self.execute_action(
            world_id,
            action.action_id,
            actor=actor,
            input_data={"content": content, "kind": kind},
        )

    def derive(self, world_id: str, content: str, *, actor: str = "WEB_USER") -> dict[str, Any]:
        action = next(a for a in self.worlds[world_id].actions.values() if a.capability == "web.world.derive")
        return self.execute_action(
            world_id,
            action.action_id,
            actor=actor,
            input_data={"content": content},
        )

    def get_world(self, world_id: str) -> dict[str, Any]:
        return self._require_world(world_id).to_dict()

    def events(self, since: int = 0) -> list[dict[str, Any]]:
        if since < 0:
            raise ValueError("since must be non-negative")
        return [
            event.__dict__.copy()
            for event in self.kernel.ledger.events
            if event.seq > since
        ]

    def status(self) -> dict[str, Any]:
        return {
            **self.kernel.status(),
            "web_worlds": len(self.worlds),
            "intents": len(self.intent_to_world),
            "innovations": len(catalog()),
            "ai_adapter": type(self.ai_adapter).__name__ if self.ai_adapter else None,
        }

    def _require_world(self, world_id: str) -> WebWorld:
        try:
            return self.worlds[world_id]
        except KeyError as exc:
            raise KeyError("unknown world") from exc
