# NEXENT Engineering Drawing Agent — v0.1

## Purpose and boundary

The engineering drawing agent converts a structured request into repeatable, inspectable output: dimensioned SVG previews, editable parametric source for supported solids, canonical JSON and a SHA-256 evidence manifest. It is a bounded generation capability for NEXENT. It does not certify the result or bypass VX/VAIXLNS release governance.

## Pipeline

    INDEX / REQUIREMENT
            |
      ENG-ARCHITECT
            |
      MATHEMATICS / PHYSICS / VIDEO
            |
      ENG-CAD / VAN
            |
      STATIC CHECKS + CONTENT HASHES
            |
      ENG-CRITIC -> ENG-VERIFIER
            |
      VX ADMISSION / EXTERNAL KERNEL / REVIEW
            |
      RELEASE ONLY WHEN POLICY PASSES

Specialist profiles are registered in DESIGN with autonomy A0. Their existence is not proof that external applications or model adapters have been started.

## Supported deterministic slice

- Mechanical primitives: box, cylinder, plate with circular holes.
- Formula curve: one-variable arithmetic expression plotted over a finite range.
- Outputs: SVG, OpenSCAD source, CadQuery Python source, canonical JSON.
- Units: mm, cm, m or inches are normalized to millimetres for solid geometry.
- Validation: finite bounded numeric values, positive dimensions, plate edge/hole spacing, formula AST allow-list, balanced generated SCAD delimiters, Python syntax parse for CadQuery source, well-formed SVG without scripts or external assets, and SHA-256 manifest.
- The formula curve uses dimensionless axes in this version. Physics-domain curves require the explicit dimensionless assumption. A sampled plot is not a symbolic proof.

## Open-source adapters and current status

| Tool | Purpose | State in this slice |
|---|---|---|
| [FreeCAD](https://github.com/FreeCAD/FreeCAD) | Parametric CAD and engineering drawings | Catalogued; not executed |
| [Open CASCADE](https://github.com/Open-Cascade-SAS/OCCT) | Geometry kernel | Catalogued; not executed |
| [CadQuery](https://github.com/CadQuery/cadquery) | Scriptable parametric CAD | Source emitter only |
| [OpenSCAD](https://github.com/openscad/openscad) | Script-based constructive geometry | Source emitter only |
| [KiCad](https://gitlab.com/kicad/code/kicad) | Schematics and PCB | Catalogued; no generator yet |
| [OpenFOAM](https://gitlab.com/openfoam/core/openfoam) | CFD/physics simulation | Catalogued; no simulation adapter yet |
| [Blender](https://github.com/blender/blender) | Visualization/geometry tools | Catalogued; not executed |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Video metadata/subtitles | Reference only; caller-managed |
| [Whisper](https://github.com/openai/whisper) | Local transcription | Reference only; caller-managed |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Media probing and frame extraction | Reference only; caller-managed |

Cataloguing a tool does not authorize running its code. A future adapter must pin the tool revision and container image, review licenses, create an SBOM, enforce CPU/memory/time limits, run in isolation, and retain logs.

## Linking engineering drawings to videos and source repositories

The video index accepts subtitle text supplied by the operator in WebVTT. It retains cue start/end seconds, transcript SHA-256, a video URL, an explicit rights basis, tool identity, upstream repository, upstream revision and source refs. Search returns the matching cue with a timestamp, not just a generic video link.

Suggested evidence chain:

1. Find an upstream tool/repository and pin the exact release or commit.
2. Select a video/tutorial whose subtitles the operator is permitted to index.
3. Provide the authorized WebVTT text to VideoKnowledgeIndex.
4. Query the index and attach selected source IDs to DrawingRequest.
5. Include time-coded segments, provenance and transcript digest in the drawing manifest.
6. Have ENG-CRITIC compare the tutorial's version and guidance to upstream documentation/tests.
7. Require independent kernel validation and VX authorization before treating geometry as approved.

Public accessibility alone is not a reuse license. A tag such as main/master is mutable and is not a proof-grade source revision. Use commit-pinned permalinks where available. This component does not download media, bypass access controls, or determine copyright permissions.

## Local example

    from nexent.engineering.drawing_agent import DrawingRequest, EngineeringDrawingAgent

    request = DrawingRequest(
        request_id="PLATE-001",
        title="Mounting plate",
        domain="mechanical",
        geometry="plate_with_holes",
        parameters={
            "width": 100, "height": 60, "thickness": 8,
            "hole_diameter": 6,
            "holes": [(-35, -20), (35, -20), (-35, 20), (35, 20)],
        },
        units="mm",
        formats=("svg", "scad", "cadquery_py", "json"),
    )
    bundle = EngineeringDrawingAgent().generate(request)
    print(bundle.manifest_json())

Generated code is never executed by the generator. Run external validators only in a pinned, isolated worker and record the exact tool version, command, stdout/stderr, exit code and resulting geometry digest.

## Non-skippable status boundary

Current generated artifacts are GENERATED_UNVERIFIED; external kernel validation and release approval are NOT_RUN / NOT_APPROVED. SVG parsing or generated-source syntax checks do not prove geometry validity, tolerance stack-up, material suitability, structural strength, manufacturability, electrical safety, regulatory compliance or fitness for life-safety use.

## Required next gates

- Isolated adapters to OpenSCAD/CadQuery/FreeCAD with pinned versions and resource limits.
- CAD-kernel solid validity, round-trip STEP/STL exports and golden-model comparisons.
- Property-based tests for geometry boundaries and dimensional invariants.
- GD&T, assemblies, electrical/PCB, BIM and FEA/CFD adapters as separate domain-specific work.
- Commit-pinned source lineage, license/security scan and SBOM.
- Independent engineering review and VX evidence-gated admission.
