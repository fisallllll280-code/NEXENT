# NEXENT Missing-System Discovery Engine

## Purpose

The Missing-System Discovery Engine (MSD) extends NEXENT from building requested
systems to discovering capability gaps that may justify a new primitive,
protocol, architecture, or system.

It is a discovery and engineering layer, not an autonomous deployment authority.

## Canonical pipeline

~~~text
REALITY
  -> OBSERVATION
  -> CAPABILITY VOID
  -> GAP CLASSIFICATION
  -> PRIMITIVE / PROTOCOL / DATA / MODEL / ARCHITECTURE / SYSTEM
  -> MISSING-SYSTEM GRAPH
  -> ARCHITECTURE SEARCH
  -> MULTI-MIND ATTACK
  -> COUNTERFACTUAL / SIMULATION
  -> PROOF OBLIGATIONS
  -> SYSTEM TWIN
  -> GOVERNANCE GATE
  -> NEXENT FORGE
  -> SYSTEM INSTANCE
  -> OBSERVATION
~~~

## Capability Void

A capability can be recorded as:

- EXISTING
- WEAK
- FRAGMENTED
- EXPENSIVE
- UNVERIFIED
- UNAVAILABLE
- UNREPRESENTABLE
- UNKNOWN

A void is not automatically a request for a new system. NEXENT first classifies
the missing layer:

- MISSING_PRIMITIVE
- MISSING_PROTOCOL
- MISSING_DATA
- MISSING_COMPUTATION
- MISSING_AUTHORITY
- MISSING_MODEL
- MISSING_PROOF
- MISSING_ARCHITECTURE
- MISSING_SYSTEM

## Multi-Mind evidence contract

A mind contributes a structured assessment containing:

CLAIM, ASSUMPTIONS, UNCERTAINTY, COUNTEREXAMPLES, and BLIND_SPOTS.

The value of multiple minds is epistemic diversity, not agent count. Their
assessments are evidence for later synthesis and attack.

## Impossibility Decomposer

NEXENT does not treat an IMPOSSIBLE claim as a final engineering result.
It decomposes the claim into possible sources:

PHYSICAL, COMPUTATIONAL, INFORMATIONAL, ECONOMIC, ARCHITECTURAL,
ONTOLOGICAL, GOVERNANCE, or UNKNOWN.

The result records bounds and unresolved unknowns. It does not claim that an
unknown obstacle has been overcome.

## System Hypothesis

A candidate system is represented by a stable SystemHypothesis containing:

- required capabilities/primitives
- required laws
- required data
- required interfaces
- proof obligations
- supporting evidence

The hypothesis is deliberately separate from deployment. Governance remains
the authority that can approve an evolution or deployment step.

## Self-application

NEXENT may audit its own capabilities using the same discovery model. A detected
NEXENT gap becomes an ordinary SystemHypothesis and must pass the same proof,
governance, and implementation boundaries as an external system.

## Non-goals

This layer does not:

1. grant itself new authority;
2. deploy a discovered system automatically;
3. treat language-model output as proof;
4. call every inconvenience a missing system;
5. claim physical or computational impossibilities have been defeated.

## Relationship to existing NEXENT layers

~~~text
MSD
  -> IR / graph representation
  -> architecture/compiler
  -> proof
  -> simulation
  -> governance
  -> runtime
~~~

The discovery layer therefore becomes a source of formally represented engineering
work rather than a separate product or an unbounded autonomous agent.
