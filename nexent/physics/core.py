from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from math import isfinite
from typing import Iterable

def _d(value):
    if isinstance(value, float) and not isfinite(value): raise ValueError("non-finite numeric value")
    out=Decimal(str(value))
    if not out.is_finite(): raise ValueError("non-finite numeric value")
    return out

@dataclass(frozen=True)
class Vector3:
    x: Decimal; y: Decimal; z: Decimal
    def __post_init__(self):
        object.__setattr__(self,"x",_d(self.x)); object.__setattr__(self,"y",_d(self.y)); object.__setattr__(self,"z",_d(self.z))
    @classmethod
    def from_values(cls,x,y,z): return cls(_d(x),_d(y),_d(z))
    def __add__(self,o): return Vector3(self.x+o.x,self.y+o.y,self.z+o.z)
    def scale(self,f):
        f=_d(f); return Vector3(self.x*f,self.y*f,self.z*f)

@dataclass(frozen=True)
class PhysicalState:
    position: Vector3; velocity: Vector3; mass: Decimal
    def __post_init__(self):
        m=_d(self.mass)
        if m<=0: raise ValueError("mass must be positive")
        object.__setattr__(self,"mass",m)

class PhysicsEngine:
    def step(self,state,force,dt):
        dt=_d(dt)
        if dt<=0: raise ValueError("dt must be positive")
        acceleration=force.scale(Decimal(1)/state.mass)
        velocity=state.velocity+acceleration.scale(dt)
        position=state.position+velocity.scale(dt)
        return PhysicalState(position,velocity,state.mass)
    def run(self,state,forces: Iterable[Vector3],dt):
        current=state
        for force in forces: current=self.step(current,force,dt)
        return current
