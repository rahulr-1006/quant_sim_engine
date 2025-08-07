# Real-Time Quant Backtester & Execution Simulator

A modular, event-driven framework for **simulating algorithmic trading strategies** with realistic market execution. This engine operates on tick-level data and models key market frictions such as **slippage**, **latency**, **queue dynamics**, and **execution cost**—factors often ignored in traditional backtests.

---

## Why This Project Matters

In quantitative trading, generating alpha is only half the story. Successfully **executing** your strategy under real-world market constraints—latency, liquidity, and slippage—determines whether your edge survives.

This project provides a realistic simulation environment to answer:

- Can a strategy survive live market conditions?
- How does execution cost impact profitability?
- What risks arise from latency and queue position?

---

## Core Features

| Feature                    | Status     | Description                                         |
|----------------------------|------------|-----------------------------------------------------|
| Tick-Level Simulation      | Implemented | Replay LOBSTER market events tick-by-tick           |
| Limit Order Book Engine   | Implemented | Price-time priority matching, order lifecycle       |
| Strategy Integration      | Implemented | Plug-and-play strategies (e.g., liquidity taker)   |
| Position & PnL Tracking   | Partial     | Tracks position size, average entry, realized PnL   |
| Execution Algorithms      | Planned     | VWAP, TWAP, POV slicing                              |
| Latency & Slippage Modeling | Planned   | Simulate realistic fills with jitter and delay      |
| Streamlit Dashboard       | Implemented | Interactive UI for event stepping and live metrics  |
| C++ Matching Engine       | Planned     | Performance boost with pybind11                      |

---

## Architecture Overview

```text
          +-------------------+
          |  Alpha Signal Gen  |
          +---------+---------+
                    |
                    v
          +-------------------+
          |   Order Manager   |
          +---------+---------+
                    |
                    v
          +-------------------+           +---------------+
          |   Execution Engine | <-------> |  Order Book   |
          +---------+---------+           +---------------+
                    |
                    v
          +-------------------+
          |      Ledger       |
          +-------------------+


---

## Dataset: LOBSTER Tick-Level Market Data

| Column | Name      | Description                                           |
| ------ | --------- | ----------------------------------------------------- |
| 1      | Time      | Seconds after midnight (e.g. 34200.189 = 9:30:00.189) |
| 2      | Type      | Event type code (new order, cancel, execution, etc.)  |
| 3      | Order ID  | Unique identifier for the order                       |
| 4      | Size      | Number of shares                                      |
| 5      | Price     | Price × 10,000 (e.g. 2237500 = \$223.75)              |
| 6      | Direction | +1 for buy, -1 for sell (if applicable)               |

---

## Usage

Run the Streamlit dashboard locally:

```bash
streamlit run app.py
```

Features include:

* Step through market events tick-by-tick
* Run full backtests over historical data
* View live order book top-of-book snapshots
* Monitor recent trades and strategy position
* Track PnL and average entry price dynamically

---

## Project Structure

```bash
quant_sim_engine/
├── core/
│   ├── market_event.py
│   ├── order_book.py
│   ├── order.py
│   ├── strategy.py
│   └── position_tracker.py
├── data/
│   └── LOBSTER_SampleFile_AMZN_2012-06-21_10/
├── app.py
├── main.py
├── progress_tracker.md
├── README.md
└── tests/
```

---

## Roadmap & Future Work

| Milestone                         | Status  | Notes                          |
| --------------------------------- | ------- | ------------------------------ |
| Complete position and PnL engine  | Partial | Realized PnL logic in progress |
| Add VWAP, TWAP, and POV algos     | Planned | Execution slicing strategies   |
| Introduce latency & jitter models | Planned | Simulate realistic delays      |
| C++ backend for matching engine   | Planned | Performance optimization       |
| Enhanced visualization dashboards | Planned | Return, drawdown, heatmaps     |

---

## About the Author

**Rahul Ramakrishnan**
Quantitative systems developer focused on realistic trading simulation and execution modeling.

* GitHub: [rahulr-1006](https://github.com/rahulr-1006)
* LinkedIn: [rahul-ramakrishnan10062003](https://www.linkedin.com/in/rahul-ramakrishnan10062003/)

---

## Collaboration & Hiring

This project is built as a technical showcase of quant systems engineering and algorithmic strategy implementation. If you’re working on market simulation infrastructure, execution algorithms, or quant research platforms, feel free to reach out!

---

For detailed weekly progress and technical logs, see the [progress tracker](PROGRESS.md).
