# core/market_event.py
from dataclasses import dataclass

@dataclass
class MarketEvent:
    timestamp: float           # Event time in seconds
    event_type: int            # LOBSTER type: 1–5, 7
    order_id: int              # Unique order ID
    size: int                  # Order size in shares
    price: float               # Price in dollars (not integer format)
    direction: int             # 1 = Buy, -1 = Sell
