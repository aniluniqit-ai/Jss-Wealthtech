"""Telegram Reader - reads messages from configured groups."""
import asyncio
import os
import time
import threading
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


class TelegramReader:
    def __init__(self, cfg):
        tg = (cfg or {}).get("telegram", {})
        self.api_id = int(tg.get("api_id") or 0)
        self.api_hash = (tg.get("api_hash") or "").strip()
        self.phone = (tg.get("phone") or "").strip()
        self.password = (tg.get("password") or "").strip()
        base = os.path.join(os.getcwd(), "data", "sessions")
        os.makedirs(base, exist_ok=True)
        self.session_name = os.path.join(base, "jss_console_session")
        self.client = None
        self.loop = asyncio.new_event_loop()
        self._loop_lock = threading.Lock()
        self.connected = False
        self.status_msg = "NOT CONNECTED"
        self.log_callback = None
        self.otp_callback = None
        self.otp_code = ""

    def set_log_callback(self, callback):
        self.log_callback = callback

    def set_otp_callback(self, callback):
        self.otp_callback = callback

    def _log(self, msg):
        if self.log_callback:
            try:
                self.log_callback(msg)
            except Exception:
                pass

    def submit_otp(self, code):
        self.otp_code = (code or "").strip()

    def submit_password(self, password):
        self.password = (password or "").strip()

    def connect(self):
        if not self.api_id or not self.api_hash:
            self.status_msg = "MISSING API"
            return False
        try:
            with self._loop_lock:
                self.client = TelegramClient(self.session_name, self.api_id, self.api_hash, loop=self.loop)
                self.loop.run_until_complete(self.client.connect())
                is_auth = self.loop.run_until_complete(self.client.is_user_authorized())
            if not is_auth:
                if not self.phone:
                    self.status_msg = "PHONE REQUIRED"
                    return False
                with self._loop_lock:
                    self.loop.run_until_complete(self.client.send_code_request(self.phone))
                self.status_msg = "WAITING OTP"
                if self.otp_callback:
                    self.otp_callback("TELEGRAM")
                for _ in range(180):
                    if self.otp_code:
                        break
                    time.sleep(1)
                if not self.otp_code:
                    self.status_msg = "OTP TIMEOUT"
                    return False
                with self._loop_lock:
                    try:
                        self.loop.run_until_complete(self.client.sign_in(self.phone, self.otp_code))
                    except SessionPasswordNeededError:
                        if not self.password:
                            self.status_msg = "WAITING 2FA PASSWORD"
                            if self.otp_callback:
                                self.otp_callback("TELEGRAM_PASSWORD")
                            for _ in range(180):
                                if self.password:
                                    break
                                time.sleep(1)
                        if not self.password:
                            self.status_msg = "2FA PASSWORD TIMEOUT"
                            return False
                        self.loop.run_until_complete(self.client.sign_in(password=self.password))
            self.connected = True
            self.status_msg = "CONNECTED"
            self._log("✅ Telegram reader connected")
            return True
        except Exception as e:
            self.status_msg = "FAILED"
            self._log(f"❌ Telegram reader error: {e}")
            return False

    def get_recent_messages(self, chat, limit=5):
        if not self.connected or not self.client or not chat:
            return []
        out = []
        try:
            async def _fetch():
                rows = []
                async for m in self.client.iter_messages(chat, limit=limit):
                    rows.append({"text": getattr(m, "message", "") or "", "date": str(getattr(m, "date", ""))})
                return rows
            with self._loop_lock:
                out = self.loop.run_until_complete(_fetch())
        except Exception:
            return []
        return out
