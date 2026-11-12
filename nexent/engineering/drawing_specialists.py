"""Register A0 bounded engineering drawing specialists in the NEXENT registry."""


def register_engineering_drawing_specialists(registry=None):
    """Register typed specialist profiles; external tool adapters remain disabled."""
    from ..agents.registry import AgentProfile, AgentRegistry, AgentStatus

    registry = registry if registry is not None else AgentRegistry()
    profiles = (
        AgentProfile("ENG-ARCHITECT", "ENGINEERING_ARCHITECT", "decompose requests into contracts and constraints",
                     capabilities=("engineering_plan", "constraint_schema"), consumes=("drawing_request",),
                     produces=("drawing_plan",), status=AgentStatus.DESIGN, autonomy_level="A0"),
        AgentProfile("ENG-MATHEMATICS", "MATHEMATICS", "validate bounded equations and numeric domains",
                     capabilities=("formula_validation", "formula_curve_svg"), consumes=("equation", "numeric_domain"),
                     produces=("formula_preview",), requires_agents=("ENG-ARCHITECT",),
                     status=AgentStatus.DESIGN, autonomy_level="A0"),
        AgentProfile("ENG-PHYSICS", "PHYSICS", "review dimensional assumptions before simulation",
                     capabilities=("unit_review", "physical_assumption_review"), consumes=("physical_parameters",),
                     produces=("physics_review",), requires_agents=("ENG-ARCHITECT",),
                     status=AgentStatus.DESIGN, autonomy_level="A0"),
        AgentProfile("ENG-CAD", "CAD_ENGINEER", "emit editable parametric CAD source and dimensioned previews",
                     capabilities=("parametric_cad", "dimensioned_svg", "openscad_generation", "cadquery_source"),
                     consumes=("drawing_plan", "validated_parameters"), produces=("cad_source", "svg_preview"),
                     requires_agents=("ENG-ARCHITECT",), status=AgentStatus.DESIGN, autonomy_level="A0"),
        AgentProfile("ENG-VIDEO", "ENGINEERING_VIDEO_RESEARCH", "index permitted transcripts with timestamps and provenance",
                     capabilities=("video_transcript_index", "timestamp_retrieval", "source_trace"),
                     consumes=("video_url", "subtitle_text", "rights_basis"), produces=("video_evidence",),
                     requires_agents=("ENG-ARCHITECT",), status=AgentStatus.DESIGN, autonomy_level="A0"),
        AgentProfile("ENG-CRITIC", "ENGINEERING_CRITIC", "challenge constraints and unsupported design claims",
                     capabilities=("constraint_review", "contradiction_detection"), consumes=("cad_source", "drawing_plan"),
                     produces=("review_findings",), requires_agents=("ENG-CAD",),
                     status=AgentStatus.DESIGN, autonomy_level="A0"),
        AgentProfile("ENG-VERIFIER", "ENGINEERING_VERIFIER", "run static checks and build a hash-linked evidence bundle",
                     capabilities=("static_validation", "artifact_hashing", "evidence_manifest"),
                     consumes=("cad_source", "svg_preview", "review_findings"), produces=("verification_bundle",),
                     requires_agents=("ENG-CAD", "ENG-CRITIC"), status=AgentStatus.DESIGN, autonomy_level="A0"),
    )
    known = {agent.agent_id for agent in registry.all()}
    for profile in profiles:
        if profile.agent_id not in known:
            registry.register(profile)
    errors = registry.validate_dependencies()
    if errors:
        raise ValueError("engineering specialist registry has unresolved dependencies: " + "; ".join(errors))
    return profiles
