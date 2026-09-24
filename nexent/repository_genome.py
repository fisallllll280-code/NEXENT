"""Canonical repository genome primitives for the NEXENT Repository Fabric.

The module is deliberately deterministic and dependency-light. It describes a
repository from observable facts; it does not promote inferred claims to truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class VerificationState(str, Enum):
    UNKNOWN = "unknown"
    DISCOVERED = "discovered"
    IDENTIFIED = "identified"
    VERIFIED = "verified"
    CONFLICTED = "conflicted"
    QUARANTINED = "quarantined"


class AnomalyType(str, Enum):
    MISSING_EXPECTED_COMPONENT = "missing_expected_component"
    UNEXPECTED_COMPONENT = "unexpected_component"
    MISPLACED_COMPONENT = "misplaced_component"
    DEPENDENCY_MISMATCH = "dependency_mismatch"
    CONTRACT_MISMATCH = "contract_mismatch"
    STALE_METADATA = "stale_metadata"
    ORPHANED_COMPONENT = "orphaned_component"
    DUPLICATE_CAPABILITY = "duplicate_capability"
    UNVERIFIED_RELATIONSHIP = "unverified_relationship"


@dataclass(frozen=True)
class Evidence:
    source: str
    kind: str
    reference: str
    observed_value: Any = None


@dataclass(frozen=True)
class RepositoryGenome:
    canonical_id: str
    name: str
    provider: str
    canonical_url: str
    revision: str | None = None
    purpose: str | None = None
    classification: str | None = None
    capabilities: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    relationships: tuple[dict[str, str], ...] = ()
    evidence: tuple[Evidence, ...] = ()
    verification: VerificationState = VerificationState.UNKNOWN
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["verification"] = self.verification.value
        data["evidence"] = [asdict(item) for item in self.evidence]
        return data


@dataclass(frozen=True)
class RepositoryAnomaly:
    anomaly_type: AnomalyType
    path: str
    expected: Any = None
    observed: Any = None
    evidence: tuple[Evidence, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["anomaly_type"] = self.anomaly_type.value
        data["evidence"] = [asdict(item) for item in self.evidence]
        return data


def compare_paths(expected: set[str], observed: set[str]) -> list[RepositoryAnomaly]:
    """Compare expected and observed paths without making destructive decisions."""
    anomalies: list[RepositoryAnomaly] = []

    for path in sorted(expected - observed):
        anomalies.append(
            RepositoryAnomaly(
                anomaly_type=AnomalyType.MISSING_EXPECTED_COMPONENT,
                path=path,
                expected="present",
                observed="missing",
            )
        )

    for path in sorted(observed - expected):
        anomalies.append(
            RepositoryAnomaly(
                anomaly_type=AnomalyType.UNEXPECTED_COMPONENT,
                path=path,
                expected="absent",
                observed="present",
            )
        )

    return anomalies
