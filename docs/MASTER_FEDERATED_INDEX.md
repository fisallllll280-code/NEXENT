# MASTER FEDERATED INDEX

## 0. Purpose

This document is the single navigational index for the large project ecosystem. It does not merge repositories into one implementation and does not replace their source files. It creates a stable federated map linking projects, systems, innovations, files, evidence, dependencies, and lifecycle states.

## 1. Governing rule

> One federated index, many independent projects, one traceable identity model.

The index must distinguish:

- `SOURCE_ASSERTED` — stated by an existing document or archive.
- `DESIGN` — architectural specification.
- `PROPOSED` — future candidate.
- `IMPLEMENTED` — present in source code.
- `TESTED` — supported by reproducible tests.
- `VERIFIED` — supported by explicit verification evidence.
- `TARGET` — intended future state.
- `DUPLICATE` — mapped to an existing canonical record.
- `CONFLICT` — conflicting definitions requiring resolution.

No item may be marked `VERIFIED` solely because it appears in a document.

## 2. Federated project registry

| Project ID | Project / Repository | Primary role | Registry status |
|---|---|---|---|
| `PRJ-VX` | `fisallllll280-code/VX-runtime` | Governed execution runtime | To be audited continuously |
| `PRJ-NEXENT` | `fisallllll280-code/NEXENT` | Organization, indexing, governance and system fabric | Active knowledge/design hub |
| `PRJ-VAIXLNS` | `fisallllll280-code/VAIXLNS` | Large-scale architecture and knowledge ecosystem | To be classified by evidence |
| `PRJ-VAIXLNS-CORE` | `fisallllll280-code/vaixlns-core` | Core architecture and verification rules | To be classified by evidence |
| `PRJ-CSD` | `fisallllll280-code/vaixlns-csd-kernel` | Root structure and constitutional definitions | To be classified by evidence |
| `PRJ-UNIFIED` | `fisallllll280-code/VAIXLNS-unified` | Unified architecture and execution concepts | To be classified by evidence |
| `PRJ-INTENT` | `fisallllll280-code/VAIXLNS-Intent-to-Reality` | Intent-to-engineering direction | To be classified by evidence |
| `PRJ-VX50` | `fisallllll280-code/VX50_COMPLETE_BUILD` | VX build/archive material | To be classified by evidence |

This registry is a navigational baseline, not a claim that every listed repository is operationally complete.

## 3. Canonical record model

Every indexed object receives one stable record:

```yaml
record_id: SYS-VX-EXEC-001
record_type: SYSTEM
canonical_name: Example System
project_ids:
  - PRJ-VX
repository: fisallllll280-code/VX-runtime
source_paths:
  - path/to/source-or-document
role: execution
status: DESIGN
implementation_state: UNKNOWN
verification_state: UNVERIFIED
parent_records: []
child_records: []
related_records: []
depends_on: []
provides: []
conflicts_with: []
merged_into: null
provenance:
  source_type: repository
  source_ref: commit-or-file-reference
  extracted_at: YYYY-MM-DD
 evidence:
  tests: []
  proofs: []
  simulations: []
  reviews: []
```

## 4. Unified classification tree

```text
MASTER INDEX
├── PROJECTS
├── SYSTEMS
├── SUBSYSTEMS
├── ENGINES
├── PROTOCOLS
├── LANGUAGES / DSLs
├── TOOLS
├── INNOVATIONS
├── MODELS / THEORIES
├── INTERFACES / ADAPTERS
├── DEPENDENCIES
├── EVIDENCE / TESTS / SIMULATIONS
├── FILES / SOURCES
├── VERSIONS / EVOLUTION
├── CONFLICTS / DUPLICATES
└── DEPLOYMENT / OPERATING TARGETS
```

## 5. Indexing pipeline

```text
DISCOVER
  → EXTRACT
  → NORMALIZE
  → ASSIGN ID
  → CLASSIFY
  → LINK SOURCES
  → DETECT DUPLICATES
  → DETECT CONFLICTS
  → MAP DEPENDENCIES
  → ATTACH EVIDENCE
  → VERIFY STATUS
  → PUBLISH INDEX SNAPSHOT
```

## 6. Relationship types

- `CONTAINS` — project contains a system or document.
- `IMPLEMENTS` — source code implements a specification.
- `SPECIFIES` — document defines an intended behavior.
- `DEPENDS_ON` — item requires another item.
- `PROVIDES_CAPABILITY` — item exposes a capability.
- `INTEGRATES_WITH` — two systems communicate through a defined boundary.
- `EVOLVES_FROM` — later record derives from an earlier record.
- `DUPLICATES` — equivalent or repeated record.
- `CONFLICTS_WITH` — definitions or identifiers disagree.
- `EVIDENCED_BY` — claim is linked to test, proof, simulation, or artifact.
- `HOSTED_BY` — runtime is carried by an environment or substrate.

## 7. Source-of-truth policy

The federated index is the source of truth for **identity and navigation**. The original repository remains the source of truth for each implementation or document. The evidence register is the source of truth for verification claims.

Therefore:

```text
INDEX IDENTITY ≠ IMPLEMENTATION SOURCE ≠ VERIFICATION EVIDENCE
```

## 8. Duplicate and conflict handling

1. Never silently delete a record.
2. Preserve the original source reference.
3. Create a conflict or duplicate relation.
4. Select a canonical record only after comparison.
5. Keep aliases and former identifiers searchable.
6. Record the decision and its provenance.

## 9. Lifecycle states

```text
RECOVERED
  → NORMALIZED
  → CLASSIFIED
  → DESIGNED
  → IMPLEMENTED
  → TESTED
  → VERIFIED
  → APPROVED
  → DEPLOYED
  → OBSERVED
  → EVOLVED
```

A record may remain in `DESIGN`, `PROPOSED`, `CONFLICT`, or `UNVERIFIED`; the index must not force every record into an implementation state.

## 10. Operating and development integration

The index is designed to connect with the operating/development layer:

```text
MASTER INDEX
   ↓
SYSTEM REGISTRY
   ↓
CONTRACTS + DEPENDENCIES
   ↓
OPERATING COORDINATION
   ↓
DEVELOPMENT PLAN
   ↓
TEST / SIMULATION
   ↓
VERIFICATION
   ↓
VERSIONED INDEX UPDATE
```

## 11. Initial implementation boundary

The next executable stages are:

1. Define machine-readable record schema.
2. Build repository and file inventory extraction.
3. Generate deterministic IDs and aliases.
4. Build relationship and dependency tables.
5. Add evidence references and verification states.
6. Detect duplicate names and identifier collisions.
7. Generate Markdown and machine-readable index snapshots.
8. Validate that every indexed source points to an existing repository path or explicitly marked historical source.

## 12. Integrity rules

- No unreferenced canonical record.
- No duplicate canonical ID.
- No verification claim without evidence reference.
- No implementation claim based only on a README.
- No deletion of historical provenance.
- Deterministic ordering for generated indexes.
- Every change produces a versioned diff.
- Every conflict remains visible until resolved.

## 13. Current status

`DESIGN / FEDERATED INDEX FOUNDATION`

This file establishes the unified indexing contract. It is not yet a generated exhaustive inventory of every file and every innovation across all repositories. Exhaustive coverage requires a repeatable extraction and verification pipeline.
