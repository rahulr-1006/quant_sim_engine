class PositionTracker:
    def __init__(self):
        self.position = 0
        self.avg_entry_price = 0.0
        self.realized_pnl = 0.0

    def update(self, trade, is_strategy_trade):
        if not is_strategy_trade:
            print("⏩ Skipped non-strategy trade:", trade)
            return

        if isinstance(trade['buy_id'], str) and trade['buy_id'].startswith("strategy_"):
            side = 1  # Strategy bought → position increases
        elif isinstance(trade['sell_id'], str) and trade['sell_id'].startswith("strategy_"):
            side = -1  # Strategy sold → position decreases
        else:
            print("⛔️ Not a strategy trade — skipping:", trade)
            return

        qty = trade['quantity']
        price = trade['price']

        prev_pos = self.position
        self.position += side * qty

        # ➕ Open or add to position (same side)
        if prev_pos * self.position > 0 or prev_pos == 0:
            total_cost = self.avg_entry_price * abs(prev_pos) + price * qty
            self.avg_entry_price = total_cost / abs(self.position)

        # 🔁 Opposite direction (partially or fully closing)
        else:
            closing_qty = min(abs(prev_pos), qty)
            pnl = closing_qty * (self.avg_entry_price - price) * (-side)
            self.realized_pnl += pnl
            print(f"📈 Realized PnL updated: +${pnl:.2f} | Total: ${self.realized_pnl:.2f}")

            # If fully closed, reset entry price
            if self.position == 0:
                self.avg_entry_price = 0.0
            else:
                # New position in opposite direction → reset entry price
                remaining_qty = abs(self.position)
                self.avg_entry_price = price  # You just opened a new trade

        print(f"📊 Pos: {self.position}, Avg Entry: {self.avg_entry_price:.2f}, Realized PnL: {self.realized_pnl:.2f}")
