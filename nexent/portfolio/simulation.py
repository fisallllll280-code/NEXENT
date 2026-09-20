from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .core import PortfolioError


@dataclass(frozen=True)
class Scenario:
    name: str
    starting_balance: Decimal
    expected_revenue: Decimal = Decimal("0")
    expected_cost: Decimal = Decimal("0")
    reserve_ratio: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        for name in ("starting_balance", "expected_revenue", "expected_cost", "reserve_ratio"):
            value = Decimal(getattr(self, name))
            if not value.is_finite():
                raise PortfolioError(f"{name} must be finite")
            object.__setattr__(self, name, value)
        if not Decimal("0") <= self.reserve_ratio <= Decimal("1"):
            raise PortfolioError("reserve_ratio must be between 0 and 1")


def simulate(scenario: Scenario) -> dict[str, Decimal | str]:
    gross = scenario.starting_balance + scenario.expected_revenue
    net_before_reserve = gross - scenario.expected_cost
    reserve = net_before_reserve * scenario.reserve_ratio
    ending = net_before_reserve - reserve
    return {
        "scenario": scenario.name,
        "gross_resources": gross,
        "reserve": reserve,
        "ending_resources": ending,
        "net_change": ending - scenario.starting_balance,
    }
