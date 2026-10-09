"""Deterministic engineering drawing generation for NEXENT.

The module emits inspectable SVG, OpenSCAD and CadQuery source. It never executes
generated source and never equates generation with kernel or manufacturing proof.
"""
from __future__ import annotations

import ast
import hashlib
import html
import json
import math
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

ENGINE_VERSION = "0.1.0"
UNIT_TO_MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "in": 25.4}
ALLOWED_FORMATS = {"svg", "scad", "cadquery_py", "json"}
FUNCTIONS = {name: getattr(math, name) for name in ("sin", "cos", "tan", "sqrt", "log", "log10", "exp")}
FUNCTIONS["abs"] = abs
BINOPS = {ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod}
UNARY = {ast.UAdd, ast.USub}


class EngineeringDomain(str, Enum):
    MECHANICAL = "mechanical"
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    ARCHITECTURE = "architecture"
    ELECTRICAL = "electrical"
    CIVIL = "civil"


@dataclass(frozen=True)
class OpenSourceTool:
    tool_id: str
    purpose: str
    upstream_url: str
    integration_state: str
    execution_policy: str = "NO_AUTOMATIC_EXECUTION"


OPEN_SOURCE_TOOLS = (
    OpenSourceTool("freecad", "Parametric CAD and technical drawings", "https://github.com/FreeCAD/FreeCAD", "CATALOGUED"),
    OpenSourceTool("opencascade", "Boundary-representation geometry kernel", "https://github.com/Open-Cascade-SAS/OCCT", "CATALOGUED"),
    OpenSourceTool("cadquery", "Scriptable parametric CAD over OCCT", "https://github.com/CadQuery/cadquery", "SOURCE_EMITTER"),
    OpenSourceTool("openscad", "Script-based constructive solid geometry", "https://github.com/openscad/openscad", "SOURCE_EMITTER"),
    OpenSourceTool("kicad", "Electronic schematic and PCB design", "https://gitlab.com/kicad/code/kicad", "CATALOGUED"),
    OpenSourceTool("openfoam", "CFD and physics simulation", "https://gitlab.com/openfoam/core/openfoam", "CATALOGUED"),
    OpenSourceTool("blender", "Geometry processing and visual rendering", "https://github.com/blender/blender", "CATALOGUED"),
    OpenSourceTool("yt-dlp", "Video metadata and permitted subtitle retrieval", "https://github.com/yt-dlp/yt-dlp", "REFERENCE_ONLY"),
    OpenSourceTool("whisper", "Local timestamped speech transcription", "https://github.com/openai/whisper", "REFERENCE_ONLY"),
    OpenSourceTool("ffmpeg", "Media probing and frame extraction", "https://github.com/FFmpeg/FFmpeg", "REFERENCE_ONLY"),
)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _sha(value: str | bytes) -> str:
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(k): _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise ValueError("canonical records accept only JSON-like values")


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _thaw(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [_thaw(v) for v in value]
    return value


def _number(value: Any, label: str, limit: float = 1e9) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or abs(result) > limit:
        raise ValueError(f"{label} must be finite and within the supported range")
    return result


def _slug(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip()).strip("-_").lower()
    return (text or "engineering-drawing")[:72]


def _fmt(value: float) -> str:
    return format(float(value), ".12g")


@dataclass(frozen=True)
class DrawingRequest:
    request_id: str
    title: str
    domain: EngineeringDomain | str
    geometry: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    units: str = "mm"
    formats: tuple[str, ...] = ("svg", "scad")
    expression: str | None = None
    x_min: float = -10.0
    x_max: float = 10.0
    samples: int = 401
    assumptions: tuple[str, ...] = ()
    source_video_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.title.strip():
            raise ValueError("request_id and title are required")
        try:
            domain = self.domain if isinstance(self.domain, EngineeringDomain) else EngineeringDomain(self.domain)
        except ValueError as exc:
            raise ValueError(f"unsupported engineering domain: {self.domain}") from exc
        object.__setattr__(self, "domain", domain)
        if self.geometry not in {"box", "cylinder", "plate_with_holes", "formula_curve"}:
            raise ValueError(f"unsupported geometry: {self.geometry}")
        if self.units not in (*UNIT_TO_MM, "unitless"):
            raise ValueError("units must be mm, cm, m, in or unitless")
        formats = tuple(dict.fromkeys(str(v).lower() for v in self.formats))
        if not formats or set(formats) - ALLOWED_FORMATS:
            raise ValueError(f"unsupported formats: {sorted(set(formats) - ALLOWED_FORMATS)}")
        object.__setattr__(self, "formats", formats)
        object.__setattr__(self, "assumptions", tuple(self.assumptions))
        object.__setattr__(self, "source_video_ids", tuple(self.source_video_ids))
        if len(set(self.source_video_ids)) != len(self.source_video_ids) or any(not v.strip() for v in self.source_video_ids):
            raise ValueError("source_video_ids must be unique non-empty identifiers")
        params = dict(self.parameters)
        if self.geometry == "formula_curve":
            if domain not in {EngineeringDomain.MATHEMATICS, EngineeringDomain.PHYSICS}:
                raise ValueError("formula_curve requires mathematics or physics domain")
            if self.units != "unitless":
                raise ValueError("formula_curve needs unitless axes until dimension-aware equations are available")
            if not self.expression:
                raise ValueError("formula_curve requires an expression in x")
            if set(formats) - {"svg", "json"}:
                raise ValueError("formula_curve currently supports only SVG and JSON")
            if domain == EngineeringDomain.PHYSICS and "dimensionless" not in self.assumptions:
                raise ValueError("physics curves require the explicit dimensionless assumption")
            lo, hi = _number(self.x_min, "x_min"), _number(self.x_max, "x_max")
            if lo >= hi:
                raise ValueError("x_min must be less than x_max")
            if isinstance(self.samples, bool) or not isinstance(self.samples, int) or not 32 <= self.samples <= 2000:
                raise ValueError("samples must be an integer in range 32..2000")
            object.__setattr__(self, "x_min", lo)
            object.__setattr__(self, "x_max", hi)
            _parse_expression(self.expression)
        else:
            if domain != EngineeringDomain.MECHANICAL or self.units == "unitless":
                raise ValueError("solid primitives require the mechanical domain and physical units")
            required = {
                "box": {"width", "height", "depth"},
                "cylinder": {"diameter", "height"},
                "plate_with_holes": {"width", "height", "thickness", "hole_diameter", "holes"},
            }[self.geometry]
            if set(params) != required:
                raise ValueError(f"parameters must exactly match required fields: {sorted(required)}")
            for key in required - {"holes"}:
                value = _number(params[key], key)
                mm_value = value * UNIT_TO_MM[self.units]
                if value <= 0 or not 1e-6 <= mm_value <= 1e9:
                    raise ValueError(f"{key} must be positive and inside the supported mm range")
                params[key] = value
            if self.geometry == "plate_with_holes":
                width, height = float(params["width"]), float(params["height"])
                diameter = float(params["hole_diameter"])
                if diameter >= min(width, height):
                    raise ValueError("hole_diameter must be smaller than plate dimensions")
                holes = params["holes"]
                if not isinstance(holes, (list, tuple)) or not holes:
                    raise ValueError("holes must be a non-empty list of [x, y] centres")
                checked = []
                for i, point in enumerate(holes):
                    if not isinstance(point, (list, tuple)) or len(point) != 2:
                        raise ValueError(f"holes[{i}] must be an [x, y] pair")
                    x, y = _number(point[0], f"holes[{i}].x"), _number(point[1], f"holes[{i}].y")
                    if abs(x) + diameter / 2 > width / 2 or abs(y) + diameter / 2 > height / 2:
                        raise ValueError(f"holes[{i}] violate plate edge clearance")
                    checked.append((x, y))
                for i, a in enumerate(checked):
                    for b in checked[i + 1:]:
                        if math.dist(a, b) < diameter:
                            raise ValueError("hole clearances overlap")
                params["holes"] = tuple(checked)
        object.__setattr__(self, "parameters", _freeze(params))

    def to_dict(self) -> dict[str, Any]:
        return {"request_id": self.request_id, "title": self.title, "domain": self.domain.value,
                "geometry": self.geometry, "parameters": _thaw(self.parameters), "units": self.units,
                "formats": list(self.formats), "expression": self.expression, "x_min": self.x_min,
                "x_max": self.x_max, "samples": self.samples, "assumptions": list(self.assumptions),
                "source_video_ids": list(self.source_video_ids)}

    @property
    def fingerprint(self) -> str:
        return _sha(_canonical(self.to_dict()))


@dataclass(frozen=True)
class GeneratedArtifact:
    path: str
    format: str
    media_type: str
    content: str
    sha256: str
    status: str = "GENERATED_UNVERIFIED"
    static_checks: tuple[str, ...] = ()


@dataclass(frozen=True)
class DesignBundle:
    request: DrawingRequest
    artifacts: tuple[GeneratedArtifact, ...]
    manifest: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "manifest", _freeze(dict(self.manifest)))

    def manifest_json(self) -> str:
        return _canonical(_thaw(self.manifest))


class EngineeringDrawingAgent:
    """Generate canonical previews/source; external kernels are not executed."""

    def __init__(self, video_index: Any | None = None) -> None:
        self.video_index = video_index

    def generate(self, request: DrawingRequest) -> DesignBundle:
        contents = []
        slug = _slug(request.title)
        for fmt in request.formats:
            if fmt == "svg":
                data = _formula_svg(request) if request.geometry == "formula_curve" else _solid_svg(request)
                contents.append((slug + ".svg", fmt, data))
            elif fmt == "scad":
                contents.append((slug + ".scad", fmt, _scad(request)))
            elif fmt == "cadquery_py":
                contents.append((slug + "_cadquery.py", fmt, _cadquery(request)))
            elif fmt == "json":
                contents.append((slug + "_design.json", fmt, _canonical(_spec(request))))
        artifacts = []
        for path, fmt, data in contents:
            checks = _static_check(fmt, data)
            media_type = {"svg": "image/svg+xml", "scad": "text/plain", "cadquery_py": "text/x-python", "json": "application/json"}[fmt]
            artifacts.append(GeneratedArtifact(path, fmt, media_type, data, _sha(data), static_checks=checks))
        video_evidence, unresolved = [], []
        for source_id in request.source_video_ids:
            try:
                video = self.video_index.get(source_id) if self.video_index else None
            except KeyError:
                video = None
            if video is None:
                unresolved.append(source_id)
            else:
                video_evidence.append({"source_id": video.source_id, "title": video.title, "url": video.url,
                    "tool_id": video.tool_id, "language": video.language, "rights_basis": video.rights_basis,
                    "license_id": video.license_id, "upstream_repo": video.upstream_repo,
                    "upstream_revision": video.upstream_revision, "transcript_sha256": video.transcript_sha256,
                    "segments": [{"start_seconds": s.start_seconds, "end_seconds": s.end_seconds, "text": s.text,
                                  "source_refs": list(s.source_refs)} for s in video.segments]})
        manifest = {"schema": "nexent.engineering-drawing-bundle/v1", "engine_version": ENGINE_VERSION,
            "request_id": request.request_id, "request_fingerprint": request.fingerprint,
            "domain": request.domain.value, "geometry": request.geometry,
            "selected_tools": ["nexent-svg-renderer" if a.format == "svg" else
                               "openscad" if a.format == "scad" else
                               "cadquery" if a.format == "cadquery_py" else "nexent-canonical-spec" for a in artifacts],
            "artifacts": [{"path": a.path, "format": a.format, "sha256": a.sha256,
                           "status": a.status, "static_checks": list(a.static_checks)} for a in artifacts],
            "source_video_ids": list(request.source_video_ids), "video_evidence": video_evidence,
            "unresolved_video_ids": unresolved,
            "video_evidence_status": "INCOMPLETE" if unresolved else ("RESOLVED" if request.source_video_ids else "NOT_REQUESTED"),
            "external_kernel_validation": "NOT_RUN", "manufacturing_review": "NOT_RUN",
            "release_approval": "NOT_APPROVED",
            "blocked_claims": ["CAD kernel validation has not run", "material and tolerance suitability have not been assessed",
                               "manufacturing, safety and regulatory approval have not been granted"]}
        manifest["manifest_sha256"] = _sha(_canonical(manifest))
        return DesignBundle(request, tuple(artifacts), manifest)


def _mm(req: DrawingRequest, key: str) -> float:
    return float(req.parameters[key]) * UNIT_TO_MM[req.units]


def _spec(req: DrawingRequest) -> dict[str, Any]:
    if req.geometry == "formula_curve":
        params = {"expression": req.expression, "x_min": req.x_min, "x_max": req.x_max, "samples": req.samples}
        units = "unitless"
    elif req.geometry == "box":
        params = {k: _mm(req, k) for k in ("width", "height", "depth")}
        units = "mm"
    elif req.geometry == "cylinder":
        params = {k: _mm(req, k) for k in ("diameter", "height")}
        units = "mm"
    else:
        params = {k: _mm(req, k) for k in ("width", "height", "thickness", "hole_diameter")}
        params["holes"] = [[x * UNIT_TO_MM[req.units], y * UNIT_TO_MM[req.units]] for x, y in req.parameters["holes"]]
        units = "mm"
    return {"schema": "nexent.engineering-design/v1", "request_id": req.request_id,
            "title": req.title, "domain": req.domain.value, "geometry": req.geometry,
            "canonical_units": units, "parameters": params, "assumptions": list(req.assumptions),
            "source_video_ids": list(req.source_video_ids), "request_fingerprint": req.fingerprint}


def _scad(req: DrawingRequest) -> str:
    p, scale = req.parameters, UNIT_TO_MM[req.units]
    lines = ["// Generated by NEXENT Engineering Drawing Agent " + ENGINE_VERSION,
             "// " + req.title.replace("\n", " ").replace("//", "/ /"),
             "// canonical dimensions: millimetres", "$fn = 128;"]
    if req.geometry == "box":
        w, h, d = (_mm(req, k) for k in ("width", "height", "depth"))
        lines += [f"cube([{_fmt(w)}, {_fmt(h)}, {_fmt(d)}], center=true);"]
    elif req.geometry == "cylinder":
        lines += [f"cylinder(h={_fmt(_mm(req, 'height'))}, d={_fmt(_mm(req, 'diameter'))}, center=true, $fn=128);"]
    elif req.geometry == "plate_with_holes":
        w, h, t, hd = (_mm(req, k) for k in ("width", "height", "thickness", "hole_diameter"))
        holes = [[float(_fmt(x * scale)), float(_fmt(y * scale))] for x, y in p["holes"]]
        lines += [f"W={_fmt(w)}; H={_fmt(h)}; T={_fmt(t)}; HD={_fmt(hd)};",
                  "HOLES=" + json.dumps(holes, separators=(",", ":")) + ";",
                  "difference() {", "  cube([W,H,T], center=true);", "  for (p=HOLES) {",
                  "    translate([p[0],p[1],0]) cylinder(h=T+0.2,d=HD,center=true,$fn=128);",
                  "  }", "}"]
    else:
        raise ValueError("OpenSCAD output is not supported for formula curves")
    return "\n".join(lines) + "\n"


def _cadquery(req: DrawingRequest) -> str:
    p = req.parameters
    lines = ['"""Generated source. Run only in a pinned isolated CadQuery environment."""',
             "import cadquery as cq", "from cadquery import exporters"]
    if req.geometry == "box":
        lines.append("model = cq.Workplane('XY').box(" + ", ".join(_fmt(_mm(req, k)) for k in ("width", "height", "depth")) + ")")
    elif req.geometry == "cylinder":
        lines.append(f"model = cq.Workplane('XY').circle({_fmt(_mm(req, 'diameter') / 2)}).extrude({_fmt(_mm(req, 'height'))})")
    elif req.geometry == "plate_with_holes":
        w, h, t, hd = (_mm(req, k) for k in ("width", "height", "thickness", "hole_diameter"))
        holes = [[float(_fmt(x * UNIT_TO_MM[req.units])), float(_fmt(y * UNIT_TO_MM[req.units]))] for x, y in p["holes"]]
        lines += [f"model = cq.Workplane('XY').rect({_fmt(w)}, {_fmt(h)}).extrude({_fmt(t)})",
                  "model = model.faces('>Z').workplane().pushPoints(" + repr(holes) + f").hole({_fmt(hd)})"]
    else:
        raise ValueError("CadQuery output is not supported for formula curves")
    name = json.dumps(_slug(req.title))
    lines += [f"exporters.export(model, {name} + '.step')", f"exporters.export(model, {name} + '.stl')"]
    return "\n".join(lines) + "\n"


def _solid_svg(req: DrawingRequest) -> str:
    p = req.parameters
    if req.geometry == "box":
        width, front_h, side_w = (_mm(req, k) for k in ("width", "height", "depth"))
        top_h, side_h = side_w, front_h
        holes = ()
    elif req.geometry == "cylinder":
        width = side_w = _mm(req, "diameter")
        top_h, front_h, side_h = width, _mm(req, "height"), _mm(req, "height")
        holes = ()
    else:
        width, height, thickness, diameter = (_mm(req, k) for k in ("width", "height", "thickness", "hole_diameter"))
        top_h, side_w, front_h, side_h = height, height, thickness, thickness
        scale_units = UNIT_TO_MM[req.units]
        holes = tuple((x * scale_units, y * scale_units) for x, y in p["holes"])
    scale = min(390.0 / max(width, top_h, front_h, side_w, side_h), 5.0)
    W, TH, SW, FH, SH = width*scale, top_h*scale, side_w*scale, front_h*scale, side_h*scale
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">',
      "<title>" + html.escape(req.title) + "</title>",
      "<desc>Dimensioned orthographic concept preview. Not a manufacturing certification.</desc>",
      '<defs><marker id="a" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse"><path d="M0 0 L7 3.5 L0 7z" fill="#b45309"/></marker></defs>',
      '<rect width="100%" height="100%" fill="white"/>',
      f'<text x="48" y="42" font-family="sans-serif" font-size="24" font-weight="700">{html.escape(req.title)}</text>',
      '<text x="48" y="68" font-family="sans-serif" font-size="13" fill="#4b5563">Concept preview · canonical units: mm · unverified</text>']
    tx, ty, fx, fy, sx, sy = 90.0, 130.0, 90.0, 405.0, 700.0, 405.0
    out += [f'<text x="{tx}" y="105" font-size="17" font-weight="600">TOP VIEW</text>',
            f'<rect x="{tx}" y="{ty}" width="{W:.3f}" height="{TH:.3f}" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>']
    if req.geometry == "plate_with_holes":
        for x, y in holes:
            out.append(f'<circle cx="{tx+W/2+x*scale:.3f}" cy="{ty+TH/2-y*scale:.3f}" r="{diameter/2*scale:.3f}" fill="white" stroke="#b91c1c" stroke-width="2"/>')
    if req.geometry == "cylinder":
        out[-1] = f'<circle cx="{tx+W/2:.3f}" cy="{ty+TH/2:.3f}" r="{W/2:.3f}" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>'
    top_w = _mm(req, "width") if req.geometry in {"box", "plate_with_holes"} else _mm(req, "diameter")
    top_h_mm = (_mm(req, "height") if req.geometry == "plate_with_holes" else
                _mm(req, "depth") if req.geometry == "box" else _mm(req, "diameter"))
    out += _dimh(tx, tx+W, ty+TH+24, f"{top_w:g} mm") + _dimv(tx-25, ty, ty+TH, f"{top_h_mm:g} mm")
    out.append(f'<text x="{fx}" y="380" font-size="17" font-weight="600">FRONT VIEW</text>')
    out.append(f'<rect x="{fx}" y="{fy}" width="{W:.3f}" height="{FH:.3f}" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>')
    front_w = _mm(req, "width") if req.geometry != "cylinder" else _mm(req, "diameter")
    front_h_mm = _mm(req, "thickness") if req.geometry == "plate_with_holes" else _mm(req, "height")
    out += _dimh(fx, fx+W, fy+FH+24, f"{front_w:g} mm") + _dimv(fx-25, fy, fy+FH, f"{front_h_mm:g} mm")
    out.append(f'<text x="{sx}" y="380" font-size="17" font-weight="600">SIDE VIEW</text>')
    out.append(f'<rect x="{sx}" y="{sy}" width="{SW:.3f}" height="{SH:.3f}" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>')
    side_w_mm = (_mm(req, "height") if req.geometry == "plate_with_holes" else
                 _mm(req, "depth") if req.geometry == "box" else _mm(req, "diameter"))
    side_h_mm = _mm(req, "thickness") if req.geometry == "plate_with_holes" else _mm(req, "height")
    out += _dimh(sx, sx+SW, sy+SH+24, f"{side_w_mm:g} mm") + _dimv(sx-25, sy, sy+SH, f"{side_h_mm:g} mm")
    if req.geometry == "plate_with_holes":
        out.append(f'<text x="700" y="{sy+SH+66:.3f}" font-size="13" fill="#991b1b">Hole diameter: {diameter:g} mm · count: {len(holes)}</text>')
    out.append(f'<text x="1152" y="735" text-anchor="end" font-family="monospace" font-size="11" fill="#6b7280">request {html.escape(req.request_id)} · NEXENT {ENGINE_VERSION}</text>')
    out.append("</svg>")
    return "\n".join(out)


def _dimh(x1: float, x2: float, y: float, label: str) -> list[str]:
    m = (x1+x2)/2
    return [f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#b45309" marker-start="url(#a)" marker-end="url(#a)"/>',
            f'<text x="{m}" y="{y-7}" text-anchor="middle" font-size="12" fill="#92400e">{html.escape(label)}</text>']


def _dimv(x: float, y1: float, y2: float, label: str) -> list[str]:
    m = (y1+y2)/2
    return [f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#b45309" marker-start="url(#a)" marker-end="url(#a)"/>',
            f'<text x="{x-8}" y="{m}" text-anchor="end" font-size="12" fill="#92400e">{html.escape(label)}</text>']


def _parse_expression(expression: str) -> ast.Expression:
    if len(expression) > 240:
        raise ValueError("formula is too long")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("invalid arithmetic expression") from exc
    nodes = list(ast.walk(tree))
    if len(nodes) > 80:
        raise ValueError("formula is too complex")
    for node in nodes:
        if isinstance(node, ast.Expression):
            continue
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)) or not math.isfinite(float(node.value)) or abs(float(node.value)) > 1e12:
                raise ValueError("formula constants must be finite bounded numbers")
        elif isinstance(node, ast.Name):
            if node.id != "x" and node.id not in FUNCTIONS:
                raise ValueError(f"unknown formula symbol: {node.id}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in BINOPS:
                raise ValueError("unsupported binary operator")
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in UNARY:
                raise ValueError("unsupported unary operator")
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTIONS or len(node.args) != 1 or node.keywords:
                raise ValueError("only approved single-argument math functions are allowed")
        elif isinstance(node, (ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.UAdd, ast.USub)):
            continue
        else:
            raise ValueError(f"formula syntax not allowed: {type(node).__name__}")
    return tree


def _eval(node: ast.AST, x: float) -> float:
    if isinstance(node, ast.Expression):
        return _eval(node.body, x)
    if isinstance(node, ast.Constant):
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id == "x":
            return x
        raise ValueError("function name used as value")
    if isinstance(node, ast.UnaryOp):
        val = _eval(node.operand, x)
        return val if isinstance(node.op, ast.UAdd) else -val
    if isinstance(node, ast.BinOp):
        a, b = _eval(node.left, x), _eval(node.right, x)
        if isinstance(node.op, ast.Add): result = a+b
        elif isinstance(node.op, ast.Sub): result = a-b
        elif isinstance(node.op, ast.Mult): result = a*b
        elif isinstance(node.op, ast.Div):
            if abs(b) < 1e-14: raise ZeroDivisionError
            result = a/b
        elif isinstance(node.op, ast.Mod):
            if abs(b) < 1e-14: raise ZeroDivisionError
            result = a%b
        else:
            if abs(b) > 12: raise ValueError("formula exponent is capped at 12")
            result = a**b
    elif isinstance(node, ast.Call):
        result = FUNCTIONS[node.func.id](_eval(node.args[0], x))
    else:
        raise ValueError("unsupported AST node")
    try:
        result = float(result)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("formula result must be real-valued") from exc
    if not math.isfinite(result) or abs(result) > 1e12:
        raise ValueError("formula result outside supported range")
    return result


def _formula_svg(req: DrawingRequest) -> str:
    tree = _parse_expression(req.expression or "")
    xs = [req.x_min+(req.x_max-req.x_min)*i/(req.samples-1) for i in range(req.samples)]
    ys = []
    for x in xs:
        try: ys.append(_eval(tree, x))
        except (ArithmeticError, ValueError, OverflowError): ys.append(None)
    valid = [y for y in ys if y is not None]
    if len(valid) < 2:
        raise ValueError("formula has fewer than two finite samples")
    ymin, ymax = min(valid), max(valid)
    if math.isclose(ymin, ymax, abs_tol=1e-12): ymin, ymax = ymin-1, ymax+1
    pad = (ymax-ymin)*0.08
    ymin, ymax = ymin-pad, ymax+pad
    left, right, top, bottom = 76.0, 1140.0, 105.0, 650.0
    px = lambda x: left+(x-req.x_min)/(req.x_max-req.x_min)*(right-left)
    py = lambda y: bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">',
           "<title>"+html.escape(req.title)+"</title>",
           '<rect width="100%" height="100%" fill="white"/>',
           f'<text x="48" y="46" font-size="24" font-weight="700">{html.escape(req.title)}</text>',
           f'<text x="48" y="72" font-family="monospace" font-size="14">y = {html.escape(req.expression or "")}</text>',
           '<g stroke="#e5e7eb" stroke-width="1">']
    for i in range(9):
        x, y = left+(right-left)*i/8, top+(bottom-top)*i/8
        out += [f'<line x1="{x:.3f}" y1="{top}" x2="{x:.3f}" y2="{bottom}"/>',
                f'<line x1="{left}" y1="{y:.3f}" x2="{right}" y2="{y:.3f}"/>']
    out.append("</g>")
    if req.x_min <= 0 <= req.x_max:
        out.append(f'<line x1="{px(0):.3f}" y1="{top}" x2="{px(0):.3f}" y2="{bottom}" stroke="#6b7280"/>')
    if ymin <= 0 <= ymax:
        out.append(f'<line x1="{left}" y1="{py(0):.3f}" x2="{right}" y2="{py(0):.3f}" stroke="#6b7280"/>')
    segments, current = [], []
    for x, y in zip(xs, ys):
        if y is None:
            if current: segments.append(current); current=[]
        else:
            current.append(f"{px(x):.3f},{py(y):.3f}")
    if current: segments.append(current)
    for segment in segments:
        if len(segment) > 1:
            out.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
    out.append(f'<text x="1145" y="735" text-anchor="end" font-family="monospace" font-size="11">{len(valid)}/{len(xs)} finite samples · sampled plot, not symbolic proof</text>')
    out.append("</svg>")
    return "\n".join(out)


def _static_check(fmt: str, data: str) -> tuple[str, ...]:
    if fmt == "svg":
        root = ET.fromstring(data)
        if not root.tag.endswith("svg"):
            raise ValueError("output is not valid SVG")
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1].lower() == "script":
                raise ValueError("scripts are forbidden in generated SVG")
            for name, value in element.attrib.items():
                if name.rsplit("}", 1)[-1].lower() in {"href", "src"} and value.lower().startswith(("http:", "https:", "file:")):
                    raise ValueError("remote or file-linked assets are forbidden")
        return ("PASS: svg_xml_well_formed", "PASS: no_svg_script_or_external_asset")
    if fmt == "scad":
        pairs, stack, quote, escape = {")":"(", "]":"[", "}":"{"}, [], None, False
        for char in data:
            if quote:
                if escape: escape = False
                elif char == "\\": escape = True
                elif char == quote: quote = None
            elif char in {"'", '"'}: quote = char
            elif char in "([{": stack.append(char)
            elif char in ")]}":
                if not stack or stack.pop() != pairs[char]: raise ValueError("unbalanced SCAD source")
        if stack or quote: raise ValueError("unbalanced SCAD source")
        return ("PASS: scad_delimiters_balanced",)
    if fmt == "cadquery_py":
        ast.parse(data)
        return ("PASS: cadquery_python_syntax",)
    json.loads(data)
    return ("PASS: canonical_json_parses",)
