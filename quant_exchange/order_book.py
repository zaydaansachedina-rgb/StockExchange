from __future__ import annotations

from collections import defaultdict

from .models import Order, Trade


class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol.strip().upper()
        self.bids: list[Order] = []
        self.asks: list[Order] = []

    def submit(self, order: Order) -> list[Trade]:
        if order.symbol != self.symbol:
            raise ValueError("order symbol does not match this book")

        trades: list[Trade] = []
        opposite = self.asks if order.side == "BUY" else self.bids
        while order.remaining and opposite and self._crosses(order, opposite[0]):
            resting = opposite[0]
            fill_quantity = min(order.remaining, resting.remaining)
            trades.append(
                Trade(
                    symbol=self.symbol,
                    price=resting.price,
                    quantity=fill_quantity,
                    maker_order_id=resting.order_id,
                    taker_order_id=order.order_id,
                )
            )
            order.remaining -= fill_quantity
            resting.remaining -= fill_quantity
            if resting.remaining == 0:
                opposite.pop(0)

        if order.remaining:
            own_side = self.bids if order.side == "BUY" else self.asks
            own_side.append(order)
            own_side.sort(key=lambda item: -item.price if order.side == "BUY" else item.price)
        return trades

    def cancel(self, order_id: str) -> bool:
        for side in (self.bids, self.asks):
            for index, order in enumerate(side):
                if order.order_id == order_id:
                    side.pop(index)
                    return True
        return False

    def best_bid(self) -> Order | None:
        return self.bids[0] if self.bids else None

    def best_ask(self) -> Order | None:
        return self.asks[0] if self.asks else None

    def spread(self) -> int | None:
        bid = self.best_bid()
        ask = self.best_ask()
        if bid is None or ask is None:
            return None
        return ask.price - bid.price

    def snapshot(self) -> dict[str, list[tuple[int, int]]]:
        return {
            "bids": self._levels(self.bids),
            "asks": self._levels(self.asks),
        }

    @staticmethod
    def _crosses(incoming: Order, resting: Order) -> bool:
        if incoming.side == "BUY":
            return incoming.price >= resting.price
        return incoming.price <= resting.price

    @staticmethod
    def _levels(orders: list[Order]) -> list[tuple[int, int]]:
        quantities: dict[int, int] = defaultdict(int)
        ordered_prices: list[int] = []
        for order in orders:
            if order.price not in quantities:
                ordered_prices.append(order.price)
            quantities[order.price] += order.remaining
        return [(price, quantities[price]) for price in ordered_prices]
