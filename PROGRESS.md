
# 🗓️ Project Progress Journal

> Each week has a section logging technical progress **and learning rationale**.

---

### 📅 Week 1: Project Setup + Data Ingestion ✅
**Report**
> For this week, my tasks were simple:
- [x] Initialized GitHub repo + folder structure
- [x] Chose LOBSTER as the initial tick-level dataset
- [x] Built a CSV parser for LOBSTER `message` files
- [x] Defined internal `MarketEvent` structure with attributes:
  - `timestamp`, `event_type`, `order_id`, `size`, `price`, `direction`
- [x] Printed and verified parsed events via test harness

I decided to choose LOBSTER amazon sample data to first get the ball rolling: simple, easy to parse data that has ample information.

The message file, which contains the sequence of market events that describe all modifications to the order bok for a given security on a specific trading day.

The columns were as follows:

 | Column | Name          | Description                                                            |
| ------ | ------------- | ---------------------------------------------------------------------- |
| 1      | **Time**      | Seconds after midnight (e.g. `34200.18960767` = 9:30:00.189)           |
| 2      | **Type**      | Event type code (see below)                                            |
| 3      | **Order ID**  | Unique ID of the order being referenced                                |
| 4      | **Size**      | Number of shares (e.g. 100)                                            |
| 5      | **Price**     | Price × 10,000 (i.e., 2237500 = \$223.75)                              |
| 6      | **Direction** | +1 = buy order, -1 = sell order (for order submissions and executions) |

This information was derived from the README file attached to the dataset

Once I got the data loaded. I set up my market_event class and the data_loader files to properly parse the csv. I tested this and it worked!

---

### 📅 Week 2: Basic Order Book Matching Engine 🔄

**Tasks In Progress:**
- [ ] Build `OrderBook` class with price-time priority
- [ ] Support new orders, cancels, deletions, hidden orders
- [ ] Implement FIFO matching logic
- [ ] Write unit tests on synthetic input
- [ ] Visualize top-of-book updates

**Why This Matters:**
> Building my own matching engine is the most educational part. This mimics how real exchanges process orders and helps me understand how queue position and latency impact fills. 

---

### 📅 Week 3: Signal Integration + Order Routing (Planned)

- [ ] Define basic alpha signal format
- [ ] Route signals to `OrderManager`
- [ ] Add latency + random network jitter
- [ ] Simulate real-time flow: signal → order → execution → ledger

---

### 📅 Week 4: Position & PnL Engine (Planned)

- [ ] Build `PositionTracker` to monitor live positions
- [ ] Compute mark-to-market and realized PnL
- [ ] Track per-trade and cumulative returns
- [ ] Plot PnL and exposure

---

### 📅 Week 5+: Risk, Execution, and Optimization (Planned)

- Execution Algos (VWAP/TWAP/POV)
- Risk Analytics (drawdown, exposure, slippage)
- C++ speedup phase
- Multi-strategy config loader
- Streamlit / dashboard visualizations

---

## ✅ Final Deliverables (By Week 10)

- [ ] Fully working event-driven backtester
- [ ] Execution engine with queue simulation + latency
- [ ] Strategy plug-in system
- [ ] Trade/PnL visualizations
- [ ] Polished GitHub repo for resume + interviews

---

## 🧾 Contact

*Built by Rahul Ramakrishnan as part of a long-term quant prep journey.  
Open to collaboration or discussion — reach me on [GitHub](https://github.com/rahulr-1006) or LinkedIn.*

---
