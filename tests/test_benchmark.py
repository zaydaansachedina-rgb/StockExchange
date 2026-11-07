import unittest

from quant_exchange.benchmark import run_benchmark


class BenchmarkTests(unittest.TestCase):
    def test_benchmark_reports_processed_messages_and_positive_throughput(self):
        result = run_benchmark(message_count=200, seed=3)

        self.assertEqual(result["messages"], 200)
        self.assertGreaterEqual(result["trades"], 0)
        self.assertGreater(result["elapsed_seconds"], 0)
        self.assertGreater(result["messages_per_second"], 0)


if __name__ == "__main__":
    unittest.main()
