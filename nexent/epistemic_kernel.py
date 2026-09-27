"""NEXENT epistemic kernel: executable primitives extracted from project source material.

The module deliberately keeps epistemic state separate from authority state.
It is deterministic and side-effect free so it can be embedded in VX verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Mapping


class EpistemicState(str, Enum):
    UNFORMED = "UNFORMED"
    PROPOSED = "PROPOSED"
    EVIDENCED = "EVIDENCED"
    PROVEN = "PROVEN"
    VALIDATED = "VALIDATED"
    SUSPECT = "SUSPECT"
    INVALIDATED = "INVALIDATED"


class AuthorityState(str, Enum):
    UNAUTHORIZED = "UNAUTHORIZED"
    ELIGIBLE = "ELIGIBLE"
    AUTHORIZED = "AUTHORIZED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"


@dataclass(frozen=True)
class NXClaim:
    claim_id: str
    property: str
    scope: str
    evidence: FrozenSet[str]
    proof: FrozenSet[str]
    assumptions: FrozenSet[str]
    authority: str
    boundary: str
    uncertainty: Mapping[str, str]
    validity: str
    epistemic: EpistemicState = EpistemicState.PROPOSED
    authorization: AuthorityState = AuthorityState.UNAUTHORIZED
    falsification_conditions: FrozenSet[str] = frozenset()

    def admissible_for_promotion(self) -> bool:
        return bool(
            self.claim_id
            and self.property
            and self.scope
            and self.boundary
            and self.falsification_conditions
            and self.epistemic in {
                EpistemicState.PROVEN,
                EpistemicState.VALIDATED,
            }
            and self.authorization
            in {AuthorityState.AUTHORIZED, AuthorityState.ACTIVE}
        )


@dataclass(frozen=True)
class Residual:
    observed: float
    expected: float
    classification: str
    causal_coverage: str

    @property
    def value(self) -> float:
        return self.observed - self.expected


def evidence_adequacy(
    *,
    relevant: bool,
    independent: bool,
    fresh: bool,
    context_match: bool,
    property_coverage: bool,
    assumption_coverage: bool,
    boundary_coverage: bool,
    contradictory: bool,
    causal_power: bool,
) -> str:
    if contradictory:
        return "CONTESTED"
    checks = (
        relevant,
        independent,
        fresh,
        context_match,
        property_coverage,
        assumption_coverage,
        boundary_coverage,
        causal_power,
    )
    if all(checks):
        return "ADEQUATE"
    if not any(checks):
        return "INSUFFICIENT"
    if not fresh:
        return "STALE"
    return "PARTIAL"


def classify_residual(observed: float, expected: float, *, cause: str) -> Residual:
    allowed = {
        "measurement_error": "R0_MEASUREMENT_ERROR",
        "context_drift": "R1_CONTEXT_DRIFT",
        "dependency_drift": "R2_DEPENDENCY_DRIFT",
        "model_error": "R3_MODEL_ERROR",
        "missing_variable": "R4_MISSING_VARIABLE",
        "causal_misattribution": "R5_CAUSAL_MISATTRIBUTION",
        "boundary_failure": "R6_BOUNDARY_FAILURE",
        "unknown": "R7_UNKNOWN_RESIDUAL",
    }
    classification = allowed.get(cause, allowed["unknown"])
    coverage = "UNEXPLAINED" if classification == "R7_UNKNOWN_RESIDUAL" else "CLASSIFIED"
    return Residual(observed, expected, classification, coverage)


def assumption_survival(state: str) -> str:
    transitions = {
        "SUPPORTED": "SUPPORTED",
        "AGING": "AGING",
        "CHALLENGED": "CHALLENGED",
        "INVALIDATED": "INVALIDATED",
    }
    return transitions.get(state, "UNKNOWN")
