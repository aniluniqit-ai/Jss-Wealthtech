from .base_strategy import BaseStrategy

class Strategy(BaseStrategy):
    NAME = "REVERSAL_SCALP"
    MARKET_TYPES = ["SIDEWAYS", "ANY"]
    DAY_TYPES = ["WED", "ANY"]
    TIME_WINDOWS = ["SLOW", "ANY"]
    EXPIRY_ONLY = False
    MIN_CONFIDENCE = 70

    def analyze(self, data, indicators, market_condition):
        ind = indicators.get('results', {})
        rsi = ind.get('RSI_14', {}).get('value', 50)
        
        if rsi < 30:
            return ("BUY", 75, f"RSI Oversold {rsi:.0f} - Reversal BUY")
        elif rsi > 70:
            return ("SELL", 75, f"RSI Overbought {rsi:.0f} - Reversal SELL")
        return ("HOLD", 10, f"RSI Neutral {rsi:.0f}")

STRATEGY = Strategy()
