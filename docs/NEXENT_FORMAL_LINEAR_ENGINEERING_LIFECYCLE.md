# NEXENT — Formal Linear Engineering Lifecycle

NEXENT is executed as a gated engineering sequence:

1. REQUIREMENTS
2. MODEL
3. ARCHITECTURE
4. CONTRACTS
5. IR
6. IMPLEMENTATION
7. VERIFICATION
8. VALIDATION
9. EVIDENCE
10. GOVERNANCE
11. RELEASE
12. OPERATION
13. EVOLUTION

A transition is valid only when the current phase is verified. Governance and release additionally require explicit approval. Skipping and backward mutation are rejected by the lifecycle controller.

Formal state: S = (p, C, G), where p is the active phase, C is the completed phase sequence, and G is the immutable gate history. A valid transition is p_i -> p_{i+1} with verification(p_i)=true and all required artifacts identified. This gives NEXENT a linear control plane while keeping semantics, IR, compiler, proof, evidence, and runtime as separate engineering layers.

Traceability, lifecycle engineering, and the distinction between verification and validation are aligned with established systems-engineering practice such as ISO/IEC/IEEE 29148 and 15288. Architecture description and architecture processes are treated as explicit engineering artifacts, consistent with ISO/IEC/IEEE 42010/42020. citeturn0search0turn0search1turn0search2turn0search8

Non-negotiable evidence boundaries:
- GENERATED != VERIFIED
- TESTED != PROVEN
- SIMULATED != PHYSICALLY VALIDATED
- HASH INTEGRITY != SYSTEM CORRECTNESS
