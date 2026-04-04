"""Risk Controls - Bulletproof"""
import time

class RiskManager:
    def __init__(self, cfg):
        t = cfg.get('trading', {}) or {}
        self.max_daily_loss = float(t.get('max_daily_loss', 200) or 200)
        self.max_trades = int(float(t.get('max_trades_per_day', 5) or 5))
        self.max_positions = int(float(t.get('max_open_positions', 3) or 3))
        self.cooldown = int(float(t.get('cooldown_seconds', 60) or 60))
        self.loss_cooldown = int(float(t.get('loss_cooldown_seconds', 120) or 120))
        self.max_consecutive_losses = int(float(t.get('max_consecutive_losses', 3) or 3))
        self.min_capital_floor = float(t.get('min_capital_floor', 300) or 300)
        
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.open_positions = {}
        self.last_trade_time = 0
        self.last_trade_was_loss = False
        self.consecutive_losses = 0
        self.kill_switch = False

    def can_trade(self, capital):
        if self.kill_switch: return False, "KILL SWITCH ACTIVE"
        if capital <= self.min_capital_floor:
            self.kill_switch = True
            return False, "Capital protection floor reached"
        if self.daily_pnl <= -self.max_daily_loss:
            self.kill_switch = True
            return False, "Daily loss limit reached"
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.kill_switch = True
            return False, "Consecutive loss limit reached"
        if self.daily_trades >= self.max_trades: return False, "Max trades reached"
        if len(self.open_positions) >= self.max_positions: return False, "Max positions reached"
        return True, "OK"

    def check_cooldown(self):
        now = time.time()
        wait = self.loss_cooldown if self.last_trade_was_loss else self.cooldown
        if self.consecutive_losses >= 3: wait = 300
        if now - self.last_trade_time < wait: return False, f"Cooldown {int(wait - (now - self.last_trade_time))}s"
        return True, "OK"
