# NEXENT Federated Repository Activation Matrix

This file is the control-plane registry for the currently identified NEXENT / VAIXLNS / VX repositories.

## Rules

1. Original repositories remain independent; integration is by provenance and explicit contracts.
2. A specification is not reported as executable until code and reproducible tests/evidence exist.
3. Every change must be traceable to a commit.
4. Unknown or missing components remain OPEN rather than being invented.
5. Verification state is evidence-based: SPECIFIED, IMPLEMENTED, TESTED, or BLOCKED.

## Repository roles

| Repository | Role | Current class | Activation requirement |
|---|---|---|---|
| fisallllll280-code/NEXENT | organizing/control fabric | IMPLEMENTED + TESTS | Python packaging + CI + Rust evidence lane |
| fisallllll280-code/VAIXLNS-unified | sovereign VX execution slice | IMPLEMENTED + TESTS | dependency closure + verification workflow |
| fisallllll280-code/vaixlns-core | constitutional computing vertical slice | IMPLEMENTED + TESTED (per repository docs) | reproduce dependency install/tests/runtime |
| fisallllll280-code/vaixlns-csd-kernel | VAIXLNS root constitution DSL | SPECIFIED | parser/compiler + executable validation |
| fisallllll280-code/VX-runtime | VX runtime contracts | SPECIFIED | implementation behind documented contracts |
| fisallllll280-code/VX50_COMPLETE_BUILD | VX build target | INCOMPLETE | recover missing source/evidence before activation |
| fisallllll280-code/VAIXLNS-Intent-to-Reality | intent-to-reality target | INCOMPLETE | recover missing source/evidence before activation |

## Cross-system contract

NEXENT controls inventory, provenance, normalization, canonicalization, impact analysis, and integration records.

VAIXLNS supplies constitutional verification, authorization, proof/evidence, ledger, replay, and governed execution concepts.

VX supplies the runtime execution boundary and deterministic replay contract.

No repository is silently merged or treated as a replacement for another.

## Activation gates

- G1: source inventory complete
- G2: dependency closure
- G3: tests execute
- G4: deterministic replay where applicable
- G5: evidence emitted
- G6: provenance recorded
- G7: specification/executable status is explicit

## Deferred material

Previously discussed concepts such as the full archive decomposition, canonical system IDs, evidence bundles, provenance registry, native NEXENT language layer, mathematical/computational/physical models, engineering drawings, and large-scale system inventory are tracked as integration targets. They are not claimed as implemented merely because they were discussed.
