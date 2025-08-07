from core.order import Order, Side, OrderType

class SimpleMeanReversionStrategy:
    def __init__(self, threshold=0.05):
        self.threshold = threshold
        self.toggle = True  # ✅ Alternate between BUY and SELL

    def generate_order(self, best_bid, best_ask, timestamp):
        spread = best_ask - best_bid

        if spread <= self.threshold:
            side = Side.BUY if self.toggle else Side.SELL
            self.toggle = not self.toggle  # 🔁 Flip side every time

            price = best_ask if side == Side.BUY else best_bid

            return Order(
                order_id=f"strategy_{timestamp}",
                price=price,
                quantity=10,
                timestamp=timestamp,
                side=side,
                order_type=OrderType.MARKET,
                is_strategy=True
            )

        return None


import random
from core.order import Order, Side, OrderType

class RandomBSGo:
    def __init__(self):
        self.toggle = True

    def generate_order(self, best_bid, best_ask, timestamp):
        if self.toggle:
            self.toggle = False
            return Order(
                order_id=-1,  # ✅ Added here
                price=best_ask,
                quantity=10,
                timestamp=timestamp,
                side=Side.BUY,
                order_type=OrderType.MARKET
            )
        else:
            self.toggle = True
            return Order(
                order_id=-1,  # ✅ Already correct
                price=best_ask,
                quantity=10,
                timestamp=timestamp,
                side=Side.BUY,
                order_type=OrderType.MARKET
            )

from core.order import Order, Side, OrderType

class AlwaysTakeLiquidityStrategy:
    def __init__(self):
        self.toggle = True  # Alternate between BUY and SELL just for symmetry

    def generate_order(self, best_bid, best_ask, timestamp):
        side = Side.BUY if self.toggle else Side.SELL
        self.toggle = not self.toggle

        price = best_ask if side == Side.BUY else best_bid

        return Order(
            order_id=f"strategy_{timestamp}",
            price=price,
            quantity=10,
            timestamp=timestamp,
            side=side,
            order_type=OrderType.MARKET,
            is_strategy=True
        )
