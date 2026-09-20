from dataclasses import dataclass
from decimal import Decimal
from .core import PhysicalState, PhysicsEngine, Vector3
@dataclass(frozen=True)
class PhysicsScenario:
    initial: PhysicalState; forces: tuple[Vector3,...]; dt: Decimal
    def __post_init__(self):
        object.__setattr__(self,"dt",Decimal(str(self.dt)))
        if self.dt<=0: raise ValueError("dt must be positive")
def simulate(scenario): return PhysicsEngine().run(scenario.initial,scenario.forces,scenario.dt)
