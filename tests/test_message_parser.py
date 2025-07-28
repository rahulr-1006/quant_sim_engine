import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_loader import LOBSTERMessageParser

def main():
    parser = LOBSTERMessageParser("/Users/rahulramakrishnan/Documents/quant/projects/quant_sim_engine/data/LOBSTER_SampleFile_AMZN_2012-06-21_10/AMZN_message.csv")
    events = parser.parse_message()

    for event in events[:5]:
        print(event)

if __name__ == "__main__":
    main()
