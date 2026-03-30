from .base_strategy import BaseStrategy

class Strategy(BaseStrategy):
    NAME = "EXPIRY_HEROPATLA"
    MARKET_TYPES = ["ANY"]
    DAY_TYPES = ["MON", "TUE", "WED", "THU", "FRI"]
    TIME_WINDOWS = ["ANY"]
    EXPIRY_ONLY = True
    MIN_CONFIDENCE = 55

    def analyze(self, data, indicators, market_condition):
        oc = market_condition.get('option_chain', {})
        atm_premium = oc.get('atm_ce_premium', 0)
        
        if atm_premium < 50:
            return ("BUY", 70, f"HEROPATLA! ATM premium Rs.{atm_premium} - Big move expected")
        elif atm_premium < 80:
            return ("BUY", 60, f"Low premium Rs.{atm_premium} - Scalping opportunity")
        else:
            return ("HOLD", 30, f"High premium Rs.{atm_premium} - Avoid")

STRATEGY = Strategy()
