"""Actual Google Chrome QA: file:// (Mac viewing path) and HTTP, all 79 pages."""
from pathlib import Path
import json, shutil, traceback, time, platform, threading, http.server, functools
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/component_atlas_v001';QA=OUT/'qa'
QA.mkdir(exist_ok=True);(QA/'screenshots').mkdir(exist_ok=True)
D=json.loads((OUT/'atlas_data.json').read_text());RESULT={'status':'RUNNING','engine':'Google Chrome','scope':79,'pages':[],'errors':[]}
KEYS=['F003','F004','F005','F006','F008','F010','F011','F012','F016','F017','F018','F019','F020','F021','F026','F027','F028','F029','F030','F031','F032','F035','F036','F053','F063','F069','F070','F071','F074','F075','F077','F079']
def ready(page):
    page.evaluate("""async()=>{document.querySelectorAll('img').forEach(im=>im.loading='eager');await document.fonts.ready;await Promise.all([...document.images].map(im=>im.decode().catch(()=>{})))}""")
    return page.evaluate("""()=>({broken:[...document.images].filter(im=>!im.complete||im.naturalWidth===0).map(im=>im.getAttribute('src')),overflow:document.documentElement.scrollWidth>innerWidth+1,images:document.images.length})""")
def main():
    exe=shutil.which('google-chrome') or shutil.which('google-chrome-stable')
    assert exe,'A real installed Google Chrome executable is required; do not substitute a deployment status.'
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'])
        RESULT['version']=browser.version;RESULT['executable']=exe;RESULT['platform']=platform.platform();RESULT['executed_at_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        ctx=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,locale='zh-CN');page=ctx.new_page();page.on('pageerror',lambda er:RESULT['errors'].append(str(er)))
        for c in D:
            url=(OUT/'pages'/f'{c["id"]}.html').as_uri();page.goto(url,wait_until='load');check=ready(page)
            assert not check['broken'],(c['id'],check)
            assert not check['overflow'],(c['id'],'desktop overflow')
            assert page.locator('h1').inner_text()==c['title'];assert page.locator('.comparison figure').count()==2
            # Search locator links and headers exist in the actual rendered DOM.
            assert page.locator('#location figure img').count()==1
            page.screenshot(path=str(QA/'screenshots'/f'{c["id"]}-desktop.jpg'),type='jpeg',quality=80)
            if c['id'] in KEYS:
                page.screenshot(path=str(QA/'screenshots'/f'{c["id"]}-full.jpg'),type='jpeg',quality=76,full_page=True)
            button=page.locator('.annotations');src=page.locator('.comparison img').first.get_attribute('src');button.click();ready(page);assert page.locator('.comparison img').first.get_attribute('src')!=src;button.click();ready(page)
            page.locator('.comparison img').first.click();assert page.locator('.lightbox').count()==1;page.keyboard.press('Escape');assert page.locator('.lightbox').count()==0
            RESULT['pages'].append(dict(id=c['id'],file_mode='PASS',desktop=check,annotations_toggle='PASS',lightbox_and_escape='PASS'))
        page.goto((OUT/'index.html').as_uri());assert not ready(page)['broken'];assert page.locator('.card').count()==79
        page.locator('#search').fill('华栱');assert page.locator('.card:visible').count()==2
        page.locator('#search').fill('');assert page.locator('.card:visible').count()==79
        page.locator('#system').select_option(label='主体木构');assert page.locator('.card:visible').count()>0
        page.locator('#system').select_option('');page.screenshot(path=str(QA/'index-desktop.jpg'),type='jpeg',quality=85)
        RESULT['index_search_and_system_filter']='PASS'
        page.set_viewport_size({'width':390,'height':844})
        for c in D:
            page.goto((OUT/'pages'/f'{c["id"]}.html').as_uri());check=ready(page);assert not check['broken'] and not check['overflow'],(c['id'],'mobile',check)
            RESULT['pages'][int(c['id'][1:])-1]['mobile']='PASS'
            if c['id'] in KEYS:page.screenshot(path=str(QA/'screenshots'/f'{c["id"]}-mobile.jpg'),type='jpeg',quality=75)
        page.goto((OUT/'index.html').as_uri());check=ready(page);assert not check['overflow'];page.screenshot(path=str(QA/'index-mobile.jpg'),type='jpeg',quality=80)
        # Also check standard local HTTP delivery in the runner. file mode is the
        # exact no-server viewing method handed to the user, not an assumption.
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(OUT))
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);threading.Thread(target=server.serve_forever,daemon=True).start()
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html');check=ready(page);assert not check['broken'];RESULT['http_index']='PASS';server.shutdown();browser.close()
    assert not RESULT['errors'],RESULT['errors']
    # Contact sheets are actual Chrome screenshots, not a DOM approximation.
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
    for start in range(1,80,8):
        sheet=Image.new('RGB',(1440,2040),'#ddd');dr=ImageDraw.Draw(sheet)
        for k,n in enumerate(range(start,min(start+8,80))):
            im=Image.open(QA/'screenshots'/f'F{n:03d}-desktop.jpg');im.thumbnail((700,480));x=k%2*720;y=k//2*510;sheet.paste(im,(x,y+24));dr.text((x+8,y+2),f'F{n:03d}',font=font,fill='black')
        sheet.save(QA/f'contact-{start:03d}.jpg',quality=86)
    RESULT['status']='PASS';RESULT['tested_viewports']=[[1440,1000],[390,844]];RESULT['local_view_method']='file://docs/component_atlas_v001/index.html';RESULT['limitations']='Linux Google Chrome verified. User macOS Chrome version/session not directly controlled. This does not verify chatgpt.site access or the historical truth of inferred identities.'
def finish():
    (QA/'CHROME_VALIDATION.json').write_text(json.dumps(RESULT,ensure_ascii=False,indent=2))
    html='<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="../v002.css"><main><p><a href="../index.html">← 返回图库</a></p><h1>实际 Chrome 浏览验证</h1><p>状态：'+RESULT['status']+' · '+RESULT.get('version','')+'</p><p>79页分别以本地文件入口打开；桌面1440×1000、移动390×844检查图片、溢出、标注切换与放大。截图来自实际Chrome。</p><p><a href="CHROME_VALIDATION.json">逐页结果与验证限制</a> · <a href="../assets/v002/STATIC_VALIDATION.json">静态和模型身份核对</a></p><div class="qa-grid">'
    for start in range(1,80,8):html+=f'<a href="contact-{start:03d}.jpg"><img src="contact-{start:03d}.jpg" alt="F{start:03d}起的实际浏览截图">F{start:03d}–F{min(start+7,79):03d}</a>'
    html+='</div><h2>重点页完整截图</h2><div class="qa-grid">'
    for k in KEYS:html+=f'<a href="screenshots/{k}-full.jpg">{k} 完整页截图</a>'
    html+='</div><p>本测试验证页面可浏览，不代替原物形态的专业独立复核。在线站点的用户访问状态未由此证明。</p></main></html>'
    (QA/'index.html').write_text(html)
if __name__=='__main__':
    try:main()
    except Exception as ex:RESULT['status']='FAIL';RESULT['errors'].append(traceback.format_exc());finish();raise
    finish();print(json.dumps({k:v for k,v in RESULT.items() if k!='pages'},ensure_ascii=False))
