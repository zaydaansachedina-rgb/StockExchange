from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Order:
    symbol: str
    side: str
    price: int
    quantity: int
    order_id: str = field(default_factory=lambda: uuid4().hex)
    remaining: int = field(init=False)

    def __post_init__(self) -> None:
        self.symbol = self.symbol.strip().upper()
        self.side = self.side.strip().upper()
        if not self.symbol:
            raise ValueError("symbol must not be empty")
        if self.side not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")
        if not isinstance(self.price, int) or isinstance(self.price, bool) or self.price <= 0:
            raise ValueError("price must be a positive integer number of cents")
        if (
            not isinstance(self.quantity, int)
            or isinstance(self.quantity, bool)
            or self.quantity <= 0
        ):
            raise ValueError("quantity must be a positive integer")
        self.remaining = self.quantity


@dataclass(frozen=True)
class Trade:
    symbol: str
    price: int
    quantity: int
    maker_order_id: str
    taker_order_id: str
