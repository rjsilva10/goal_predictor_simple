import requests, time, logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class TelegramSimple:
    def __init__(self, token: str, chat_id: str, max_retries: int = 3, backoff: float = 1.5):
        self.token = token
        self.chat_id = chat_id
        self.base = f"https://api.telegram.org/bot{self.token}"
        self.max_retries = max_retries
        self.backoff = backoff

    def send(self, text: str, parse_mode="Markdown") -> Tuple[bool, dict]:
        url = f"{self.base}/sendMessage"
        data = {"chat_id": self.chat_id, "text": text, "parse_mode": parse_mode}
        for attempt in range(1, self.max_retries + 1):
            try:
                r = requests.post(url, data=data, timeout=10)
                if r.status_code == 200:
                    logging.info("Mensagem enviada com sucesso")
                    return True, r.json()
                elif r.status_code == 429:
                    delay = int(r.json().get("parameters", {}).get("retry_after", self.backoff * attempt))
                    logging.warning("Rate limit; a aguardar %s s", delay)
                    time.sleep(delay)
                else:
                    logging.warning("Falha (%s): %s", r.status_code, r.text[:200])
                    time.sleep(self.backoff * attempt)
            except Exception as e:
                logging.warning("Erro ao enviar mensagem (%s): %s", attempt, e)
                time.sleep(self.backoff * attempt)
        return False, {"error": "failed_after_retries"}
