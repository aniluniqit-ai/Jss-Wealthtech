"""
JSS WEALTHTECH - DIVINE DESKTOP UI
॥ जय श्री सांवरीया सेठ ि॥
"""
import os
import json
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

BG = "#C9A227"
BG2 = "#A67C00"
BG3 = "#8B6B00"
GOLD = "#FFD700"
DARK_GOLD = "#B8860B"
ORANGE = "#FF8C00"
GREEN = "#00FF88"
RED = "#FF4444"
WHITE = "#FFFFFF"
GRAY = "#999977"
PURPLE = "#9370DB"
CYAN = "#00CED1"
BLACK = "#000000"

MANTRAS = """॥ ॐ श्री गणेशाय नमः ि॥
श्री शिवाय नमस्तुभ्यं
जय श्री सांवरीया सेठ ि॥
लक्ष्मी कुबेर की कृपा ि॥
शुभं करोति कल्याणम् ि॥"""

MODE_COLORS = {
    "NORMAL": WHITE, "EXPIRY": ORANGE, "SAFE": CYAN, "AGGRESSIVE": GREEN,
    "KILL": RED, "OBSERVE": PURPLE, "WAIT": GRAY, "AI_LEARN": PURPLE
}

SYMBOLS_LIST = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "SENSEX", "BANKEX", "CRUDEOIL", "NATURALGAS"]


class JssDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("॥ Jss Wealthtech - जय श्री सांवरीया सेठ ि॥")
        self.root.geometry("1400x920")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.config_data = self._load_config()
        self.kotak = None
        self.tg_reader = None
        self.tg_bot = None
        self.engine = None
        self.running = False
        self._img_refs = []

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(3000, self._auto_start)

    def _load_config(self):
        cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}
        cfg.setdefault('trading', {})
        cfg['trading']['paper_mode'] = True
        cfg['trading']['initial_capital'] = 1000
        return cfg

    def _build_ui(self):
        main = Frame(self.root, bg=BG)
        main.pack(fill=BOTH, expand=True, padx=5, pady=5)

        top = Frame(main, bg=BG2, height=60)
        top.pack(fill=X, pady=(0, 5))
        top.pack_propagate(False)

        center_head = Frame(top, bg=BG2)
        center_head.pack(side=LEFT, expand=True)
        ganesh = Frame(center_head, bg=BG2)
        ganesh.pack()
        if not self._make_image_label(ganesh, "ganesh.png", (64, 64), BG2):
            Label(ganesh, text="🙏🙏", font=("Arial", 26), bg=BG2, fg=GOLD).pack()

        title = Frame(center_head, bg=BG2)
        title.pack()
        Label(title, text="॥ जय श्री सांवरीया सेठ ि॥", font=("Arial", 17, "bold"), bg=BG2, fg=GOLD).pack()
        Label(title, text="JSS WEALTHTECH V8.0", font=("Arial", 9), bg=BG2, fg=DARK_GOLD).pack()

        self.lbl_mode = Label(top, text="OBSERVE", font=("Arial", 13, "bold"), bg=BG2, fg=PURPLE)
        self.lbl_mode.pack(side=LEFT, padx=15)

        self.lbl_tg = Label(top, text="❌ TG", font=("Arial", 10), bg=BG2, fg=RED)
        self.lbl_tg.pack(side=RIGHT, padx=10)
        self.lbl_kotak = Label(top, text="❌ Kotak", font=("Arial", 10), bg=BG2, fg=RED)
        self.lbl_kotak.pack(side=RIGHT, padx=10)

        mid = Frame(main, bg=BG)
        mid.pack(fill=BOTH, expand=True, pady=5)

        left = Frame(mid, bg=BG2, width=200)
        left.pack(side=LEFT, fill=Y, padx=(0, 5))
        left.pack_propagate(False)

        m_box = Frame(left, bg=BG3, padx=6, pady=6)
        m_box.pack(fill=X, padx=6, pady=6)
        Label(m_box, text="॥ MANTRAS ि॥", font=("Arial", 10, "bold"), bg=BG3, fg=GOLD).pack()
        txt = Text(m_box, bg=BG3, fg=GOLD, font=("Arial", 9), wrap=WORD, relief=FLAT, height=7, bd=0)
        txt.insert("1.0", MANTRAS)
        txt.config(state=DISABLED)
        txt.pack()

        Frame(left, bg=GOLD, height=2).pack(fill=X, padx=8, pady=6)

        i_box = Frame(left, bg=BG3, padx=6, pady=6)
        i_box.pack(fill=X, padx=6)
        Label(i_box, text="📊 INFO", font=("Arial", 10, "bold"), bg=BG3, fg=GOLD).pack(anchor="w", pady=(0, 5))

        self.lbl_day = Label(i_box, text="Day: -", font=("Arial", 9), bg=BG3, fg=WHITE, anchor="w")
        self.lbl_day.pack(fill=X, pady=1)
        self.lbl_time = Label(i_box, text="Time: -", font=("Arial", 9), bg=BG3, fg=WHITE, anchor="w")
        self.lbl_time.pack(fill=X, pady=1)
        self.lbl_expiry = Label(i_box, text="Expiry: -", font=("Arial", 9), bg=BG3, fg=WHITE, anchor="w")
        self.lbl_expiry.pack(fill=X, pady=1)
        self.lbl_tg_read = Label(i_box, text="TG Read: -", font=("Arial", 9), bg=BG3, fg=WHITE, anchor="w", wraplength=180, justify=LEFT)
        self.lbl_tg_read.pack(fill=X, pady=1)
        self.lbl_tg_poll = Label(i_box, text="TG Poll: -", font=("Arial", 9), bg=BG3, fg=WHITE, anchor="w")
        self.lbl_tg_poll.pack(fill=X, pady=1)
        self.lbl_sentiment = Label(left, text="😐 NEUTRAL", font=("Arial", 11, "bold"), bg=BG2, fg=WHITE)
        self.lbl_sentiment.pack(pady=8)
        self._make_image_label(left, "swastik.png", (72, 72), BG2)

        center = Frame(mid, bg=BG)
        center.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        r_hdr = Frame(center, bg=BG3)
        r_hdr.pack(fill=X, pady=(0, 3))
        Label(r_hdr, text="📈 LIVE RATES", font=("Arial", 11, "bold"), bg=BG3, fg=GOLD).pack(side=LEFT, padx=10, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG2, foreground=WHITE, fieldbackground=BG2, font=("Arial", 9), rowheight=24)
        style.configure("Treeview.Heading", background=BG3, foreground=GOLD, font=("Arial", 9, "bold"), rowheight=25)

        cols = ("Symbol", "LTP", "Change", "Chg%", "High", "Low", "Status")
        self.rates_tree = ttk.Treeview(center, columns=cols, show="headings", height=8)
        for col in cols:
            self.rates_tree.heading(col, text=col)
            self.rates_tree.column(col, width=105, anchor="center")
        for sym in SYMBOLS_LIST:
            self.rates_tree.insert("", END, values=(sym, "0.00", "0.00", "0.00%", "0.00", "0.00", "⏳"))
        self.rates_tree.pack(fill=X, pady=(0, 8))

        t_hdr = Frame(center, bg=BG3)
        t_hdr.pack(fill=X)
        Label(t_hdr, text="📊 CURRENT TRADE", font=("Arial", 11, "bold"), bg=BG3, fg=GOLD).pack(side=LEFT, padx=10, pady=5)
        Label(t_hdr, text="🔒 PAPER", font=("Arial", 9, "bold"), bg=BG3, fg=RED).pack(side=RIGHT, padx=10)
        self.lbl_trade = Label(center, text="No Open Trade", font=("Arial", 11), bg=BG2, fg=GRAY, anchor="w", padx=10, pady=15)
        self.lbl_trade.pack(fill=X)

        right = Frame(mid, bg=BG2, width=200)
        right.pack(side=RIGHT, fill=Y, padx=(5, 0))
        right.pack_propagate(False)

        c_box = Frame(right, bg=BG3, padx=8, pady=8)
        c_box.pack(fill=X, padx=8, pady=8)
        Label(c_box, text="💰 CAPITAL", font=("Arial", 11, "bold"), bg=BG3, fg=GOLD).pack()
        self.lbl_capital = Label(c_box, text="₹1,000.00", font=("Arial", 18, "bold"), bg=BG3, fg=GREEN)
        self.lbl_capital.pack(pady=3)
        self.lbl_pnl = Label(c_box, text="P&L: ₹0.00", font=("Arial", 12), bg=BG3, fg=GREEN)
        self.lbl_pnl.pack()

        Frame(right, bg=GOLD, height=2).pack(fill=X, padx=8, pady=10)

        mo_box = Frame(right, bg=BG3, padx=8, pady=8)
        mo_box.pack(fill=X, padx=8)
        Label(mo_box, text="🔧 MODE", font=("Arial", 10, "bold"), bg=BG3, fg=GOLD).pack(pady=(0, 5))
        Label(mo_box, text="🔒 PAPER MODE", font=("Arial", 13, "bold"), bg=BG3, fg=RED).pack()
        self._make_image_label(right, "laxmi_kuber.png", (96, 96), BG2)

        bottom = Frame(main, bg=BG2, height=180)
        bottom.pack(fill=X, pady=(5, 0))
        bottom.pack_propagate(False)
        Label(bottom, text="📋 LOG", font=("Arial", 10, "bold"), bg=BG3, fg=GOLD, anchor="w").pack(fill=X, padx=10, pady=3)
        self.log_text = Text(bottom, bg=BG, fg=GREEN, font=("Consolas", 9), relief=FLAT, wrap=WORD, bd=0)
        self.log_text.pack(fill=BOTH, expand=True, padx=8, pady=(0, 5))

        Label(self.root, text="॥ जय श्री सांवरीया सेठ ि॥ | Jss Wealthtech V8.0 | 🔒 PAPER MODE", font=("Arial", 9), bg=BG, fg=DARK_GOLD).pack(fill=X, pady=(0, 3))

        self._log("🙏 ॥ जय श्री सांवरीया सेठ ि॥")
        self._log("ि॥ श्री गणेशाय नमः ि॥")
        self._log("Software Loaded")
        self._log("⏳ Auto-Starting in 3 seconds...")

    def _make_image_label(self, parent, image_name, size, bg):
        img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images", image_name)
        if not os.path.exists(img_path):
            return False
        try:
            img = Image.open(img_path).resize(size, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self._img_refs.append(tk_img)
            Label(parent, image=tk_img, bg=bg).pack(pady=4)
            return True
        except Exception as e:
            self._log(f"⚠️ Image load failed ({image_name}): {e}")
            return False

    def _log(self, msg):
        try:
            self.log_text.config(state=NORMAL)
            ts = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S")
            self.log_text.insert(END, "[" + ts + "] " + msg + "\n")
            self.log_text.see(END)
            self.log_text.config(state=DISABLED)
        except Exception:
            pass

    def _auto_start(self):
        self._log("🔄 Auto-Starting...")
        self._connect_kotak()
        self.root.after(5000, self._connect_telegram)

    def _connect_kotak(self):
        self._log("🔌 Connecting Kotak...")
        try:
            from brokers.kotak_neo import KotakNeo
            self.kotak = KotakNeo(self.config_data.get('kotak_neo', {}))
            self.kotak.set_log_callback(self._log)
            threading.Thread(target=self._kotak_thread, daemon=True).start()
        except Exception as e:
            self._log("❌ Kotak: " + str(e))

    def _kotak_thread(self):
        try:
            ok = self.kotak.connect()
            if ok:
                self.root.after(0, lambda: self._log("🎉 Kotak Connected!"))
                self.root.after(0, lambda: self.lbl_kotak.config(text="✅ Kotak", fg=GREEN))
                self.running = True
                self.root.after(0, self._ltp_loop)
                self.root.after(0, self._start_engine)
            else:
                msg = self.kotak.status_msg
                self.root.after(0, lambda m=msg: self._log("❌ Kotak: " + m))
                self.root.after(0, lambda: self.lbl_kotak.config(text="❌ Kotak", fg=RED))
        except Exception as e:
            self.root.after(0, lambda: self._log("❌ Kotak Error: " + str(e)))

    def _connect_telegram(self):
        self._log("📱 Connecting Telegram reader + bot...")
        try:
            from telegram.reader import TelegramReader
            from telegram.bot import TelegramBot
            self.tg_reader = TelegramReader(self.config_data)
            self.tg_reader.set_log_callback(self._log)
            self.tg_reader.set_otp_callback(self._show_otp_popup)
            self.tg_bot = TelegramBot(self.config_data)
            self.tg_bot.connect()
            threading.Thread(target=self._tg_thread, daemon=True).start()
        except Exception as e:
            self._log("❌ TG Setup: " + str(e))

    def _tg_thread(self):
        try:
            ok = self.tg_reader.connect()
            if ok:
                self.root.after(0, lambda: self._log("🎉 Telegram Connected!"))
                self.root.after(0, lambda: self.lbl_tg.config(text="✅ TG", fg=GREEN))
            else:
                msg = self.tg_reader.status_msg
                self.root.after(0, lambda m=msg: self._log("❌ TG: " + m))
        except Exception as e:
            self.root.after(0, lambda: self._log("❌ TG Error: " + str(e)))

    def _show_otp_popup(self, source):
        self.root.after(0, lambda: self._create_otp_window(source))

    def _create_otp_window(self, source):
        win = Toplevel(self.root)
        win.title("🔑 OTP - " + source)
        win.geometry("420x280")
        win.configure(bg=BG2)
        win.transient(self.root)

        Label(win, text="🔑", font=("Arial", 36), bg=BG2, fg=GOLD).pack(pady=8)
        title = "TELEGRAM LOGIN CODE"
        hint = "Enter OTP received in Telegram app"
        if source == "TELEGRAM_PASSWORD":
            title = "TELEGRAM 2FA PASSWORD"
            hint = "Enter your Telegram two-step verification password"
        Label(win, text=title, font=("Arial", 14, "bold"), bg=BG2, fg=GOLD).pack(pady=3)
        Label(win, text=hint, font=("Arial", 9), bg=BG2, fg=WHITE).pack(pady=(0, 5))

        entry = Entry(win, font=("Arial", 20), bg=BG3, fg=WHITE, insertbackground=WHITE, justify="center")
        entry.pack(pady=10, ipady=5, ipadx=20)
        entry.focus_force()

        def on_submit():
            code = entry.get().strip()
            if code and self.tg_reader:
                if source == "TELEGRAM_PASSWORD":
                    self.tg_reader.submit_password(code)
                    self._log("🔐 Telegram 2FA Password Received")
                else:
                    self.tg_reader.submit_otp(code)
                    self._log("📱 OTP Received")
            win.destroy()

        btn = Button(win, text="✅ SUBMIT OTP", font=("Arial", 14, "bold"), bg=GOLD, fg=BLACK, command=on_submit)
        btn.pack(pady=10)
        entry.bind("<Return>", lambda e: on_submit())

    def _start_engine(self):
        if self.engine:
            return
        try:
            from core.engine import TradingEngine
            from core.option_chain import OptionChain
            from core.indicators import Indicators
            from core.capital import CapitalManager
            from core.risk import RiskManager
            from telegram.parser import SignalParser
            from strategies import load_all_strategies

            capital = CapitalManager(initial_capital=1000)
            risk = RiskManager(self.config_data)
            parser = SignalParser()
            strategies = load_all_strategies()

            self.engine = TradingEngine(
                config=self.config_data,
                kotak=self.kotak,
                option_chain=OptionChain(),
                indicators=Indicators(),
                capital=capital,
                risk=risk,
                telegram_bot=self.tg_bot,
                telegram_reader=self.tg_reader,
                signal_parser=parser,
                strategies=strategies,
            )
            self.engine.on_log = self._log
            self.engine.on_update = self._on_engine_update
            self.engine.on_trade = self._on_trade
            self.engine.start()
            self._log("🤖 Engine started (Paper mode | Capital ₹1000)")
        except Exception as e:
            self._log("❌ Engine start failed: " + str(e))

    def _on_engine_update(self, status):
        self.root.after(0, lambda s=status: self._apply_status(s))

    def _apply_status(self, s):
        mode = s.get('mode', 'NORMAL')
        self.lbl_mode.config(text=mode, fg=MODE_COLORS.get(mode, WHITE))
        self.lbl_day.config(text="Day: " + s.get('day_type', '-'))
        self.lbl_time.config(text="Time: " + s.get('time_window', '-'))
        self.lbl_expiry.config(text="Expiry: " + str(s.get('expiry_symbol') or 'None'))
        tg_groups_read = s.get('tg_groups_read', [])
        if tg_groups_read:
            self.lbl_tg_read.config(text="TG Read: " + ", ".join(tg_groups_read[-3:]))
        else:
            self.lbl_tg_read.config(text="TG Read: None")
        self.lbl_tg_poll.config(text="TG Poll: " + str(s.get('tg_last_poll') or '-'))
        cap = float(s.get('capital', 1000) or 1000)
        pnl = float(s.get('total_pnl', 0) or 0)
        self.lbl_capital.config(text=f"₹{cap:,.2f}")
        self.lbl_pnl.config(text=f"P&L: ₹{pnl:,.2f}", fg=GREEN if pnl >= 0 else RED)
        if not s.get('current_trade'):
            d = s.get('last_decision', {}) or {}
            if d.get('signal'):
                txt = f"Last Decision: {d.get('signal')} {d.get('confidence', 0):.0f}% @ {d.get('time','-')} | {d.get('reason','')}"
                self.lbl_trade.config(text=txt, fg=WHITE)

    def _on_trade(self, trade, event):
        if event == 'ENTRY':
            text = f"{trade.symbol} {trade.strike} {trade.option_type} | Qty {trade.qty} | Entry ₹{trade.entry_price:.2f}"
            self.root.after(0, lambda: self.lbl_trade.config(text=text, fg=WHITE))
        elif event == 'EXIT':
            text = f"Last Exit: {trade.symbol} {trade.option_type} | P&L ₹{trade.pnl:.2f}"
            self.root.after(0, lambda: self.lbl_trade.config(text=text, fg=GREEN if trade.pnl >= 0 else RED))

    def _ltp_loop(self):
        if not self.running or not self.kotak or not self.kotak.logged_in:
            return
        try:
            items = self.rates_tree.get_children()
            for i, sym in enumerate(SYMBOLS_LIST):
                data = self.kotak.get_ltp(sym)
                if i < len(items):
                    if data and data.get('ltp', 0) > 0:
                        d = data
                        self.rates_tree.item(items[i], values=(
                            sym, "{:.2f}".format(d['ltp']), "{:+.2f}".format(d['change']),
                            "{:+.2f}%".format(d['change_pct']), "{:.2f}".format(d['high']),
                            "{:.2f}".format(d['low']), "✅ LIVE"
                        ))
        except Exception:
            pass
        self.root.after(1000, self._ltp_loop)

    def _on_close(self):
        try:
            if self.engine:
                self.engine.stop()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = Tk()
    app = JssDesktop(root)
    root.mainloop()


if __name__ == "__main__":
    main()
