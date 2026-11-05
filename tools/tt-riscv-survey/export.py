"""Write the survey rows (from parse.py) as a CSV for docs/research/data/."""
import csv, json, os, sys

base = os.path.dirname(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else __file__))
rows = json.load(open(os.path.join(base, 'riscv_rows.json'), encoding='utf-8'))
out = sys.argv[2] if len(sys.argv) > 2 else 'tt-riscv-metrics.csv'
cols = ['shuttle', 'pdk', 'macro', 'title', 'author', 'tiles', 'die_um2', 'util', 'synth_cells', 'synth_area_um2',
        'ge', 'ff', 'seq_pct', 'power_mw', 'clock_hz', 'period_ns', 'ws_tt', 'ws_ss', 'fmax_tt_mhz', 'fmax_ss_mhz', 'flow', 'repo']
with open(out, 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(cols)
    for r in rows:
        w.writerow(['' if r.get(c) is None else (round(r[c], 2) if isinstance(r[c], float) else r[c]) for c in cols])
print(f'{len(rows)} rows -> {out}')
