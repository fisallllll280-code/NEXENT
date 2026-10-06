"""NEXENT-side boundary.

NEXENT may discover and formulate an external integration, but it cannot
grant runtime authority. The output is a proposal payload for VAIXLNS.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class ExternalIntegrationProposal:
    integration_id: str
    name: str
    kind: str
    endpoint: str
    capabilities: tuple[str, ...]
    contract_version: str
    dependency_fingerprint: str
    environment_fingerprint: str
    owner: str
    status: str = "PROPOSED"

    @property
    def identity(self) -> str:
        payload = {
            "integration_id": self.integration_id,
            "name": self.name,
            "kind": self.kind,
            "endpoint": self.endpoint,
            "capabilities": self.capabilities,
            "contract_version": self.contract_version,
            "dependency_fingerprint": self.dependency_fingerprint,
            "environment_fingerprint": self.environment_fingerprint,
            "owner": self.owner,
        }
        return sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def to_vaixlns_handoff(self) -> dict:
        return {
            "integration_id": self.integration_id,
            "identity": self.identity,
            "status": "PROPOSED",
            "authority": "VAIXLNS",
            "required_stages": [
                "DISCOVER",
                "CONTRACT",
                "SANDBOX",
                "FUNCTIONAL_TEST",
                "FAILURE_RECOVERY",
                "REPLAY",
                "INDEPENDENT_VERIFICATION",
                "PROOF_FRESHNESS",
                "CAUSAL_IMPACT_BUDGET",
                "EXPLICIT_AUTHORITY",
                "ADMISSION",
            ],
        }
