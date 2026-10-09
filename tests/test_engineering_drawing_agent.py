import json
import pytest

from nexent.agents.registry import AgentRegistry
from nexent.engineering.drawing_agent import (
    DrawingRequest, EngineeringDrawingAgent, OPEN_SOURCE_TOOLS
)
from nexent.engineering.drawing_specialists import register_engineering_drawing_specialists
from nexent.engineering.video_index import EngineeringVideo, VideoKnowledgeIndex, parse_vtt


def plate(**overrides):
    params = {"width": 100, "height": 60, "thickness": 8, "hole_diameter": 6,
              "holes": [(-35, -20), (35, -20), (-35, 20), (35, 20)]}
    values = dict(request_id="PLATE-001", title="Mounting plate", domain="mechanical",
                  geometry="plate_with_holes", parameters=params, units="mm",
                  formats=("svg", "scad", "cadquery_py", "json"))
    values.update(overrides)
    return DrawingRequest(**values)


def test_deterministic_bundle_hashes_and_release_boundary():
    agent = EngineeringDrawingAgent()
    a, b = agent.generate(plate()), agent.generate(plate())
    assert [(x.path, x.sha256) for x in a.artifacts] == [(x.path, x.sha256) for x in b.artifacts]
    assert all(x.status == "GENERATED_UNVERIFIED" for x in a.artifacts)
    assert a.manifest["external_kernel_validation"] == "NOT_RUN"
    assert a.manifest["release_approval"] == "NOT_APPROVED"
    assert json.loads(a.manifest_json())["manifest_sha256"]


def test_unit_conversion_is_canonical_millimetres():
    request = DrawingRequest("BOX-1", "Box", "mechanical", "box",
                             {"width": 1, "height": 2, "depth": 3},
                             units="cm", formats=("json",))
    spec = json.loads(EngineeringDrawingAgent().generate(request).artifacts[0].content)
    assert spec["parameters"] == {"width": 10, "height": 20, "depth": 30}
    assert spec["canonical_units"] == "mm"


def test_plate_clearance_rejects_edge_and_overlapping_holes():
    with pytest.raises(ValueError, match="edge clearance"):
        plate(parameters={"width": 100, "height": 60, "thickness": 8,
                          "hole_diameter": 6, "holes": [(48, 0)]})
    with pytest.raises(ValueError, match="overlap"):
        plate(parameters={"width": 100, "height": 60, "thickness": 8,
                          "hole_diameter": 6, "holes": [(-2, 0), (2, 0)]})


def test_dimensioned_projection_has_expected_plate_views():
    svg = EngineeringDrawingAgent().generate(plate(formats=("svg",))).artifacts[0].content
    assert "100 mm" in svg and "60 mm" in svg and "8 mm" in svg
    assert "Hole diameter: 6 mm" in svg and "count: 4" in svg
    assert 'width="234.000" height="31.200"' in svg
    assert "not certified" not in svg.lower()


@pytest.mark.parametrize("expression", [
    "__import__('os').system('false')", "x.__class__", "open(x)", "x**99", "(-1)**0.5", "1e999+x"
])
def test_formula_engine_rejects_unsafe_or_non_real_results(expression):
    req = DrawingRequest("MATH-1", "Unsafe", "mathematics", "formula_curve",
                         units="unitless", formats=("svg",), expression=expression)
    with pytest.raises(ValueError):
        EngineeringDrawingAgent().generate(req)


def test_formula_curve_is_sampled_and_svg_is_well_formed():
    req = DrawingRequest("MATH-2", "Parabola", "mathematics", "formula_curve",
                         units="unitless", formats=("svg", "json"),
                         expression="x**2 - 2*x", x_min=-3, x_max=3)
    bundle = EngineeringDrawingAgent().generate(req)
    assert "sampled plot, not symbolic proof" in bundle.artifacts[0].content
    assert "PASS: svg_xml_well_formed" in bundle.artifacts[0].static_checks


def test_physics_curve_needs_explicit_dimensionless_assumption():
    with pytest.raises(ValueError, match="dimensionless"):
        DrawingRequest("P-1", "Curve", "physics", "formula_curve",
                       units="unitless", formats=("svg",), expression="sin(x)")
    req = DrawingRequest("P-2", "Curve", "physics", "formula_curve",
                         units="unitless", formats=("svg",), expression="sin(x)",
                         assumptions=("dimensionless",))
    assert EngineeringDrawingAgent().generate(req).artifacts[0].status == "GENERATED_UNVERIFIED"


def test_video_index_keeps_timestamps_repository_and_transcript_hash():
    vtt = "WEBVTT\n\n00:00:01.000 --> 00:00:02.500\nUse OpenSCAD parameters.\n\n00:00:03.000 --> 00:00:04.000\nCheck the output mesh.\n"
    segments = parse_vtt(vtt, source_refs=("https://github.com/openscad/openscad",))
    video = EngineeringVideo("video-1", "OpenSCAD tutorial", "https://example.org/video",
                             "openscad", "en", "owner-authorized transcript indexing",
                             vtt, segments, upstream_repo="https://github.com/openscad/openscad",
                             upstream_revision="0123456789abcdef0123456789abcdef01234567")
    index = VideoKnowledgeIndex()
    index.add(video)
    hit = index.search("OpenSCAD parameters", tool_id="openscad")[0]
    assert hit.start_seconds == 1.0
    assert hit.source_refs == ("https://github.com/openscad/openscad",)
    assert len(hit.transcript_sha256) == 64


def test_video_index_requires_rights_basis_and_rejects_changed_source_identity():
    with pytest.raises(ValueError, match="rights_basis"):
        EngineeringVideo("x", "Video", "https://example.org/v", "openscad", "en", "", "", ())
    index = VideoKnowledgeIndex()
    index.add(EngineeringVideo("same-id", "A", "https://example.org/a", "openscad", "en", "authorized", "text", ()))
    with pytest.raises(ValueError, match="changed provenance"):
        index.add(EngineeringVideo("same-id", "B", "https://example.org/a", "openscad", "en", "authorized", "text", ()))


def test_missing_video_reference_is_explicitly_incomplete():
    req = plate(source_video_ids=("not-indexed",), formats=("json",))
    bundle = EngineeringDrawingAgent().generate(req)
    assert bundle.manifest["video_evidence_status"] == "INCOMPLETE"
    assert bundle.manifest["unresolved_video_ids"] == ("not-indexed",)


def test_specialist_roles_are_bounded_and_dependency_complete():
    registry = AgentRegistry()
    profiles = register_engineering_drawing_specialists(registry)
    assert len(profiles) == 7
    assert registry.validate_dependencies() == ()
    assert all(item.autonomy_level == "A0" and item.status.value == "DESIGN" for item in profiles)


def test_open_source_catalog_does_not_enable_automatic_execution():
    tools = {tool.tool_id: tool for tool in OPEN_SOURCE_TOOLS}
    assert tools["openscad"].integration_state == "SOURCE_EMITTER"
    assert tools["freecad"].integration_state == "CATALOGUED"
    assert all(tool.execution_policy == "NO_AUTOMATIC_EXECUTION" for tool in tools.values())


def test_parameters_and_manifest_are_recursively_immutable():
    holes = [[-35, -20], [35, 20], [-35, 20], [35, -20]]
    request = plate(parameters={"width": 100, "height": 60, "thickness": 8, "hole_diameter": 6, "holes": holes})
    fingerprint = request.fingerprint
    holes[0][0] = 999
    assert request.fingerprint == fingerprint
    bundle = EngineeringDrawingAgent().generate(request)
    with pytest.raises(TypeError):
        bundle.manifest["artifacts"][0]["status"] = "KERNEL_VALIDATED"
    with pytest.raises(TypeError):
        request.parameters["holes"][0][0] = 7
