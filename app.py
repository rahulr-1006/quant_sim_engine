import streamlit as st
import pandas as pd
from core.order_book import OrderBook
from core.order import Order, Side, OrderType
from core.strategy import AlwaysTakeLiquidityStrategy
from core.position_tracker import PositionTracker

# ------------------------------
# Initialize strategy and PnL tracker
# ------------------------------
strategy = AlwaysTakeLiquidityStrategy()

# ------------------------------
# Load and cache data
# ------------------------------
@st.cache_resource
def get_book_and_tracker():
    tracker = PositionTracker()
    book = OrderBook(position_tracker=tracker)
    return book, tracker

book, position_tracker = get_book_and_tracker()


@st.cache_data
def load_message_data():
    path = "data/LOBSTER_SampleFile_AMZN_2012-06-21_10/AMZN_message.csv"
    cols = ['timestamp', 'type', 'order_id', 'size', 'price', 'direction']
    df = pd.read_csv(path, header=None, names=cols)
    df['price'] = df['price'] / 10000  # Convert to dollars
    return df

df = load_message_data()

# ------------------------------
# Initialize Streamlit state
# ------------------------------
if 'event_index' not in st.session_state:
    st.session_state['event_index'] = 0
if 'position' not in st.session_state:
    st.session_state['position'] = 0
if 'avg_entry' not in st.session_state:
    st.session_state['avg_entry'] = 0.0
if 'realized_pnl' not in st.session_state:
    st.session_state['realized_pnl'] = 0.0



# ------------------------------
# Event Processor
# ------------------------------
def process_lobster_event(row):
    event_type = row['type']
    price = row['price']
    qty = int(row['size'])
    order_id = int(row['order_id'])
    side = Side.BUY if row['direction'] == 1 else Side.SELL
    timestamp = row['timestamp']

    if event_type == 1:  # Add limit order
        order = Order(
            order_id=order_id,
            side=side,
            price=price,
            quantity=qty,
            timestamp=timestamp,
            order_type=OrderType.LIMIT
        )
        book.add_order(order)

    elif event_type == 2:  # Cancel order
        book.cancel_order(order_id)

    elif event_type == 4:  # Execute visible resting order
        resting_order = book.order_map.get(order_id)
        if resting_order:
            executed_qty = min(resting_order.quantity, qty)
            trade = {
                'price': resting_order.price,
                'quantity': executed_qty,
                'timestamp': timestamp,
                'buy_id': order_id if resting_order.side == Side.SELL else 'market',
                'sell_id': order_id if resting_order.side == Side.BUY else 'market'
            }
            book.trades.append(trade)
            if resting_order.is_strategy:
                position_tracker.update(trade, is_strategy_trade=True)

            resting_order.quantity -= executed_qty
            if resting_order.quantity <= 0:
                book.cancel_order(order_id)

    # Run strategy
    best_bid = book.get_best_bid()
    best_ask = book.get_best_ask()
    if best_bid is None or best_ask is None:
        return

    if best_bid and best_ask:
        algo_order = strategy.generate_order(best_bid[0], best_ask[0], timestamp)
        if algo_order:
            algo_order.order_id = f"strategy_{timestamp}"
            algo_order.is_strategy = True
            book.add_order(algo_order)
        # else:
        #     print(f"No strategy order generated at timestamp {timestamp}")


# ------------------------------
# Streamlit UI
# ------------------------------
st.title("Real-Time LOBSTER Order Book Simulator")

st.subheader("Event Replay Controls")
col1, col2 = st.columns(2)

with col1:
    if st.button("Step Forward One Tick"):
        if st.session_state.event_index < len(df):
            row = df.iloc[st.session_state.event_index]
            st.session_state.event_index += 1
            process_lobster_event(row)

with col2:
    if st.button("Run Full Backtest"):
        while st.session_state.event_index < len(df):
            row = df.iloc[st.session_state.event_index]
            st.session_state.event_index += 1
            process_lobster_event(row)
        st.success("Full backtest complete.")

# ------------------------------
# Top-of-Book Display
# ------------------------------
st.subheader("Top-of-Book Snapshot")

def get_top_of_book(book, depth=5):
    data = {"Bids": [], "Asks": []}
    for price in list(book.bids.keys())[:depth]:
        qty = sum(order.quantity for order in book.bids[price])
        data["Bids"].append(f"{price:.2f} x {qty}")
    for price in list(book.asks.keys())[:depth]:
        qty = sum(order.quantity for order in book.asks[price])
        data["Asks"].append(f"{price:.2f} x {qty}")
    return data

top = get_top_of_book(book)
col1, col2 = st.columns(2)
with col1:
    st.write("Bids")
    for entry in top["Bids"]:
        st.write(entry)
with col2:
    st.write("Asks")
    for entry in top["Asks"]:
        st.write(entry)

# ------------------------------
# Trade Log
# ------------------------------
st.subheader("Recent Trades")
if book.trades:
    for trade in reversed(book.trades[-10:]):
        st.write(
            f"{trade['timestamp']:.2f} | "
            f"{trade['buy_id']} bought from {trade['sell_id']} @ "
            f"${trade['price']} x {trade['quantity']}"
        )
else:
    st.info("No trades yet.")

# -----------------------------------
# Display: Strategy PnL & Position
# -----------------------------------
st.subheader("Strategy Position & PnL")
st.write(f"**Position:** {position_tracker.position} shares")
st.write(f"**Average Entry:** ${position_tracker.avg_entry_price:.2f}")
st.write(f"**Realized PnL:** ${position_tracker.realized_pnl:.2f}")
