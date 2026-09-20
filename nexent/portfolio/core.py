from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Iterable
import uuid


class PortfolioError(ValueError):
    """Raised when a portfolio invariant or input contract is violated."""


class EntryType(str, Enum):
    ASSET = "ASSET"
    REVENUE = "REVENUE"
    COST = "COST"
    RESERVE = "RESERVE"
    OBLIGATION = "OBLIGATION"
    ALLOCATION = "ALLOCATION"
    COMMITMENT = "COMMITMENT"
    REVERSAL = "REVERSAL"


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "amount", Decimal(self.amount))
        currency = self.currency.upper().strip()
        if len(currency) != 3 or not currency.isalpha():
            raise PortfolioError("currency must be a 3-letter code")
        object.__setattr__(self, "currency", currency)
        if not self.amount.is_finite():
            raise PortfolioError("money amount must be finite")

    @classmethod
    def parse(cls, amount: str | int | Decimal, currency: str) -> "Money":
        try:
            value = Decimal(str(amount))
        except InvalidOperation as exc:
            raise PortfolioError("invalid monetary amount") from exc
        return cls(value, currency)


@dataclass(frozen=True)
class PortfolioEntry:
    entry_type: EntryType
    amount: Money
    portfolio_id: str
    source_reference: str
    authorization_reference: str | None = None
    evidence_reference: str | None = None
    entry_id: str = field(default_factory=lambda: "PE-" + uuid.uuid4().hex)

    def signed_amount(self) -> Decimal:
        if self.entry_type in {EntryType.COST, EntryType.OBLIGATION}:
            return -self.amount.amount
        return self.amount.amount


class Portfolio:
    """Deterministic in-memory computational portfolio ledger.

    Posted entries are immutable. Corrections are compensating entries, never edits.
    """

    def __init__(self, portfolio_id: str, currency: str) -> None:
        self.portfolio_id = portfolio_id
        self.currency = currency.upper()
        self._entries: list[PortfolioEntry] = []

    @property
    def entries(self) -> tuple[PortfolioEntry, ...]:
        return tuple(self._entries)

    def post(self, entry: PortfolioEntry) -> PortfolioEntry:
        if entry.portfolio_id != self.portfolio_id:
            raise PortfolioError("portfolio mismatch")
        if entry.amount.currency != self.currency:
            raise PortfolioError("currency mismatch")
        if entry.amount.amount < 0:
            raise PortfolioError("posted amount must be non-negative")
        if entry.entry_type in {EntryType.REVENUE, EntryType.COST, EntryType.OBLIGATION, EntryType.COMMITMENT} and not entry.source_reference:
            raise PortfolioError("source_reference is required")
        self._entries.append(entry)
        return entry

    def balance(self) -> Decimal:
        return sum((e.signed_amount() for e in self._entries), Decimal("0"))

    def total(self, *types: EntryType) -> Decimal:
        selected = set(types)
        return sum((e.amount.amount for e in self._entries if e.entry_type in selected), Decimal("0"))

    def available(self, allocated: Decimal = Decimal("0")) -> Decimal:
        value = self.balance() - Decimal(allocated)
        if value < 0:
            raise PortfolioError("allocation exceeds available portfolio balance")
        return value

    def reconcile(self) -> dict[str, Decimal]:
        revenue = self.total(EntryType.REVENUE)
        costs = self.total(EntryType.COST)
        obligations = self.total(EntryType.OBLIGATION)
        commitments = self.total(EntryType.COMMITMENT)
        return {
            "revenue": revenue,
            "costs": costs,
            "obligations": obligations,
            "commitments": commitments,
            "net": revenue - costs - obligations,
            "available_after_commitments": revenue - costs - obligations - commitments,
        }

    def assert_invariants(self) -> None:
        if any(e.amount.currency != self.currency for e in self._entries):
            raise PortfolioError("mixed currencies detected")
        ids = [e.entry_id for e in self._entries]
        if len(ids) != len(set(ids)):
            raise PortfolioError("duplicate entry id detected")
        self.reconcile()

    def snapshot(self) -> dict:
        self.assert_invariants()
        return {
            "portfolio_id": self.portfolio_id,
            "currency": self.currency,
            "entry_count": len(self._entries),
            "balance": str(self.balance()),
            "reconciliation": {k: str(v) for k, v in self.reconcile().items()},
        }
