import pandas as pd 
from core.market_event import MarketEvent

class LOBSTERMessageParser:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def parse_message(self):
        df = pd.read_csv(self.filepath, header=None)
        df.columns = ["timestamp", 
                      "type", 
                      "orderID", 
                      "size", 
                      "price",
                      "direction"]
        
        events = []
        for _, row in df.iterrows():
            event = MarketEvent(
                timestamp=float(row["timestamp"]),
                event_type=int(row["type"]),
                orderID = int(row["orderID"]),
                size = int(row["size"]),
                price = float(row["price"])/1000,
                direction = int(row["direction"])
            )
            events.append(event)
        
        return events 