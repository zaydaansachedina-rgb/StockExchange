import unittest

from quant_exchange.models import Order


class OrderTests(unittest.TestCase):
    def test_valid_order_normalizes_symbol_and_side(self):
        order = Order(" aapl ", "buy", 15_005, 10, order_id="o-1")

        self.assertEqual(order.symbol, "AAPL")
        self.assertEqual(order.side, "BUY")
        self.assertEqual(order.price, 15_005)
        self.assertEqual(order.quantity, 10)

    def test_order_rejects_unknown_side(self):
        with self.assertRaisesRegex(ValueError, "side"):
            Order("AAPL", "HOLD", 15_005, 10)

    def test_order_rejects_non_positive_price(self):
        with self.assertRaisesRegex(ValueError, "price"):
            Order("AAPL", "BUY", 0, 10)

    def test_order_rejects_non_positive_quantity(self):
        with self.assertRaisesRegex(ValueError, "quantity"):
            Order("AAPL", "BUY", 15_005, -1)


if __name__ == "__main__":
    unittest.main()
