# 📘 Real-Time Quant Backtester & Execution Simulator

**Last Updated:** 2025-07-28 09:30:16

This project is a modular, event-driven backtesting and execution simulation framework designed for **realistic modeling of algorithmic trading strategies** on **tick-level financial data**.

Unlike traditional vectorized backtesters that assume perfect execution and unrealistic fills, this engine simulates the full **signal-to-execution pipeline** with real-world constraints in mind — **slippage**, **latency**, **queue dynamics**, and **execution algorithms** like **VWAP**, **TWAP**, and **POV**.

---

## 🎯 Why This Project Matters

In quantitative trading, designing alpha models is only half the battle. How you **execute** those models in the market — given latency, liquidity, and slippage — can make or break your edge. This project was built to bridge that gap.

It reflects the real-world concerns of quant trading desks:

- Can our strategy survive under real-time conditions?
- How much does execution cost eat into our alpha?
- What are the risks of poor liquidity or delayed fills?

---

## 🛠️ Key Features

- ✅ Tick-level, event-driven architecture simulating real market flow.
- ✅ Limit Order Book simulator with market/limit/cancel order support.
- ✅ Execution algorithms: VWAP, TWAP, POV with dynamic slicing.
- ✅ Latency + slippage modeling to reflect execution realism.
- ✅ Modular alpha signal integration for plug-and-play strategy testing.
- ✅ Built-in risk and performance analytics (Sharpe, drawdown, win rate).
- ✅ Optional C++ optimizations for low-latency order matching.

---

## 👨‍💻 Tech Stack

- **Python** for core infrastructure
- **C++** (optional) for performance-critical modules
- **Matplotlib / Streamlit** for analytics and dashboards
- **NumPy / Pandas** for performance analysis
- **pybind11** for Python-C++ bindings (planned)

---

## 📌 Use Cases

- Backtest high-frequency or low-latency strategies on real data.
- Compare different execution strategies under adverse conditions.
- Study the interaction between alpha strength and execution cost.
- Showcase professional-grade trading infra engineering on your resume.

---

## 🗓️ Project Progress Journal

> Each week has a section logging technical progress **and learning rationale**.

---

### Week 2: Order Book Matching Engine (Detailed Report)

### Completed Tasks:

* [x] Designed the core `OrderBook` class to maintain separate bid and ask order books using Python dictionaries:

  * Key: price level (float)
  * Value: list of `Order` objects at that price, preserving FIFO order
* [x] Implemented `add_order(order)` method to insert new orders at correct price level, appending to the FIFO list
* [x] Implemented `cancel_order(order_id)` method to find and remove an order by ID from the relevant book side
* [x] Maintained an `order_map` dictionary mapping `order_id` to the `Order` instance for fast lookups
* [x] Developed `get_best_bid()` and `get_best_ask()` methods by sorting bid and ask price keys and returning top-of-book prices
* [x] Managed order quantity updates when partial fills occur and removed fully executed or canceled orders cleanly
* [x] Built a `trades` list to log all execution events, storing dictionaries with `price`, `quantity`, `timestamp`, and IDs of buy/sell sides
* [x] Tested matching engine with synthetic order sequences to validate FIFO matching and proper book state transitions
* [x] Integrated bid/ask top-of-book snapshots into Streamlit UI for live monitoring and debugging

### Design Decisions:

* Chose dictionary with price keys → lists of orders to represent the book because it naturally enforces FIFO queue order per price level and supports quick appends/removals
* Sorting price keys on-demand to get best bid/ask keeps complexity manageable for this prototype phase; full priority queues could be added later for optimization
* Kept a global `order_map` for quick order lookups to handle cancelations and partial fills, avoiding costly linear scans
* Designed order removal logic carefully to ensure no dangling references in both price-level lists and the `order_map`

### Testing & Debugging:

* Created manual synthetic events for adding, canceling, and executing orders to observe correct queue updates and match prices
* Logged internal book states after each event to verify price-level order lists remained consistent and FIFO
* Used Streamlit live UI snapshot of top bids and asks to visually verify expected changes during testing

### Challenges Faced:

* Handling cancellations was tricky — needed to find and remove orders efficiently without breaking the FIFO queue structure
* Making sure partial fills updated the correct order’s quantity and triggered removal when quantity dropped to zero required careful checks
* Avoiding desync between `order_map` and price-level lists during removes was a common source of bugs early on

### Reflection:

Week 2 was me wrestling with the core matching logic. Writing an order book from scratch made me realize how fundamental price-time priority really is and how subtle queue maintenance can get. It was frustrating at times, especially when cancels and partial executions didn’t update properly, but now the core engine feels rock solid. Having live top-of-book snapshots in Streamlit really helped me debug visually and get immediate feedback.

---

### Week 3: Strategy Integration + Signal Routing (Detailed Report)

### Completed Tasks:

* [x] Integrated `AlwaysTakeLiquidityStrategy` into the event processing loop:

  * After processing each market event, strategy generates new market orders based on best bid/ask
* [x] Added `is_strategy` flag on orders to distinguish strategy-generated orders vs. native market orders
* [x] Modified execution logic to update strategy position and PnL on trades involving strategy orders
* [x] Displayed real-time trade logs in the Streamlit UI, showing executed prices, quantities, and buy/sell IDs for traceability
* [x] Wired up position tracking through `PositionTracker` class, recording position size and average entry price
* [x] Tested execution of strategy orders against top-of-book liquidity, verifying fills and position updates
* [x] Started planning abstraction for multiple strategies and latency/jitter simulation

### Design Decisions:

* Strategy logic runs synchronously after each event to maintain event-driven real-time feel
* `is_strategy` flag enables clean separation of strategy trades for accurate PnL and position accounting
* Position tracker centralizes position state, decoupling it from order book and strategy code
* Trade logging and UI display aid rapid debugging and validation of strategy behavior

### Testing & Debugging:

* Verified that strategy orders hit resting liquidity and correctly update position size live
* Used printed trade logs and UI feedback to catch edge cases like multiple executions per tick
* Observed position tracker values in Streamlit update accurately in response to trade events

### 🔄 Challenges Faced:

* Ensuring position tracker correctly updated on partial fills with multiple overlapping orders required careful trade event handling
* Making sure that strategy orders don’t get double counted or missed during fills was subtle
* Keeping the UI in sync with internal state during rapid tick replay involved some session state management

### Reflection:

Week 3 was all about connecting the pieces: from market events to strategy orders to execution fills and position updates. The AlwaysTakeLiquidityStrategy was a perfect first test since it’s straightforward but forces full pipeline execution. Seeing my strategy trades hit the order book and update the UI gave me a huge boost of confidence. Next steps are making the strategy plug-in architecture more flexible and adding realistic latency — that will make things way more interesting.
```