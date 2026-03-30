"""Technical Indicators"""
import pandas as pd
import numpy as np

class Indicators:
    def __init__(self):
        self.results = {}

    def calc_all(self, df):
        if df.empty or len(df) < 30:
            return {}
        self.results = {}
        c, h, l = df['close'], df['high'], df['low']
        v = df['volume'] if 'volume' in df else pd.Series([1]*len(df))

        # SMA
        for p in [5, 10, 20, 50]:
            sma = c.rolling(p).mean().iloc[-1]
            self.results[f'SMA_{p}'] = {'value': round(sma,2), 'signal': "BULLISH" if c.iloc[-1] > sma else "BEARISH"}

        # EMA
        for p in [9, 21]:
            ema = c.ewm(span=p).mean().iloc[-1]
            self.results[f'EMA_{p}'] = {'value': round(ema,2), 'signal': "BULLISH" if c.iloc[-1] > ema else "BEARISH"}

        # RSI
        delta = c.diff()
        g = delta.where(delta>0,0).rolling(14).mean()
        ls = (-delta.where(delta<0,0)).rolling(14).mean()
        rsi = (100 - (100/(1+g/ls))).iloc[-1]
        self.results['RSI_14'] = {'value': round(rsi,2), 'signal': "BULLISH" if rsi<30 else ("BEARISH" if rsi>70 else "NEUTRAL")}

        # VWAP
        tp = (h + l + c) / 3
        vwap = (tp * v).cumsum() / v.cumsum()
        self.results['VWAP'] = {'value': round(vwap.iloc[-1],2), 'signal': "BULLISH" if c.iloc[-1] > vwap.iloc[-1] else "BEARISH"}

        # MACD
        ema12 = c.ewm(span=12).mean()
        ema26 = c.ewm(span=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        hist = macd - signal
        self.results['MACD'] = {'value': round(macd.iloc[-1],2), 'signal': "BULLISH" if hist.iloc[-1] > 0 else "BEARISH"}

        # SuperTrend
        atr = (h - l).rolling(10).mean()
        mid = (h + l) / 2
        st_upper = mid + 2 * atr
        st_lower = mid - 2 * atr
        self.results['SuperTrend'] = {'value': round(mid.iloc[-1],2), 'signal': "BULLISH" if c.iloc[-1] > st_lower.iloc[-1] else "BEARISH"}

        # ATR
        self.results['ATR_14'] = {'value': round(atr.rolling(14).mean().iloc[-1],2), 'signal': "N/A"}

        # Bollinger
        bb_sma = c.rolling(20).mean()
        bb_std = c.rolling(20).std()
        bb_upper = bb_sma + 2 * bb_std
        bb_lower = bb_sma - 2 * bb_std
        self.results['Bollinger_20'] = {'value': round(bb_sma.iloc[-1],2), 'signal': "NEUTRAL" if bb_lower.iloc[-1] < c.iloc[-1] < bb_upper.iloc[-1] else "EXTREME"}

        # Summary
        bullish = sum(1 for v in self.results.values() if v.get('signal') == 'BULLISH')
        bearish = sum(1 for v in self.results.values() if v.get('signal') == 'BEARISH')
        self.results['_summary'] = {'bullish': bullish, 'bearish': bearish, 'total': len(self.results)}
        
        return self.results
