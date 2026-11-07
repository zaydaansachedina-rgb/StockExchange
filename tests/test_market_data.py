import tempfile
import unittest
from pathlib import Path

from quant_exchange.exchange import Exchange
from quant_exchange.market_data import (
    generate_messages,
    read_jsonl,
    replay_messages,
    write_jsonl,
)


class MarketDataTests(unittest.TestCase):
    def test_generator_is_deterministic_for_a_seed(self):
        first = generate_messages(8, seed=42, symbols=("AAPL", "MSFT"))
        second = generate_messages(8, seed=42, symbols=("AAPL", "MSFT"))

        self.assertEqual(first, second)
        self.assertEqual(len(first), 8)

    def test_jsonl_round_trip_preserves_messages(self):
        messages = generate_messages(5, seed=9, symbols=("AAPL",))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "messages.jsonl"

            write_jsonl(messages, path)

            self.assertEqual(read_jsonl(path), messages)

    def test_replay_processes_add_and_cancel_messages(self):
        messages = [
            {"action": "ADD", "order_id": "b1", "symbol": "AAPL", "side": "BUY", "price": 9_900, "quantity": 2},
            {"action": "ADD", "order_id": "s1", "symbol": "AAPL", "side": "SELL", "price": 10_100, "quantity": 3},
            {"action": "CANCEL", "order_id": "b1", "symbol": "AAPL"},
        ]
        exchange = Exchange()

        trades = replay_messages(exchange, messages)

        self.assertEqual(trades, [])
        self.assertIsNone(exchange.book("AAPL").best_bid())
        self.assertEqual(exchange.book("AAPL").best_ask().order_id, "s1")


if __name__ == "__main__":
    unittest.main()
