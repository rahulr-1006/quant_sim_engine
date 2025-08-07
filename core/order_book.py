#order_book.py
from collections import defaultdict, deque

from sortedcontainers import SortedDict
from collections import deque
from core.order import Order, Side, OrderType

class OrderBook:
    def __init__(self, position_tracker=None):
        self.bids = defaultdict(deque)
        self.asks = defaultdict(deque)
        self.order_map = {}
        self.trades = []
        self.position_tracker = position_tracker  # ✅ NEW

    def add_order(self, order):
        book_side = self.bids if order.side == Side.BUY else self.asks

        # Market orders go to matching engine
        if order.order_type == OrderType.MARKET:
            trades = self.match_order(order)  # 🔥 Call actual matching logic here
            for trade in trades:
                if order.is_strategy and self.position_tracker:
                    self.position_tracker.update(trade, is_strategy_trade=True)
            return  # Skip adding to book

        # Limit orders are added to book
        book_side[order.price].append(order)
        self.order_map[order.order_id] = order


    def match_order(self, incoming: Order):
        """
        Matches an incoming order against the opposite side of the book.
        Logs trades and updates book state.
        """
        trades = []
        book_side = self.asks if incoming.side == Side.BUY else self.bids

        for price in list(book_side.keys()):
            # Skip non-matching prices for LIMIT orders
            if incoming.order_type == OrderType.LIMIT:  # ✅ correct
                if (incoming.side == Side.BUY and price > incoming.price) or \
                   (incoming.side == Side.SELL and price < incoming.price):
                    break

            queue = book_side[price]

            while queue and incoming.quantity > 0:
                resting = queue[0]
                trade_qty = min(incoming.quantity, resting.quantity)

                trade = {
                    'price': price,
                    'quantity': trade_qty,
                    'timestamp': incoming.timestamp,
                    'buy_id': incoming.order_id if incoming.side == Side.BUY else resting.order_id,
                    'sell_id': incoming.order_id if incoming.side == Side.SELL else resting.order_id
                }
                trades.append(trade)
                self.trades.append(trade)
                if incoming.is_strategy and self.position_tracker:
                    self.position_tracker.update(trade, is_strategy_trade=True)

                # 🔍 Debugging
                if incoming.is_strategy:
                    print("✅ Executed strategy trade (incoming):", trade)
                elif isinstance(trade['buy_id'], str) and trade['buy_id'].startswith("strategy_"):
                    print("✅ Executed strategy trade (from resting):", trade)


                # Update quantities
                incoming.quantity -= trade_qty
                resting.quantity -= trade_qty

                if resting.quantity == 0:
                    queue.popleft()
                    del self.order_map[resting.order_id]
                else:
                    break  # FIFO: can’t skip over partially filled orders

            if not queue:
                del book_side[price]

            if incoming.quantity == 0:
                break

        return trades

    def cancel_order(self, order_id: int):
        """
        Removes an existing order from the book.
        """
        order = self.order_map.get(order_id)
        if not order:
            return False

        book_side = self.bids if order.side == Side.BUY else self.asks
        queue = book_side.get(order.price)
        if queue:
            for i, queued in enumerate(queue):
                if queued.order_id == order_id:
                    del queue[i]
                    del self.order_map[order_id]
                    if not queue:
                        del book_side[order.price]
                    return True
        return False

    def print_book(self, depth=5):
        """
        Print top-of-book snapshot (for debugging).
        """
        print("ORDER BOOK:")
        print(" Asks (Sell side):")
        for price in list(self.asks.keys())[:depth]:
            qty = sum(order.quantity for order in self.asks[price])
            print(f"  {price:.2f} × {qty}")
        print(" Bids (Buy side):")
        for price in list(self.bids.keys())[:depth]:
            qty = sum(order.quantity for order in self.bids[price])
            print(f"  {price:.2f} × {qty}")
        print("-" * 30)
    
    def get_best_bid(self):
        if self.bids:
            best_price = next(iter(self.bids))
            total_qty = sum(order.quantity for order in self.bids[best_price])
            return (best_price, total_qty)
        return None

    def get_best_ask(self):
        if self.asks:
            best_price = next(iter(self.asks))
            total_qty = sum(order.quantity for order in self.asks[best_price])
            return (best_price, total_qty)
        return None

