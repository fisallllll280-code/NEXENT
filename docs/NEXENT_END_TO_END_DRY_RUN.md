# NEXENT End-to-End Dry Run

The canonical acceptance test is a single requirement propagated through the complete engineering spine.

Requirement -> Model -> Architecture -> Contract -> IR -> Implementation -> Verification -> Validation -> Evidence -> Governance -> Release -> Operation -> Evolution.

For each phase the run must:
1. create an artifact owned by the current phase;
2. compute its deterministic digest;
3. submit that artifact to the phase gate;
4. obtain verification acceptance;
5. obtain explicit approval at Governance and Release;
6. advance exactly one phase.

The dry run also attempts a zero-bypass transition with a missing artifact. The control plane must reject it before state mutation.

Acceptance conditions:
- all 12 promotion gates close;
- the lifecycle reaches EVOLUTION;
- execution is marked ready only after RELEASE/OPERATION progression;
- every recorded artifact has a digest;
- a foreign or missing artifact cannot close a gate.

This dry run is a control-plane test. It does not claim that the produced system is correct merely because the pipeline completes. Verification, validation, simulation, proof, security testing, and operational evidence remain separate obligations. This separation follows established systems-engineering practice; ISO/IEC/IEEE 29148 defines requirements engineering information and traceability, while ISO/IEC/IEEE 15288:2023 defines a common framework of system life-cycle processes. citeturn0search0turn0search5
