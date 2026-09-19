from __future__ import annotations
from dataclasses import dataclass
import time, hashlib, json

@dataclass(frozen=True)
class ProofLease:
    lease_id: str
    capability: str
    policy_hash: str
    issued_at: int
    expires_at: int
    scope: tuple[str,...] = ()
    def active(self, now: int | None = None) -> bool:
        return (int(time.time()) if now is None else now) < self.expires_at

class LeaseManager:
    def issue(self, capability: str, policy: dict, ttl: int = 300, scope: tuple[str,...]=()) -> ProofLease:
        issued=int(time.time())
        raw=json.dumps({"capability":capability,"policy":policy},sort_keys=True)
        ph=hashlib.sha256(raw.encode()).hexdigest()
        return ProofLease("L-"+ph[:20],capability,ph,issued,issued+ttl,scope)
