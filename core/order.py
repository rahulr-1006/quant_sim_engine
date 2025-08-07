# order.py
from dataclasses import dataclass
from enum import Enum

class Side(Enum):
    BUY = 'buy'
    SELL = 'sell'

class OrderType(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'

@dataclass
class Order:
    order_id: int 
    side: Side
    price: float 
    quantity: int 
    timestamp: float
    order_type: OrderType = OrderType.LIMIT
    is_strategy: bool = False  # ✅ Add this line
