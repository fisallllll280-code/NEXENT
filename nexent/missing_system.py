"""NEXENT Missing-System Discovery Engine.

Deterministic domain model for discovering capability gaps and turning them
into governed system hypotheses. This module does not decide to deploy or
modify NEXENT; it produces auditable engineering artifacts.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from .model import digest


class GapClass(str, Enum):
    PRIMITIVE = "MISSING_PRIMITIVE"
    PROTOCOL = "MISSING_PROTOCOL"
    DATA = "MISSING_DATA"
    COMPUTATION = "MISSING_COMPUTATION"
    AUTHORITY = "MISSING_AUTHORITY"
    MODEL = "MISSING_MODEL"
    PROOF = "MISSING_PROOF"
    ARCHITECTURE = "MISSING_ARCHITECTURE"
    SYSTEM = "MISSING_SYSTEM"


class ImpossibilityClass(str, Enum):
    PHYSICAL = "PHYSICAL"
    COMPUTATIONAL = "COMPUTATIONAL"
    INFORMATIONAL = "INFORMATIONAL"
    ECONOMIC = "ECONOMIC"
    ARCHITECTURAL = "ARCHITECTURAL"
    ONTOLOGICAL = "ONTOLOGICAL"
    GOVERNANCE = "GOVERNANCE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Evidence:
    source: str
    claim: str
    strength: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("evidence strength must be in [0, 1]")


@dataclass(frozen=True)
class CapabilityObservation:
    capability: str
    state: str
    evidence: tuple[Evidence, ...] = ()

    def key(self) -> str:
        return digest({
            "capability": self.capability,
            "state": self.state,
            "evidence": [e.__dict__ for e in self.evidence],
        })[:20]


@dataclass(frozen=True)
class MindAssessment:
    mind: str
    claim: str
    assumptions: tuple[str, ...] = ()
    uncertainty: float = 1.0
    counterexamples: tuple[str, ...] = ()
    blind_spots: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.uncertainty <= 1.0:
            raise ValueError("uncertainty must be in [0, 1]")


@dataclass
class CapabilityVoid:
    capability: str
    observations: list[CapabilityObservation] = field(default_factory=list)
    cause: str | None = None
    gap_class: GapClass | None = None
    assessments: list[MindAssessment] = field(default_factory=list)

    def classify(self, gap_class: GapClass, cause: str) -> None:
        self.gap_class = gap_class
        self.cause = cause


@dataclass(frozen=True)
class ImpossibilityDecomposition:
    original_claim: str
    classes: tuple[ImpossibilityClass, ...]
    bounds: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()

    @property
    def requires_further_search(self) -> bool:
        return ImpossibilityClass.UNKNOWN in self.classes


@dataclass(frozen=True)
class SystemHypothesis:
    id: str
    capability: str
    required_primitives: tuple[str, ...]
    required_laws: tuple[str, ...]
    required_data: tuple[str, ...]
    required_interfaces: tuple[str, ...]
    proof_obligations: tuple[str, ...]
    evidence: tuple[Evidence, ...] = ()
    status: str = "HYPOTHESIS"

    @staticmethod
    def create(
        capability: str,
        required_primitives: list[str],
        required_laws: list[str],
        required_data: list[str],
        required_interfaces: list[str],
        proof_obligations: list[str],
        evidence: list[Evidence] | None = None,
    ) -> "SystemHypothesis":
        payload = {
            "capability": capability,
            "required_primitives": required_primitives,
            "required_laws": required_laws,
            "required_data": required_data,
            "required_interfaces": required_interfaces,
            "proof_obligations": proof_obligations,
        }
        return SystemHypothesis(
            id="MSH-" + digest(payload)[:20],
            capability=capability,
            required_primitives=tuple(required_primitives),
            required_laws=tuple(required_laws),
            required_data=tuple(required_data),
            required_interfaces=tuple(required_interfaces),
            proof_obligations=tuple(proof_obligations),
            evidence=tuple(evidence or ()),
        )


class MissingSystemDiscoveryEngine:
    """Deterministic discovery layer; generation/deployment remain governed."""

    def observe(
        self, capability: str, state: str, evidence: list[Evidence] | None = None
    ) -> CapabilityObservation:
        return CapabilityObservation(capability, state, tuple(evidence or ()))

    def discover_void(
        self,
        capability: str,
        observations: list[CapabilityObservation],
        *,
        assessments: list[MindAssessment] | None = None,
    ) -> CapabilityVoid:
        return CapabilityVoid(
            capability=capability,
            observations=list(observations),
            assessments=list(assessments or ()),
        )

    def decompose_impossibility(
        self,
        claim: str,
        classes: list[ImpossibilityClass],
        *,
        bounds: list[str] | None = None,
        unknowns: list[str] | None = None,
    ) -> ImpossibilityDecomposition:
        if not classes:
            raise ValueError("at least one impossibility class is required")
        return ImpossibilityDecomposition(
            original_claim=claim,
            classes=tuple(classes),
            bounds=tuple(bounds or ()),
            unknowns=tuple(unknowns or ()),
        )

    def hypothesize(self, void: CapabilityVoid, **kwargs) -> SystemHypothesis:
        if void.gap_class is None:
            raise ValueError("capability void must be classified before hypothesis")
        return SystemHypothesis.create(void.capability, **kwargs)


__all__ = [
    "CapabilityObservation",
    "CapabilityVoid",
    "Evidence",
    "GapClass",
    "ImpossibilityClass",
    "ImpossibilityDecomposition",
    "MindAssessment",
    "MissingSystemDiscoveryEngine",
    "SystemHypothesis",
]
