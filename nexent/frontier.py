from __future__ import annotations

from dataclasses import dataclass

from .compute import FrontierComputationEngine
from .intelligence import MultiMindCouncil


@dataclass(frozen=True)
class FrontierFabric:
    council: MultiMindCouncil
    compute: FrontierComputationEngine

    def interfaces(self) -> dict:
        return {
            "name": "NEXENT Frontier Fabric",
            "layers": [
                "INTELLIGENCE",
                "RESEARCH",
                "ARCHITECTURE",
                "MATHEMATICAL",
                "COMPUTATIONAL",
                "PHYSICAL",
                "VERIFICATION",
                "GOVERNANCE_HANDOFF",
            ],
            "http": [
                "GET /health",
                "GET /v1/interfaces",
                "POST /v1/think",
                "POST /v1/engineer",
                "POST /v1/compute/linear2x2",
                "POST /v1/simulate/physics",
            ],
            "model": {
                "provider": "openai",
                "default_model_env": "NEXENT_OPENAI_MODEL",
                "default_model": self.council.fabric.provider.model,
                "api_env": "NEXENT_OPENAI_API_KEY or OPENAI_API_KEY",
            },
        }

    def think(self, problem: str, roles=None) -> dict:
        return self.council.deliberate(problem, roles=roles).public()

    def engineer(self, problem: str, roles=None) -> dict:
        result = self.council.deliberate(problem, roles=roles)
        synthesis = result.synthesis.public() if result.synthesis else None
        return {
            "kind": "ARCHITECTURE_CANDIDATE",
            "status": "MODEL_UNAVAILABLE" if not synthesis else "GENERATED",
            "problem": problem,
            "multi_mind": result.public(),
            "next_gates": [
                "COUNTERFACTUAL_SIMULATION",
                "ADVERSARIAL_ATTACK",
                "VERIFICATION",
                "PROOF",
                "VAIXLNS_GOVERNANCE",
            ],
        }

    def simulate_physics(self, scenario: dict) -> dict:
        return self.compute.simulate_physics(scenario)

    def solve_linear2x2(self, payload: dict) -> dict:
        result = self.compute.solve_2x2(
            payload["a"], payload["b"], payload["c"], payload["d"], payload["y1"], payload["y2"]
        )
        return {"kind": "MATHEMATICAL_SOLUTION", "deterministic": True, "result": result.public()}
