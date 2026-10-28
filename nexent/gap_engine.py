"""Evidence-first capability gap analysis and candidate specification generation.

This module creates reviewable candidate manifests only. It never edits source files,
installs dependencies, calls external models, merges, or deploys.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from typing import Iterable


class EvidenceState(str, Enum):
    VERIFIED = "VERIFIED"
    IMPLEMENTED_UNVERIFIED = "IMPLEMENTED_UNVERIFIED"
    SPECIFIED = "SPECIFIED"
    PROPOSED = "PROPOSED"
    NOT_OBSERVED = "NOT_OBSERVED"
    INACCESSIBLE = "INACCESSIBLE"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class CapabilityRecord:
    capability_id: str
    name: str
    required: bool
    state: EvidenceState
    source_refs: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.capability_id.strip() or not self.name.strip():
            raise ValueError("capability_id and name are required")
        if self.state in (EvidenceState.VERIFIED, EvidenceState.IMPLEMENTED_UNVERIFIED) and not self.source_refs:
            raise ValueError("implemented or verified records require source_refs")


@dataclass(frozen=True)
class Gap:
    capability_id: str
    name: str
    gap_type: str
    evidence_state: str
    required: bool
    source_refs: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    safe_next_step: str


def _candidate_id(capability_id: str, gap_type: str) -> str:
    digest = hashlib.sha256(f"{capability_id}:{gap_type}".encode()).hexdigest()[:12]
    return f"CAND-{digest.upper()}"


def analyze_gaps(records: Iterable[CapabilityRecord]) -> list[Gap]:
    """Compute gaps without treating NOT_OBSERVED/INACCESSIBLE as proven absence."""
    gaps: list[Gap] = []
    seen: set[str] = set()
    for record in records:
        if record.capability_id in seen:
            raise ValueError(f"duplicate capability_id: {record.capability_id}")
        seen.add(record.capability_id)
        if record.state == EvidenceState.VERIFIED:
            continue
        if record.state == EvidenceState.CONFLICT:
            kind, next_step = "CONFLICT", "Resolve the source conflict; do not generate a replacement yet."
        elif record.state in (EvidenceState.NOT_OBSERVED, EvidenceState.INACCESSIBLE):
            kind, next_step = "INVENTORY_GAP", "Perform a bounded inventory and record coverage before classifying absence."
        elif record.state == EvidenceState.IMPLEMENTED_UNVERIFIED:
            kind, next_step = "VERIFICATION_GAP", "Add or run reproducible tests and attach results."
        elif record.state == EvidenceState.SPECIFIED:
            kind, next_step = "IMPLEMENTATION_GAP", "Generate a candidate implementation specification for review."
        else:
            kind, next_step = "SPECIFICATION_GAP", "Generate a candidate specification with acceptance criteria."
        if record.required or record.state in (EvidenceState.CONFLICT, EvidenceState.NOT_OBSERVED, EvidenceState.INACCESSIBLE):
            gaps.append(Gap(record.capability_id, record.name, kind, record.state.value,
                record.required, record.source_refs, record.acceptance_criteria, next_step))
    return sorted(gaps, key=lambda g: (not g.required, g.gap_type, g.capability_id))


def generate_candidate_manifests(gaps: Iterable[Gap]) -> list[dict[str, object]]:
    """Generate deterministic candidate manifests; these are not implementations or proof."""
    candidates = []
    for gap in gaps:
        if gap.gap_type in ("CONFLICT", "INVENTORY_GAP"):
            continue
        candidate = {
            "candidate_id": _candidate_id(gap.capability_id, gap.gap_type),
            "capability_id": gap.capability_id,
            "name": gap.name,
            "candidate_type": gap.gap_type,
            "status": "PROPOSED",
            "source_refs": list(gap.source_refs),
            "acceptance_criteria": list(gap.acceptance_criteria),
            "required_human_review": True,
            "tests_required_before_promotion": True,
            "merge_authorized": False,
            "deployment_authorized": False,
        }
        candidates.append(candidate)
    return candidates


def build_report(records: Iterable[CapabilityRecord]) -> dict[str, object]:
    records = list(records)
    gaps = analyze_gaps(records)
    candidates = generate_candidate_manifests(gaps)
    return {
        "schema_version": "1.0.0",
        "engine": "NEXENT-GAP-DRIVEN-GENERATION",
        "status": "ANALYSIS_ONLY",
        "input_count": len(records),
        "verified_count": sum(r.state == EvidenceState.VERIFIED for r in records),
        "gap_count": len(gaps),
        "candidate_count": len(candidates),
        "gaps": [asdict(g) for g in gaps],
        "candidates": candidates,
        "limitations": [
            "Input inventory completeness is not independently proven.",
            "NOT_OBSERVED and INACCESSIBLE do not mean MISSING.",
            "Candidates are specifications only, not generated or tested source code.",
            "No repository writes, external calls, merges, or deployments occur.",
        ],
    }


def report_json(records: Iterable[CapabilityRecord]) -> str:
    return json.dumps(build_report(records), ensure_ascii=False, sort_keys=True, indent=2)
