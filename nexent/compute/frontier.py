from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from typing import Mapping

from ..model import digest
from ..physics import PhysicalState, PhysicsEngine, Vector3

getcontext().prec = 40


def _d(value) -> Decimal:
    return Decimal(str(value))


@dataclass(frozen=True)
class LinearSolveResult:
    x: Decimal
    y: Decimal
    residual_1: Decimal
    residual_2: Decimal

    def public(self) -> dict[str, str]:
        return {k: str(v) for k, v in {
            "x": self.x,
            "y": self.y,
            "residual_1": self.residual_1,
            "residual_2": self.residual_2,
        }.items()}


class FrontierComputationEngine:
    """Bridge for mathematical models, computation, and physical scenarios.

    The engine is deterministic and does not ask an LLM to perform arithmetic.
    """

    def solve_2x2(self, a: object, b: object, c: object, d: object, y1: object, y2: object) -> LinearSolveResult:
        a, b, c, d, y1, y2 = map(_d, (a, b, c, d, y1, y2))
        det = a * d - b * c
        if det == 0:
            raise ValueError("singular 2x2 system")
        x = (y1 * d - b * y2) / det
        y = (a * y2 - y1 * c) / det
        return LinearSolveResult(
            x=x,
            y=y,
            residual_1=a * x + b * y - y1,
            residual_2=c * x + d * y - y2,
        )

    def simulate_physics(self, scenario: Mapping[str, object]) -> dict:
        def vec(data: Mapping[str, object]) -> Vector3:
            return Vector3.from_values(data["x"], data["y"], data["z"])

        initial = scenario["initial"]
        state = PhysicalState(
            position=vec(initial["position"]),
            velocity=vec(initial["velocity"]),
            mass=_d(initial["mass"]),
        )
        forces = tuple(vec(item) for item in scenario.get("forces", ()))
        dt = _d(scenario["dt"])
        final = PhysicsEngine().run(state, forces, dt)
        public = {
            "position": {"x": str(final.position.x), "y": str(final.position.y), "z": str(final.position.z)},
            "velocity": {"x": str(final.velocity.x), "y": str(final.velocity.y), "z": str(final.velocity.z)},
            "mass": str(final.mass),
        }
        return {
            "kind": "PHYSICAL_SIMULATION",
            "deterministic": True,
            "result": public,
            "input_digest": digest(scenario),
            "result_digest": digest(public),
        }
