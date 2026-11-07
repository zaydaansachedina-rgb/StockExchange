from __future__ import annotations

from time import perf_counter

from .exchange import Exchange
from .market_data import generate_messages, replay_messages


def run_benchmark(*, message_count: int = 10_000, seed: int = 0) -> dict[str, int | float]:
    messages = generate_messages(message_count, seed=seed)
    exchange = Exchange()
    started = perf_counter()
    trades = replay_messages(exchange, messages)
    elapsed = perf_counter() - started
    return {
        "messages": message_count,
        "trades": len(trades),
        "elapsed_seconds": elapsed,
        "messages_per_second": message_count / elapsed,
    }
