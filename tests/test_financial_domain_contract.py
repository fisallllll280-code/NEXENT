import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_financial_domain_forbids_real_world_execution():
    data = json.loads((ROOT / "registry/domains/financial-domain.json").read_text())
    assert data["role"] == "RESEARCH_AND_SIMULATION"
    assert data["authority"] == "NO_REAL_WORLD_EXECUTION"
    assert data["canonical_mutation"] is False


def test_financial_record_schema_has_epistemic_and_proof_fields():
    schema = json.loads((ROOT / "schemas/financial-research-record.schema.json").read_text())
    required = set(schema["required"])
    assert {"claim", "scope", "assumptions", "evidence", "proof_obligations"} <= required
