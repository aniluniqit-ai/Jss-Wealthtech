"""Kotak Neo Broker - Hardcoded Values - No Config Needed"""
import json
import pyotp
import requests

INSTRUMENTS = {
    'NIFTY': 'nse_cm|Nifty 50',
    'BANKNIFTY': 'nse_cm|Nifty Bank',
    'FINNIFTY': 'nse_cm|Nifty Fin Service',
    'MIDCPNIFTY': 'nse_cm|NIFTY MID SELECT',
    'SENSEX': 'bse_cm|SENSEX',
    'BANKEX': 'bse_cm|BANKEX',
    'CRUDEOIL': 'mcx_fo|CRUDEOIL',
    'NATURALGAS': 'mcx_fo|NATURALGAS'
}

SYMBOLS = INSTRUMENTS

# === HARDCODED VALUES - DIRECT CONNECT ===
HARDCODED = {
    "access_token": "4330d772-bb66-498d-a4cb-3ae8e8c324a8",
    "client_code": "XV3ZT",
    "mobile": "+919509675779",
    "mpin": "112151",
    "totp_secret": "YYDEDABS3PAAOWLECS3C33GUOM"
}


class KotakNeo:
    def __init__(self, cfg=None, session_mgr=None):
        # USE HARDCODED VALUES - CONFIG OPTIONAL
        self.access_token = HARDCODED["access_token"]
        self.client_code = HARDCODED["client_code"]
        self.mobile = HARDCODED["mobile"]
        self.mpin = HARDCODED["mpin"]
        self.totp_secret = HARDCODED["totp_secret"]

        # Override from config if available
        if cfg:
            if cfg.get('access_token', '').strip():
                self.access_token = cfg['access_token'].strip()
            if cfg.get('client_code', '').strip():
                self.client_code = cfg['client_code'].strip()
            if cfg.get('mobile', '').strip():
                self.mobile = cfg['mobile'].strip()
            if cfg.get('mpin', '').strip():
                self.mpin = cfg['mpin'].strip()
            if cfg.get('totp_secret', '').strip():
                self.totp_secret = cfg['totp_secret'].strip()

        self.session_mgr = session_mgr
        self.logged_in = False
        self.base_url = ""
        self.session_token = ""
        self.session_sid = ""
        self.status_msg = "NOT INITIALIZED"
        self.log_callback = None

    def set_log_callback(self, callback):
        self.log_callback = callback

    def set_otp_callback(self, callback):
        pass

    def submit_otp(self, code):
        pass

    def _log(self, msg):
        print("[KOTAK] " + msg)
        if self.log_callback:
            try:
                self.log_callback(msg)
            except Exception:
                pass

    def connect(self):
        self._log("━━━ KOTAK DIRECT LOGIN ━━━")
        self._log("✅ Token: " + self.access_token[:10] + "****")
        self._log("✅ Client Code: " + self.client_code)
        self._log("✅ Mobile: " + self.mobile[:7] + "****")
        self._log("✅ TOTP: " + self.totp_secret[:8] + "****")

        try:
            # STEP 1: Generate TOTP
            self._log("🔐 Generating TOTP...")
            current_totp = pyotp.TOTP(self.totp_secret).now()
            self._log("✅ TOTP: " + str(current_totp)[:2] + "****")

            # STEP 2: tradeApiLogin
            self._log("🔄 Step 1: tradeApiLogin...")
            headers_1 = {
                "Authorization": self.access_token,
                "neo-fin-key": "neotradeapi",
                "Content-Type": "application/json"
            }
            payload_1 = {
                "mobileNumber": self.mobile,
                "ucc": self.client_code,
                "totp": current_totp
            }

            res_1 = requests.post(
                "https://mis.kotaksecurities.com/login/1.0/tradeApiLogin",
                headers=headers_1,
                json=payload_1
            )
            data_1 = res_1.json()

            status_1 = data_1.get("data", {}).get("status", "")
            if status_1 != "success":
                err_msg = data_1.get("data", {}).get("message", "") or data_1.get("message", "Unknown error")
                self.status_msg = "Login Failed"
                self._log("❌ tradeApiLogin failed: " + str(err_msg))
                return False

            view_token = data_1["data"]["token"]
            view_sid = data_1["data"]["sid"]
            self._log("✅ Step 1 passed!")

            # STEP 3: tradeApiValidate
            self._log("🔄 Step 2: tradeApiValidate (MPIN)...")
            headers_2 = {
                "Authorization": self.access_token,
                "neo-fin-key": "neotradeapi",
                "sid": view_sid,
                "Auth": view_token,
                "Content-Type": "application/json"
            }

            res_2 = requests.post(
                "https://mis.kotaksecurities.com/login/1.0/tradeApiValidate",
                headers=headers_2,
                json={"mpin": self.mpin}
            )
            data_2 = res_2.json()

            status_2 = data_2.get("data", {}).get("status", "")
            if status_2 != "success":
                err_msg = data_2.get("data", {}).get("message", "") or data_2.get("message", "Unknown error")
                self.status_msg = "MPIN Failed"
                self._log("❌ tradeApiValidate failed: " + str(err_msg))
                return False

            self.base_url = data_2["data"]["baseUrl"]
            self.session_token = data_2["data"]["token"]
            self.session_sid = data_2["data"]["sid"]
            self.logged_in = True
            self.status_msg = "Connected"
            self._log("✅ Step 2 passed!")
            self._log("🎉 KOTAK CONNECTED!")
            return True

        except Exception as e:
            self.status_msg = "Error"
            self._log("❌ Error: " + str(e))
            return False

    def get_ltp(self, symbol):
        if not self.logged_in:
            return None

        sym_str = INSTRUMENTS.get(symbol)
        if not sym_str:
            return None

        try:
            url = self.base_url + "/script-details/1.0/quotes/neosymbol/" + sym_str + "/all"
            headers = {
                "Authorization": self.access_token,
                "Content-Type": "application/json"
            }

            res = requests.get(url, headers=headers, timeout=5)

            if res.status_code != 200:
                if symbol == "NIFTY":
                    self._log("⚠️ Quote error " + str(res.status_code))
                return None

            data = res.json()

            if isinstance(data, list) and len(data) > 0:
                item = data[0]

                ltp_str = item.get("ltp", "0")
                if not ltp_str or ltp_str == "0":
                    return None

                ltp_val = float(ltp_str)
                if ltp_val <= 0:
                    return None

                ohlc = item.get("ohlc", {})

                return {
                    'ltp': ltp_val,
                    'change': float(item.get("change", "0") or "0"),
                    'change_pct': float(item.get("per_change", "0") or "0"),
                    'high': float(ohlc.get("high", "0") or "0"),
                    'low': float(ohlc.get("low", "0") or "0"),
                    'open': float(ohlc.get("open", "0") or "0"),
                    'close': float(ohlc.get("close", "0") or "0"),
                    'volume': int(item.get("last_volume", "0") or "0")
                }

            return None

        except Exception as e:
            if symbol == "NIFTY":
                self._log("⚠️ Rate error: " + str(e)[:80])
            return None