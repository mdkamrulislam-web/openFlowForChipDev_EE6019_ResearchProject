"""Add an editable step-2 annotation around the unchanged official screenshot."""
from pathlib import Path
import base64
import sys

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'images/pages.png'
OUT=ROOT/'images/pages-numbered.svg'

def main():
    # Preserve the original screenshot pixels; put the missing annotation in
    # added margin, so it cannot be cropped out at the original image boundary.
    data=base64.b64encode(SOURCE.read_bytes()).decode('ascii')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1880" height="880" viewBox="0 0 1880 880">
<title>GitHub Pages setup: 1 Settings, 2 Pages, 3 GitHub Actions</title>
<rect width="1880" height="880" fill="white"/>
<image x="80" y="0" width="1800" height="810" href="data:image/png;base64,{data}"/>
<rect x="82" y="714" width="177" height="100" fill="none" stroke="#ff1717" stroke-width="4"/>
<text x="25" y="778" fill="#ff1717" font-family="Arial,sans-serif" font-size="56">2</text>
</svg>'''
    OUT.write_text(svg,encoding='utf-8')
    deps=Path('C:/Users/THINKPAD/repos/.codex-work/ee6019/beginner-guide/deps')
    if deps.exists():sys.path.insert(0,str(deps))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
        page=browser.new_page(viewport={'width':1880,'height':880},device_scale_factor=1)
        page.set_content('<html><body style="margin:0">'+svg+'</body></html>')
        page.locator('svg').screenshot(path=str(ROOT/'images/pages-numbered.png'))
        browser.close()
    print('Rendered numbered screenshot: original pixels retained, missing red 2 added in margin.')

if __name__=='__main__':main()
