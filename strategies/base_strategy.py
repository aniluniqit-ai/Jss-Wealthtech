"""Base Strategy Template"""
class BaseStrategy:
    NAME = "BASE"
    MARKET_TYPES = ["BULLISH", "BEARISH", "SIDEWAYS", "ANY"]
    DAY_TYPES = ["MON", "TUE", "WED", "THU", "FRI", "ANY"]
    TIME_WINDOWS = ["OPENING", "TRENDING", "SLOW", "RE_ENTRY", "CLOSING", "ANY"]
    EXPIRY_ONLY = False
    MIN_CONFIDENCE = 60

    def analyze(self, data, indicators, market_condition):
        return ("HOLD", 0, "Base strategy")

    def info(self):
        return {
            "name": self.NAME,
            "market": self.MARKET_TYPES,
            "days": self.DAY_TYPES,
            "times": self.TIME_WINDOWS,
            "expiry_only": self.EXPIRY_ONLY,
            "min_confidence": self.MIN_CONFIDENCE
        }
