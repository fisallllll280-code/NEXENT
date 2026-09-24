"""Deterministic architecture-contract checks for NEXENT candidates.

This module validates structure only. It does not approve deployment or grant
authority to a candidate architecture.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

REQUIRED_GENOME_FIELDS = (
    "identity", "purpose", "behavior", "capabilities",
    "dependencies", "constraints", "evidence", "history",
)

@dataclass(frozen=True)
class ContractResult:
    valid: bool
    errors: tuple[str, ...]

    def raise_if_invalid(self) -> None:
        if not self.valid:
            raise ValueError("; ".join(self.errors))

def validate_candidate(candidate: Mapping[str, Any]) -> ContractResult:
    errors: list[str] = []
    missing = [name for name in REQUIRED_GENOME_FIELDS if name not in candidate]
    if missing:
        errors.append("missing genome fields: " + ", ".join(missing))

    for name in ("identity", "purpose"):
        value = candidate.get(name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{name} must be a non-empty string")

    for name in ("capabilities", "dependencies", "constraints", "evidence", "history"):
        value = candidate.get(name)
        if value is not None and not isinstance(value, (list, tuple)):
            errors.append(f"{name} must be a list or tuple")

    behavior = candidate.get("behavior")
    if behavior is not None and not isinstance(behavior, Mapping):
        errors.append("behavior must be a mapping")

    status = candidate.get("status")
    if status in {"CANONICAL", "APPROVED", "DEPLOYED"}:
        errors.append("candidate validator cannot promote authority status")

    return ContractResult(valid=not errors, errors=tuple(errors))
