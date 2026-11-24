#!/usr/bin/env python3
"""Add Vest real-time perp 1-minute bars (#VCANDLES) to gexterm snapshot files.

Usage: python3 vest_backfill.py FILE [FILE ...]
SPX file -> SPX-USD-PERP (tracks CME ES), GLD file -> GC-PERP (tracks COMEX GC),
NDX file -> NDX-USD-PERP (tracks NQ). Bars cover the current futures session
(from 18:00 ET of the previous day) up to now. Existing #VCANDLES lines are replaced.
"""
import json, os, re, sys, time, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BASE = 'https://server-prod.hz.vestmarkets.com/v2/klines'
MAP = {'SPX': 'SPX-USD-PERP', 'GLD': 'GC-PERP', 'NDX': 'NDX-USD-PERP'}
ET = ZoneInfo('America/New_York')


def _get(sym, iv):
    # Vest returns the most recent ~500 bars per interval (time-window params are ignored)
    req = urllib.request.Request(f'{BASE}?symbol={sym}&interval={iv}&limit=1000', headers={'xrestservermm': 'restserver0', 'User-Agent': 'gexterm'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r).get('data') or []


def klines(sym, start_ms, end_ms):
    """1-minute bars for the last ~8 h, 5-minute bars before that, back to the session start."""
    one = {int(k[0]): k for k in _get(sym, '1m')}
    first1 = min(one) if one else end_ms
    five = {int(k[0]): k for k in _get(sym, '5m') if start_ms <= int(k[0]) and int(k[0]) + 300000 <= first1}
    out = {**five, **one}
    return [out[t] for t in sorted(out) if start_ms <= t <= end_ms]


def session_start_ms(now_et):
    d = now_et if now_et.hour >= 18 else now_et - timedelta(days=1)
    while d.weekday() == 5:  # Saturday -> Friday evening session is closed; step back
        d -= timedelta(days=1)
    s = d.replace(hour=18, minute=0, second=0, microsecond=0)
    if now_et.weekday() == 0 and now_et.hour < 18:  # Monday: session opened Sunday 18:00
        s = (now_et - timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)
    return int(s.timestamp() * 1000)


def fmt(x):
    return ('%.4f' % float(x)).rstrip('0').rstrip('.')


def main(paths):
    now = datetime.now(ET)
    start, end = session_start_ms(now), int(time.time() * 1000)
    for p in paths:
        m = re.match(r'(SPX|GLD|NDX)_', os.path.basename(p))
        if not m:
            print('skip', p); continue
        vsym = MAP[m.group(1)]
        try:
            ks = klines(vsym, start, end)
        except Exception as e:
            print(f'{p}: Vest fetch failed ({e}); file left unchanged'); continue
        if not ks:
            print(f'{p}: no Vest bars'); continue
        line = f'#VCANDLES {vsym} ' + ';'.join(f'{int(k[0])},{fmt(k[1])},{fmt(k[2])},{fmt(k[3])},{fmt(k[4])}' for k in ks)
        lines = [l for l in open(p).read().split('\n') if not l.startswith('#VCANDLES ')]
        idx = max([i for i, l in enumerate(lines) if l.startswith('#GEXSNAP') or l.startswith('#CANDLES ')] or [0]) + 1
        lines.insert(idx, line)
        open(p, 'w').write('\n'.join(lines))
        print(f'{p}: {len(ks)} {vsym} bars, last close {fmt(ks[-1][4])}')


if __name__ == '__main__':
    main(sys.argv[1:])
