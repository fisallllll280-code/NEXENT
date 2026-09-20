from decimal import Decimal
import pytest

from nexent.portfolio import Money, Portfolio, PortfolioEntry, PortfolioError, Scenario, simulate
from nexent.portfolio.core import EntryType


def entry(portfolio, kind, amount, source="test"):
    return PortfolioEntry(kind, Money.parse(amount, "USD"), portfolio.portfolio_id, source)


def test_decimal_safe_posting_and_reconciliation():
    p = Portfolio("P1", "USD")
    p.post(entry(p, EntryType.REVENUE, "100.10"))
    p.post(entry(p, EntryType.COST, "0.10"))
    assert p.balance() == Decimal("100.00")
    assert p.reconcile()["net"] == Decimal("100.00")
    assert p.snapshot()["entry_count"] == 2


def test_mixed_currency_is_rejected():
    p = Portfolio("P1", "USD")
    with pytest.raises(PortfolioError):
        p.post(PortfolioEntry(EntryType.REVENUE, Money.parse("1", "EUR"), "P1", "x"))


def test_negative_posted_amount_is_rejected():
    p = Portfolio("P1", "USD")
    with pytest.raises(PortfolioError):
        p.post(entry(p, EntryType.REVENUE, "-1"))


def test_simulation_is_deterministic():
    s = Scenario("base", Decimal("1000"), Decimal("250"), Decimal("100"), Decimal("0.10"))
    assert simulate(s) == simulate(s)
    assert simulate(s)["ending_resources"] == Decimal("1035.00")
