from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class WebInnovation:
    innovation_id: str
    name: str
    purpose: str
    implementation: tuple[str, ...]
    verification: tuple[str, ...]
    status: str = "IMPLEMENTED_FOUNDATION"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


WEB_INNOVATIONS = (
    WebInnovation(
        "WEB-001",
        "Intent Internet",
        "Make intent the primary navigation unit instead of pages and clicks.",
        ("WebRuntime.start_intent", "POST /api/intent"),
        ("test_intent_creates_world",),
    ),
    WebInnovation(
        "WEB-002",
        "Web World",
        "Materialize a live task-specific world from an intent.",
        ("WebWorld", "WebRuntime.get_world"),
        ("test_world_is_deterministic",),
    ),
    WebInnovation(
        "WEB-003",
        "Web Object Model",
        "Represent web entities as semantic, stateful, capability-bearing objects.",
        ("WebObject",),
        ("test_world_contains_web_objects",),
    ),
    WebInnovation(
        "WEB-004",
        "Intent Continuity",
        "Carry task context through the lifecycle of a world.",
        ("WebWorld.metadata.context", "WebWorld.memory"),
        ("test_intent_context_is_preserved",),
    ),
    WebInnovation(
        "WEB-005",
        "Executable Web",
        "Expose governed actions as explicit capabilities rather than opaque clicks.",
        ("WebAction", "WebRuntime.execute_action"),
        ("test_action_produces_evidence",),
    ),
    WebInnovation(
        "WEB-006",
        "Evidence Web",
        "Bind meaningful web actions to the NEXENT event ledger and proof layer.",
        ("NexentKernel.execute", "Evidence", "EventLedger"),
        ("test_action_produces_evidence",),
    ),
    WebInnovation(
        "WEB-007",
        "World Memory",
        "Retain structured task memory so the next interaction does not start from zero.",
        ("WebWorld.memory", "WebRuntime.remember"),
        ("test_memory_round_trip",),
    ),
    WebInnovation(
        "WEB-008",
        "Generative Interface",
        "Generate the workspace from the active intent and its world state.",
        ("web/static/index.html", "web/static/app.js"),
        ("test_index_is_served",),
    ),
    WebInnovation(
        "WEB-009",
        "Web Evolution",
        "Keep world state and action history observable for controlled evolution.",
        ("GET /api/events", "WebRuntime.events"),
        ("test_events_are_queryable",),
    ),
    WebInnovation(
        "WEB-010",
        "Governed Intelligence Surface",
        "Expose an AI-ready adapter boundary without granting an external model implicit authority.",
        ("WebRuntime.capabilities", "Constitution"),
        ("test_unknown_action_is_rejected",),
    ),
    WebInnovation(
        "WEB-011",
        "Cognitive Source Ingestion",
        "Turn public HTTPS resources into governed semantic web objects inside a world.",
        ("source.fetch_source", "web.source.ingest"),
        ("test_source_policy_rejects_non_https_and_private",),
    ),
    WebInnovation(
        "WEB-012",
        "Living Source Object",
        "Retain source identity, content meaning, provenance, and relationships as a first-class world object.",
        ("WebObject(object_type='web-source')",),
        ("test_action_produces_evidence",),
    )
)


def catalog() -> list[dict[str, Any]]:
    return [item.to_dict() for item in WEB_INNOVATIONS]
