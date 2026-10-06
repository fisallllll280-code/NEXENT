from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import fingerprint


REQUIRED_FIELDS = (
    "record_id",
    "domain",
    "status",
    "claim",
    "scope",
    "assumptions",
    "evidence",
    "proof_obligations",
)


@dataclass(frozen=True)
class FinancialProofPackage:
    record: dict[str, Any]
    fingerprint: str
    disposition: str = "ADOPTION_REQUESTED"
    execution_authority: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "record": self.record,
            "fingerprint": self.fingerprint,
            "disposition": self.disposition,
            "execution_authority": self.execution_authority,
        }


def build_financial_proof_package(record: dict[str, Any]) -> FinancialProofPackage:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise ValueError("incomplete financial proof package: " + ", ".join(missing))

    if record["domain"] not in {
        "MARKET_RESEARCH",
        "ECONOMIC_MODELING",
        "RISK_ENGINEERING",
        "TREASURY_SIMULATION",
        "ACCOUNTING_PRECISION",
        "PORTFOLIO_ALLOCATION_RESEARCH",
        "FINANCIAL_ARCHITECTURE",
        "PROOF_AND_ASSURANCE",
    }:
        raise ValueError("unsupported financial research domain")

    if record["status"] not in {"PROPOSED", "EVIDENCED", "PROVEN", "VALIDATED"}:
        raise ValueError("record is not admissible for an adoption request")

    if not isinstance(record["evidence"], list) or not record["evidence"]:
        raise ValueError("financial proof package requires evidence")

    if not isinstance(record["proof_obligations"], list) or not record["proof_obligations"]:
        raise ValueError("financial proof package requires proof obligations")

    if record.get("execution_authority", "NONE") != "NONE":
        raise ValueError("NEXENT financial research cannot grant execution authority")

    normalized = dict(record)
    normalized["execution_authority"] = "NONE"
    return FinancialProofPackage(
        record=normalized,
        fingerprint=fingerprint(normalized),
    )
