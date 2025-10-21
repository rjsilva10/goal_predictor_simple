import os
from utils import get_live_matches_sample, compute_probability_from_stats
def run_live_check(notifier):
    matches = get_live_matches_sample()
    threshold = float(os.getenv('ALERT_THRESHOLD', 0.75))
    for m in matches:
        prob, breakdown = compute_probability_from_stats(m['stats'])
        print(f"Live check {m['home']} vs {m['away']} — prob={prob:.3f}")
        if prob >= threshold and not m.get('notified', False):
            text = (f"⚠️ ALERTA LIVE — {m['home']} vs {m['away']}\n"
                    f"Probabilidade de evento: {prob*100:.1f}%\n"
                    f"Score: {m['score']}\n"
                    f"Detalhe: {breakdown}")
            notifier.send_alert(text)
            m['notified'] = True
