"""Telegram Bot - Send Messages"""
import requests as req_lib

MANTRAS = {
    'start': '॥ ॐ श्री गणेशाय नमः ि॥\nश्री शिवाय नमस्तुभ्यं\nजय श्री सांवरीया सेठ ि॥\nलक्ष्मी कुबेर की कृपा ि॥\nशुभं करोति कल्याणम् ि॥',
    'buy': '🙏 ॐ श्री गणेशाय नमः ि॥\nलक्ष्मी कुबेर की कृपा ि॥',
    'sell': '॥ शुभं करोति कल्याणम् ि॥\nजय श्री सांवरीया सेठ ि॥',
    'profit': '🙏 शुभ लाभ श्री गणेशाय ि॥\nलक्ष्मी माँ की कृपा ि॥',
    'loss': '॥ ॐ शान्तिः ॥\nधैर्य धरो 🙏',
}

class TelegramBot:
    def __init__(self, cfg):
        self.cfg = cfg.get('telegram_alerts', {}) or cfg.get('telegram', {})
        self.bot_token = self.cfg.get('bot_token', '')
        self.chat_id = self.cfg.get('chat_id', '') or self.cfg.get('my_chat_id', '')
        self.status_msg = "NOT SET"

    def connect(self):
        if not self.bot_token:
            self.status_msg = "NO TOKEN"
            return False
        try:
            r = req_lib.get(f"https://api.telegram.org/bot{self.bot_token}/getMe", timeout=5)
            if r.status_code == 200:
                self.status_msg = "CONNECTED"
                self.send(MANTRAS['start'] + "\n✅ Jss Wealthtech Connected!")
                return True
        except:
            pass
        self.status_msg = "FAILED"
        return False

    def send(self, msg):
        if not self.bot_token:
            return
        try:
            req_lib.post(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                json={'chat_id': self.chat_id, 'text': msg},
                timeout=10
            )
        except:
            pass
