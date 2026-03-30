"""Option Chain Analysis"""
from dataclasses import dataclass

@dataclass
class OptionChainData:
    atm_strike: int = 0
    atm_ce_premium: float = 0
    atm_pe_premium: float = 0
    pcr: float = 0
    max_ce_oi_strike: int = 0
    max_pe_oi_strike: int = 0
    ce_oi_atm: int = 0
    pe_oi_atm: int = 0
    support: float = 0
    resistance: float = 0

class OptionChain:
    def __init__(self):
        self.cache = {}

    def get_atm(self, symbol, index_price, kotak_api=None):
        if kotak_api:
            data = self._from_kotak(symbol, index_price, kotak_api)
            if data:
                return data
        return self._estimate(symbol, index_price)

    def _from_kotak(self, symbol, index_price, api):
        try:
            from brokers.kotak_neo import SYMBOLS
            info = SYMBOLS.get(symbol, {})
            step = info.get('step', 50)
            atm = round(index_price / step) * step
            
            # Estimate premium (2% of index)
            premium = index_price * 0.02
            
            return OptionChainData(
                atm_strike=atm,
                atm_ce_premium=round(premium, 2),
                atm_pe_premium=round(premium * 0.9, 2),
                pcr=1.0,
                support=atm - step,
                resistance=atm + step
            )
        except:
            return None

    def _estimate(self, symbol, index_price):
        from brokers.kotak_neo import SYMBOLS
        info = SYMBOLS.get(symbol, {})
        step = info.get('step', 50)
        atm = round(index_price / step) * step
        premium = index_price * 0.02
        
        return OptionChainData(
            atm_strike=atm,
            atm_ce_premium=round(premium, 2),
            atm_pe_premium=round(premium * 0.9, 2),
            pcr=1.0,
            support=atm - step,
            resistance=atm + step
        )
