import os, traceback
from telegram import Bot
from datetime import datetime
class TelegramBot:
    def __init__(self, token=None, chat_id=None, dry_run=False):
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('CHAT_ID')
        self.dry_run = dry_run
        if not self.dry_run:
            if not self.token or not self.chat_id:
                print('Missing token/chat_id — switching to dry_run')
                self.dry_run = True
        if not self.dry_run:
            self.bot = Bot(token=self.token)
    def _send(self, text):
        print('Telegram send:', text[:200])
        if self.dry_run:
            return True
        try:
            self.bot.send_message(chat_id=self.chat_id, text=text)
            return True
        except Exception as e:
            print('Telegram error:', e)
            traceback.print_exc()
            return False
    def send_alert(self, text):
        ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        return self._send(f"{text}\n\nSent: {ts}")
    def send_heartbeat(self):
        return self._send(f"💡 Heartbeat - Goal Predictor online ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')})")
