import json

from quant_exchange.benchmark import run_benchmark


if __name__ == "__main__":
    print(json.dumps(run_benchmark(message_count=25_000, seed=7), indent=2))
