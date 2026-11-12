# NEXENT — RIRF Repository Mutation Boundary V1

## Role

NEXENT owns the discovery and engineering intelligence side of repository repair. It may understand a repository, identify anomalies, calculate semantic impact, and generate repair candidates.

## It does not own

- canonical governance;
- final authority;
- direct production merge;
- finality certification.

## Pipeline

DISCOVER → IDENTIFY → GENOME → ANOMALY → SEMANTIC IMPACT CONE → REPAIR CANDIDATES → ISOLATED HANDOFF

## Repair candidate

Each candidate must preserve the base revision, affected entities, expected invariants, predicted changes, preconditions, risk, and required verification checks.

Suggested record shape:

```yaml
candidate_id:
repository:
base_revision:
changed_paths: []
architecture_delta:
preconditions: []
invariants: []
verification_plan: []
risk:
provenance:
```

## Decision boundary

The existing Semantic Impact Cone is the analysis boundary. Governance and runtime systems decide whether a candidate may be mutated. The cone itself is not an approval mechanism.

## Relationship to canonical VAIXLNS

NEXENT outputs records consumed by VAIXLNS governance and VAIXLNS-unified execution. Canonical Finality policy remains in the VAIXLNS repository.
