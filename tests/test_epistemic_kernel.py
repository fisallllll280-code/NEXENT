from nexent.epistemic_kernel import (
    AuthorityState,
    EpistemicState,
    NXClaim,
    classify_residual,
    evidence_adequacy,
)


def test_claim_requires_scope_and_falsification_for_promotion():
    claim = NXClaim(
        claim_id="C-001",
        property="p95_latency <= 180ms",
        scope="service-A",
        evidence=frozenset({"EV-1"}),
        proof=frozenset({"PR-1"}),
        assumptions=frozenset({"A-1"}),
        authority="policy-A",
        boundary="service-A/prod",
        uncertainty={"observational": "bounded"},
        validity="2026-09",
        epistemic=EpistemicState.VALIDATED,
        authorization=AuthorityState.AUTHORIZED,
        falsification_conditions=frozenset({"p95_latency > 180ms"}),
    )
    assert claim.admissible_for_promotion()


def test_evidence_count_is_not_sufficiency():
    assert evidence_adequacy(
        relevant=True,
        independent=False,
        fresh=True,
        context_match=True,
        property_coverage=True,
        assumption_coverage=False,
        boundary_coverage=False,
        contradictory=False,
        causal_power=False,
    ) == "PARTIAL"


def test_unknown_residual_blocks_unqualified_interpretation():
    residual = classify_residual(490, 180, cause="unknown")
    assert residual.value == 310
    assert residual.classification == "R7_UNKNOWN_RESIDUAL"
    assert residual.causal_coverage == "UNEXPLAINED"
