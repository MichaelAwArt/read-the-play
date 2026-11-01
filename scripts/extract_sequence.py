"""Build a Read the Play sequence file from a Wisehockey match-events CSV.

Runs locally on the confidential challenge files and writes private/sequence.js,
which is ignored by git. Usage:

    python scripts/extract_sequence.py EVENTS.csv --period 1 --from 298 --to 311

--from / --to are MatchClock values in seconds (elapsed time in the period).
The puck path (puckFree, carry) is set by hand afterwards: the script lists the
puck-control events of the window to help you write it.
"""
import argparse, json, os
import pandas as pd

def player_id(name, team):
    number = str(name).split()[0].lstrip('#')
    return number + ('d' if team == 'Away' else 'u')   # 'd' = HC Davos (Away in this game)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('csv')
    p.add_argument('--period', type=int, required=True)
    p.add_argument('--from', dest='start', type=int, required=True)
    p.add_argument('--to', dest='end', type=int, required=True)
    p.add_argument('--out', default='private/sequence.js')
    a = p.parse_args()

    d = pd.read_csv(a.csv, encoding='utf-8-sig', low_memory=False)
    s = d[(d.Period == a.period) & (d.MatchClock.between(a.start, a.end))]
    t0 = s.Timestamp.iloc[0]
    snaps, players = [], {}
    for _, r in s.iterrows():
        t = round((r.Timestamp - t0) / 1000, 2)
        pos = {}
        for k in range(1, 13):
            c = r.get(f'StartPlayerCoordinates{k}')
            if isinstance(c, str):
                pid = player_id(r[f'StartPlayerName{k}'], r[f'StartPlayerTeam{k}'])
                x, y = map(float, c.split(','))
                pos[pid] = [x, y]
                v = r.get(f'StartPlayerVelocity{k}')
                players.setdefault(pid, {
                    'name': str(r[f'StartPlayerName{k}']).split(' ', 1)[1],
                    'team': 'HC Davos' if pid.endswith('d') else 'U.S. Collegiate Selects',
                    'kmh': None if pd.isna(v) else round(float(v) * 3.6),  # velocity looks like m/s: to confirm
                    'g': {}})
        if pos:
            snaps.append([t, pos])
        if r.EventType == 'PuckControl':
            print(f"t={t:6.2f}  {r.EventPrimaryPlayerName or 'loose':28}  start={r.EventStartCoordinate}")

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    data = {'note': 'REAL DATA - confidential, do not commit', 'snaps': snaps,
            'puckFree': [], 'carry': [], 'players': players}
    with open(a.out, 'w') as f:
        f.write('window.RTP_DATA = ' + json.dumps(data) + ';\n')
    print(f'\nWrote {a.out} with {len(snaps)} snapshots. Now fill puckFree and carry by hand.')

if __name__ == '__main__':
    main()
