# Quant Exchange

Quant Exchange is an educational limit-order exchange simulator written in Python. It models the core mechanics of an electronic exchange without connecting to a brokerage or live market.

## MVP status

The core MVP is implemented and tested.

- Multi-symbol order books
- Price-time priority
- Best bid, best ask, spread, and aggregated price-level snapshots
- Exact, partial, and multi-order fills
- Order cancellation and trade records
- Deterministic synthetic `ADD` and `CANCEL` messages
- JSONL market-message import and export
- Reproducible throughput benchmark
- 17 automated unit tests

Prices use integer cents to avoid floating-point rounding errors. A price of `15005` represents `$150.05`.

## Project structure

```text
quant_exchange/
|-- models.py        # Order and Trade records
|-- order_book.py    # Matching, priority, cancellation, snapshots
|-- exchange.py      # Multi-symbol exchange coordinator
|-- market_data.py   # Synthetic messages and JSONL replay
`-- benchmark.py     # Throughput measurement
tests/
|-- test_models.py
|-- test_exchange.py
|-- test_market_data.py
`-- test_benchmark.py
main.py              # Small matching example
run_benchmark.py     # Reproducible benchmark entry point
```

## Run the example

Requires Python 3.10 or newer. The project uses only the standard library.

```bash
python main.py
```

Example output:

```text
TRADE AAPL 4 @ $150.05 maker=sell-1 taker=buy-1
TRADE AAPL 4 @ $150.10 maker=sell-2 taker=buy-1
BOOK {'bids': [], 'asks': [(15010, 2)]}
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The suite covers validation, price-time priority, empty books, spreads, exact and partial fills, matching across multiple price levels, cancellation, symbol isolation, snapshots, deterministic market data, JSONL replay, and benchmark reporting.

## Run the benchmark

```bash
python run_benchmark.py
```

The benchmark generates 25,000 deterministic local messages, replays them through the exchange, and reports elapsed time, trade count, and messages processed per second. Results vary by machine, so the repository does not claim a fixed throughput number.

## Design notes

An incoming order executes at the resting order's price. If it is not fully filled, its remaining quantity joins the book. Orders at the same price keep arrival order. Each symbol has an independent book, while the `Exchange` object keeps a combined trade history.

The code favors clarity over production-scale optimization. A real exchange would require stronger persistence, concurrency control, risk checks, market rules, audit logging, and operational safeguards.

## Educational use only

This simulator is not financial advice and does not connect to a live exchange or brokerage account. It must not be used to place or manage real trades.
