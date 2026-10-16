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

    def best_bid(self):
        if len(self.add_buyorder) == 0:
            return None
    
        best_bid = self.add_buyorder[0]
        return best_bid 
      
    def best_ask(self):
        if len(self.add_sellorder) == 0:
            return None 
        
        best_ask = self.add_sellorder[0]
        return best_ask
    
    def spread(self):
        bid = self.best_bid() 
        ask = self.best_ask()
        if bid is None or ask is None:
            return None 

        if bid.symbol != ask.symbol:
            return None 
        spread = ask.price - bid.price 
        return spread 
    
    def match_orders(self):
        bid = self.best_bid()
        ask = self.best_ask()

        if bid is None or ask is None:
            return None
         
       # if 
book = OrderBook()

order1 = Order("AAPL", "BUY", 320, 10)
order2 = Order("AAPL", "BUY", 325, 5)
order3 = Order("AAPL", "BUY", 322, 8)

order4 = Order("AAPL", "SELL", 335, 4)
order5 = Order("AAPL", "SELL", 330, 7)
order6 = Order("AAPL", "SELL", 340, 3)

book.get_order(order1)
book.get_order(order2)
book.get_order(order3)
book.get_order(order4)
book.get_order(order5)

print("Best bid:", book.best_bid().price)
print("Best ask:", book.best_ask().price)
print("Spread:", book.spread())