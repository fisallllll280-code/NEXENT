"""Semantic impact analysis for governed system changes.

The Impact Cone is stronger than a file diff: it follows declared architecture
dependencies and invariants to calculate what a change can affect.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict, deque
from ..model import digest

@dataclass(frozen=True)
class ImpactNode:
    node_id: str
    requires: tuple[str, ...] = ()
    invariants: tuple[str, ...] = ()

@dataclass(frozen=True)
class ImpactCone:
    root_changes: tuple[str, ...]
    affected_nodes: tuple[str, ...]
    affected_invariants: tuple[str, ...]
    frontier: tuple[str, ...]
    digest: str

    @property
    def bounded(self) -> bool:
        return bool(self.affected_nodes)

    def as_dict(self) -> dict:
        return {"root_changes": list(self.root_changes), "affected_nodes": list(self.affected_nodes), "affected_invariants": list(self.affected_invariants), "frontier": list(self.frontier), "digest": self.digest}

class ImpactConeAnalyzer:
    """Compute the transitive semantic blast radius of a proposed change."""
    def __init__(self, nodes: list[ImpactNode] | tuple[ImpactNode, ...]):
        self.nodes = {n.node_id: n for n in nodes}
        self.reverse: dict[str, set[str]] = defaultdict(set)
        for node in nodes:
            for dependency in node.requires:
                self.reverse[dependency].add(node.node_id)

    def analyze(self, changes: list[str] | tuple[str, ...]) -> ImpactCone:
        roots = tuple(sorted(set(changes)))
        unknown = [node for node in roots if node not in self.nodes]
        if unknown: raise KeyError(f"unknown impact root: {unknown}")
        seen = set(roots)
        queue = deque(roots)
        while queue:
            current = queue.popleft()
            for dependent in sorted(self.reverse.get(current, ())):
                if dependent not in seen:
                    seen.add(dependent); queue.append(dependent)
        invariants = sorted({i for node_id in seen for i in self.nodes[node_id].invariants})
        frontier = sorted({d for node_id in seen for d in self.reverse.get(node_id, ()) if d not in seen})
        payload = {"roots": roots, "affected": sorted(seen), "invariants": invariants, "frontier": frontier}
        return ImpactCone(roots, tuple(sorted(seen)), tuple(invariants), tuple(frontier), "IC-" + digest(payload)[:20])

__all__ = ["ImpactCone", "ImpactConeAnalyzer", "ImpactNode"]