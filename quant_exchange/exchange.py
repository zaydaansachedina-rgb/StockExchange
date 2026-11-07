from __future__ import annotations

from .models import Order, Trade
from .order_book import OrderBook


class Exchange:
    def __init__(self):
        self._books: dict[str, OrderBook] = {}
        self.trades: list[Trade] = []

    def book(self, symbol: str) -> OrderBook:
        normalized = symbol.strip().upper()
        if normalized not in self._books:
            self._books[normalized] = OrderBook(normalized)
        return self._books[normalized]

    def submit(self, order: Order) -> list[Trade]:
        trades = self.book(order.symbol).submit(order)
        self.trades.extend(trades)
        return trades

    def cancel(self, symbol: str, order_id: str) -> bool:
        return self.book(symbol).cancel(order_id)
