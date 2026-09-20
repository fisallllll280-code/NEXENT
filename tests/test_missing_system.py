from nexent.missing_system import (
    Evidence,
    GapClass,
    ImpossibilityClass,
    MindAssessment,
    MissingSystemDiscoveryEngine,
)


def test_discovery_pipeline_produces_stable_hypothesis():
    engine = MissingSystemDiscoveryEngine()
    evidence = [Evidence("test", "capability is fragmented", 0.9)]
    observation = engine.observe("coordination", "FRAGMENTED", evidence)
    assessment = MindAssessment(
        "adversarial",
        "fragmentation may be caused by missing protocol",
        blind_spots=("limited sample",),
    )
    void = engine.discover_void("coordination", [observation], assessments=[assessment])
    void.classify(GapClass.PROTOCOL, "no shared coordination protocol")
    hypothesis = engine.hypothesize(
        void,
        required_primitives=["identity"],
        required_laws=["deterministic ordering"],
        required_data=["events"],
        required_interfaces=["coordination"],
        proof_obligations=["ordering is deterministic"],
        evidence=evidence,
    )
    assert hypothesis.id.startswith("MSH-")
    assert hypothesis.status == "HYPOTHESIS"


def test_impossibility_decomposition_preserves_unknowns():
    engine = MissingSystemDiscoveryEngine()
    result = engine.decompose_impossibility(
        "claim",
        [ImpossibilityClass.UNKNOWN],
        unknowns=["missing bound"],
    )
    assert result.requires_further_search
    assert result.unknowns == ("missing bound",)
