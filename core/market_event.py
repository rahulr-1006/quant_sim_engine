from dataclasses import dataclass

@dataclass
class MarketEvent:
    timestamp: float
    event_type: int      # 1–5, 7
    orderID: int
    size: int
    price: float         # In dollars
    direction: int       # 1 = Buy, -1 = Sell
