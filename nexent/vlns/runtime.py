"""Evidence-first, deterministic VLNS legal-agent runtime prototype.

Offline only. Does not fetch laws, connect to Najiz, give legal advice, or execute procedures.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import hashlib
import json
from typing import Iterable

@dataclass(frozen=True)
class EvidenceSource:
    source_id: str
    title: str
    jurisdiction: str
    citation: str
    text: str
    source_url: str = ""
    effective_from: str = ""
    effective_to: str = ""
    retrieved_at: str = ""
    sha256: str = ""

    def __post_init__(self) -> None:
        if any(not value.strip() for value in (self.source_id, self.title, self.jurisdiction, self.citation, self.text)):
            raise ValueError("source_id, title, jurisdiction, citation, and text are required")
        for field in (self.effective_from, self.effective_to):
            if field:
                try: date.fromisoformat(field)
                except ValueError as exc: raise ValueError("effective dates must use YYYY-MM-DD") from exc
        actual = hashlib.sha256(self.text.encode("utf-8")).hexdigest()
        if self.sha256 and self.sha256 != actual:
            raise ValueError("source text hash mismatch")
        object.__setattr__(self, "sha256", actual)

class LegalKnowledgeBase:
    """In-memory source registry with explicit replacement and an audit event trail."""
    def __init__(self) -> None:
        self._sources: dict[str, EvidenceSource] = {}
        self._events: list[dict[str, str]] = []

    def register(self, source: EvidenceSource, *, replace: bool = False) -> None:
        if source.source_id in self._sources and not replace:
            raise ValueError(f"source already exists: {source.source_id}; explicit replace required")
        previous = self._sources.get(source.source_id)
        self._sources[source.source_id] = source
        self._events.append({"event": "SOURCE_REGISTERED" if previous is None else "SOURCE_REPLACED", "source_id": source.source_id, "sha256": source.sha256, "timestamp": datetime.now(timezone.utc).isoformat(), "previous_sha256": previous.sha256 if previous else ""})

    def sources(self) -> tuple[EvidenceSource, ...]:
        return tuple(self._sources[key] for key in sorted(self._sources))

    def events(self) -> tuple[dict[str, str], ...]:
        return tuple(dict(event) for event in self._events)

    def search(self, query: str, *, jurisdiction: str | None = None) -> list[EvidenceSource]:
        terms = {term.casefold() for term in query.split() if len(term) > 1}
        if not terms: return []
        ranked = []
        for source in self.sources():
            if jurisdiction and source.jurisdiction.casefold() != jurisdiction.casefold(): continue
            corpus = f"{source.title} {source.citation} {source.text}".casefold()
            score = sum(term in corpus for term in terms)
            if score: ranked.append((score, source.source_id, source))
        return [row[2] for row in sorted(ranked, key=lambda row: (-row[0], row[1]))]

    def export_manifest(self) -> str:
        return json.dumps({"schema_version": "1.0.0", "sources": [asdict(s) for s in self.sources()], "events": list(self.events())}, ensure_ascii=False, sort_keys=True, indent=2)

@dataclass(frozen=True)
class LegalAgent:
    agent_id: str
    specialty: str
    mandate: str

    def review(self, query: str, knowledge: LegalKnowledgeBase, *, jurisdiction: str | None = None) -> dict:
        matches = knowledge.search(query, jurisdiction=jurisdiction)
        if not matches:
            return {"agent_id": self.agent_id, "specialty": self.specialty, "status": "INSUFFICIENT_EVIDENCE", "findings": [], "limitations": ["No matching registered source; no legal conclusion is produced."]}
        return {"agent_id": self.agent_id, "specialty": self.specialty, "status": "SOURCE_MATCHES_FOUND", "findings": [{"source_id": s.source_id, "title": s.title, "citation": s.citation, "jurisdiction": s.jurisdiction, "source_url": s.source_url, "effective_from": s.effective_from, "effective_to": s.effective_to, "sha256": s.sha256, "matched_text": s.text} for s in matches], "limitations": ["Retrieval matches are not legal advice or confirmation that the source is current."]}

class VXCoordinator:
    """Routes bounded legal research tasks to specialist agents; never executes legal actions."""
    def __init__(self, knowledge: LegalKnowledgeBase, agents: Iterable[LegalAgent] | None = None) -> None:
        self.knowledge = knowledge
        self.agents = tuple(agents or (LegalAgent("legal-source-researcher", "source research", "Find registered source material."), LegalAgent("legal-citation-auditor", "citation audit", "Return provenance and hashes."), LegalAgent("legal-conflict-reviewer", "evidence-gap review", "Surface gaps for human review.")))
        if not self.agents: raise ValueError("at least one specialist agent is required")

    def review(self, query: str, *, jurisdiction: str | None = None) -> dict:
        if not query.strip(): raise ValueError("query must not be empty")
        results = [agent.review(query, self.knowledge, jurisdiction=jurisdiction) for agent in self.agents]
        found = any(result["status"] == "SOURCE_MATCHES_FOUND" for result in results)
        return {"runtime": "VLNS-LEGAL-AGENTS-PROTOTYPE", "coordinator": "VX", "status": "REVIEW_REQUIRED" if found else "HOLD_INSUFFICIENT_EVIDENCE", "query": query, "jurisdiction_filter": jurisdiction, "agent_results": results, "authority": "HUMAN_REVIEW_REQUIRED", "external_actions_performed": False, "najiz_connected": False, "generated_at": datetime.now(timezone.utc).isoformat()}
