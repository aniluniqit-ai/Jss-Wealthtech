from .base_strategy import BaseStrategy

class Strategy(BaseStrategy):
    NAME = "MOMENTUM_FOLLOW"
    MARKET_TYPES = ["BULLISH", "BEARISH"]
    DAY_TYPES = ["TUE", "WED", "THU", "ANY"]
    TIME_WINDOWS = ["TRENDING", "RE_ENTRY", "ANY"]
    EXPIRY_ONLY = False
    MIN_CONFIDENCE = 65

    def analyze(self, data, indicators, market_condition):
        ind = indicators.get('results', {})
        ema9 = ind.get('EMA_9', {}).get('signal', '')
        ema21 = ind.get('EMA_21', {}).get('signal', '')
        macd = ind.get('MACD', {}).get('signal', '')
        st = ind.get('SuperTrend', {}).get('signal', '')
        
        score = 0
        if ema9 == "BULLISH": score += 25
        if ema21 == "BULLISH": score += 20
        if macd == "BULLISH": score += 25
        if st == "BULLISH": score += 30
        
        if score >= 70:
            return ("BUY", score, f"Momentum BUY score={score}")
        elif score <= -70:
            return ("SELL", abs(score), f"Momentum SELL score={score}")
        return ("HOLD", 15, f"No momentum score={score}")

STRATEGY = Strategy()
