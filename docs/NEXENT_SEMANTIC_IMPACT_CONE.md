# NEXENT Semantic Impact Cone

## Why this exists
A normal code diff answers: which files changed? That is not the same as which system behaviours, invariants, proofs, and dependent systems can be affected.

NEXENT therefore adds a **Semantic Impact Cone**. It treats architecture dependencies as a directed graph and computes the transitive set of dependents of a proposed change, while collecting declared invariants.

## Engineering rule
A change is not considered semantically understood until its impact cone is computed. The cone is not an approval mechanism; governance remains responsible for authorization.

## Determinism
The same architecture graph and change roots produce the same cone digest. This gives proof, review, simulation, quarantine, and evolution layers a stable reference.

## Example

    ledger -> replay -> proof -> ui

A change at ledger therefore exposes replay, proof, and UI as affected nodes and collects their invariants.

## Pipeline

    CODE CHANGE -> ARCHITECTURAL CONSEQUENCE -> INVARIANTS -> PROOF/TEST OBLIGATIONS -> GOVERNANCE