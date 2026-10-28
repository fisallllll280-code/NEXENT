# NEXENT Gap-Driven Generation v1

Status: PROTOTYPE / ANALYSIS ONLY / NOT PRODUCTION VERIFIED

## Intent
Inspect a declared capability inventory, measure evidence-backed gaps, and generate deterministic candidate manifests for review. This extends NEXENT's existing discovery → gap → candidate → simulation/verification direction; it does not replace the master federated index or VAIXLNS canonical registries.

## Pipeline
1. Accept capability records with stable IDs, state, source references, and acceptance criteria.
2. Classify gaps as inventory, specification, implementation, verification, or conflict gaps.
3. Preserve uncertainty: NOT_OBSERVED and INACCESSIBLE require bounded inventory; neither means MISSING.
4. Generate candidate manifests only for gaps that are safe to specify. Conflicts and incomplete inventories are held.
5. Require human review, tests, evidence, and explicit authorization before any later promotion.

## Current implementation boundary
- The engine analyzes only the records supplied to it; it does not crawl all repositories.
- It does not generate executable source code, run tests, invoke models, or modify files.
- Candidate manifests are PROPOSED and never authorize merge or deployment.
- No completeness claim is made for VAIXLNS, VX, VLNS, NEXENT, or other repositories.
- Protected canonical files are out of scope.

## Test command
`python -m unittest discover -s tests -p 'test_gap_engine.py' -v`

## Promotion gates
Source inventory → reproducible gap report → candidate specification → isolated implementation → tests → review → proof bundle → explicit owner approval. No proof, no promotion.
