from dataclasses import dataclass
@dataclass(frozen=True)
class VANDesign:
    name: str; viewport: tuple[int,int]; components: tuple[str,...]; data_bindings: dict; interactions: dict; states: tuple[str,...]=("loading","ready","empty","error")
    def to_dict(self): return {"name":self.name,"viewport":list(self.viewport),"components":list(self.components),"data_bindings":dict(self.data_bindings),"interactions":dict(self.interactions),"states":list(self.states)}
