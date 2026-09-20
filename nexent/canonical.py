from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from typing import Any

class RecordStatus(str, Enum):
    IDEA="IDEA"; RESTORED="RESTORED"; FORMULATED="FORMULATED"; PROPOSED="PROPOSED"
    IMPLEMENTED="IMPLEMENTED"; TESTED="TESTED"; VERIFIED="VERIFIED"; CANONICAL="CANONICAL"
    EXPERIMENTAL="EXPERIMENTAL"; ARCHIVE="ARCHIVE"; CONFLICT="CONFLICT"; DUPLICATE="DUPLICATE"

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def fingerprint(value: Any) -> str:
    return sha256(canonical_json(value).encode()).hexdigest()

@dataclass(frozen=True)
class SystemGenome:
    identity: str
    purpose: str
    behavior: dict[str, Any]=field(default_factory=dict)
    capabilities: tuple[str,...]=()
    dependencies: tuple[str,...]=()
    constraints: tuple[str,...]=()
    evidence: tuple[str,...]=()
    history: tuple[str,...]=()
    def canonical_form(self):
        return {"identity":self.identity,"purpose":self.purpose,"behavior":self.behavior,
                "capabilities":list(self.capabilities),"dependencies":list(self.dependencies),
                "constraints":list(self.constraints),"evidence":list(self.evidence),"history":list(self.history)}
    @property
    def genome_id(self): return "GEN-"+fingerprint(self.canonical_form())[:32]

@dataclass(frozen=True)
class InnovationRecord:
    canonical_id: str
    name: str
    kind: str
    family: str
    definition: str
    origin: str
    status: RecordStatus
    first_appearance: str|None=None
    aliases: tuple[str,...]=()
    parent: str|None=None
    children: tuple[str,...]=()
    dependencies: tuple[str,...]=()
    derived_from: tuple[str,...]=()
    mathematical_basis: tuple[str,...]=()
    computational_basis: tuple[str,...]=()
    physical_basis: tuple[str,...]=()
    implementation: tuple[str,...]=()
    tests: tuple[str,...]=()
    evidence: tuple[str,...]=()
    limitations: tuple[str,...]=()
    @classmethod
    def create(cls,name,kind,family,definition,origin,status=RecordStatus.PROPOSED,**kwargs):
        seed={"name":name,"kind":kind,"family":family,"definition":definition,"origin":origin}
        return cls("INN-"+fingerprint(seed)[:32],name,kind,family,definition,origin,status,**kwargs)

@dataclass(frozen=True)
class NexusRelation:
    source: str
    target: str
    relation: str
    layer: str
    conditions: dict[str,Any]=field(default_factory=dict)
    version: str="1"
    def to_dict(self): return {"source":self.source,"target":self.target,"relation":self.relation,"layer":self.layer,"conditions":self.conditions,"version":self.version}

class Nexus:
    LAYERS=("semantic","dependency","capability","contract","evidence","causal","execution","provenance","evolution","architecture")
    def __init__(self): self._relations=[]
    def link(self,relation):
        if relation.layer not in self.LAYERS: raise ValueError("unknown nexus layer: "+relation.layer)
        self._relations.append(relation)
    def relations(self,layer=None):
        return tuple(r for r in self._relations if layer is None or r.layer==layer)
    def neighbors(self,node,layer=None): return tuple(r.target for r in self.relations(layer) if r.source==node)
    def impact(self,node,layer=None):
        seen=set(); frontier=[node]
        while frontier:
            cur=frontier.pop()
            for nxt in self.neighbors(cur,layer):
                if nxt not in seen: seen.add(nxt); frontier.append(nxt)
        return tuple(sorted(seen))
    def manifest(self): return {l:[r.to_dict() for r in self.relations(l)] for l in self.LAYERS}

def compose(a,b): return {"op":"compose","left":a,"right":b}
def decompose(system): return tuple(system.get("children",()))
def refine(system,r): return {**system,"refinement":r}
def substitute(system,old,new): return {**system,"substitution":{"old":old,"new":new}}
def diff(a,b):
    keys=sorted(set(a)|set(b))
    return {k:{"left":a.get(k),"right":b.get(k)} for k in keys if a.get(k)!=b.get(k)}

@dataclass(frozen=True)
class NEXENTUIR:
    version: str
    semantic: dict[str,Any]
    genome: dict[str,Any]
    contracts: tuple[dict[str,Any],...]=()
    capabilities: tuple[dict[str,Any],...]=()
    relations: tuple[dict[str,Any],...]=()
    proof_obligations: tuple[dict[str,Any],...]=()
    def to_dict(self):
        return {"version":self.version,"semantic":self.semantic,"genome":self.genome,
                "contracts":list(self.contracts),"capabilities":list(self.capabilities),
                "relations":list(self.relations),"proof_obligations":list(self.proof_obligations)}
    @property
    def fingerprint(self): return fingerprint(self.to_dict())
