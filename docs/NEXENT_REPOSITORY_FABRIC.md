# NEXENT Repository Fabric

## Mission

NEXENT turns a disordered repository landscape into a discoverable, evidence-backed, governable system fabric.

The objective is not to collect repositories. The objective is to understand what each repository is, what it contains, how it relates to other systems, what evidence supports those relationships, and which changes are safe to execute.

## Core rule

**Proposal is not state. Inference is not proof. Mutation requires an explicit plan and verification.**

## Fabric lifecycle

DISCOVER → IDENTIFY → CLASSIFY → RELATE → VERIFY → PLAN → AUTHORIZE → EXECUTE → VERIFY → RECORD

## Repository Genome

Every managed repository receives a canonical genome containing:

- identity
- provider and canonical URL
- revision
- purpose
- classification
- capabilities
- dependencies
- relationships
- evidence
- verification state
- governance state

The genome is a projection of evidence, not an unrestricted source of truth.

## Relationship vocabulary

NEXENT may represent:

- DEPENDS_ON
- IMPLEMENTS
- CONTAINS
- GENERATES
- DERIVED_FROM
- TESTS
- VERIFIES
- DEPLOYS
- REPLACES
- SUPERSEDES
- CONFLICTS_WITH
- RELATED_TO

## Mutation boundary

NEXENT must not silently mutate a repository merely because an agent inferred a desirable change.

Mutation path:

REQUEST → PLAN → POLICY → AUTHORIZATION → EXECUTION → VERIFICATION → LEDGER

## Repository Anomaly principle

NEXENT compares expected architecture with observed repository state. Differences are classified as evidence-backed anomalies, not automatically treated as errors.

Initial anomaly classes:

- missing_expected_component
- unexpected_component
- misplaced_component
- dependency_mismatch
- contract_mismatch
- stale_metadata
- orphaned_component
- duplicate_capability
- unverified_relationship

## Innovation rule

NEXENT is explicitly allowed to propose new structures and mechanisms when they improve coherence, reliability, verification, or execution. New proposals must preserve provenance and must not erase earlier work.

## Preservation rule

Existing project material is evidence. Refactoring must be additive or traceable. Destructive replacement requires an explicit migration plan and verification.

## v0.1 target

The first operational fabric must be able to:

1. represent a repository genome;
2. compare observed and expected repository structure;
3. classify relationships and anomalies;
4. emit deterministic JSON for downstream graph/verification layers;
5. remain usable without an external AI dependency.
