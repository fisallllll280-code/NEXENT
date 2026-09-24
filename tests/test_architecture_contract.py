from nexent.architecture_contract import validate_candidate

def test_valid_candidate_passes():
    candidate = {
        "identity": "NEXENT-CANDIDATE-001",
        "purpose": "test architecture",
        "behavior": {},
        "capabilities": ["observe"],
        "dependencies": [],
        "constraints": [],
        "evidence": ["EV-001"],
        "history": [],
        "status": "PROPOSED",
    }
    result = validate_candidate(candidate)
    assert result.valid
    assert result.errors == ()

def test_missing_identity_fails():
    candidate = {
        "purpose": "test", "behavior": {}, "capabilities": [],
        "dependencies": [], "constraints": [], "evidence": [], "history": [],
    }
    result = validate_candidate(candidate)
    assert not result.valid
    assert "identity" in result.errors[0]

def test_validator_cannot_promote_authority():
    candidate = {
        "identity": "NEXENT-CANDIDATE-001",
        "purpose": "test", "behavior": {}, "capabilities": [],
        "dependencies": [], "constraints": [], "evidence": [], "history": [],
        "status": "CANONICAL",
    }
    result = validate_candidate(candidate)
    assert not result.valid
