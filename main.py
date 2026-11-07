from quant_exchange import Exchange, Order


def main() -> None:
    exchange = Exchange()
    exchange.submit(Order("AAPL", "SELL", 15_005, 4, order_id="sell-1"))
    exchange.submit(Order("AAPL", "SELL", 15_010, 6, order_id="sell-2"))
    trades = exchange.submit(
        Order("AAPL", "BUY", 15_010, 8, order_id="buy-1")
    )

    for trade in trades:
        print(
            f"TRADE {trade.symbol} {trade.quantity} @ ${trade.price / 100:.2f} "
            f"maker={trade.maker_order_id} taker={trade.taker_order_id}"
        )
    print("BOOK", exchange.book("AAPL").snapshot())


if __name__ == "__main__":
    main()
