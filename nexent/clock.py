from dataclasses import dataclass
@dataclass
class LogicalClock:
    value: int = 0
    def tick(self) -> int:
        self.value += 1
        return self.value
