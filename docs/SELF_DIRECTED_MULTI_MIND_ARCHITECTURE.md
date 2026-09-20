# SELF-DIRECTED MULTI-MIND ARCHITECTURE

## 1. Objective

Upgrade the federated index from a passive catalog into a governed self-directed coordination layer for planning, engineering, innovation, verification, execution, memory, and evolution across independent repositories.

The system is not granted unrestricted autonomy. Autonomy is bounded by explicit policies, capability scopes, evidence requirements, approval gates, and an append-only decision history.

## 2. Core model

```text
                    ┌──────────────────────────┐
                    │ CONSTITUTIONAL GOVERNANCE │
                    │ policies / permissions    │
                    └────────────┬─────────────┘
                                 │
┌──────────────┐   ┌──────────────▼─────────────┐   ┌──────────────┐
│ HUMAN INPUT  │──▶│ MULTI-MIND COORDINATOR     │◀──│ EVENT LEDGER │
└──────────────┘   │ task graph / arbitration    │   └──────────────┘
                   └──────┬─────────┬───────────┘
                          │         │
        ┌─────────────────┘         └─────────────────┐
        ▼                                             ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ PLANNER MIND  │ │ ENGINEER MIND │ │ INNOVATOR MIND│ │ MEMORY MIND   │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
        │                 │                 │                 │
        └─────────────────┬─────────────────┴─────────────────┘
                          ▼
                 ┌─────────────────┐
                 │ VERIFIER MIND   │
                 │ tests / proofs  │
                 └────────┬────────┘
                          ▼
                 ┌─────────────────┐
                 │ EXECUTOR MIND   │
                 │ bounded actions │
                 └────────┬────────┘
                          ▼
                 ┌─────────────────┐
                 │ OBSERVATION     │
                 │ results / drift │
                 └─────────────────┘
```

## 3. Mind responsibilities

- `PLANNER`: converts objectives into a dependency-aware task graph.
- `ENGINEER`: produces contracts, interfaces, architecture, and implementation plans.
- `INNOVATOR`: proposes alternatives and records novelty claims without treating them as proven.
- `VERIFIER`: challenges assumptions and attaches reproducible tests, proofs, simulations, or review evidence.
- `EXECUTOR`: performs only actions permitted by the capability and policy layers.
- `MEMORY`: records decisions, provenance, artifacts, failures, and lessons in durable storage.
- `COORDINATOR`: assigns work, merges compatible outputs, exposes disagreement, and resolves deadlocks through explicit rules.
- `GOVERNANCE`: enforces risk levels, approval requirements, isolation, rollback, and auditability.

## 4. Self-direction loop

```text
OBSERVE → INTERPRET → PLAN → DEBATE → VERIFY → AUTHORIZE → EXECUTE
   ▲                                                     │
   └────────────── RECORD → EVALUATE → ADAPT ────────────┘
```

The loop must be event-driven and replayable. No state critical to coordination may exist only in transient process memory.

## 5. Autonomy levels

| Level | Behavior | Required control |
|---|---|---|
| A0 | Suggestions only | Human review optional |
| A1 | Draft plans and files | Scope validation |
| A2 | Run tests and simulations | Sandboxed capabilities |
| A3 | Create bounded repository changes | Policy approval and rollback |
| A4 | Coordinate recurring maintenance | Monitoring and stop conditions |
| A5 | Cross-project evolution proposals | Human approval for consequential changes |

A level is earned through evidence; it is not inferred from the presence of an agent or model.

## 6. Shared work contract

Each task must include:

```yaml
task_id: TASK-<deterministic-id>
objective: explicit objective
assigned_minds: []
input_records: []
required_outputs: []
constraints: []
risk_level: LOW | MEDIUM | HIGH | CRITICAL
allowed_capabilities: []
acceptance_tests: []
approval_required: true
status: PLANNED | ACTIVE | BLOCKED | VERIFIED | REJECTED | COMPLETE
provenance: []
```

## 7. Arbitration rules

1. Prefer evidence-backed outputs over unsupported assertions.
2. Preserve disagreement as a first-class record; do not silently overwrite it.
3. Separate factual extraction, design proposals, implementation claims, and verification claims.
4. Require deterministic tie-breaking when outputs are otherwise equivalent.
5. Escalate unresolved high-risk conflicts to human approval.
6. Record the reason for every merge, rejection, rollback, or policy denial.

## 8. Safety and execution boundaries

- Least-privilege capability tokens.
- Repository and path allowlists.
- Dry-run before mutation when feasible.
- Mandatory test and diff inspection for generated changes.
- Rollback references for every mutation.
- Stop conditions for repeated failure, policy conflict, or unexpected scope expansion.
- No autonomous modification of secrets, access permissions, or irreversible external systems without explicit authorization.

## 9. Verification contract

A claim can progress through:

```text
ASSERTED → DESIGNED → IMPLEMENTED → TESTED → VERIFIED → APPROVED
```

Each transition must reference its evidence. Documentation alone cannot establish implementation or verification.

## 10. Initial implementation sequence

1. Add machine-readable mind, task, capability, policy, and decision schemas.
2. Implement a coordinator that emits events rather than mutating hidden state.
3. Add a deterministic task graph and dependency scheduler.
4. Add isolated mind adapters with a common contract.
5. Add verifier gates and evidence registration.
6. Add bounded repository execution with diff and rollback metadata.
7. Generate human-readable reports and machine-readable snapshots.
8. Add replay tests proving that the same event history produces the same coordination state.

## 11. Definition of done

The architecture is considered operational only when it demonstrates:

- deterministic task creation and replay;
- explicit capability enforcement;
- multiple independent mind outputs;
- recorded disagreement and arbitration;
- evidence-linked verification;
- bounded execution with rollback metadata;
- reproducible tests in CI;
- a complete audit trail from objective to observed result.

## 12. Current status

`DESIGN / ARCHITECTURAL SPECIFICATION`

This document defines the target architecture. It does not claim that all listed minds, autonomy levels, or execution controls are already implemented.
