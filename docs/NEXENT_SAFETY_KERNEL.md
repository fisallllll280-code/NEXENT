# NEXENT Safety Kernel

## Purpose

The safety kernel is a containment boundary beneath higher-level reasoning.
Its job is not to decide what the system should want. Its job is to prevent
unverified or out-of-bound transitions from becoming executable transitions.

## Core rule

```
PROPOSE
  ↓
IMPACT CONE
  ↓
VERIFY
  ↓
CONTAINMENT CHECK
  ├── PASS → governed execution path
  └── FAIL → QUARANTINE
```

The containment engine is deliberately deterministic, fail-closed, and
independent of language-model output.

## Multiple barriers

Safety is not a single check. A robust architecture uses independent barriers:
boundary constraints, invariant checks, verification evidence, quarantine,
and recovery/halting states. This follows the systems-engineering principle of
defense in depth: loss control should not rely on one defensive element.

NIST SP 800-160 describes protective failure/recovery and defense in depth as
engineering principles for trustworthy systems.

## Important boundary

Containment does not grant authority and does not deploy changes. Governance
remains the authorization layer. The safety kernel only answers whether a
transition satisfies its declared mechanical constraints.

## Next integration

The containment decision should become an input to:
- proof obligations
- counterfactual simulation
- governance
- runtime execution
- immutable audit/ledger

No component should silently bypass this boundary.
