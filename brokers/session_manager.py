"""Session Manager - OTP Once, Save Session"""
import json, os
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sessions')
        os.makedirs(self.base, exist_ok=True)
        self.kotak_file = os.path.join(self.base, 'kotak_session.json')

    def save_kotak_session(self, access_token, sid):
        data = {
            'access_token': access_token,
            'sid': sid,
            'created_at': datetime.now().isoformat(),
            'expires_at': ''
        }
        with open(self.kotak_file, 'w') as f:
            json.dump(data, f, indent=2)
        return True

    def load_kotak_session(self):
        try:
            if os.path.exists(self.kotak_file):
                with open(self.kotak_file, 'r') as f:
                    data = json.load(f)
                if data.get('access_token') and data.get('sid'):
                    return data
        except:
            pass
        return None

    def clear_kotak_session(self):
        if os.path.exists(self.kotak_file):
            os.remove(self.kotak_file)
