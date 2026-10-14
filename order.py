class Order:
    def __init__(self, symbol, side, price, quantity):
        self.symbol = symbol 
        self.side = side 
        self.price = price 
        self.quantity = quantity


class OrderBook:
    def __init__(self):
        self.add_buyorder = []
        self.add_sellorder = []

    def get_order(self, order):
        self.order = order
        if order.side == "BUY":
            self.add_buyorder.append(order)
            self.add_buyorder.sort(key= lambda order: order.price, reverse=True )
        elif order.side == "SELL":
            self.add_sellorder.append(order)
            self.add_sellorder.sort(key=lambda order: order.price)


book = OrderBook()
order1 = Order("APPL", "BUY", 323, 10)
order2 = Order("TD", "SELL", 323, 12)
order3 = Order("GOOGL", "BUY", 432, 10)
order4 = Order("NVDIA", "SELL", 455, 10)
book.get_order(order1)
book.get_order(order2)
book.get_order(order3)
book.get_order(order4)
print(len(book.add_buyorder))
print(len(book.add_sellorder))
print(book.add_buyorder)
