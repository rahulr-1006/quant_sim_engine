import pandas as pd 

class Simulator:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        print(f" Loaded {len(self.data)} ticks from {data_path}")
    
    def run(self):
        for index, row in self.data.iterrows:
            tick = {
                "timestamp": row.get("Dat")
            }
