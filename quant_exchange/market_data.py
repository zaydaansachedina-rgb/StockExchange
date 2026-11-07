from __future__ import annotations

import json
import random
from collections.abc import Iterable
from pathlib import Path

from .exchange import Exchange
from .models import Order, Trade


def generate_messages(
    count: int,
    *,
    seed: int = 0,
    symbols: tuple[str, ...] = ("AAPL", "MSFT", "NVDA"),
) -> list[dict[str, object]]:
    if count < 0:
        raise ValueError("count must be non-negative")
    if not symbols:
        raise ValueError("symbols must not be empty")

    rng = random.Random(seed)
    open_orders: list[tuple[str, str]] = []
    messages: list[dict[str, object]] = []
    next_id = 1
    while len(messages) < count:
        if open_orders and rng.random() < 0.25:
            symbol, order_id = rng.choice(open_orders)
            open_orders.remove((symbol, order_id))
            messages.append(
                {"action": "CANCEL", "symbol": symbol, "order_id": order_id}
            )
            continue

        symbol = rng.choice(symbols).strip().upper()
        order_id = f"sim-{next_id}"
        next_id += 1
        side = rng.choice(("BUY", "SELL"))
        price = 10_000 + rng.randint(-250, 250)
        quantity = rng.randint(1, 25)
        messages.append(
            {
                "action": "ADD",
                "order_id": order_id,
                "symbol": symbol,
                "side": side,
                "price": price,
                "quantity": quantity,
            }
        )
        open_orders.append((symbol, order_id))
    return messages


def write_jsonl(messages: Iterable[dict[str, object]], path: str | Path) -> None:
    output = Path(path)
    with output.open("w", encoding="utf-8") as stream:
        for message in messages:
            stream.write(json.dumps(message, sort_keys=True) + "\n")


def read_jsonl(path: str | Path) -> list[dict[str, object]]:
    with Path(path).open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def replay_messages(
    exchange: Exchange, messages: Iterable[dict[str, object]]
) -> list[Trade]:
    trades: list[Trade] = []
    for message in messages:
        action = str(message["action"]).upper()
        if action == "ADD":
            trades.extend(
                exchange.submit(
                    Order(
                        symbol=str(message["symbol"]),
                        side=str(message["side"]),
                        price=int(message["price"]),
                        quantity=int(message["quantity"]),
                        order_id=str(message["order_id"]),
                    )
                )
            )
        elif action == "CANCEL":
            exchange.cancel(str(message["symbol"]), str(message["order_id"]))
        else:
            raise ValueError(f"unknown action: {action}")
    return trades
