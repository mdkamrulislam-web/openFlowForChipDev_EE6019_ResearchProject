import json, os, subprocess, sys

base = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(base, 'riscv_raw.json'), encoding='utf-8'))


def gh_raw(path):
    r = subprocess.run(['gh', 'api', path, '-H', 'Accept: application/vnd.github.raw'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout if r.returncode == 0 else None


for k, r in raw.items():
    if r.get('config_fetched'):
        continue
    repo = (r['repo'] or '').replace('https://github.com/', '').replace('git@github.com:', '').removesuffix('.git')
    ref = r.get('commit') or ''
    cfg = None
    if repo:
        for p in ('src/config.json', 'src/config.yaml', 'src/config.tcl'):
            cfg = gh_raw(f'repos/{repo}/contents/{p}?ref={ref}')
            if cfg:
                r['config_path'] = p
                break
    r['config'] = cfg
    r['info_md'] = gh_raw(f"repos/{r['shuttle_repo']}/contents/projects/{r['macro']}/docs/info.md")
    r['config_fetched'] = True
    print(k, bool(cfg), bool(r['info_md']), file=sys.stderr)

json.dump(raw, open(os.path.join(base, 'riscv_raw.json'), 'w', encoding='utf-8'), indent=1)
