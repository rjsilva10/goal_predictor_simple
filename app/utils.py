import random
def get_live_matches_sample():
    return [
        {'id': 101, 'home': 'Benfica', 'away': 'Porto', 'score': '0-0',
         'stats': {'xg': 1.1, 'shots_on_target': 4, 'dangerous_attacks': 28, 'possession': 62, 'red_cards_diff': 0}},
        {'id': 102, 'home': 'Orbit', 'away': 'Richards Bay', 'score': '0-0',
         'stats': {'xg': 0.05, 'shots_on_target': 0, 'dangerous_attacks': 2, 'possession': 32, 'red_cards_diff': 0}},
    ]
def compute_probability_from_stats(stats):
    xg = min(stats.get('xg',0),3)/3.0
    shots = min(stats.get('shots_on_target',0),10)/10.0
    attacks = min(stats.get('dangerous_attacks',0),40)/40.0
    possession = min(max(stats.get('possession',50),0),100)/100.0
    red_diff = stats.get('red_cards_diff', 0)
    base = (xg*0.35) + (shots*0.25) + (attacks*0.25) + (possession*0.10)
    if red_diff < 0:
        base *= 0.85
    base = min(max(base, 0.0), 1.0)
    breakdown = {'xg':xg, 'shots':shots, 'attacks':attacks, 'possession':possession, 'red_adj': 0.85 if red_diff<0 else 1.0}
    return base, breakdown
