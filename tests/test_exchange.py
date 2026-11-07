import unittest

from quant_exchange.exchange import Exchange
from quant_exchange.models import Order


class ExchangeTests(unittest.TestCase):
    def setUp(self):
        self.exchange = Exchange()

    def test_same_price_orders_keep_arrival_priority(self):
        first = Order("AAPL", "BUY", 10_000, 2, order_id="first")
        second = Order("AAPL", "BUY", 10_000, 3, order_id="second")

        self.exchange.submit(first)
        self.exchange.submit(second)

        self.assertEqual(
            [order.order_id for order in self.exchange.book("AAPL").bids],
            ["first", "second"],
        )

    def test_non_crossing_orders_report_best_prices_and_spread(self):
        self.exchange.submit(Order("AAPL", "BUY", 9_900, 2, order_id="bid"))
        self.exchange.submit(Order("AAPL", "SELL", 10_100, 3, order_id="ask"))

        book = self.exchange.book("AAPL")
        self.assertEqual(book.best_bid().price, 9_900)
        self.assertEqual(book.best_ask().price, 10_100)
        self.assertEqual(book.spread(), 200)

    def test_exact_fill_removes_both_orders_and_records_trade(self):
        self.exchange.submit(Order("AAPL", "SELL", 10_000, 5, order_id="sell"))

        trades = self.exchange.submit(
            Order("AAPL", "BUY", 10_000, 5, order_id="buy")
        )

        self.assertEqual(len(trades), 1)
        self.assertEqual(
            (trades[0].price, trades[0].quantity, trades[0].maker_order_id, trades[0].taker_order_id),
            (10_000, 5, "sell", "buy"),
        )
        self.assertIsNone(self.exchange.book("AAPL").best_bid())
        self.assertIsNone(self.exchange.book("AAPL").best_ask())

    def test_partial_fill_leaves_resting_quantity(self):
        resting = Order("AAPL", "SELL", 10_000, 10, order_id="sell")
        self.exchange.submit(resting)

        trades = self.exchange.submit(
            Order("AAPL", "BUY", 10_000, 4, order_id="buy")
        )

        self.assertEqual(trades[0].quantity, 4)
        self.assertEqual(resting.remaining, 6)
        self.assertEqual(self.exchange.book("AAPL").best_ask().order_id, "sell")

    def test_incoming_order_matches_multiple_price_levels(self):
        self.exchange.submit(Order("AAPL", "SELL", 10_000, 4, order_id="s1"))
        self.exchange.submit(Order("AAPL", "SELL", 10_100, 5, order_id="s2"))

        trades = self.exchange.submit(
            Order("AAPL", "BUY", 10_500, 8, order_id="buy")
        )

        self.assertEqual([(trade.price, trade.quantity) for trade in trades], [(10_000, 4), (10_100, 4)])
        self.assertEqual(self.exchange.book("AAPL").best_ask().remaining, 1)

    def test_cancel_removes_open_order(self):
        self.exchange.submit(Order("AAPL", "BUY", 9_900, 2, order_id="bid"))

        cancelled = self.exchange.cancel("AAPL", "bid")

        self.assertTrue(cancelled)
        self.assertIsNone(self.exchange.book("AAPL").best_bid())

    def test_cancel_returns_false_for_unknown_order(self):
        self.assertFalse(self.exchange.cancel("AAPL", "missing"))

    def test_symbols_have_independent_order_books(self):
        self.exchange.submit(Order("AAPL", "BUY", 10_000, 1, order_id="aapl"))
        self.exchange.submit(Order("MSFT", "SELL", 20_000, 1, order_id="msft"))

        self.assertEqual(self.exchange.book("AAPL").best_bid().order_id, "aapl")
        self.assertIsNone(self.exchange.book("AAPL").best_ask())
        self.assertEqual(self.exchange.book("MSFT").best_ask().order_id, "msft")

    def test_snapshot_aggregates_quantity_at_each_price(self):
        self.exchange.submit(Order("AAPL", "BUY", 10_000, 2, order_id="b1"))
        self.exchange.submit(Order("AAPL", "BUY", 10_000, 5, order_id="b2"))
        self.exchange.submit(Order("AAPL", "SELL", 10_200, 3, order_id="s1"))

        snapshot = self.exchange.book("AAPL").snapshot()

        self.assertEqual(snapshot, {"bids": [(10_000, 7)], "asks": [(10_200, 3)]})


if __name__ == "__main__":
    unittest.main()
