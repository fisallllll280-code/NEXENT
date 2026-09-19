from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DslIntent:
    name: str
    actor: str
    capability: str
    payload: dict[str, str]

class NexentDSL:
    @staticmethod
    def parse(line: str) -> DslIntent:
        tokens=line.strip().split()
        if len(tokens) < 6 or tokens[0] != "INTENT" or tokens[2] != "BY" or tokens[4] != "USING":
            raise ValueError("syntax: INTENT name BY actor USING capability [WITH k=v,...]")
        name,actor,capability=tokens[1],tokens[3],tokens[5]
        payload={}
        if len(tokens)>6:
            if tokens[6]!="WITH": raise ValueError("expected WITH")
            for item in " ".join(tokens[7:]).split(","):
                if not item.strip(): continue
                if "=" not in item: raise ValueError("payload must use k=v")
                k,v=item.split("=",1); payload[k.strip()]=v.strip()
        return DslIntent(name,actor,capability,payload)
