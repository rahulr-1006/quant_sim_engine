# 📘 Real-Time Quant Backtester & Execution Simulator

A modular, event-driven framework for **simulating algorithmic trading strategies** with **realistic market execution**. This engine is built for tick-level backtesting and designed to model real-world frictions like **slippage**, **latency**, **queue dynamics**, and **execution cost**—key factors often ignored by traditional backtesters.

---

## 🚀 Why This Project Matters

In the real world, alpha generation is only half the battle. The other half? Executing that alpha *under real constraints*. Every trading strategy is subject to slippage, order queueing, and latency—factors that can erode profitability or even invert your edge.

This project simulates the **entire signal-to-execution pipeline** as realistically as possible to answer questions like:

- Can our strategy survive live execution in a high-frequency setting?
- How does slippage impact performance across venues and instruments?
- What are the PnL and risk implications of different execution strategies?

---

## 🛠️ Core Features

- **Tick-Level Simulation**: Reads granular market event data (LOBSTER), simulates order flow minute by minute.
- **Limit Order Book (LOB) Engine**: Implements price-time priority with support for market, limit, cancel, and delete events.
- **Execution Algorithms**: Built-in VWAP, TWAP, and POV slicing strategies to test realistic fill scenarios.
- **Latency & Slippage Modeling**: Add execution delays, simulate queue position, jitter, and fill degradation.
- **Signal Routing**: Modular plug-in system for alpha generation logic → order → execution → ledger.
- **PnL + Risk Engine**: Real-time position tracking, mark-to-market, cumulative returns, Sharpe, drawdown, win rate.
- **Optional C++ Optimization**: Performance-critical modules (e.g., order book matching) written in C++ with Python bindings via `pybind11`.
- **Visualization Suite**: Streamlit dashboards and Matplotlib for live performance monitoring and analysis.

---

## 🧠 Learning Objectives

This project was designed not just to build a functional backtester, but to **deeply understand the real mechanics of market structure** and execution:

- Internalize how exchange-level matching works
- Analyze how latency affects fill quality
- Experiment with slicing vs. aggressive execution
- Quantify execution cost and its impact on alpha retention

---

## 📚 Dataset: LOBSTER

We use [LOBSTER](https://lobsterdata.com/) tick-level order book data (Amazon stock) as our primary input. The `message` file encodes all market events with:

| Column | Name         | Description                                                |
|--------|--------------|------------------------------------------------------------|
| 1      | Time         | Seconds after midnight (e.g. 34200.189 = 9:30:00.189)     |
| 2      | Type         | Event type (e.g. new order, cancel, execution, delete)     |
| 3      | Order ID     | Unique identifier per order                                |
| 4      | Size         | Number of shares                                           |
| 5      | Price        | Price × 10,000 (e.g. 2237500 = \$223.75)                  |
| 6      | Direction    | +1 for buy, -1 for sell (only for applicable messages)     |

---

## 🧱 Architecture Overview

```text
 ┌─────────────┐
 │ Alpha Signal│
 └────┬────────┘
      ▼
┌────────────┐       ┌────────────┐
│ OrderManager│─────▶│ Execution  │
└────┬────────┘       │ Engine     │
     │                └────┬───────┘
     ▼                     ▼
┌──────────┐       ┌────────────┐
│ Ledger   │◀──────│ Order Book │
└──────────┘       └────────────┘
````

---

## 💻 Tech Stack

| Layer                  | Tools                            |
| ---------------------- | -------------------------------- |
| Core Engine            | Python                           |
| Execution Optimization | C++ (planned) + pybind11         |
| Data Analysis          | NumPy, Pandas                    |
| Visualization          | Matplotlib, Streamlit            |
| Dataset Format         | LOBSTER (message file)           |
| Testing                | Pytest + synthetic order streams |

---

## 📈 Sample Use Cases

* **Backtest latency-sensitive strategies** on real order book microstructure
* **Quantify slippage cost** across VWAP vs. aggressive routing
* Study **queue priority impact** for market-making strategies
* Use as a **resume-ready proof of systems knowledge** for quant interviews

---

## 🔮 Planned Modules (v1 Milestone)

* [ ] Full support for real-time alpha integration
* [ ] Live signal → order → fill simulation pipeline
* [ ] Execution algos: POV, TWAP, VWAP with parameters
* [ ] Realistic fill modeling (queue depletion, latency jitter)
* [ ] Position and exposure tracking
* [ ] Real-time PnL visualization dashboard
* [ ] C++ backend for high-speed matching (via pybind11)

---

## 🧪 Sample Output (Coming Soon)

```text
> MarketEvent(timestamp=34200.189, type='add', order_id=1234, price=223.75, size=100, direction=+1)
> Order matched: buy 100 @ 223.75 (queue pos: 2, latency: 3ms, slippage: 0.02%)
> Current PnL: +$0.84 | Position: +100 | Max Drawdown: -$1.12
```

---

## 📁 Project Structure

```bash
quant_backtester/
├── core/
│   ├── market_event.py
│   ├── order_book.py
│   ├── order_manager.py
│   └── execution_engine.py
├── data/
│   └── lobster_amzn_sample.csv
├── signals/
│   └── simple_momentum.py
├── analytics/
│   ├── pnl_tracker.py
│   └── risk_metrics.py
├── notebooks/
│   └── walk_through.ipynb
└── streamlit_dashboard/
    └── app.py
```

---

## 🎓 Author & Contact

**Rahul Ramakrishnan**
Quant systems enthusiast building infrastructure from scratch as part of a long-term prep journey.
📧 [GitHub](https://github.com/rahulr-1006) · 💼 [LinkedIn](https://www.linkedin.com/in/rahulr-1006)

---

## ⭐️ If you’re hiring or collaborating…

This project was built to *simulate*, *learn*, and *showcase* real-world quant systems knowledge — especially execution nuance. If you’re working on research infra, HFT platforms, or simulation stacks — reach out!

