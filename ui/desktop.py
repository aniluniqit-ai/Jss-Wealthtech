"""
JSS WEALTHTECH - DIVINE DESKTOP UI
॥ जय श्री सांवरीया सेठ ि॥
"""
import os, sys, json, time
from datetime import datetime
from zoneinfo import ZoneInfo
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

BG = "#1a1508"
BG2 = "#2a2310"
BG3 = "#353018"
GOLD = "#FFD700"
ORANGE = "#FF8C00"
GREEN = "#00FF88"
RED = "#FF4444"
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#999977"
PURPLE = "#9370DB"
CYAN = "#00CED1"

MANTRAS = """॥ ॐ श्री गणेशाय नमः ि॥
श्री शिवाय नमस्तुभ्यं
जय श्री सांवरीया सेठ ि॥
लक्ष्मी कुबेर की कृपा ि॥
शुभं करोति कल्याणम् ि॥"""

class JssDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("॥ Jss Wealthtech - जय श्री सांवरीया सेठ ि॥")
        self.root.geometry("1400x900")
        self.root.configure(bg=BG)
        self.root.minsize(1200, 800)
        
        self.base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.engine = None
        self.running = False
        
        # YAHAN PAPER MODE FIXED HAI (CHANGE NAHI HOGA)
        self.auto_var = BooleanVar(value=True)
        self.paper_var = BooleanVar(value=True)
        
        self.images = {}
        self._load_images()
        
        self._build_header()
        self._build_main()
        self._build_footer()
        
        # Engine init hone ke 2 second baad AUTO START karega
        self.root.after(2000, self._init_engine)

    def _load_images(self):
        img_path = os.path.join(self.base, 'images')
        files = {
            'ganesh': 'ganesh.png', 'swastik': 'swastik.png', 'shubh': 'shubh.png',
            'om': 'om.png', 'laxmi_kuber': 'laxmi_kuber.png', 'bell': 'bell.png',
            'kalash': 'kalash.png', 'mor_pankh': 'mor_pankh.png', 'golden_fish': 'golden_fisk.png',
            'hanging_deepak': 'hanging_deepak.png', 'shyam_baba': 'shyam_baba.png', 'yantra': 'yantra.png',
            'ai_robot': 'ai_robot.jpg', 'ai_analyst': 'ai_robot_analyst.png',
            'bull': 'market_bull.png', 'bear': 'market_bear.png',
        }
        for key, fname in files.items():
            path = os.path.join(img_path, fname)
            if os.path.exists(path):
                try:
                    self.images[key] = Image.open(path)
                except:
                    pass

    def _get_img(self, key, size=(60, 60)):
        if key in self.images:
            try:
                img = self.images[key].resize(size, Image.Resampling.LANCZOS)
                return ImageTk.ImageTk(img)
            except:
                pass
        return None

    def _build_header(self):
        header = Frame(self.root, bg=BG2, height=180)
        header.pack(fill=X, padx=5, pady=(5, 0))
        header.pack_propagate(False)
        
        top = Frame(header, bg=BG2)
        top.pack(fill=X, pady=5)
        
        left = Frame(top, bg=BG2, width=200)
        left.pack(side=LEFT, padx=20)
        swastik_img = self._get_img('swastik', (50, 50))
        if swastik_img:
            lbl = Label(left, image=swastik_img, bg=BG2)
            lbl.image = swastik_img
            lbl.pack()
        else:
            Label(left, text="स्वस्तिक", font=("Arial", 20), fg=GOLD, bg=BG2).pack()
        
        center = Frame(top, bg=BG2)
        center.pack(expand=True)
        ganesh_img = self._get_img('ganesh', (100, 100))
        if ganesh_img:
            lbl = Label(center, image=ganesh_img, bg=BG2)
            lbl.image = ganesh_img
            lbl.pack()
        else:
            Label(center, text="🙏", font=("Arial", 60), bg=BG2).pack()
        
        right = Frame(top, bg=BG2, width=200)
        right.pack(side=RIGHT, padx=20)
        shubh_img = self._get_img('shubh', (50, 50))
        if shubh_img:
            lbl = Label(right, image=shubh_img, bg=BG2)
            lbl.image = shubh_img
            lbl.pack()
        else:
            Label(right, text="शुभ", font=("Arial", 20), fg=GOLD, bg=BG2).pack()
        
        robot_img = self._get_img('ai_robot', (40, 40))
        if robot_img:
            lbl = Label(right, image=robot_img, bg=BG2)
            lbl.image = robot_img
            lbl.pack(pady=5)
        
        mantra_frame = Frame(header, bg=BG2)
        mantra_frame.pack(fill=X, pady=2)
        Label(mantra_frame, text=MANTRAS, font=("Arial", 10), fg=GOLD, bg=BG2, justify=CENTER).pack()

    def _build_main(self):
        main = Frame(self.root, bg=BG)
        main.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        left = Frame(main, bg=BG2, width=250)
        left.pack(side=LEFT, fill=Y, padx=(0, 5))
        left.pack_propagate(False)
        self._build_controls(left)
        self._build_divine_gallery(left)
        
        center = Frame(main, bg=BG)
        center.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self._build_live_rates(center)
        self._build_status_panel(center)
        
        right = Frame(main, bg=BG2, width=350)
        right.pack(side=RIGHT, fill=Y, padx=(5, 0))
        right.pack_propagate(False)
        self._build_ai_panel(right)
        self._build_log(right)

    def _build_controls(self, parent):
        Label(parent, text="⚙️ CONTROLS", font=("Arial", 12, "bold"), fg=GOLD, bg=BG2).pack(pady=10)
        
        btn_frame = Frame(parent, bg=BG2)
        btn_frame.pack(fill=X, padx=10)
        
        # START BUTTON DISABLED HAI (AUTO-START HAI)
        self.btn_start = Button(btn_frame, text="⏳ AUTO-STARTING...", font=("Arial", 11, "bold"),
                               bg=GRAY, fg=BLACK, width=10, state=DISABLED)
        self.btn_start.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_stop = Button(btn_frame, text="⏹️ STOP", font=("Arial", 11, "bold"),
                              bg=RED, fg=WHITE, command=self._stop, width=10, state=DISABLED)
        self.btn_stop.grid(row=0, column=1, padx=5, pady=5)
        
        auto_frame = Frame(parent, bg=BG2)
        auto_frame.pack(fill=X, padx=10, pady=5)
        Checkbutton(auto_frame, text="Auto Trade", variable=self.auto_var,
                   font=("Arial", 10), fg=WHITE, bg=BG2, selectcolor=BG3,
                   command=self._toggle_auto).pack(side=LEFT)
        self.lbl_auto = Label(auto_frame, text="ON", font=("Arial", 10, "bold"), fg=GREEN, bg=BG2)
        self.lbl_auto.pack(side=RIGHT)
        
        # PAPER MODE LOCK (DISABLED - CHANGE NAHI HOGA)
        paper_frame = Frame(parent, bg=BG2)
        paper_frame.pack(fill=X, padx=10, pady=5)
        Checkbutton(paper_frame, text="🔒 Paper Mode (Locked)", variable=self.paper_var,
                   font=("Arial", 10), fg=GRAY, bg=BG2, selectcolor=BG3, state=DISABLED).pack(side=LEFT)
        self.lbl_paper = Label(paper_frame, text="🔒 LOCKED", font=("Arial", 10, "bold"), fg=CYAN, bg=BG2)
        self.lbl_paper.pack(side=RIGHT)
        
        Button(parent, text="🔧 Settings", font=("Arial", 10),
               bg=PURPLE, fg=WHITE, command=self._open_settings, width=20).pack(pady=10)
        
        cap_frame = LabelFrame(parent, text="💰 CAPITAL", font=("Arial", 10, "bold"),
                              fg=GOLD, bg=BG2, labelanchor='n')
        cap_frame.pack(fill=X, padx=10, pady=10)
        
        self.lbl_capital = Label(cap_frame, text="₹1,000", font=("Arial", 16, "bold"),
                                fg=GREEN, bg=BG2)
        self.lbl_capital.pack(pady=5)
        
        self.lbl_pnl = Label(cap_frame, text="P&L: ₹0", font=("Arial", 11),
                            fg=WHITE, bg=BG2)
        self.lbl_pnl.pack()
        
        self.lbl_peak = Label(cap_frame, text="Peak: ₹1,000", font=("Arial", 9),
                             fg=GRAY, bg=BG2)
        self.lbl_peak.pack(pady=(0, 5))

    def _build_divine_gallery(self, parent):
        Label(parent, text="🙏 DIVINE GALLERY", font=("Arial", 10, "bold"),
              fg=GOLD, bg=BG2).pack(pady=(10, 5))
        
        gallery = Frame(parent, bg=BG2)
        gallery.pack(fill=X, padx=10)
        
        divine_imgs = ['om', 'laxmi_kuber', 'bell', 'kalash', 'mor_pankh', 
                       'golden_fish', 'hanging_deepak', 'shyam_baba', 'yantra']
        emojis = ['🕉️', '🙏', '🔔', '🪷', '🦚', '🐟', '🪔', '🕉️', '🔮']
        
        for i, key in enumerate(divine_imgs):
            img = self._get_img(key, (35, 35))
            if img:
                lbl = Label(gallery, image=img, bg=BG2)
                lbl.image = img
                lbl.grid(row=i//3, column=i%3, padx=2, pady=2)
            else:
                Label(gallery, text=emojis[i], font=("Arial", 18), bg=BG2).grid(row=i//3, column=i%3, padx=2, pady=2)

    def _build_live_rates(self, parent):
        Label(parent, text="📊 LIVE MARKET RATES", font=(" Arial", 12, "bold"),
              fg=GOLD, bg=BG).pack(pady=5)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview", background=BG3, foreground=WHITE,
                        fieldbackground=BG3, font=("Arial", 10))
        style.configure("Custom.Treeview.Heading", background=BG2, foreground=GOLD,
                        font=("Arial", 10, "bold"))
        
        cols = ('Symbol', 'LTP', 'Change', 'Chg%', 'High', 'Low', 'Status')
        self.rates_tree = ttk.Treeview(parent, columns=cols, show='headings',
                                       style="Custom.Treeview", height=8)
        
        widths = [100, 90, 80, 70, 80, 80, 100]
        for col, w in zip(cols, widths):
            self.rates_tree.heading(col, text=col)
            self.rates_tree.column(col, width=w, anchor='center')
        
        self.rates_tree.pack(fill=X, padx=10, pady=5)
        
        symbols = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY', 'SENSEX', 
                   'BANKEX', 'CRUDEOIL', 'NATURALGAS']
        for sym in symbols:
            self.rates_tree.insert('', END, values=(sym, '-', '-', '-', '-', '-', '⏳'))

    def _build_status_panel(self, parent):
        status_frame = LabelFrame(parent, text="⚡ SYSTEM STATUS", font=("Arial", 11, "bold"),
                                 fg=GOLD, bg=BG2, labelanchor='n')
        status_frame.pack(fill=X, padx=10, pady=10)
        
        grid = Frame(status_frame, bg=BG2)
        grid.pack(fill=X, padx=10, pady=10)
        
        labels = [
            ('Mode:', 'lbl_mode'), ('Day:', 'lbl_day'),
            ('Time Window:', 'lbl_time'), ('Expiry:', 'lbl_expiry'),
            ('Market:', 'lbl_market'), ('Confidence:', 'lbl_conf'),
            ('Momentum:', 'lbl_momentum'), ('Buyer/Seller:', 'lbl_bs'),
            ('Kotak:', 'lbl_kotak'), ('Telegram:', 'lbl_tg'),
        ]
        
        for i, (text, attr) in enumerate(labels):
            row, col = i // 2, (i % 2) * 2
            Label(grid, text=text, font=("Arial", 9), fg=GRAY, bg=BG2).grid(
                row=row, column=col, sticky='w', padx=5, pady=2)
            lbl = Label(grid, text="-", font=("Arial", 9, "bold"), fg=WHITE, bg=BG2)
            lbl.grid(row=row, column=col+1, sticky='w', padx=5, pady=2)
            setattr(self, attr, lbl)
        
        trade_frame = LabelFrame(parent, text="📈 CURRENT TRADE", font=("Arial", 11, "bold"),
                                fg=GOLD, bg=BG2, labelanchor='n')
        trade_frame.pack(fill=X, padx=10, pady=5)
        
        self.lbl_trade = Label(trade_frame, text="No Open Trade", font=("Arial", 10),
                              fg=GRAY, bg=BG2, justify=LEFT)
        self.lbl_trade.pack(padx=10, pady=10, anchor='w')

    def _build_ai_panel(self, parent):
        Label(parent, text="🤖 AI ANALYSIS", font=("Arial", 12, "bold"),
              fg=GOLD, bg=BG2).pack(pady=10)
        
        robot_img = self._get_img('ai_analyst', (80, 80))
        if robot_img:
            lbl = Label(parent, image=robot_img, bg=BG2)
            lbl.image = robot_img
            lbl.pack(pady=5)
        
        self.lbl_sentiment = Label(parent, text="😐 NEUTRAL", font=("Arial", 14, "bold"),
                                  fg=WHITE, bg=BG2)
        self.lbl_sentiment.pack()
        
        tg_frame = LabelFrame(parent, text="📱 TELEGRAM SIGNALS", font=("Arial", 10, "bold"),
                             fg=CYAN, bg=BG2, labelanchor='n')
        tg_frame.pack(fill=X, padx=10, pady=10)
        
        self.lbl_tg_signals = Label(tg_frame, text="No signals", font=("Arial", 9),
                                   fg=GRAY, bg=BG2, justify=LEFT, wraplength=300)
        self.lbl_tg_signals.pack(padx=5, pady=5, anchor='w')
        
        hist_frame = LabelFrame(parent, text="📋 TRADE HISTORY", font=("Arial", 10, "bold"),
                               fg=GOLD, bg=BG2, labelanchor='n')
        hist_frame.pack(fill=X, padx=10, pady=5)
        
        self.lbl_history = Label(hist_frame, text="No trades yet", font=("Arial", 9),
                                fg=GRAY, bg=BG2, justify=LEFT, wraplength=300)
        self.lbl_history.pack(padx=5, pady=5, anchor='w')

    def _build_log(self, parent):
        Label(parent, text="📝 LOG", font=("Arial", 10, "bold"),
              fg=GOLD, bg=BG2).pack(pady=5)
        
        log_frame = Frame(parent, bg=BG3)
        log_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = Text(log_frame, bg=BG3, fg=WHITE, font=("Consolas", 8),
                            wrap=WORD, state=DISABLED)
        scrollbar = Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=RIGHT, fill=Y)
        self.log_text.pack(fill=BOTH, expand=True)

    def _build_footer(self):
        footer = Frame(self.root, bg=BG2, height=30)
        footer.pack(fill=X, padx=5, pady=(0, 5))
        
        self.lbl_footer = Label(footer, text="॥ जय श्री सांवरीया सेठ ि॥ | Jss Wealthtech V8.0 | 🔒 PAPER MODE LOCKED",
                               font=("Arial", 9), fg=GOLD, bg=BG2)
        self.lbl_footer.pack(expand=True)

    def _show_otp_popup(self, title, callback):
        win = Toplevel(self.root)
        win.title(title)
        win.geometry("400x200")
        win.configure(bg=BG2)
        win.transient(self.root)
        win.grab_set()
        
        Label(win, text="🔐 OTP AAYA HAI", font=("Arial", 14, "bold"), fg=GOLD, bg=BG2).pack(pady=20)
        
        entry = Entry(win, font=("Arial", 16), bg=BG3, fg=WHITE, insertbackground=WHITE, justify='center')
        entry.pack(pady=10, ipadx=20, ipady=10)
        entry.focus_set()
        
        def submit():
            code = entry.get().strip()
            if code:
                callback(code)
                win.destroy()
            else:
                messagebox.showwarning("Error", "OTP enter karo!")
        
        Button(win, text="✅ SUBMIT OTP", font=("Arial", 12, "bold"),
               bg=GREEN, fg=BLACK, command=submit, width=15).pack(pady=10)
        
        win.bind('<Return>', lambda e: submit())

    def _init_engine(self):
        try:
            from core.engine import TradingEngine
            from brokers.kotak_neo import KotakNeo
            from brokers.session_manager import SessionManager
            from core.option_chain import OptionChain
            from core.indicators import Indicators
            from core.capital import CapitalManager
            from core.risk import RiskManager
            from telegram.bot import TelegramBot
            from telegram.reader import TelegramReader
            from telegram.parser import SignalParser
            from strategies import load_all_strategies
            
            cfg = self._load_config()
            session = SessionManager()
            kotak = KotakNeo(cfg, session)
            oc = OptionChain()
            ind = Indicators()
            cap = CapitalManager(float(cfg.get('trategy', {}).get('capital', 1000) or 1000))
            risk = RiskManager(cfg)
            bot = TelegramBot(cfg)
            reader = TelegramReader(cfg)
            parser = SignalParser()
            strategies = load_all_strategies()
            
            # OTP POPUP CONNECTIONS YAHAN HAI
            kotak.otp_callback = lambda: self.root.after(0, lambda: self._show_popup("🔑 KOTAK NEO OTP", kotak.set_otp_code))
            reader.otp_callback = lambda: self.root.after(0, lambda: self._show_popup("📱 TELEGRAM OTP", reader.set_otp_code))
            
            self.engine = TradingEngine(cfg, kotak, oc, ind, cap, risk, bot, reader, parser, strategies)
            self.engine.on_log = self._log
            self.engine.on_update = self._update_ui
            self.engine.on_trade = self._on_trade
            
            self._log("✅ Engine initialized")
            
            # YAHAN AUTO START HAI (5 SECOND BAAD)
            self.root.after(5000, self._auto_start)
            
        except Exception as e:
            self._log(f"❌ Engine init error: {e}")

    def _show_popup(self, title, callback):
        """Shortcut for popup"""
        self.root.after(0, lambda: self._show_otp_popup(title, callback))

    def _auto_start(self):
        """AUTO START - Button dabane ki zaroorat nahi"""
        if not self.engine:
            self._log("❌ Engine not ready, retrying in 5 sec...")
            self.root.after(5000, self._auto_start)
            return
            
        self._log("🔌 Auto-connecting Kotak & Telegram...")
        
        def bg_connect():
            if self.engine.kotak and not self.engine.kotak.connected:
                self.engine.kotak.try_login()
            if self.engine.tg_reader and not self.engine.tg_reader.connected:
                self.engine.tg_reader.try_connect()
            # Ab actual start karo
            self.root.after(0, self._actual_start)
        
        threading.Thread(target=bg_connect, daemon=True).start()

    def _actual_start(self):
        self.engine.start()
        self.running = True
        self.btn_start.config(text="▶️ RUNNING", bg=GREEN, state=DISABLED)
        self.btn_stop.config(state=NORMAL)
        self._log("🚀 Auto-Started successfully!")
        self._update_loop()

    def _start(self):
        """Manual Start (Agar auto fail ho jaye toh manual use karo)"""
        if not self.engine:
            messagebox.showwarning("Error", "Engine not initialized!")
            return
        self._actual_start()

    def _stop(self):
        if self.engine:
            self.engine.stop()
        self.running = False
        self.btn_start.config(text="▶️ RESTART", bg=GREEN, state=NORMAL)
        self.btn_stop.config(state=DISABLED)
        self._log("🛑 Engine stopped")

    def _toggle_auto(self):
        v = self.auto_var.get()
        self.lbl_auto.config(text="ON" if v else "OFF", fg=GREEN if v else RED)

    def _toggle_paper(self):
        pass # YEH AB LOCKED HAI - KUCH NAHI HOGA

    def _open_settings(self):
        win = Toplevel(self.root)
        win.title("🔧 Settings")
        win.geometry("600x700")
        win.configure(bg=BG2)
        win.transient(self.root)
        win.grab_set()
        
        cfg = self._load_config()
        notebook = ttk.Notebook(win)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Kotak tab
        kotak_frame = Frame(notebook, bg=BG2)
        notebook.add(kotak_frame, text="Kotak Neo")
        kotak_entries = {}
        for field in ['consumer_key', 'mobile', 'password', 'totp_secret']:
            f = Frame(kotak_frame, bg=BG2)
            f.pack(fill=X, padx=20, pady=5)
            Label(f, text=field.replace('_', ' ').title(), fg=WHITE, bg=BG2, width=15, anchor='w').pack(side=LEFT)
            e = Entry(f, bg=BG3, fg=WHITE, insertbackground=WHITE)
            e.insert(0, cfg.get('kotak_neo', {}).get(field, ''))
            e.pack(side=LEFT, fill=X, expand=True, padx=5)
            kotak_entries[field] = e
        
        # Telegram tab
        tg_frame = Frame(notebook, bg=BG2)
        notebook.add(tg_frame, text="Telegram")
        tg_entries = {}
        for field in ['bot_token', 'chat_id', 'api_id', 'api_hash', 'phone']:
            f = Frame(tg_frame, bg=BG2)
            f.pack(fill=X, padx=20, pady=5)
            Label(f, text=field.replace('_', ' ').title(), fg=WHITE, bg=BG2, width=15, anchor='w').pack(side=LEFT)
            e = Entry(f, bg=BG3, fg=WHITE, insertbackground=WHITE)
            e.insert(0, cfg.get('telegram', {}).get(field, ''))
            e.pack(side=LEFT, fill=X, expand=True, padx=5)
            tg_entries[field] = e
        
        # Groups tab
        groups_frame = Frame(notebook, bg=BG2)
        notebook.add(groups_frame, text="Groups")
        canvas = Canvas(groups_frame, bg=BG2)
        scrollbar = Scrollbar(groups_frame, orient="vertical", command=canvas.yview)
        scroll_frame = Frame(canvas, bg=BG2)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        groups = cfg.get('telegram_groups', [])
        group_entries = []
        for i, group in enumerate(groups):
            gf = LabelFrame(scroll_frame, text=group.get('name', f'Group {i+1}'), fg=GOLD, bg=BG2)
            gf.pack(fill=X, padx=10, pady=5)
            for field in ['hash_id', 'chat_id']:
                f = Frame(gf, bg=BG2)
                f.pack(fill=X, padx=5, pady=2)
                Label(f, text=field, fg=WHITE, bg=BG2, width=10, anchor='w').pack(side=LEFT)
                e = Entry(f, bg=BG3, fg=WHITE, insertbackground=WHITE)
                e.insert(0, group.get(field, ''))
                e.pack(side=LEFT, fill=X, expand=True, padx=5)
                group_entries.append((i, field, e))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Trading tab (PAPER MODE LOCK HAI)
        trading_frame = Frame(notebook, bg=BG2)
        notebook.add(trading_frame, text="Trading")
        trading_fields = [
            ('capital', 'Initial Capital', 1000),
            ('max_daily_loss', 'Max Daily Loss', 200),
            ('max_trades_per_day', 'Max Trades/Day', 5),
            ('sl_pct', 'SL %', 50),
            ('target_pct', 'Target %', 100),
            ('update_interval', 'Update Interval (sec)', 5),
        ]
        trading_entries = {}
        for field, label, default in trading_fields:
            f = Frame(trading_frame, bg=BG2)
            f.pack(fill=X, padx=20, pady=5)
            Label(f, text=label, fg=WHITE, bg=BG2, width=20, anchor='w').pack(side=LEFT)
            e = Entry(f, bg=BG3, fg=WHITE, insertbackground=WHITE)
            e.insert(0, str(cfg.get('trading', {}).get(field, default)))
            e.pack(side=LEFT, padx=5)
            trading_entries[field] = e