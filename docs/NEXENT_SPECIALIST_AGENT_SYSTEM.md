# NEXENT SPECIALIST AGENT SYSTEM

## Purpose

NEXENT does not use a pool of generic agents. It uses specialist agents whose identity, mission, inputs, outputs, capabilities, dependencies, autonomy level, and evidence obligations are explicit.

## Agent classes

| Agent | Primary responsibility | Produces |
|---|---|---|
| ARCHITECT | system structure and contracts | architecture contracts |
| PLANNER | dependency-aware task decomposition | task graphs |
| ENGINEER | implementation design and code changes | implementation artifacts |
| MATHEMATICS | equations, invariants, formal models | mathematical evidence |
| PHYSICS | physical models and simulations | physical-state evidence |
| DATA | operational data schemas and lineage | data contracts |
| VERIFIER | tests, proofs, simulations, review evidence | verification bundles |
| INNOVATOR | alternatives and novelty records | candidate innovations |
| MEMORY | provenance, decisions, failures, lessons | durable records |
| GOVERNANCE | permissions, risk, approval and rollback | policy decisions |
| EXECUTOR | bounded actions only | execution results |
| VAN | visual architecture and engineering handoff | visual blueprints |
| CRITIC | adversarial review and contradiction detection | review findings |
| EVOLUTION | controlled improvement proposals | evolution proposals |

These are roles, not claims of consciousness. A role may be implemented by deterministic software, a model adapter, or a combination of tools.

## The important distinction

A generic agent asks: What should I do?

A NEXENT specialist asks:

1. What is my mission?
2. What evidence may I consume?
3. What outputs am I authorized to produce?
4. Which capabilities may I invoke?
5. Which specialists must precede me?
6. What acceptance tests apply?
7. What evidence must I leave behind?
8. What actions are forbidden?

## VAN enablement path

VAN is fed structured outputs rather than unbounded prose:

    ARCHITECT + MATHEMATICS + PHYSICS + DATA + ENGINEER
                         |
                         v
               VERIFIED SYSTEM CONTRACT
                         |
                         v
                        VAN
                         |
                         v
                 VISUAL BLUEPRINT
                         |
                         v
                COMPONENT HANDOFF
                         |
                         v
                    FRONTEND
                         |
                         v
                 RUNTIME OBSERVATION
                         |
                         v
                   CRITIC/VERIFIER
                         |
                         +----> VAN FEEDBACK

Thus VAN learns from relations between specification, implementation, runtime state and verification, not merely from screenshots.

## Agent contract

Every specialist is represented by a machine-readable profile containing:

- stable agent_id;
- role and mission;
- allowed capabilities;
- input and output record types;
- required specialist dependencies;
- autonomy level;
- lifecycle status.

The registry rejects duplicate identities, invalid autonomy levels, and duplicate capability declarations. Dependencies are validated before coordination.

## Coordination rule

The coordinator should schedule specialists by dependency and evidence flow, not by arbitrary agent count. Multiple specialists may work in parallel when their input sets are independent; dependent work waits for the required records.

## Capability boundary

Agent identity never grants permission. Capabilities are explicitly checked. High-impact external execution, secrets, access-control changes, irreversible operations, and consequential financial actions remain outside implicit agent authority and require the applicable governance and authorization path.

## Status

UNDER DEVELOPMENT — SPECIALIST REGISTRY IMPLEMENTED; FULL COORDINATOR AND ADAPTER NETWORK REMAIN TARGET WORK.
