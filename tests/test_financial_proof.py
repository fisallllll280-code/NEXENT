import pytest

from nexent.financial_proof import build_financial_proof_package


def valid_record():
    return {
        "record_id": "NX-FIN-001",
        "domain": "TREASURY_SIMULATION",
        "status": "PROVEN",
        "claim": "simulation preserves declared treasury invariants",
        "scope": {"system": "paper-treasury"},
        "assumptions": ["fixed input dataset"],
        "evidence": [{"id": "E1", "type": "deterministic-test"}],
        "proof_obligations": [{"id": "P1", "property": "balance-conservation"}],
    }


def test_incomplete_record_rejected():
    with pytest.raises(ValueError, match="incomplete"):
        build_financial_proof_package({"record_id": "NX-FIN-001"})


def test_proof_package_is_adoption_request_only():
    package = build_financial_proof_package(valid_record())
    assert package.disposition == "ADOPTION_REQUESTED"
    assert package.execution_authority == "NONE"
    assert package.record["execution_authority"] == "NONE"


def test_execution_authority_cannot_be_granted():
    record = valid_record()
    record["execution_authority"] = "ACTIVE"
    with pytest.raises(ValueError, match="execution authority"):
        build_financial_proof_package(record)


def test_fingerprint_is_deterministic():
    a = build_financial_proof_package(valid_record())
    b = build_financial_proof_package(valid_record())
    assert a.fingerprint == b.fingerprint
