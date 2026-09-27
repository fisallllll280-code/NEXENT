# NEXENT — Repository Federation & AI Agent Provider Fabric

## Repository boundary

NEXENT is the discovery/research/architecture-search engine in the VAIXLNS federation.

It may:

`DISCOVER → DESIGN → SEARCH → SIMULATE → ATTACK → PROVE → PROPOSE`

It must not silently mutate the VAIXLNS canonical surface.

## Provider boundary

AI models are registered as **agent workers**. The provider layer is deliberately
separate from canonical meaning, governance, and runtime authority.

```text
Engineering Task
    ↓
Multi-Mind Coordinator
    ↓
Agent Provider Registry
    ├── Anthropic Fable
    ├── Other remote providers
    └── Local providers
    ↓
Artifact + Evidence
    ↓
Tests / Verification / Proof
    ↓
Governance / Adoption
```

The supplied `https://claude-fable-5.md` reference is represented as an adapter
contract and model identifiers only. Its exact markdown contents are not copied
into the repository.

## Development loop

`DISCOVER → UNDERSTAND → PLAN → MODIFY → TEST → REVIEW → PROVE → GOVERN → COMMIT → OBSERVE → RECOVER`

Provider replacement must not require changes to the NEXENT or VAIXLNS
canonical contracts.

## Repository federation

Canonical project repositories:

- `VAIXLNS`: canonical registry, governance, architecture and lineage.
- `NEXENT`: discovery, architecture search and research.
- `VAIXLNS-unified`: executable projection.
- `vaixlns-core`: focused constitutional/core reference.
- `vaixlns-csd-kernel`: specialized kernel surface.
- `VAIXLNS-Intent-to-Reality`: intent boundary.
- `VX-runtime` / `VX50_COMPLETE_BUILD`: VX runtime/build surfaces.

Historical and unclassified repositories remain outside automatic mutation.
