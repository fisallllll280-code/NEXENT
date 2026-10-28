# VLNS Legal Agents Runtime v1 — Prototype

Status: PROTOTYPE / OFFLINE ONLY / NOT LEGAL ADVICE / NOT PRODUCTION VERIFIED

## Purpose
Provide a small, deterministic source registry and VX-coordinated retrieval prototype for evaluating evidence provenance and missing-evidence handling before any larger implementation.

## Components
- `EvidenceSource`: source metadata, jurisdiction, citation, effective dates, and SHA-256 of the stored text.
- `LegalKnowledgeBase`: in-memory registry, explicit replacement, lexical retrieval, and JSON manifest with an event trail.
- `LegalAgent`: specialist retrieval role. The current implementation does not provide independent legal reasoning.
- `VXCoordinator`: routes the same bounded retrieval query to specialist roles and fails closed when no source matches.

## Important limitations
- The three configured specialist roles currently use the same retrieval mechanism. They are not three independent AI models, and the conflict-reviewer does not perform semantic conflict detection.
- The knowledge base is in-memory; it is not durable storage and does not automatically ingest or refresh official law.
- Hashes prove identity of the stored text, not authenticity, legal authority, completeness, or current validity of the source.
- Lexical matching is not legal interpretation.
- No Najiz integration, external actions, court filing, or production deployment is implemented.
- Human legal review remains mandatory. Never use this prototype to determine a case outcome or replace a lawyer or judge.

## Suggested test command
`python -m unittest discover -s tests -p 'test_vlns_legal_agents.py' -v`

## Promotion gates
1. Run tests in the repository environment and retain CI evidence.
2. Review source licensing, official-source ingestion, effective-date handling, and provenance.
3. Add independent analysis/critic passes and a real conflict detector with adversarial test cases.
4. Validate privacy, access control, retention, threat model, and audit integrity.
5. Obtain qualified legal review and any required approvals before external integration.
6. No merge or deployment without explicit owner approval.
