import csv, io, json, os, re

base = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(base, 'riscv_raw.json'), encoding='utf-8'))

# NAND2_1 cell area (um^2) used for gate equivalents: sky130_fd_sc_hd__nand2_1 is 1.38 x 2.72 um,
# sg13g2_nand2_1 is 1.92 x 3.78 um. GF180 left out (cell size not verified).
NAND2 = {'sky130': 3.7536, 'ihp': 7.2576}


def num(x):
    try:
        v = float(x)
        return None if abs(v) > 1e30 or v == -1 else v
    except (TypeError, ValueError):
        return None


def period_ns(cfg, path):
    if not cfg:
        return None
    if path.endswith('.json'):
        try:
            c = json.loads(re.sub(r'//.*', '', cfg))
            return num(c.get('CLOCK_PERIOD'))
        except Exception:
            pass
    m = re.search(r'set ::env\(CLOCK_PERIOD\)\s+"?([\d.]+)', cfg) or \
        re.search(r'CLOCK_PERIOD["\']?\s*[:=]\s*["\']?([\d.]+)', cfg)
    return num(m.group(1)) if m else None


rows = []
for k, r in raw.items():
    s = r['stats/synthesis-stats.txt'] or ''
    shuttle = r['shuttle']
    pdk = 'ihp' if shuttle.startswith('ttihp') else 'gf' if shuttle.startswith('ttgf') else 'sky130'
    met = r['stats/metrics.csv'] or ''
    lines = list(csv.reader(io.StringIO(met)))
    if lines and lines[0][:2] == ['Metric', 'Value']:
        m = {row[0]: row[1] for row in lines[1:] if len(row) >= 2}
        fmt = 'ol2'
    elif len(lines) >= 2:
        m = dict(zip(lines[0], lines[1]))
        fmt = 'ol1'
    else:
        m, fmt = {}, None

    cells = re.findall(r'Number of cells:\s+(\d+)', s)
    chip = re.findall(r"Chip area for (?:top )?module '\\?([^']+)':\s*([\d.]+)", s)
    seq = re.findall(r'sequential elements:\s*[\d.]+\s*\(([\d.]+)%\)', s)
    last_block = s.split('=== ')[-1] if '=== ' in s else s
    ff = 0
    for name, cnt in re.findall(r'^\s+\\?([A-Za-z0-9_$]+)\s+(\d+)\s*$', last_block, re.M):
        cell = name.split('__')[-1] if '__' in name else re.sub(r'^sg13g2_', '', name)
        if re.match(r'(s?e?df|dff)', cell, re.I):
            ff += int(cnt)

    T = period_ns(r.get('config'), r.get('config_path') or '')
    crit = None
    ws_tt = ws_ss = cell_area = die = util = power_mw = None
    if fmt == 'ol2':
        ws_tt = num(next((v for a, v in m.items() if a.startswith('timing__setup__ws__corner:nom_tt')), None))
        ws_ss = num(next((v for a, v in m.items() if a.startswith('timing__setup__ws__corner:nom_ss')), None))
        if ws_tt is None:  # IHP flows report a single corner
            ws_tt = num(m.get('timing__setup__ws'))
        cell_area = num(m.get('design__instance__area__stdcell') or m.get('design__instance__area'))
        die = num(m.get('design__die__area'))
        util = num(m.get('design__instance__utilization'))
        p = num(m.get('power__total'))
        power_mw = p * 1e3 if p else None
    elif fmt == 'ol1':
        crit = num(m.get('critical_path_ns'))
        T = T or num(m.get('CLOCK_PERIOD'))
        d = num(m.get('DIEAREA_mm^2'))
        die = d * 1e6 if d else None
        u = num(m.get('Final_Util'))
        util = u / 100 if u else None
        if not cells and m.get('synth_cell_count'):
            cells = [m['synth_cell_count']]
        if not ff and num(m.get('DFF')):
            ff = int(num(m['DFF']))

    fmax_tt = None
    if crit:
        fmax_tt = 1e3 / crit
    elif T and ws_tt is not None and T - ws_tt > 0:
        fmax_tt = 1e3 / (T - ws_tt)
    fmax_ss = 1e3 / (T - ws_ss) if (T and ws_ss is not None and T - ws_ss > 0) else None

    synth_area = num(chip[-1][1]) if chip else None
    ge = synth_area / NAND2[pdk] if synth_area and pdk in NAND2 else None
    rows.append(dict(
        key=k, shuttle=shuttle, pdk=pdk, macro=r['macro'], title=r['title'], author=r['author'],
        tiles=r['tiles'], clock_hz=r['clock_hz'], repo=r['repo'], flow=fmt,
        synth_cells=num(cells[-1]) if cells else None, synth_area_um2=synth_area, ge=ge,
        seq_pct=num(seq[-1]) if seq else None, ff=ff or None,
        placed_area_um2=cell_area, die_um2=die, util=util, power_mw=power_mw,
        period_ns=T, ws_tt=ws_tt, ws_ss=ws_ss, crit_ns=crit, fmax_tt_mhz=fmax_tt, fmax_ss_mhz=fmax_ss,
        has_info=bool(r.get('info_md')), description=r['description']))

json.dump(rows, open(os.path.join(base, 'riscv_rows.json'), 'w', encoding='utf-8'), indent=1)


def f(x, p=0):
    return '-' if x is None else f'{x:.{p}f}'


for x in rows:
    print(f"{x['key'][:50]:50} {x['pdk']:6} {x['tiles']:4} {x['flow'] or '-':4} cells={f(x['synth_cells'])} GE={f(x['ge'])} ff={x['ff'] or '-'} "
          f"seq%={f(x['seq_pct'])} die={f(x['die_um2'])} util={f(x['util'], 2)} P={f(x['power_mw'], 1)}mW T={f(x['period_ns'], 1)} "
          f"wsTT={f(x['ws_tt'], 2)} fTT={f(x['fmax_tt_mhz'])} fSS={f(x['fmax_ss_mhz'])} clk={f((x['clock_hz'] or 0) / 1e6)}")
