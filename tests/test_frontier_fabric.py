from decimal import Decimal

from nexent.compute import FrontierComputationEngine
from nexent.frontier import FrontierFabric
from nexent.intelligence import OpenAIResponsesProvider, MultiMindCouncil


def test_linear_engine_is_deterministic():
    result = FrontierComputationEngine().solve_2x2(2, 1, 1, -1, 4, 1)
    assert result.x == Decimal(5) / Decimal(3)
    assert result.y == Decimal(2) / Decimal(3)
    assert abs(result.residual_1) < Decimal("1e-30")
    assert abs(result.residual_2) < Decimal("1e-30")


def test_physics_engine_is_exposed_through_frontier():
    fabric = FrontierFabric(MultiMindCouncil(), FrontierComputationEngine())
    output = fabric.simulate_physics({
        "initial": {
            "position": {"x": 0, "y": 0, "z": 0},
            "velocity": {"x": 0, "y": 0, "z": 0},
            "mass": 2,
        },
        "forces": [{"x": 2, "y": 0, "z": 0}],
        "dt": 1,
    })
    assert output["kind"] == "PHYSICAL_SIMULATION"
    assert output["result"]["velocity"]["x"] in {"1", "1.0"}


def test_missing_model_key_is_explicitly_unavailable(monkeypatch):
    monkeypatch.delenv("NEXENT_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIResponsesProvider(api_key=None)
    reply = provider.complete(role="system", instructions="test", prompt="hello")
    assert reply.status == "UNAVAILABLE"


def test_interface_manifest_exposes_model_and_domains():
    fabric = FrontierFabric(MultiMindCouncil(), FrontierComputationEngine())
    manifest = fabric.interfaces()
    assert "MATHEMATICAL" in manifest["layers"]
    assert manifest["http"]
    assert manifest["model"]["default_model"]
