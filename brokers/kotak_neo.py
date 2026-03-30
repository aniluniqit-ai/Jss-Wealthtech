"""Kotak Neo Broker - With OTP Popup Support"""
import os
import threading

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

try:
    from neo_api_client import NeoAPI
    KOTAK_OK = True
except:
    KOTAK_OK = False

try:
    import pyotp
    PYOTP_OK = True
except:
    PYOTP_OK = False

class KotakNeo:
    def __init__(self, cfg, session_mgr):
        self.cfg = cfg.get('kotak_neo', {})
        self.session_mgr = session_mgr
        self.api = None
        self.logged_in = False
        self.status_msg = "NOT CONFIGURED"
        
        # OTP Popup System
        self.otp_required = threading.Event()
        self.otp_code = None
        self.otp_callback = None
        
        self._try_load_session()

    def _try_load_session(self):
        session = self.session_mgr.load_kotak_session()
        if session:
            self.cfg['access_token'] = session.get('access_token', '')
            self.cfg['sid'] = session.get('sid', '')

    def set_otp_code(self, code):
        """UI se OTP aayega yahan"""
        self.otp_code = code
        self.otp_required.set()  # Resume waiting thread

    def try_login(self):
        """Background mein call hoga - agar OTP chahiye toh popup mangega"""
        try:
            if not KOTAK_OK:
                self.status_msg = "Install neo-api-client"
                return False
            
            consumer_key = self.cfg.get('consumer_key', '')
            mobile = self.cfg.get('mobile', '')
            password = self.cfg.get('password', '')
            
            if not all([consumer_key, mobile, password]):
                self.status_msg = "Missing credentials in settings"
                return False
            
            self.status_msg = "Connecting..."
            self.api = NeoAPI(consumer_key=consumer_key, environment='prod')
            
            # Step 1: Login with mobile/password
            self.api.login(mobile=mobile, password=password)
            
            # Agar yahan tak kaam chal gaya toh OTP nahi chahiye
            self.logged_in = True
            self.status_msg = "CONNECTED"
            self.session_mgr.save_kotak_session(self.api.access_token, self.api.sid)
            return True
            
        except Exception as e:
            error_text = str(e).lower()
            
            # Check if OTP is required
            if 'otp' in error_text or '2fa' in error_text or 'totp' in error_text:
                self.status_msg = "OTP REQUIRED"
                
                # UI ko bol popup dikhane ke liye
                if self.otp_callback:
                    self.otp_callback()
                
                # Wait for user to enter OTP in popup
                self.otp_required.wait(timeout=120)  # 2 min wait
                
                if not self.otp_code:
                    self.status_msg = "OTP Timeout"
                    return False
                
                # Step 2: Submit OTP
                try:
                    self.api.session_2fa(otp=self.otp_code)
                    self.logged_in = True
                    self.status_msg = "CONNECTED"
                    self.otp_code = None
                    
                    # Save session
                    try:
                        self.session_mgr.save_kotak_session(self.api.access_token, self.api.sid)
                    except:
                        pass
                    
                    return True
                except Exception as e2:
                    self.status_msg = f"Invalid OTP: {e2}"
                    self.otp_code = None
                    return False
            else:
                self.status_msg = f"Login failed: {e}"
                return False

    def get_quote(self, token, exchange):
        if not self.logged_in or not self.api:
            return None
        try:
            return self.api.quotation(instrument_token=token, exchange_segment=exchange)
        except:
            return None

    def get_history(self, token, exchange):
        if not self.logged_in or not self.api:
            return None
        try:
            return self.api.intraday_chart(instrument_token=token, exchange_segment=exchange)
        except:
            return None