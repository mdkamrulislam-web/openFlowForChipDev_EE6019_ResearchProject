import json,glob,re,os,subprocess,sys
base=os.path.dirname(os.path.abspath(__file__))
pat=re.compile(r'risc[\s\-_]?v|rv32|rv64|rv16|\bserv\b|qerv|fazyrv|exotiny|tinyqv|nanov|kianv|picorv|hazard3|minimax|femtorv|ibex|vexriscv|darkriscv',re.I)
skip=re.compile(r'hazard|_alu$|riscv_branch|peripheral|i2c|register$|fp8|cwru|McCoy|wokwi_4349',re.I)
out={}
for f in sorted(glob.glob(os.path.join(base,'*.json'))):
    d=json.load(open(f,encoding='utf-8')); shuttle=os.path.basename(f)[:-5]
    repo=d.get('repo','').replace('https://github.com/','')
    for p in d['projects']:
        txt=' '.join(str(p.get(k,'')) for k in ('macro','title','description','repo'))
        if not pat.search(txt) or skip.search(p['macro']+p.get('title','')): continue
        key=f"{shuttle}/{p['macro']}"
        rec=dict(shuttle=shuttle,shuttle_repo=repo,**{k:p.get(k) for k in ('macro','title','author','tiles','clock_hz','repo','commit','description')})
        for fn in ('info.yaml','stats/metrics.csv','stats/synthesis-stats.txt'):
            r=subprocess.run(['gh','api',f"repos/{repo}/contents/projects/{p['macro']}/{fn}",'-H','Accept: application/vnd.github.raw'],capture_output=True,text=True,encoding='utf-8',errors='replace')
            rec[fn]=r.stdout if r.returncode==0 else None
        out[key]=rec
        print(key, rec['stats/metrics.csv'] is not None, file=sys.stderr)
json.dump(out,open(os.path.join(base,'riscv_raw.json'),'w',encoding='utf-8'),indent=1)
