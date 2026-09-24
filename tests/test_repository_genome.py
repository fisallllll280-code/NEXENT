from nexent.repository_genome import (
    AnomalyType,
    Evidence,
    RepositoryGenome,
    VerificationState,
    compare_paths,
)


def test_genome_preserves_evidence_and_verification_state():
    genome = RepositoryGenome(
        canonical_id="NEXENT-REP-000001",
        name="NEXENT",
        provider="github",
        canonical_url="https://github.com/fisallllll280-code/NEXENT",
        verification=VerificationState.DISCOVERED,
        evidence=(
            Evidence(
                source="github",
                kind="repository_metadata",
                reference="repo:main",
            ),
        ),
    )

    data = genome.to_dict()

    assert data["canonical_id"] == "NEXENT-REP-000001"
    assert data["verification"] == "discovered"
    assert data["evidence"][0]["source"] == "github"


def test_compare_paths_is_non_destructive_and_deterministic():
    anomalies = compare_paths(
        {"README.md", "docs", "nexent"},
        {"README.md", "nexent", "scratch"},
    )

    assert [item.path for item in anomalies] == ["docs", "scratch"]
    assert anomalies[0].anomaly_type is AnomalyType.MISSING_EXPECTED_COMPONENT
    assert anomalies[1].anomaly_type is AnomalyType.UNEXPECTED_COMPONENT
