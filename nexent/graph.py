from __future__ import annotations
from collections import defaultdict
from .model import EntitySpec

class SystemGraph:
    def __init__(self) -> None:
        self.entities: dict[str, EntitySpec] = {}
        self.edges: dict[str, set[str]] = defaultdict(set)

    def register(self, spec: EntitySpec) -> None:
        if spec.id in self.entities:
            raise ValueError(f"duplicate entity: {spec.id}")
        self.entities[spec.id] = spec
        for dep in spec.requires:
            self.edges[spec.id].add(dep)

    def validate(self) -> list[str]:
        errors: list[str] = []
        provided = {cap for e in self.entities.values() for cap in e.provides}
        for e in self.entities.values():
            for req in e.requires:
                if req not in self.entities and req not in provided:
                    errors.append(f"{e.id}: missing dependency {req}")
        visiting, visited = set(), set()
        def dfs(n: str) -> None:
            if n in visiting:
                errors.append(f"dependency cycle at {n}")
                return
            if n in visited: return
            visiting.add(n)
            for d in self.edges.get(n, ()):
                if d in self.entities: dfs(d)
            visiting.remove(n); visited.add(n)
        for n in self.entities: dfs(n)
        return errors

    def snapshot(self) -> dict:
        return {"entities":{k:{"kind":v.kind,"domain":v.domain,"provides":v.provides,"requires":v.requires}
                            for k,v in self.entities.items()},
                "edges":{k:sorted(v) for k,v in self.edges.items()}}
