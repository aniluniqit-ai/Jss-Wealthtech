"""Capital Management"""
from datetime import datetime
from zoneinfo import ZoneInfo

class CapitalManager:
    def __init__(self, initial_capital=1000):
        self.initial = initial_capital
        self.current = initial_capital
        self.peak = initial_capital
        self.total_pnl = 0.0
        self.trades_count = 0
        self.wins = 0
        self.losses = 0
        self.history = []

    def _now(self):
        return datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

    def add_profit(self, amount):
        self.total_pnl += amount
        self.current += amount
        self.wins += 1
        self.trades_count += 1
        if self.current > self.peak:
            self.peak = self.current
        self.history.append((self._now(), self.current, amount))

    def add_loss(self, amount):
        self.total_pnl -= amount
        self.current -= amount
        self.losses += 1
        self.trades_count += 1
        self.history.append((self._now(), self.current, -amount))

    def get_lot_size(self, symbol_lot=50):
        if self.current < 10000:
            return 1
        return min(3, max(1, int(self.current / (symbol_lot * 200))))

    def get_drawdown_pct(self):
        if self.peak <= 0:
            return 0
        return (self.peak - self.current) / self.peak * 100
