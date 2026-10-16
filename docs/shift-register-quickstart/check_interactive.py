"""Check the offline guide's navigation, experiment, download and narrow layout."""
import io, json, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DEPS=Path('C:/Users/THINKPAD/repos/.codex-work/ee6019/beginner-guide/deps')
if DEPS.exists(): sys.path.insert(0,str(DEPS))
from playwright.sync_api import sync_playwright, expect
OUT=Path('C:/Users/THINKPAD/repos/.codex-work/ee6019/shift-register-review')
OUT.mkdir(parents=True,exist_ok=True)
report={'errors':[],'pages':[]}
count=len(json.loads((ROOT/'lesson.json').read_text(encoding='utf-8'))['pages'])
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
    ctx=b.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
    page=ctx.new_page()
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto((ROOT/'START-HERE.html').as_uri())
    nav=page.locator('nav button')
    assert nav.count()==count
    for i in range(count):
        nav.nth(i).click()
        active=page.locator('article:visible')
        assert active.count()==1
        assert page.locator('#pagecount').inner_text()==f'Page {i+1} of {count}'
        assert active.locator('h1').inner_text()
        width=page.evaluate('document.documentElement.scrollWidth')
        assert width<=1440
        active.locator('.checkpoint input').check()
        page.screenshot(path=str(OUT/f'interactive-{i+1:02d}.png'),full_page=True)
        report['pages'].append({'page':i+1,'desktop_width':width})
    assert page.locator('#progresslabel').inner_text()==f'{count} / {count} checked'
    page.reload()
    assert page.locator('#progresslabel').inner_text()==f'{count} / {count} checked'
    nav.nth(1).click()
    def value():return ''.join(page.locator('.bit').nth(i).evaluate('(e)=>e.firstChild.textContent') for i in range(8))
    for bit,expected in [(1,'00000001'),(0,'00000010'),(1,'00000101')]:
        page.locator('#serial').set_checked(bool(bit));page.locator('#clock').click();assert value()==expected
    page.locator('#enable').uncheck();page.locator('#clock').click();assert value()=='00000101'
    page.locator('#resetpin').check();page.locator('#clock').click();assert value()=='00000000'
    page.locator('#restartlab').click();assert '0 rising edges' in page.locator('#labnote').inner_text()
    report['experiment']='shift sequence, hold, synchronous reset and restart passed'
    prediction=page.locator('article:visible details').first
    prediction.locator('summary').click();assert prediction.locator('.answer').is_visible()
    page.locator('article:visible .copy').first.click();expect(page.locator('article:visible .copy').first).to_have_text('Copied')
    with page.expect_download() as pending:page.locator('.download').click()
    dl=pending.value;dl.save_as(str(OUT/'downloaded-starter.zip'))
    with zipfile.ZipFile(OUT/'downloaded-starter.zip') as z:
        expected=sorted(str(x.relative_to(ROOT/'starter')).replace('\\','/') for x in (ROOT/'starter').rglob('*') if x.is_file())
        assert sorted(z.namelist())==expected and len(expected)==7
        for name in expected:assert z.read(name)==(ROOT/'starter'/name).read_bytes()
    report['download']='seven exact paths and bytes passed'
    page.set_viewport_size({'width':390,'height':844})
    for i in range(count):
        nav.nth(i).click()
        width=page.evaluate('document.documentElement.scrollWidth');assert width<=390,(i,width)
        report['pages'][i]['mobile_width']=width
    nav.nth(1).click();page.screenshot(path=str(OUT/'interactive-mobile.png'),full_page=True)
    page.locator('#clearchecks').click();assert page.locator('#progresslabel').inner_text()==f'0 / {count} checked'
    assert not report['errors'],report['errors']
    b.close()
(OUT/'interactive-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'pages':count,'desktop_and_mobile':'passed','interactions':report['experiment'],'zip':report['download'],'javascript_errors':len(report['errors'])}))
