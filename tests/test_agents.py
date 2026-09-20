from nexent.agents import AgentProfile, AgentRegistry

def test_registry_orders_agents_deterministically_and_validates_dependencies():
    registry = AgentRegistry()
    registry.register(AgentProfile("van", "VISUAL_ARCHITECT", "Translate verified system contracts into visual blueprints", ("visualize",), produces=("visual_blueprint",), requires_agents=("math",)))
    registry.register(AgentProfile("math", "MATHEMATICS", "Validate mathematical structures", ("math.verify",), produces=("math_evidence",)))
    assert [a.agent_id for a in registry.all()] == ["math", "van"]
    assert registry.validate_dependencies() == ()

def test_registry_rejects_missing_dependency_and_capability():
    registry = AgentRegistry()
    registry.register(AgentProfile("van", "VISUAL_ARCHITECT", "Design visual contracts", ("visualize",), requires_agents=("missing",)))
    assert registry.validate_dependencies() == ("van: missing dependency missing",)
    try:
        registry.require_capabilities(["van"], ["execute.external"])
    except PermissionError as exc:
        assert "execute.external" in str(exc)
    else:
        raise AssertionError("expected capability denial")
