from .base_strategy import BaseStrategy

class Strategy(BaseStrategy):
    NAME = "MULTI_SCALPING"
    MARKET_TYPES = ["BULLISH", "BEARISH", "ANY"]
    DAY_TYPES = ["MON", "TUE", "WED", "THU", "FRI", "ANY"]
    TIME_WINDOWS = ["TRENDING", "RE_ENTRY", "CLOSING", "ANY"]
    EXPIRY_ONLY = False
    MIN_CONFIDENCE = 60

    def analyze(self, data, indicators, market_condition):
        summary = indicators.get('summary', {})
        bullish = summary.get('bullish', 0)
        bearish = summary.get('bearish', 0)
        total = summary.get('total', 1)
        
        buy_score = bullish - bearish
        
        if buy_score > 3:
            return ("BUY", min(85, 60 + buy_score * 3), f"Bullish dominance {bullish}/{total}")
        elif buy_score < -3:
            return ("SELL", min(85, 60 + abs(buy_score) * 3), f"Bearish dominance {bearish}/{total}")
        else:
            return ("HOLD", 20, f"No clear edge {bullish}vs{bearish}")

STRATEGY = Strategy()
