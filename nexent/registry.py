from __future__ import annotations
from .model import Capability

class CapabilityRegistry:
    def __init__(self): self.items: dict[str,Capability]={}
    def add(self, cap: Capability):
        if cap.id in self.items: raise ValueError("duplicate capability")
        self.items[cap.id]=cap
    def resolve(self, name: str) -> Capability | None:
        return self.items.get(name)
    def snapshot(self):
        return {k:{"version":v.version,"description":v.description,"constraints":v.constraints}
                for k,v in self.items.items()}
