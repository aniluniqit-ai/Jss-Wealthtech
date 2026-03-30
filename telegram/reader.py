"""Telegram Group Reader - With OTP Popup Support"""
import os
import threading

try:
    from telethon.sync import TelegramClient
    from telethon.errors import SessionPasswordNeededError
    TELETHON_OK = True
except:
    TELETHON_OK = False

class TelegramReader:
    def __init__(self, cfg):
        self.cfg = cfg
        self.client = None
        self.connected = False
        self.status_msg = "NOT CONFIGURED"
        self.session_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data', 'sessions', 'tg_reader.session'
        )
        
        # OTP Popup System
        self.otp_required = threading.Event()
        self.otp_code = None
        self.otp_callback = None

    def set_otp_code(self, code):
        """UI se OTP aayega yahan"""
        self.otp_code = code
        self.otp_required.set()  # Resume waiting thread

    def try_connect(self):
        """Background mein call hoga - agar OTP chahiye toh popup mangega"""
        if not TELETHON_OK:
            self.status_msg = "Install telethon"
            return False

        api_id = self.cfg.get('telegram', {}).get('api_id', '')
        api_hash = self.cfg.get('telegram', {}).get('api_hash', '')
        phone = self.cfg.get('telegram', {}).get('phone', '')

        if not api_id or not api_hash or not phone:
            self.status_msg = "Need api_id, api_hash & phone in settings"
            return False

        try:
            self.status_msg = "Connecting TG..."
            self.client = TelegramClient(self.session_path, int(api_id), api_hash)
            self.client.connect()
            
            # Check if already authorized
            if self.client.is_user_authorized():
                self.connected = True
                self.status_msg = "CONNECTED"
                return True
            
            # Not authorized - Need OTP
            self.status_msg = "TG OTP REQUIRED"
            
            # UI ko bol popup dikhane ke liye
            if self.otp_callback:
                self.otp_callback()
            
            # Wait for user to enter OTP in popup
            self.otp_required.wait(timeout=120) # 2 min wait
            
            if not self.otp_code:
                self.status_msg = "TG OTP Timeout"
                return False
            
            # Submit OTP to Telethon
            self.client.sign_in(code=self.otp_code)
            self.connected = True
            self.status_msg = "CONNECTED"
            self.otp_code = None
            return True
            
        except SessionPasswordNeededError:
            # 2FA Password required (not OTP)
            self.status_msg = "TG 2FA Password needed (Contact Dev)"
            return False
        except Exception as e:
            self.status_msg = f"TG Error: {e}"
            return False

    def get_recent_messages(self, chat_id, limit=5):
        if not self.connected or not self.client:
            return []
        try:
            messages = self.client.get_messages(chat_id, limit=limit)
            return [{'text': m.text or '', 'date': str(m.date)} for m in messages if m.text]
        except:
            return []