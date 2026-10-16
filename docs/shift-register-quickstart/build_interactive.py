"""Build a self-contained, offline interactive learner document."""
from pathlib import Path
import base64, html, json, zipfile
from project_files import sync_starter
ROOT = Path(__file__).resolve().parent
def esc(s): return html.escape(str(s))
def diagram(kind):
    def box(x,y,w,h,title,sub=''):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#eff8f5" stroke="#147d70"/><text x="{x+w/2}" y="{y+27}" text-anchor="middle" font-weight="700">{esc(title)}</text><text x="{x+w/2}" y="{y+49}" text-anchor="middle" font-size="12">{esc(sub)}</text>'
    def arrow(x,y,x2,y2): return f'<path d="M{x},{y} L{x2},{y2}" stroke="#147d70" stroke-width="2" fill="none" marker-end="url(#arr)"/>'
    start='<svg role="img" viewBox="0 0 880 210" xmlns="http://www.w3.org/2000/svg"><title>'+esc(kind+' diagram')+'</title><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#147d70"/></marker></defs><g font-family="Arial,sans-serif" font-size="15" fill="#17334b">'
    body=''
    if kind=='route':
        for i,(a,b) in enumerate([('Your Verilog','Existing circuit'),('Connect pins','Add a wrapper'),('Run tests','Check behaviour'),('Build layout','Check gates + wires'),('Save evidence','Keep one revision')]):
            body+=box(8+i*176,70,158,65,a,b)
            if i<4: body+=arrow(166+i*176,103,180+i*176,103)
    elif kind=='shift':
        body+='<text x="440" y="28" text-anchor="middle">On an enabled rising edge, each bit moves towards bit 7</text>'
        body+=box(10,80,105,65,'serial_in','New bit')
        for i in range(8):
            x=150+i*88; body+=box(x,80,70,65,'q['+str(i)+']','1 bit')
            body+=arrow(x-27,112,x-3,112)
        body+='<text x="440" y="189" text-anchor="middle" font-size="13">We display the output as q[7] … q[0]; new bits enter on the right.</text>'
    elif kind=='mapping':
        body+=box(5,30,210,145,'Tiny Tapeout','ui_in[0], ui_in[1]')
        body+='<text x="110" y="105" text-anchor="middle">clk, rst_n</text><text x="110" y="136" text-anchor="middle">uio pins unused</text>'
        body+=box(280,30,260,145,'Wrapper: project.v','Connects the fixed interface')
        body+='<text x="410" y="108" text-anchor="middle">rst = ~rst_n</text><text x="410" y="140" text-anchor="middle">q → uo_out</text>'
        body+=box(615,30,260,145,'Existing shift register','serial_in, enable, clk, rst')
        body+='<text x="745" y="125" text-anchor="middle">Eight-bit q output</text>'
        body+=arrow(220,75,275,75)+arrow(545,75,610,75)+arrow(610,155,545,155)
    elif kind=='files':
        for i,(title,sub) in enumerate([('project.v','Declares the wrapper'),('info.yaml','Names it + lists sources'),('test/tb.v','Instantiates it')]):
            body+=box(30+i*287,35,250,75,title,sub)
        body+='<text x="440" y="140" text-anchor="middle" font-weight="700">Same top name: tt_um_student_shift_register</text><text x="440" y="178" text-anchor="middle">Both source lists: project.v + shift_register.v</text>'
    elif kind=='checks':
        start=start.replace('880 210','880 390')
        body+=box(5,135,170,65,'Commit / push','Same saved version')
        body+=box(240,10,230,65,'RTL test','Check source behaviour')
        body+=box(240,110,230,65,'docs','Build the datasheet')
        body+=box(240,210,230,65,'gds build','Place gates + route wires')
        body+=box(600,130,275,60,'precheck','Integration rules')
        body+=box(600,210,275,60,'gate-level test (GLS)','Same checks on logic cells')
        body+=box(600,290,275,60,'viewer','Publish the layout view')
        body+='<path d="M175,167 L205,167 M205,42 L205,242" stroke="#147d70" stroke-width="2" fill="none"/>'
        for yy in [42,142,242]:body+=arrow(205,yy,235,yy)
        body+='<path d="M470,242 L540,242 M540,160 L540,320" stroke="#147d70" stroke-width="2" fill="none"/>'
        for yy in [160,240,320]:body+=arrow(540,yy,595,yy)
        body+='<text x="440" y="380" text-anchor="middle" font-size="13">Three workflows start independently; precheck, GLS and viewer wait for the GDS build.</text>'
    graphic=(start+body+'</g></svg>').replace('id="arr"',f'id="arr-{kind}"').replace('url(#arr)',f'url(#arr-{kind})')
    return '<div class="diagram"><div class="diagramhint">Scroll sideways to explore the diagram ↔</div>'+graphic+'</div>'

CSS=r'''
:root{--ink:#17334b;--muted:#566779;--teal:#147d70;--paper:#fffdfa;--line:#dbe3e6;--orange:#d87537}*{box-sizing:border-box}body{margin:0;background:#f2f4f2;color:var(--ink);font:16px/1.55 'Segoe UI',Arial,sans-serif}button,a,input{touch-action:manipulation}a{color:#087364}button{font:inherit;cursor:pointer;border:1px solid var(--line);border-radius:8px;padding:9px 14px;background:white;color:var(--ink)}button:hover{background:#edf6f3}button:focus-visible,a:focus-visible{outline:3px solid #e6a568;outline-offset:3px}button:disabled{opacity:.4;cursor:default}.app{display:grid;grid-template-columns:250px minmax(0,1fr);max-width:1480px;margin:auto;min-height:100vh}aside{background:var(--ink);color:white;padding:26px 18px;position:sticky;top:0;height:100vh;overflow:auto}aside .brand{font-size:23px;font-weight:700;line-height:1.2;margin-bottom:8px}aside p{color:#bbcdd2;font-size:13px}nav{display:grid;gap:5px;margin:25px 0}nav button{text-align:left;border:0;background:transparent;color:#c8d8dc;font-size:13px;padding:9px}nav button.active{background:#285268;color:white}nav button.done:before{content:'✓ ';color:#85dfb9}.download{display:block;background:#e4f3ee;border-radius:9px;padding:10px;text-decoration:none;font-size:13px;font-weight:700;text-align:center}main{padding:30px 48px;min-width:0}.topbar{display:flex;gap:20px;align-items:center;justify-content:space-between;margin-bottom:22px;font-size:13px;color:var(--muted)}progress{width:150px;accent-color:var(--teal)}article{background:var(--paper);padding:38px 44px;border:1px solid var(--line);border-radius:18px;max-width:1030px;box-shadow:0 7px 25px #15334b08}article[hidden]{display:none}.kicker{color:var(--teal);font-size:12px;letter-spacing:1.2px;font-weight:800}h1{font-size:34px;line-height:1.18;margin:10px 0 18px;letter-spacing:-.8px}h2{font-size:20px;margin:22px 0 12px}.intro{font-size:18px;line-height:1.55;margin-bottom:23px;color:#3c5262}ol{padding-left:26px}li{padding-left:5px;margin-bottom:14px}svg{display:block;width:100%;height:auto;margin:18px 0;background:#f8fbf9;border-radius:12px}table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}th{background:#eaf3ef}td:first-child{font-family:Consolas,monospace;font-size:13px}.codewrap{position:relative;margin:22px 0}.codehead{display:flex;justify-content:space-between;background:#e7eeef;padding:8px 12px;border-radius:9px 9px 0 0;font:13px Consolas,monospace;align-items:center}.copy{font:12px 'Segoe UI',sans-serif;padding:4px 10px}pre{background:#17334b;color:#e4f2f4;padding:19px;margin:0;border-radius:0 0 9px 9px;overflow:auto;font:13px/1.5 Consolas,monospace;tab-size:4;white-space:pre}figure{margin:25px 0}figure img{width:100%;max-height:430px;object-fit:contain;object-position:left;background:white;border:1px solid var(--line);border-radius:9px}figcaption{font-size:12px;color:var(--muted);margin-top:8px}.terms{padding:12px 16px;background:#f4f0e9;border-radius:10px;font-size:14px}.terms p{margin:8px 0}.checkpoint{display:flex;gap:12px;align-items:flex-start;padding:18px;border:1px solid #b9dcd0;background:#edf8f1;border-radius:11px;font-size:15px;font-weight:600;margin-top:25px}.checkpoint input{width:20px;height:20px;flex:none;accent-color:var(--teal)}details{border:1px solid var(--line);border-radius:9px;margin:13px 0;padding:12px 15px}summary{cursor:pointer;font-weight:600}.answer{color:#405c65;margin:12px 0 0}.links{display:flex;gap:9px;flex-wrap:wrap;margin:22px 0}.links a{font-size:13px;border-bottom:1px solid #9dcbbb;text-decoration:none}.footnav{display:flex;justify-content:space-between;gap:15px;max-width:1030px;margin:22px 0}.primary{background:var(--teal);color:white;border-color:var(--teal)}.primary:hover{background:#0d685e}.lab{background:#eaf4f0;border-radius:14px;padding:20px;margin:20px 0}.lab .bits{display:flex;gap:8px;margin:18px 0}.bit{flex:1;text-align:center;background:var(--ink);color:white;border-radius:8px;padding:12px 0;font:26px Consolas,monospace}.bit small{display:block;font:10px 'Segoe UI',sans-serif;color:#b6d1d2}.labcontrols{display:flex;gap:15px;align-items:center;flex-wrap:wrap}.labcontrols label{font-size:14px}.lab input{accent-color:var(--teal)}#labnote{font-size:13px;margin:15px 0 0}#history{font:13px/1.6 Consolas,monospace;max-height:150px;overflow:auto;margin:10px 0 0}.nojs{background:#ffeddd;padding:20px}footer{font-size:12px;color:var(--muted);margin-top:20px}@media(max-width:900px){.app{grid-template-columns:1fr}aside{position:relative;height:auto;padding:15px 20px}aside .brand{font-size:21px}aside p{margin:5px 0}nav{display:flex;overflow:auto;margin:12px 0}nav button{white-space:nowrap;flex:none}main{padding:20px}article{padding:24px}h1{font-size:28px}.topbar{gap:8px}.download{display:inline-block}figure img{max-height:360px}table{font-size:12px}th,td{padding:8px 5px}}@media print{aside,.topbar,.footnav,.lab,button,.checkpoint input{display:none!important}.app,main{display:block;margin:0;padding:0}article,article[hidden]{display:block!important;page-break-after:always;border:0;box-shadow:none;padding:0;border-radius:0}details .answer{display:block}details{break-inside:avoid}h1{font-size:26px}pre{font-size:10px;white-space:pre-wrap}footer{display:none}}
'''
CSS+='\n.diagramhint{display:none}.diagram{overflow:auto}@media(max-width:600px){.diagram svg{min-width:600px}.diagramhint{display:block;font-size:12px;color:#566779;margin:12px 0 0}}\n'

JS=r'''
const pages=[...document.querySelectorAll('article')], navs=[...document.querySelectorAll('nav button')];let index=0;const key='tt-shift-guide-v1';let state={};try{state=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}function save(){try{localStorage.setItem(key,JSON.stringify(state))}catch(e){}}
function refresh(){let count=0;document.querySelectorAll('.checkpoint input').forEach((x,i)=>{x.checked=!!state[pages[i].id];navs[i].classList.toggle('done',x.checked);if(x.checked)count++});document.querySelector('progress').value=count;document.getElementById('progresslabel').textContent=count+' / '+pages.length+' checked'}
function go(n){index=Math.max(0,Math.min(pages.length-1,n));pages.forEach((p,i)=>p.hidden=i!==index);navs.forEach((b,i)=>{b.classList.toggle('active',i===index);b.setAttribute('aria-current',i===index?'step':'false')});document.getElementById('pagecount').textContent='Page '+(index+1)+' of '+pages.length;document.getElementById('prev').disabled=index===0;document.getElementById('next').disabled=index===pages.length-1;history.replaceState(null,'','#'+pages[index].id);window.scrollTo(0,0);pages[index].querySelector('h1').focus({preventScroll:true})}
navs.forEach((b,i)=>b.addEventListener('click',()=>go(i)));document.querySelectorAll('.checkpoint input').forEach((x,i)=>x.addEventListener('change',()=>{state[pages[i].id]=x.checked;save();refresh()}));document.getElementById('prev').onclick=()=>go(index-1);document.getElementById('next').onclick=()=>go(index+1);document.getElementById('clearchecks').onclick=()=>{state={};save();refresh()};
document.querySelectorAll('.copy').forEach(b=>b.onclick=async()=>{const t=b.closest('.codewrap').querySelector('pre').textContent;try{await navigator.clipboard.writeText(t);b.textContent='Copied'}catch(e){const area=document.createElement('textarea');area.value=t;document.body.append(area);area.select();document.execCommand('copy');area.remove();b.textContent='Copied'}setTimeout(()=>b.textContent='Copy code',1800)});
let q=0,edges=0;function renderLab(){document.querySelectorAll('.bit').forEach((el,i)=>el.firstChild.textContent=String((q>>(7-i))&1));document.getElementById('labnote').textContent='Output q[7:0] = '+q.toString(2).padStart(8,'0')+' (decimal '+q+'). '+edges+' rising edges applied.'}document.getElementById('clock').onclick=()=>{const bit=+document.getElementById('serial').checked,en=document.getElementById('enable').checked,reset=document.getElementById('resetpin').checked;const old=q;q=reset?0:en?((q<<1)|bit)&255:q;edges++;const row=document.createElement('div');row.textContent='Edge '+edges+': '+(reset?'reset':en?'shift '+bit:'hold')+' → '+q.toString(2).padStart(8,'0');document.getElementById('history').prepend(row);renderLab()};document.getElementById('restartlab').onclick=()=>{q=0;edges=0;document.getElementById('history').replaceChildren();renderLab()};renderLab();refresh();const initial=pages.findIndex(p=>p.id===location.hash.slice(1));go(initial<0?0:initial);
'''

def main():
    sync_starter()
    d=json.loads((ROOT/'lesson.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(ROOT/'shift-register-starter.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((ROOT/'starter').rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(ROOT/'starter').as_posix())
    sections=[]
    for i,p in enumerate(d['pages']):
        content=f'<article id="{p["id"]}"><div class="kicker">{esc(p.get("kicker",""))}</div><h1 tabindex="-1">{esc(p["title"])}</h1><p class="intro">{esc(p["intro"])}</p>'
        if p.get('diagram'): content+=diagram(p['diagram'])
        content+='<ol>'+''.join('<li>'+esc(x)+'</li>' for x in p.get('actions',[]))+'</ol>'
        if p['id']=='design':
            bits=''.join(f'<div class="bit">0<small>q[{7-j}]</small></div>' for j in range(8))
            content+='<section class="lab" aria-label="Shift register experiment"><h2>Try it: one click = one rising clock edge</h2><div class="bits">'+bits+'</div><div class="labcontrols"><label><input id="serial" type="checkbox"> Serial input = 1</label><label><input id="enable" type="checkbox" checked> Enable shifting</label><label><input id="resetpin" type="checkbox"> Reset requested (rst_n = 0)</label><button id="clock" class="primary">Apply rising edge</button><button id="restartlab">Start over</button></div><p id="labnote" aria-live="polite"></p><div id="history"></div></section>'
        if p.get('table'):
            t=p['table'];content+='<table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in t['rows'])+'</tbody></table>'
        if p.get('code'):
            c=p['code'];text=c.get('text','')
            if c.get('from_file'): text=(ROOT/c['from_file']).read_text(encoding='utf-8')
            content+='<div class="codewrap"><div class="codehead"><span>'+esc(c['file'])+'</span><button class="copy">Copy code</button></div><pre><code>'+esc(text)+'</code></pre></div>'
        if p.get('image'):
            im=p['image'];f=ROOT/im['src'];ext='jpeg' if f.suffix=='.jpg' else 'png'
            content+=f'<figure><img src="data:image/{ext};base64,{base64.b64encode(f.read_bytes()).decode()}" alt="{esc(im["caption"])}"><figcaption>{esc(im["caption"])}</figcaption></figure>'
        if p.get('terms'): content+='<div class="terms">'+''.join('<p><strong>'+esc(t['word'])+'</strong> — '+esc(t['meaning'])+'</p>' for t in p['terms'])+'</div>'
        if p.get('predict'): content+='<details><summary>Predict first: '+esc(p['predict']['question'])+'</summary><p class="answer">'+esc(p['predict']['answer'])+'</p></details>'
        for h in p.get('help',[]): content+='<details><summary>'+esc(h['problem'])+'</summary><p class="answer">'+esc(h['fix'])+'</p></details>'
        if p.get('links'): content+='<div class="links">'+''.join(f'<a href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])} ↗</a>' for l in p['links'])+'</div>'
        content+='<label class="checkpoint"><input type="checkbox"><span>Check before continuing: '+esc(p['checkpoint'])+'</span></label></article>'
        sections.append(content)
    nav=''.join(f'<button type="button">{i+1:02d} · {esc(p["title"].split(". ",1)[-1])}</button>' for i,p in enumerate(d['pages']))
    zipped=base64.b64encode((ROOT/'shift-register-starter.zip').read_bytes()).decode()
    output='<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(d['title'])+'</title><style>'+CSS+'</style></head><body><noscript><div class="nojs">Enable JavaScript for the step navigation and experiment. All lesson text remains available below.</div></noscript><div class="app"><aside><div class="brand">Your Verilog<br>to Tiny Tapeout</div><p>Short practical guide · Shift register<br>11 October 2026</p><nav aria-label="Lesson pages">'+nav+f'</nav><a class="download" href="data:application/zip;base64,{zipped}" download="shift-register-starter.zip">↓ Download the seven files</a><p>Checkpoints stay in this browser.<br><button id="clearchecks">Clear checkpoints</button></p></aside><main><div class="topbar"><span id="pagecount"></span><span><span id="progresslabel"></span> <progress max="{len(d["pages"])}" value="0" aria-label="Completed checkpoints"></progress></span></div>'+''.join(sections)+'<div class="footnav"><button id="prev">← Previous</button><button id="next" class="primary">Next step →</button></div><footer>Fresh lesson written for an existing Verilog design. Diagram/clock experiment is a learning model; verification details are in verification/report.md. Genuine screenshot sources: sources.json. Open the supplied PDF or Word document for printing.</footer></main></div><script>'+JS+'</script></body></html>'
    output=output.replace('verification/report.md','verification/README.md').replace('11 October 2026',d['date'])
    (ROOT/'START-HERE.html').write_text(output,encoding='utf-8')
    print(f'Built offline interactive guide: {len(sections)} steps; starter ZIP contains seven adaptation files.')

if __name__=='__main__': main()
