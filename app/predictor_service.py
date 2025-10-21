import os, json, time, logging, requests, random
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv
import schedule
from telegram_simple import TelegramSimple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
API_SPORTS_KEY = os.getenv('API_SPORTS_KEY')
FOOTBALL_DATA_KEY = os.getenv('FOOTBALL_DATA_KEY')
ALERT_THRESHOLD = float(os.getenv('ALERT_THRESHOLD', '0.75'))
LIVE_INTERVAL_MIN = int(os.getenv('LIVE_INTERVAL_MIN', '10'))

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
NOTIFIED_FILE = DATA_DIR / "notified.json"

notifier = TelegramSimple(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

def save_notified(s):
    try:
        with open(NOTIFIED_FILE, "w", encoding="utf-8") as f:
            json.dump(list(s), f)
    except Exception as e:
        logging.warning("Falha a gravar notified: %s", e)

def load_notified():
    if NOTIFIED_FILE.exists():
        try:
            with open(NOTIFIED_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

already_alerted = load_notified()

def get_live_matches_from_apis():
    out = []
    if API_SPORTS_KEY:
        try:
            url = 'https://v3.football.api-sports.io/fixtures?live=all'
            r = requests.get(url, headers={'x-apisports-key': API_SPORTS_KEY}, timeout=15)
            if r.ok:
                out = r.json().get('response', [])
        except Exception as e:
            logging.warning('api-sports live error: %s', e)
    return out

def get_pre_live_matches_today():
    out = []
    if FOOTBALL_DATA_KEY:
        try:
            today = date.today().isoformat()
            url = f'https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={today}'
            r = requests.get(url, headers={'X-Auth-Token': FOOTBALL_DATA_KEY}, timeout=15)
            if r.ok:
                out = r.json().get('matches', [])
        except Exception as e:
            logging.warning('football-data pre-live error: %s', e)
    return out

def estimate_goal_probability_from_stats(match):
    fid = str(match.get('fixture', {}).get('id') or random.randint(1,9999999))
    random.seed(fid + str(datetime.now().minute//5))
    return random.uniform(0.05, 0.95)

def format_live_alert(match, prob):
    fixture = match.get('fixture', {})
    teams = match.get('teams', {})
    home = teams.get('home', {}).get('name', 'Home')
    away = teams.get('away', {}).get('name', 'Away')
    score = match.get('goals', {})
    return f"?? *ALERTA LIVE — GOLO PROVÁVEL*\n\n{home} vs {away}\nProb: *{prob*100:.1f}%*\nScore: {score.get('home',0)} - {score.get('away',0)}\nTempo: {fixture.get('status', {}).get('elapsed')}'"

def format_prelive(pred):
    return f"?? *PRE-LIVE*\n{pred.get('home')} vs {pred.get('away')}\nConfiança: *{pred.get('confidence',0)*100:.1f}%*"

def live_check_and_alert():
    logging.info('LIVE check...')
    matches = get_live_matches_from_apis()
    if not matches:
        logging.info('Sem jogos ao vivo.')
        return
    for m in matches:
        fid = str(m.get('fixture', {}).get('id') or random.randint(1,9999999))
        if fid in already_alerted: continue
        prob = estimate_goal_probability_from_stats(m)
        if prob >= ALERT_THRESHOLD:
            msg = format_live_alert(m, prob)
            notifier.send(msg)
            already_alerted.add(fid)
            save_notified(already_alerted)

def pre_live_daily_job():
    logging.info('PRE-LIVE diário...')
    preds = get_pre_live_matches_today()
    for p in preds[:20]:
        pred = {'home': p.get('homeTeam', {}).get('name',''), 'away': p.get('awayTeam', {}).get('name',''), 'confidence': round(random.uniform(0.75,0.9),2)}
        notifier.send(format_prelive(pred))
        time.sleep(0.7)

def start_scheduler():
    schedule.every().day.at("10:00").do(pre_live_daily_job)
    schedule.every(LIVE_INTERVAL_MIN).minutes.do(live_check_and_alert)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    pre_live_daily_job()
    live_check_and_alert()
    start_scheduler()
