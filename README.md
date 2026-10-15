# Quant Exchange

> A beginner-built electronic exchange simulator for learning Python, algorithms, data structures, testing, and market-system design.

## Project Overview

Quant Exchange is an educational simulation of a small electronic financial exchange. The project starts with simple Python classes for orders and an order book, then grows into a system that can prioritize orders, match buyers with sellers, record trades, process generated market messages, and measure performance.

The goal is not to build a profitable trading bot. The goal is to understand a complete system from end to end and be able to explain every important line of code.

## Current Status

**In progress - early order-book stage**

The current learning milestone is organizing orders by price priority.

| Component | Status | Notes |
| --- | --- | --- |
| `Order` model | Complete | Stores core order information such as symbol, side, price, and quantity. |
| Basic `OrderBook` | Complete | Accepts orders and separates buy orders from sell orders. |
| Price-priority sorting | Complete | Buy orders should be highest-to-lowest; sell orders should be lowest-to-highest. |
| Best bid, best ask, and spread | In Progress | Read the best available prices from the sorted book. |
| Matching engine | Planned | Match compatible buy and sell orders and support partial fills. |
| Automated tests | Planned | Cover expected behavior, invalid data, and edge cases with `pytest`. |

This status reflects the current learning progress. The full structure and later modules below are planned and will be added gradually.

## Goals

- Build a working exchange simulation without relying on live market data or a brokerage account.
- Learn how buy and sell orders are represented and prioritized.
- Implement price-time matching and partial fills.
- Practice writing clear, modular, testable Python.
- Use generated market messages to test realistic workloads safely.
- Measure performance before changing data structures or optimizing code.
- Create a project that demonstrates steady technical growth for GitHub and future internship applications.

## How the System Fits Together

```text
Generated market messages
          |
          v
       Parser
          |
          v
      Order book
          |
          v
    Matching engine -----> Trades
          |
          v
 Strategy and portfolio -----> Positions and P&L
```

### Core Components

- **Order** - represents a request to buy or sell a quantity of a symbol at a specified price.
- **Order book** - keeps buy and sell orders separate and maintains the correct priority on each side.
- **Matching engine** - creates trades when the best buy price is greater than or equal to the best sell price.
- **Market-data parser** - converts generated `ADD` and `CANCEL` messages into actions the exchange can process.
- **Strategy and portfolio** - later modules for simple signals, cash, positions, completed trades, and profit and loss.
- **Benchmark** - measures processing time and messages per second before any optimization work.

### Order Priority

The best available prices appear first:

```text
BUY orders                 SELL orders
highest price first        lowest price first

$325  <- best bid          $330  <- best ask
$322                       $335
$320                       $340
```

When two orders have the same price, the earlier order should receive priority. This is called **price-time priority**.

### Price Representation

Prices are stored as integer cents instead of floating-point dollars. For example:

```python
price = 15005  # $150.05
```

Integer prices avoid floating-point rounding problems and map more naturally to a future hardware implementation.

## Planned Features

- Buy and sell order books with price-time priority
- Best bid, best ask, and bid-ask spread calculations
- Exact and partial order fills
- Multiple matches from a single incoming order
- Unique order IDs and order cancellation
- Generated `ADD` and `CANCEL` market messages
- Input validation and empty-book handling
- Trade history and execution reporting
- Portfolio tracking for cash, positions, and P&L
- Simple research signals using simulated or replayed data
- Throughput and latency benchmarks
- Compact binary message encoding
- A simulated FPGA accelerator for one narrow calculation

## Tech Stack

| Area | Technology | Purpose |
| --- | --- | --- |
| Main language | Python | Build the exchange while strengthening Python fundamentals. |
| Testing | pytest | Verify matching logic, partial fills, invalid data, and edge cases. |
| Data | Generated local files | Avoid live-market and brokerage dependencies. |
| Version control | Git and GitHub | Show steady progress and preserve project history. |
| Performance | `time.perf_counter()` | Measure processing time and throughput. |
| Later analysis | pandas | Explore trade and market data after the core exchange works. |
| Hardware stretch goal | SystemVerilog and Verilator | Simulate and compare one hardware calculation with Python. |

The core version intentionally avoids a web interface, database, cloud deployment, machine learning model, live brokerage account, and physical FPGA board. Those additions would distract from the exchange fundamentals at this stage.

## Planned Project Structure

The project will be split into modules as it grows. Not every file needs to exist on day one.

```text
quant-exchange/
|-- main.py
|-- exchange/
|   |-- order.py
|   |-- orderbook.py
|   |-- matching.py
|   `-- exchange.py
|-- market_data/
|   |-- parser.py
|   `-- generator.py
|-- strategy/
|   |-- strategy.py
|   `-- portfolio.py
|-- tests/
|   |-- test_orders.py
|   |-- test_orderbook.py
|   `-- test_matching.py
|-- benchmarks/
|   `-- benchmark.py
`-- README.md
```

## Roadmap

### Phase 1 - Python and Orders

- Create the `Order` class.
- Store the symbol, side, price, and quantity.
- Create and print several example orders.

### Phase 2 - Order Book

- Create separate buy and sell collections.
- Add orders to the correct side.
- Sort buys from highest to lowest price.
- Sort sells from lowest to highest price.

### Phase 3 - Market View

- Implement `best_bid()`.
- Implement `best_ask()`.
- Calculate the bid-ask `spread()`.
- Handle an empty side of the book safely.

### Phase 4 - Matching Engine

- Match one buy order with one sell order when their prices cross.
- Support exact fills and partial fills.
- Support one order matching multiple resting orders.
- Preserve price-time priority while quantities change.

### Phase 5 - Reliability

- Validate symbols, sides, prices, and quantities.
- Add at least ten focused tests.
- Cover empty books, non-matching orders, invalid input, exact fills, partial fills, and multiple matches.

### Phase 6 - Complete the Minimum Viable Project

- Add unique order IDs and cancellation.
- Read generated market messages.
- Record completed trades.
- Run one reproducible benchmark.
- Keep the architecture and usage instructions documented.

### Phase 7 - Extensions

- Improve data structures only when profiling shows a real bottleneck.
- Add a portfolio and a simple research strategy.
- Encode and decode a compact binary market protocol.
- Compare a Python calculation with a simulated hardware version.

## How to Run the Current Version

### Prerequisites

- Python 3.10 or newer
- Git, if you are cloning the repository

The core project currently uses only the Python standard library.

### 1. Get the project

```bash
git clone <repository-url>
cd quant-exchange
```

If the project is already on your computer, open a terminal in its root folder instead.

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Run the current example

```bash
python main.py
```

At the current stage, the program should create sample orders, add them to an `OrderBook`, and print the buy and sell sides. As price-priority sorting is completed, buy orders should appear from highest to lowest price and sell orders from lowest to highest price.

### 4. Run tests when the test suite is added

```bash
python -m pip install pytest
python -m pytest
```

> The repository is still being built. If the filenames in the implementation differ from this planned layout, run the actual entry file in place of `main.py` and update this section.

## Learning Goals

This project is designed to build practical understanding of:

- Python variables, strings, integers, functions, lists, and classes
- Objects, methods, return values, and `None`
- Sorting objects with `key=`, `lambda`, and `reverse=True`
- Loops, comparisons, and changing program state
- Data structures and algorithmic trade-offs
- Financial-market concepts such as bids, asks, spreads, liquidity, and fills
- Unit testing, edge cases, and debugging
- File parsing and binary data representation
- Profiling, throughput, latency, and evidence-based optimization
- Git commits and maintaining a readable engineering history

An important project rule is to understand every major function: what it does, what data it changes, and why it exists.

## Future FPGA Stretch Goal

The FPGA work begins only after the Python exchange is correct and tested. The idea is to choose one narrow, measurable calculation, such as:

- bid-ask spread
- order-book imbalance
- a simple pre-trade risk check

That calculation can then be implemented in SystemVerilog, simulated with Verilator, and compared with the Python version for correctness and estimated latency or cycle count.

```text
Python exchange
     |
     +--> Python calculation
     |
     `--> Simulated FPGA calculation
                    |
                    v
         Compare outputs and performance
```

This is a stretch goal, not a requirement for a successful project. A clean, tested software exchange is already a complete and valuable result.

## Educational Use Only

This project is an educational simulation. It is not financial advice, is not connected to a live exchange or brokerage account, and must not be used to place or manage real trades. The simulated behavior may omit rules, safeguards, fees, latency, and other details found in production trading systems.

## Project Philosophy

Build the smallest working piece, test it, understand it, and then add the next layer. Correctness and clear reasoning matter more than feature count.

