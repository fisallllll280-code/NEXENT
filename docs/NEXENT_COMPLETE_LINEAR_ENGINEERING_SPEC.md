# NEXENT — Complete Linear Engineering Specification

NEXENT is one engineering pipeline with explicit phase boundaries. Internal subsystems may operate in parallel, but promotion of the canonical system is linear and gated.

Canonical flow:

REQUIREMENTS -> MODEL -> ARCHITECTURE -> CONTRACTS -> IR -> IMPLEMENTATION -> VERIFICATION -> VALIDATION -> EVIDENCE -> GOVERNANCE -> RELEASE -> OPERATION -> EVOLUTION

Every phase emits identifiable artifacts. Artifacts are content-addressed by deterministic SHA-256 digests. A digest provides integrity and identity; it is not semantic proof.

Layer mapping:
- FOUNDATION: identity, canonical records, laws, invariants.
- KNOWLEDGE: observations, evidence, provenance, memory.
- DISCOVERY: capability voids, missing-system discovery, impossibility decomposition.
- REASONING: specialist perspectives, adversarial challenge, counterexamples, counterfactuals.
- SYNTHESIS: genome, architecture candidates, graph, dependencies.
- FORMAL ENGINEERING: contracts, IR, compiler, proof, verification, validation.
- FORGE: deterministic generation, packaging, system twin.
- GOVERNANCE: authority, safety, approval, change control.
- RUNTIME: execution, ledger, replay, monitoring, containment.
- EVOLUTION: self-audit and governed capability evolution.

Promotion law:
V(p_i) = true AND A(p_i) is non-empty AND every submitted artifact belongs to p_i. GOVERNANCE and RELEASE additionally require approval. No phase may be skipped.

Evidence law:
Evidence Pack integrity, test results, simulation output, proof obligations, and governance approval are separate evidence classes. None substitutes for another.

Execution law:
The system becomes executable only after RELEASE has been closed and the lifecycle has entered OPERATION. EVOLUTION is controlled post-release change, not a bypass.

Implementation:
nexent/engineering/formal_execution.py is the control-plane facade. It composes lifecycle and deterministic artifact handling without collapsing semantic subsystems into a monolith.
