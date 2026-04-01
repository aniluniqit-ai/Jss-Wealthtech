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

BG = "#1a1508"
BG2 = "#2a2310"
BG3 = "#353018"
GOLD = "#FFD700"
DARK_GOLD = "#B8860B"
ORANGE = "#FF8C00"
GREEN = "#00FF88"
RED = "#FF4444"
WHITE = "#FFFFFF"
GRAY = "#999977"
PURPLE = "#9370DB"
CYAN = "#00CED1"

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

        self.kotak = None
        self.tg_reader = None
        self.running = False

        self._build_ui()
        self.root.after(3000, self._auto_start)

    def _build_ui(self):
        main = Frame(self.root, bg=BG)
        main.pack(fill=BOTH, expand=True, padx=5, pady=5)

        top = Frame(main, bg=BG2, height=60)
        top.pack(fill=X, pady=(0, 5))
        top.pack_propagate(False)

        ganesh = Frame(top, bg=BG2)
        ganesh.pack(side=LEFT, padx=15)
        Label(ganesh, text="🙏🙏", font=("Arial", 24), bg=BG2, fg=GOLD).pack()

        title = Frame(top, bg=BG2)
        title.pack(side=LEFT, expand=True)
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
        self.lbl_sentiment = Label(left, text="😐 NEUTRAL", font=("Arial", 11, "bold"), bg=BG2, fg=WHITE)
        self.lbl_sentiment.pack(pady=8)

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
            self.kotak = KotakNeo()
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
            else:
                msg = self.kotak.status_msg
                self.root.after(0, lambda m=msg: self._log("❌ Kotak: " + m))
                self.root.after(0, lambda: self.lbl_kotak.config(text="❌ Kotak", fg=RED))
        except Exception as e:
            self.root.after(0, lambda: self._log("❌ Kotak Error: " + str(e)))

    def _connect_telegram(self):
        self._log("📱 Connecting Telegram...")
        try:
            from telegram.reader import TelegramReader
            self.tg_reader = TelegramReader()
            self.tg_reader.set_log_callback(self._log)
            self.tg_reader.set_otp_callback(self._show_otp_popup)
            threading.Thread(target=self._tg_thread, daemon=True).start()
        except Exception as e:
            self._log("❌ TG Import: " + str(e))
            if 'telethon' in str(e).lower():
                self._log("💡 Run: pip install telethon")

    def _tg_thread(self):
        try:
            ok = self.tg_reader.connect()
            if ok:
                self.root.after(0, lambda: self._log("🎉 Telegram Connected!"))
                self.root.after(0, lambda: self.lbl_tg.config(text="✅ TG", fg=GREEN))
            else:
                msg = self.tg_reader.status_msg
                self.root.after(0, lambda m=msg: self._log("❌ TG: " + m))
                self.root.after(0, lambda: self.lbl_tg.config(text="❌ TG", fg=RED))
        except Exception as e:
            self.root.after(0, lambda: self._log("❌ TG Error: " + str(e)))

    def _show_otp_popup(self, source):
        self.root.after(0, lambda: self._create_otp_window(source))

    # =========================================================================
    # --- ✅ FIXED: OTP WINDOW (Variable Set + Method Call) ---
    # =========================================================================
    def _create_otp_window(self, source):
        win = Toplevel(self.root)
        win.title("🔑 OTP - " + source)
        win.geometry("420x320") # Thoda height badha di
        win.configure(bg=BG2)
        win.transient(self.root)
        # grab_set() commented out per your original code to avoid freezing
        
        Label(win, text="🔑", font=("Arial", 36), bg=BG2, fg=GOLD).pack(pady=8)

        if source == "TELEGRAM":
            Label(win, text="TELEGRAM LOGIN CODE", font=("Arial", 14, "bold"), bg=BG2, fg=GOLD).pack(pady=3)
            Label(win, text="Check Telegram app for login code\n(From 'Telegram' official account)", font=("Arial", 9), bg=BG2, fg=ORANGE).pack(pady=3)
        else:
            Label(win, text="KOTAK OTP", font=("Arial", 14, "bold"), bg=BG2, fg=GOLD).pack(pady=3)

        entry = Entry(win, font=("Arial", 20), bg=BG3, fg=WHITE, insertbackground=WHITE, justify="center")
        entry.pack(pady=10, ipady=5, ipadx=20)
        entry.focus_force() 

        def on_submit():
            code = entry.get().strip()
            if not code:
                return
            
            self._log("📱 OTP Received: " + code[:2] + "****")

            # --- FIX LOGIC START ---
            try:
                if source == "TELEGRAM" and self.tg_reader:
                    # FIX 1: Direct Variable Set (Logs wale 'Waiting' loop ke liye)
                    if hasattr(self.tg_reader, 'otp_code'):
                        self.tg_reader.otp_code = code
                    
                    # FIX 2: Method Call (Agar library direct function use karti hai)
                    try:
                        self.tg_reader.submit_otp(code)
                    except:
                        pass # Ignore agar method fail ho jaye, variable set ho chuka hai

                elif source == "KOTAK" and self.kotak:
                    self.kotak.submit_otp(code)
            except Exception as e:
                self._log(f"❌ OTP Error: {e}")
            # --- FIX LOGIC END ---

            win.destroy()

        # Button with explicit command
        btn = Button(win, text="✅ SUBMIT OTP", font=("Arial", 14, "bold"), 
                     bg=GOLD, fg=BLACK, activebackground=DARK_GOLD, 
                     command=on_submit, relief=RAISED, cursor="hand2", padx=20, pady=5)
        btn.pack(pady=10)

        # Enter key binding
        entry.bind("<Return>", lambda e: on_submit())

        # Keep window on top
        win.attributes('-topmost', True)
        win.after(100, entry.focus_force)

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

            now = datetime.now(ZoneInfo("Asia/Kolkata"))
            t = now.hour * 60 + now.minute
            day = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][now.weekday()]
            tw = "MARKET CLOSED"
            if 9*60+15 <= t < 9*60+30: tw = "OPENING"
            elif 9*60+30 <= t < 11*60: tw = "TRENDING"
            elif 13*60+30 <= t < 15*60+15: tw = "CLOSING"

            exp_map = {"MON": "FINNIFTY", "TUE": "BANKNIFTY", "WED": "MIDCPNIFTY", "THU": "NIFTY", "FRI": "None", "SAT": "None", "SUN": "None"}
            mode = "OBSERVE" if day == "MON" else ("EXPIRY" if exp_map.get(day, "None") != "None" else ("WAIT" if tw == "MARKET CLOSED" else "NORMAL"))

            self.lbl_day.config(text="Day: " + day)
            self.lbl_time.config(text="Time: " + tw)
            self.lbl_expiry.config(text="Expiry: " + exp_map.get(day, "None"))
            self.lbl_mode.config(text=mode, fg=MODE_COLORS.get(mode, WHITE))
        except Exception:
            pass
        self.root.after(1000, self._ltp_loop)


def main():
    root = Tk()
    app = JssDesktop(root)
    root.mainloop()


if __name__ == "__main__":
    main()