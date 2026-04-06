"""
JSS WEALTHTECH - TRADING ENGINE V8.0
॥ जय श्री सांवरीया सेठ ि॥
"""
import os, sys, json, time, threading
from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional

class Mode(Enum):
    NORMAL = "NORMAL"
    EXPIRY = "EXPIRY"
    SAFE = "SAFE"
    AGGRESSIVE = "AGGRESSIVE"
    KILL = "KILL"
    OBSERVE = "OBSERVE"
    WAIT = "WAIT"
    AI_LEARN = "AI_LEARN"

class TimeWindow(Enum):
    OPENING = "OPENING"
    TRENDING = "TRENDING"
    FAKE_BREAKOUT = "FAKE_BREAKOUT"
    SLOW = "SLOW"
    RE_ENTRY = "RE_ENTRY"
    CLOSING = "CLOSING"
    NO_TRADE = "NO_TRADE"
    MARKET_CLOSED = "MARKET_CLOSED"

class DayType(Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"

class MarketCondition(Enum):
    TRENDING_UP = "TRENDING_UP"
    TRENDING_DOWN = "TRENDING_DOWN"
    SIDEWAYS = "SIDEWAYS"
    REVERSAL_UP = "REVERSAL_UP"
    REVERSAL_DOWN = "REVERSAL_DOWN"
    UNKNOWN = "UNKNOWN"

class Season(Enum):
    SUMMER = "SUMMER"
    MONSOON = "MONSOON"
    WINTER = "WINTER"
    POST_MONSOON = "POST_MONSOON"

@dataclass
class Trade:
    id: str
    symbol: str
    direction: str
    option_type: str
    strike: int
    entry_price: float
    entry_time: str
    qty: int
    lot_size: int
    sl: float
    target: float
    trailing_sl: float
    confidence: float
    strategy: str
    reason: str
    exit_price: Optional[float] = None
    exit_time: Optional[str] = None
    pnl: Optional[float] = None
    status: str = "OPEN"
    partial_exited: bool = False

@dataclass
class MarketData:
    ltp: float = 0
    change: float = 0
    change_pct: float = 0
    high: float = 0
    low: float = 0
    open: float = 0
    close: float = 0
    volume: int = 0

class TradingEngine:
    EXPIRY_MAP = {
        DayType.MON: "FINNIFTY",
        DayType.TUE: "BANKNIFTY",
        DayType.WED: "MIDCPNIFTY",
        DayType.THU: "NIFTY",
        DayType.FRI: None,
        DayType.SAT: None,
        DayType.SUN: None
    }
    
    SYMBOLS = {
        'NIFTY': {'token': '26000', 'exchange': 'NSE_FO', 'lot': 50, 'step': 50},
        'BANKNIFTY': {'token': '26001', 'exchange': 'NSE_FO', 'lot': 15, 'step': 100},
        'FINNIFTY': {'token': '26002', 'exchange': 'NSE_FO', 'lot': 25, 'step': 50},
        'MIDCPNIFTY': {'token': '26004', 'exchange': 'NSE_FO', 'lot': 50, 'step': 25},
        'SENSEX': {'token': '26003', 'exchange': 'BSE_FO', 'lot': 10, 'step': 100},
        'BANKEX': {'token': '26005', 'exchange': 'BSE_FO', 'lot': 15, 'step': 100},
        'CRUDEOIL': {'token': '23737', 'exchange': 'MCX_FO', 'lot': 100, 'step': 50},
        'NATURALGAS': {'token': '23739', 'exchange': 'MCX_FO', 'lot': 1250, 'step': 10},
    }

    def __init__(self, config, kotak, option_chain, indicators, capital, risk, 
                 telegram_bot, telegram_reader, signal_parser, strategies):
        self.config = config
        self.kotak = kotak
        self.option_chain = option_chain
        self.indicators = indicators
        self.capital = capital
        self.risk = risk
        self.tg_bot = telegram_bot
        self.tg_reader = telegram_reader
        self.signal_parser = signal_parser
        self.strategies = strategies
        
        self.running = False
        self.mode = Mode.NORMAL
        self.current_trade = None
        self.trades_history = []
        self.telegram_signals = []
        self.telegram_read_groups = []
        self.last_tg_poll = ""
        self.last_decision = {}
        
        self.ltp_data = {}
        self.option_chain_data = {}
        self.candle_data = {}
        
        self.confidence = 0
        self.day_type = DayType.MON
        self.time_window = TimeWindow.MARKET_CLOSED
        self.market_condition = MarketCondition.UNKNOWN
        self.season = Season.WINTER
        self.expiry_symbol = None
        self.is_monthly_expiry = False
        self.momentum_score = 0
        self.buyer_seller_score = 0
        
        self.on_log = None
        self.on_update = None
        self.on_trade = None
        self._thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._log("🚀 Trading Engine Started")

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        self._log("🛑 Trading Engine Stopped")

    def _log(self, msg):
        if self.on_log:
            self.on_log(msg)
        print(f"[ENGINE] {msg}")

    def _notify(self, msg):
        self._log(msg)
        try:
            if self.tg_bot:
                self.tg_bot.send(msg)
        except:
            pass

    def _run(self):
        while self.running:
            try:
                self._update_time_context()
                
                if self.day_type in [DayType.SAT, DayType.SUN]:
                    self.mode = Mode.AI_LEARN
                    self._log("🧠 AI Learning Mode - Weekend")
                    time.sleep(60)
                    continue
                
                if self.time_window == TimeWindow.MARKET_CLOSED:
                    time.sleep(60)
                    continue
                
                self._update_mode()
                
                if self.mode == Mode.KILL:
                    time.sleep(30)
                    continue
                
                if self.mode == Mode.WAIT:
                    time.sleep(10)
                    continue
                
                self._fetch_data()
                self._read_telegram_signals()
                self._analyze_market()
                
                if self.current_trade:
                    self._check_exit_conditions()
                else:
                    self._find_trade()
                
                if self.on_update:
                    self.on_update(self._get_status())
                
                # YAHAN PEHLI GALTI THI - ABHI THEEK HAI
                interval = float(self.config.get('trading', {}).get('update_interval', 5) or 5)
                time.sleep(interval)
                
            except Exception as e:
                self._log(f"❌ Engine Error: {e}")
                time.sleep(5)

    def _update_time_context(self):
        now = datetime.now(ZoneInfo('Asia/Kolkata'))
        hour, minute = now.hour, now.minute
        time_val = hour * 60 + minute
        
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        self.day_type = DayType(days[now.weekday()])
        
        if time_val < 9 * 60 + 15:
            self.time_window = TimeWindow.MARKET_CLOSED
        elif time_val < 9 * 60 + 30:
            self.time_window = TimeWindow.OPENING
        elif time_val < 11 * 60:
            self.time_window = TimeWindow.TRENDING
        elif time_val < 11 * 60 + 5 or (time_val >= 11 * 60 + 55 and time_val < 12 * 60):
            self.time_window = TimeWindow.FAKE_BREAKOUT
        elif time_val < 13 * 60 + 30:
            self.time_window = TimeWindow.SLOW
        elif time_val < 14 * 60 + 30:
            self.time_window = TimeWindow.RE_ENTRY
        elif time_val < 15 * 60 + 15:
            self.time_window = TimeWindow.CLOSING
        elif time_val < 15 * 60 + 30:
            self.time_window = TimeWindow.NO_TRADE
        else:
            self.time_window = TimeWindow.MARKET_CLOSED
        
        month = now.month
        if month in [3, 4, 5]:
            self.season = Season.SUMMER
        elif month in [6, 7, 8]:
            self.season = Season.MONSOON
        elif month in [9, 10, 11]:
            self.season = Season.POST_MONSOON
        else:
            self.season = Season.WINTER
        
        self.expiry_symbol = self.EXPIRY_MAP.get(self.day_type)
        self.is_monthly_expiry = self._check_monthly_expiry(now)

    def _check_monthly_expiry(self, now):
        if now.weekday() != 3:
            return False
        next_thursday = now
        while next_thursday.month == now.month:
            next_thursday = next_thursday + timedelta(days=7)
        return next_thursday.month != now.month

    def _update_mode(self):
        prev_mode = self.mode
        can_trade, reason = self.risk.can_trade(self.capital.current)
        if not can_trade:
            self.mode = Mode.KILL
            if prev_mode != Mode.KILL:
                self._notify(f"🚨 {reason}")
            return
        
        drawdown = self.capital.get_drawdown_pct()
        if drawdown > 30:
            self.mode = Mode.KILL
        elif drawdown > 15:
            self.mode = Mode.SAFE
        elif self.capital.wins > 3 and (self.capital.total_pnl / self.capital.initial * 100) > 30:
            self.mode = Mode.AGGRESSIVE
        elif self.day_type == DayType.MON:
            self.mode = Mode.OBSERVE
        elif self.expiry_symbol:
            self.mode = Mode.EXPIRY
        elif self.time_window == TimeWindow.OPENING:
            self.mode = Mode.WAIT
        else:
            self.mode = Mode.NORMAL
        
        if prev_mode != self.mode:
            self._log(f"🔄 Mode: {prev_mode.value} → {self.mode.value}")

    def _fetch_data(self):
        if not self.kotak or not self.kotak.logged_in:
            return
        
        for symbol in self.SYMBOLS:
            try:
                quote = self.kotak.get_ltp(symbol)
                if quote:
                    self.ltp_data[symbol] = MarketData(
                        ltp=float(quote.get('ltp', 0)),
                        change=float(quote.get('change', 0)),
                        change_pct=float(quote.get('change_pct', 0)),
                        high=float(quote.get('high', 0)),
                        low=float(quote.get('low', 0)),
                        open=float(quote.get('open', 0)),
                        close=float(quote.get('close', 0)),
                        volume=int(quote.get('volume', 0))
                    )
            except:
                pass
        
        if self.expiry_symbol and self.expiry_symbol in self.ltp_data:
            idx_price = self.ltp_data[self.expiry_symbol].ltp
            if idx_price > 0:
                oc_data = self.option_chain.get_atm(self.expiry_symbol, idx_price, self.kotak)
                if oc_data:
                    self.option_chain_data[self.expiry_symbol] = oc_data

    def _read_telegram_signals(self):
        if not self.tg_reader or not self.tg_reader.connected:
            return
        read_groups = []
        for group in self.config.get('telegram_groups', []):
            if not group.get('active', False):
                continue
            try:
                gname = group.get('name', 'Unknown')
                messages = self.tg_reader.get_recent_messages(
                    group.get('hash_id') or group.get('chat_id'), limit=5
                )
                read_groups.append(gname)
                for msg in messages:
                    parsed = self.signal_parser.parse(msg.get('text', ''))
                    if parsed:
                        parsed['source'] = gname
                        parsed['time'] = msg.get('date', '')
                        self.telegram_signals.append(parsed)
                        self.telegram_signals = self.telegram_signals[-50:]
            except:
                pass
        self.telegram_read_groups = read_groups
        self.last_tg_poll = datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%H:%M:%S')

    def _analyze_market(self):
        for symbol in self.candle_data:
            if len(self.candle_data[symbol]) >= 30:
                self.indicators.calc_all(self.candle_data[symbol])
                break
        self.market_condition = self._detect_market_condition()
        self.momentum_score = self._calculate_momentum()
        self.buyer_seller_score = self._calculate_buyer_seller()

    def _detect_market_condition(self):
        ind = self.indicators.results
        if not ind:
            symbol = self.expiry_symbol if self.expiry_symbol else 'NIFTY'
            md = self.ltp_data.get(symbol)
            if md:
                if md.change_pct > 0.35:
                    return MarketCondition.TRENDING_UP
                if md.change_pct < -0.35:
                    return MarketCondition.TRENDING_DOWN
                if abs(md.change_pct) < 0.10:
                    return MarketCondition.SIDEWAYS
            return MarketCondition.UNKNOWN
        
        ema9 = ind.get('EMA_9', {}).get('signal', '')
        ema21 = ind.get('EMA_21', {}).get('signal', '')
        rsi = ind.get('RSI_14', {}).get('value', 50)
        st = ind.get('SuperTrend', {}).get('signal', '')
        
        if ema9 == 'BULLISH' and ema21 == 'BULLISH' and st == 'BULLISH':
            return MarketCondition.TRENDING_UP
        if ema9 == 'BEARISH' and ema21 == 'BEARISH' and st == 'BEARISH':
            return MarketCondition.TRENDING_DOWN
        if rsi < 30:
            return MarketCondition.REVERSAL_UP
        if rsi > 70:
            return MarketCondition.REVERSAL_DOWN
        return MarketCondition.UNKNOWN

    def _calculate_momentum(self):
        score = 0
        for symbol in self.candle_data:
            candles = self.candle_data[symbol]
            if len(candles) < 5:
                continue
            recent = candles[-5:]
            for c in recent:
                body = abs(c.get('close', 0) - c.get('open', 0))
                change = c.get('close', 0) - c.get('open', 0)
                if change > 0:
                    score += min(25, body * 2)
                else:
                    score -= min(25, body * 2)
            break
        if score == 0 and self.ltp_data:
            symbol = self.expiry_symbol if self.expiry_symbol else 'NIFTY'
            md = self.ltp_data.get(symbol)
            if md:
                score = md.change_pct * 25
        return max(-100, min(100, score))

    def _calculate_buyer_seller(self):
        score = 0
        ind = self.indicators.results
        if not ind:
            symbol = self.expiry_symbol if self.expiry_symbol else 'NIFTY'
            md = self.ltp_data.get(symbol)
            if not md:
                return 0
            return max(-100, min(100, md.change_pct * 40))
        for val in ind.values():
            signal = val.get('signal', '')
            if signal == 'BULLISH':
                score += 10
            elif signal == 'BEARISH':
                score -= 10
        return max(-100, min(100, score))

    def _find_trade(self):
        can_trade, reason = self.risk.can_trade(self.capital.current)
        if not can_trade:
            return
        cooldown_ok, _ = self.risk.check_cooldown()
        if not cooldown_ok:
            return
        if self.time_window in [TimeWindow.SLOW, TimeWindow.NO_TRADE, TimeWindow.MARKET_CLOSED]:
            return
        if self.market_condition == MarketCondition.SIDEWAYS:
            return
        
        strategy = self._select_strategy()
        if not strategy:
            return
        
        mc = {
            'time_window': self.time_window.value,
            'day_type': self.day_type.value,
            'expiry': self.expiry_symbol,
            'market_condition': self.market_condition.value,
            'option_chain': self.option_chain_data.get(self.expiry_symbol, {}),
            'momentum': self.momentum_score,
            'buyer_seller': self.buyer_seller_score,
            'season': self.season.value
        }
        
        signal, confidence, reason = strategy.analyze(
            self.ltp_data,
            {'results': self.indicators.results, 'summary': {}},
            mc
        )
        self.last_decision = {
            'signal': signal,
            'confidence': confidence,
            'reason': reason,
            'time': datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%H:%M:%S')
        }
        
        if self.time_window == TimeWindow.FAKE_BREAKOUT:
            confidence -= 15
        if self.day_type == DayType.MON:
            confidence -= 10
        
        tg_boost = self._check_telegram_agreement(signal)
        if tg_boost > 0:
            confidence += tg_boost
        
        self.confidence = max(0, min(100, confidence))
        min_momentum = int(float(self.config.get('trading', {}).get('min_momentum', 35) or 35))
        min_buyer_seller = int(float(self.config.get('trading', {}).get('min_buyer_seller', 20) or 20))
        if abs(self.momentum_score) < min_momentum:
            return
        if abs(self.buyer_seller_score) < min_buyer_seller:
            return
        symbol = self.expiry_symbol if self.expiry_symbol else 'NIFTY'
        md = self.ltp_data.get(symbol)
        min_expected_move = float(self.config.get('trading', {}).get('min_expected_move', 10) or 10)
        if md and (md.high - md.low) < min_expected_move:
            return
        
        min_conf = strategy.MIN_CONFIDENCE
        if self.mode == Mode.SAFE:
            min_conf += 20
        elif self.mode == Mode.AGGRESSIVE:
            min_conf -= 10
        
        if signal in ['BUY', 'SELL'] and self.confidence >= min_conf:
            self._execute_trade(signal, self.confidence, reason, strategy.NAME)

    def _select_strategy(self):
        active = []
        for name, strategy in self.strategies.items():
            info = strategy.info()
            if info.get('expiry_only', False) and not self.expiry_symbol:
                continue
            if self.day_type.value not in info.get('days', ['ANY']) and 'ANY' not in info.get('days', []):
                continue
            if self.time_window.value not in info.get('times', ['ANY']) and 'ANY' not in info.get('times', []):
                continue
            if self.market_condition.value not in info.get('market', ['ANY']) and 'ANY' not in info.get('market', []):
                continue
            active.append(strategy)
        return active[0] if active else None

    def _check_telegram_agreement(self, own_signal):
        if not self.telegram_signals:
            return 0
        recent = self.telegram_signals[-5:]
        agreement = 0
        for sig in recent:
            tg_dir = sig.get('direction', '')
            if tg_dir == own_signal:
                agreement += 5
            elif tg_dir in ['BUY', 'SELL']:
                agreement -= 3
        return max(0, agreement)

    def _execute_trade(self, signal, confidence, reason, strategy_name):
        try:
            symbol = self.expiry_symbol if self.expiry_symbol else 'NIFTY'
            if symbol not in self.SYMBOLS:
                symbol = 'NIFTY'
            
            sym_info = self.SYMBOLS[symbol]
            idx_price = self.ltp_data.get(symbol, MarketData()).ltp
            
            if idx_price <= 0:
                return
            
            step = sym_info['step']
            atm = round(idx_price / step) * step
            option_type = 'CE' if signal == 'BUY' else 'PE'
            
            oc = self.option_chain_data.get(symbol)
            premium = oc.atm_ce_premium if oc and option_type == 'CE' else (oc.atm_pe_premium if oc else 0)
            if premium <= 0:
                premium = idx_price * 0.02
            
            lot_size = sym_info['lot']
            lots = self.capital.get_lot_size(lot_size)
            margin = premium * lot_size * lots
            if margin > self.capital.current * 0.8:
                lots = max(1, int((self.capital.current * 0.8) / (premium * lot_size)))
            
            sl_pct = float(self.config.get('trading', {}).get('sl_pct', 50) or 50) / 100
            target_pct = float(self.config.get('trading', {}).get('target_pct', 100) or 100) / 100
            trail_pct = float(self.config.get('trading', {}).get('trailing_sl_pct', 5) or 5) / 100
            
            trade = Trade(
                id=f"{symbol}_{datetime.now().strftime('%H%M%S')}",
                symbol=symbol,
                direction=signal,
                option_type=option_type,
                strike=atm,
                entry_price=premium,
                entry_time=datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%H:%M:%S'),
                qty=lot_size * lots,
                lot_size=lot_size,
                sl=premium * sl_pct,
                target=premium * target_pct,
                trailing_sl=premium * trail_pct,
                confidence=confidence,
                strategy=strategy_name,
                reason=reason
            )
            
            self.current_trade = trade
            self.risk.open_positions[trade.id] = trade
            self.risk.last_trade_time = time.time()
            
            paper = self.config.get('trading', {}).get('paper_mode', True)
            msg = f"🙏 ॐ श्री गणेशाय नमः ि॥\n{'📝 PAPER' if paper else '💰 LIVE'} {signal} {symbol} {atm} {option_type}\nPremium: Rs.{premium:.2f}\nLots: {lots}\nSL: Rs.{trade.sl:.2f} | Target: Rs.{trade.target:.2f}\nConfidence: {confidence:.0f}%"
            self._notify(msg)
            
            if self.on_trade:
                self.on_trade(trade, 'ENTRY')
        except Exception as e:
            self._log(f"❌ Trade error: {e}")

    def _check_exit_conditions(self):
        if not self.current_trade:
            return
        
        trade = self.current_trade
        oc = self.option_chain_data.get(trade.symbol)
        current_premium = oc.atm_ce_premium if oc and trade.option_type == 'CE' else (oc.atm_pe_premium if oc else 0)
        
        if current_premium <= 0:
            return
        
        premium_change = current_premium - trade.entry_price
        pnl = premium_change * trade.qty
        exit_reason = None
        
        if premium_change <= -trade.sl:
            exit_reason = "SL Hit"
        elif premium_change >= trade.target:
            exit_reason = "Target Achieved"
        elif trade.trailing_sl > 0:
            new_trail = trade.entry_price + premium_change - trade.trailing_sl
            if new_trail > trade.trailing_sl:
                trade.trailing_sl = new_trail
            if premium_change < 0 and abs(premium_change) > trade.trailing_sl:
                exit_reason = "Trailing SL Hit"
        
        now = datetime.now(ZoneInfo('Asia/Kolkata'))
        if now.hour >= 15 and now.minute >= 10:
            exit_reason = "Market Closing"
        
        if exit_reason:
            self._exit_trade(exit_reason, current_premium, pnl)

    def _exit_trade(self, reason, exit_price, pnl):
        if not self.current_trade:
            return
        
        trade = self.current_trade
        trade.exit_price = exit_price or trade.entry_price
        trade.exit_time = datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%H:%M:%S')
        trade.pnl = pnl or 0
        trade.status = "CLOSED"
        
        if trade.pnl > 0:
            self.capital.add_profit(trade.pnl)
            self.risk.last_trade_was_loss = False
            self.risk.consecutive_losses = 0
            emoji = "🙏 शुभ लाभ"
        else:
            self.capital.add_loss(abs(trade.pnl))
            self.risk.last_trade_was_loss = True
            self.risk.consecutive_losses += 1
            emoji = "॥ ॐ शान्तिः ॥"
        
        self.risk.daily_pnl += trade.pnl
        self.risk.daily_trades += 1
        self.risk.last_trade_time = time.time()
        
        self.trades_history.append(trade)
        if trade.id in self.risk.open_positions:
            del self.risk.open_positions[trade.id]
        self.current_trade = None
        
        msg = f"{emoji}\nEXIT: {trade.symbol} {trade.strike} {trade.option_type}\nP&L: {'+' if trade.pnl >= 0 else ''}Rs.{trade.pnl:.2f}\nReason: {reason}"
        self._notify(msg)
        
        if self.on_trade:
            self.on_trade(trade, 'EXIT')

    def _get_status(self):
        return {
            'mode': self.mode.value,
            'day_type': self.day_type.value,
            'time_window': self.time_window.value,
            'market_condition': self.market_condition.value,
            'season': self.season.value,
            'expiry_symbol': self.expiry_symbol,
            'is_monthly_expiry': self.is_monthly_expiry,
            'confidence': self.confidence,
            'momentum': self.momentum_score,
            'buyer_seller': self.buyer_seller_score,
            'capital': self.capital.current,
            'capital_peak': self.capital.peak,
            'total_pnl': self.capital.total_pnl,
            'wins': self.capital.wins,
            'losses': self.capital.losses,
            'daily_pnl': self.risk.daily_pnl,
            'daily_trades': self.risk.daily_trades,
            'current_trade': asdict(self.current_trade) if self.current_trade else None,
            'ltp': {k: asdict(v) for k, v in self.ltp_data.items()},
            'kotak_connected': self.kotak.logged_in if self.kotak else False,
            'tg_connected': self.tg_bot.status_msg if self.tg_bot else "N/A",
            'tg_reader_connected': self.tg_reader.status_msg if self.tg_reader else "N/A",
            'paper_mode': self.config.get('trading', {}).get('paper_mode', True),
            'telegram_recent': [
                {
                    'source': s.get('source', ''),
                    'direction': s.get('direction', ''),
                    'time': s.get('time', '')
                } for s in self.telegram_signals[-5:]
            ],
            'tg_groups_read': self.telegram_read_groups[-8:],
            'tg_last_poll': self.last_tg_poll,
            'last_decision': self.last_decision
        }
