import os, datetime
def run_pre_live_if_time(notifier):
    now = datetime.datetime.now()
    print('Pre-live job triggered at', now.strftime('%Y-%m-%d %H:%M:%S'))
    sample = [
        {'home':'Benfica','away':'Porto','market':'BTTS','confidence':0.82},
        {'home':'Arsenal','away':'Chelsea','market':'OVER_2_5','confidence':0.78},
        {'home':'Real Madrid','away':'Barcelona','market':'1X2_HOME','confidence':0.80},
    ]
    for p in sample:
        if p['confidence'] >= float(os.getenv('PRELIVE_THRESHOLD',0.75)):
            msg = (f'📢 PRE-LIVE: {p["home"]} vs {p["away"]} - {p["market"]} - '
                   f'Confidence {p["confidence"]*100:.1f}%')
            notifier.send_alert(msg)
