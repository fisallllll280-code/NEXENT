from nexent.engineering.impact import ImpactConeAnalyzer, ImpactNode

def test_impact_cone_follows_dependents_and_collects_invariants():
    analyzer = ImpactConeAnalyzer([
        ImpactNode("ledger", invariants=("append_only",)),
        ImpactNode("replay", requires=("ledger",), invariants=("deterministic_replay",)),
        ImpactNode("proof", requires=("replay",), invariants=("evidence_matches_replay",)),
        ImpactNode("ui", requires=("proof",)),
        ImpactNode("isolated"),
    ])
    cone = analyzer.analyze(["ledger"])
    assert cone.affected_nodes == ("ledger", "proof", "replay", "ui")
    assert cone.affected_invariants == ("append_only", "deterministic_replay", "evidence_matches_replay")
    assert cone.digest.startswith("IC-")

def test_impact_cone_is_deterministic():
    nodes = [ImpactNode("b", requires=("a",), invariants=("B",)), ImpactNode("a", invariants=("A",)), ImpactNode("c", requires=("b",), invariants=("C",))]
    analyzer = ImpactConeAnalyzer(nodes)
    assert analyzer.analyze(["a"]).digest == analyzer.analyze(["a"]).digest