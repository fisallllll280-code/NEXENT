# NEXENT Financial Domain Contract

## Status
SPECIFIED — domain boundary contract; not an authorization for real financial execution.

## Purpose
NEXENT may research, model, simulate, stress-test, and generate proof packages for financial systems and hypotheses.

## Boundary
Financial-domain outputs are candidates until independently admitted by VAIXLNS/VX governance.

NEXENT MUST NOT:
- mutate VAIXLNS canonical state directly;
- execute real financial transactions;
- promote an unverified model to VERIFIED;
- treat market observations or model outputs as ground truth without evidence provenance.

## Domain capabilities
- market research
- economic and financial modeling
- risk analysis
- treasury-state simulation
- accounting/precision analysis
- counterfactual and stress simulation
- invariant generation and testing
- proof-package generation

## Epistemic lifecycle
PROPOSED -> EVIDENCED -> PROVEN/VALIDATED -> ADOPTION_REQUESTED

Authority lifecycle is separate:
UNAUTHORIZED -> ELIGIBLE -> AUTHORIZED -> ACTIVE

No epistemic state alone grants execution authority.

## Financial precision
Use Decimal or integer minor-units at monetary boundaries. Do not use binary floating point for authoritative monetary arithmetic.

## Required evidence
Every material financial claim must identify:
- source/evidence IDs
- observation time
- scope and boundary
- assumptions
- uncertainty
- reproducibility information
- falsification conditions

## Promotion gate
A financial candidate can be proposed to VAIXLNS only with a complete evidence/proof package. Final real-world execution remains a VX admission decision.
