"""Actual installed Google Chrome, every HTML page via file:// and HTTP.

Failure reports link only screenshots already produced, so a partial run does
not create broken links that prevent the next full validation run.
"""
from pathlib import Path
import json, shutil, time, traceback, platform, http.server, functools, threading
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parents[1];QA=OUT/'qa';QA.mkdir(exist_ok=True)
RESULT={'status':'RUNNING','engine':'Google Chrome','pages':[],'errors':[]}
def ready(p):
 p.evaluate("""async()=>{await document.fonts.ready;await Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(i=>i.decode().catch(()=>{})))}""")
 return p.evaluate("""()=>({broken:[...document.images].filter(i=>i.getAttribute('src')&&(!i.complete||!i.naturalWidth)).map(i=>i.getAttribute('src')),horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1,images:[...document.images].filter(i=>i.getAttribute('src')).length})""")
def main():
 exe=shutil.which('google-chrome') or shutil.which('google-chrome-stable');assert exe,'Actual Google Chrome is required'
 ids=[r['id'] for r in json.loads((OUT/'data.json').read_text())]
 (QA/'screenshots').mkdir(exist_ok=True)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'])
  RESULT.update(version=browser.version,executable=exe,platform=platform.platform(),tested_at_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
  ctx=browser.new_context(viewport={'width':1440,'height':1100},locale='zh-CN',device_scale_factor=1);p=ctx.new_page();p.on('pageerror',lambda error:RESULT['errors'].append(str(error)))
  pages=[OUT/'index.html',OUT/'sources.html']+[OUT/'pages'/f'{i}.html' for i in ids]
  for file in pages:
   p.goto(file.as_uri());d=ready(p);assert not d['broken'] and not d['horizontalOverflow'],(file.name,d)
   if file.parent.name=='pages':
    assert p.locator('.triad figure').count()==3
    for j in range(3):
     assert p.locator('.triad .zoom').nth(j).bounding_box()['height']>=250
     p.locator('.triad .zoom').nth(j).click();assert p.locator('#viewer').evaluate('(d)=>d.open');ready(p)
     assert p.locator('#viewer-image').evaluate('(i)=>i.complete&&i.naturalWidth>0')
     p.locator('#zoom-in').click();assert p.locator('.viewer-scroll').evaluate('(d)=>d.classList.contains("zoomed")')
     p.locator('#zoom-reset').click();p.keyboard.press('Escape');assert not p.locator('#viewer').evaluate('(d)=>d.open')
    for j in range(p.locator('details').count()):p.locator('details').nth(j).evaluate('(d)=>d.open=true')
    d2=ready(p);assert not d2['broken'],(file.name,'detail images',d2)
    for j in range(p.locator('details').count()):p.locator('details').nth(j).evaluate('(d)=>d.open=false')
   p.screenshot(path=str(QA/'screenshots'/f'{file.stem}-desktop.jpg'),type='jpeg',quality=82,full_page=True)
   p.screenshot(path=str(QA/'screenshots'/f'{file.stem}-first-screen.jpg'),type='jpeg',quality=87)
   RESULT['pages'].append(dict(file=str(file.relative_to(OUT)),desktop=d,file_scheme='PASS',lightbox='PASS' if file.parent.name=='pages' else 'N/A'))
  p.goto((OUT/'index.html').as_uri());ready(p);assert p.locator('.gallery tbody tr').count()==16
  assert p.locator('thead th').all_text_contents()==['家族','构件','位置','个数','应有形制','当前模型']
  p.locator('#search').fill('华栱');assert p.locator('.gallery tbody tr:visible').count()==3
  assert p.locator('.gallery tbody tr:visible .name').all_text_contents()==['华栱 · 一跳 ↗','华栱 · 二跳 ↗','令栱 ↗']
  p.locator('#search').fill('');p.locator('#group').select_option('斗栱');assert p.locator('.gallery tbody tr:visible').count()==6
  p.locator('#group').select_option('gap');assert p.locator('.gallery tbody tr:visible').count()==3
  p.locator('#group').select_option('');RESULT['search_and_filters']='PASS'
  p.set_viewport_size({'width':390,'height':844})
  for i,file in enumerate(pages):
   p.goto(file.as_uri());d=ready(p);assert not d['broken'] and not d['horizontalOverflow'],(file.name,'mobile',d)
   p.screenshot(path=str(QA/'screenshots'/f'{file.stem}-mobile.jpg'),type='jpeg',quality=80,full_page=True)
   RESULT['pages'][i]['mobile']=d
  handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(OUT));server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);threading.Thread(target=server.serve_forever,daemon=True).start()
  for file in pages:
   p.goto(f'http://127.0.0.1:{server.server_port}/'+str(file.relative_to(OUT)));d=ready(p);assert not d['broken'];RESULT['pages'][pages.index(file)]['HTTP']='PASS'
  server.shutdown()
  # Inspectable, actual Chrome rasterization of the seven vector drawings.
  p.set_viewport_size({'width':1600,'height':1000})
  for fid in ['F003','F004','F005','F007','F008','F009','F030']:
   vector=OUT/'assets/v002'/f'{fid}-form.svg'
   if vector.exists():
    p.goto(vector.as_uri());p.evaluate('async()=>await document.fonts.ready')
    p.screenshot(path=str(QA/'screenshots'/f'{fid}-form.png'),full_page=True)
  browser.close()
 assert not RESULT['errors'],RESULT['errors']
 for start in range(0,len(ids),4):
  sheet=Image.new('RGB',(1800,1460),'#e5e5df');dr=ImageDraw.Draw(sheet)
  for j,fid in enumerate(ids[start:start+4]):
   im=Image.open(QA/'screenshots'/f'{fid}-first-screen.jpg');im.thumbnail((890,680));x=j%2*900;y=j//2*730;sheet.paste(im,(x,y+25));dr.text((x+8,y+6),fid,fill='black')
  sheet.save(QA/f'contact-{start//4+1}.jpg',quality=90)
 RESULT.update(status='PASS',viewports=[[1440,1100],[390,844]],limitations='Linux Google Chrome verified, all content pages and images. User macOS Chrome was not remotely operated. Passing browser checks does not establish historical authenticity.')
 # QA is itself a delivered HTML page; test it after its screenshots exist.
 finish()
 with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox','--allow-file-access-from-files'])
  pg=br.new_page(viewport={'width':1440,'height':1100})
  pg.goto((QA/'index.html').as_uri());d=ready(pg);assert not d['broken'] and not d['horizontalOverflow'],d
  pg.screenshot(path=str(QA/'screenshots/index-qa-desktop.jpg'),type='jpeg',quality=80,full_page=True)
  pg.set_viewport_size({'width':390,'height':844});pg.goto((QA/'index.html').as_uri());m=ready(pg);assert not m['broken'] and not m['horizontalOverflow'],m
  pg.screenshot(path=str(QA/'screenshots/index-qa-mobile.jpg'),type='jpeg',quality=80,full_page=True)
  RESULT['pages'].append(dict(file='qa/index.html',desktop=d,mobile=m,file_scheme='PASS',screenshot_stem='index-qa'))
  br.close()
def finish():
 (QA/'CHROME_VALIDATION.json').write_text(json.dumps(RESULT,ensure_ascii=False,indent=2))
 h='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="../style.css"><nav><a href="../index.html">← 返回图库</a><span>实际Chrome浏览验证</span></nav><main><header><h1>浏览器验证与截图</h1><p>状态：'+RESULT['status']+' · Google Chrome '+RESULT.get('version','')+'</p><p>全部内容页面分别以本地文件及HTTP打开；桌面与390px窄屏检查图片解码、布局、搜索筛选和放大。截图是真实Chrome输出。</p><p><a href="CHROME_VALIDATION.json">逐页机器结果</a> · <a href="STATIC_VALIDATION.json">来源／范围自动验证</a> · <a href="VISUAL_REVIEW.json">人工视觉检查范围与限制</a></p></header><div class="qa-grid">'
 for k in range(1,5):
  if (QA/f'contact-{k}.jpg').exists():h+=f'<a href="contact-{k}.jpg"><img src="contact-{k}.jpg" alt="第{k}组实际截图"><span>第{k}组：4个详情页首屏</span></a>'
 h+='</div><h2>逐页完整截图</h2><p>'
 for row in RESULT['pages']:
  stem=row.get('screenshot_stem',Path(row['file']).stem)
  if (QA/f'screenshots/{stem}-desktop.jpg').exists():h+=f'<a href="screenshots/{stem}-desktop.jpg">{stem} 桌面</a>　'
  if (QA/f'screenshots/{stem}-mobile.jpg').exists():h+=f'<a href="screenshots/{stem}-mobile.jpg">{stem} 窄屏</a>　'
 h+='</p></main></html>'; (QA/'index.html').write_text(h)
if __name__=='__main__':
 try:main()
 except Exception:RESULT['status']='FAIL';RESULT['errors'].append(traceback.format_exc());finish();raise
 finish();print(json.dumps({k:v for k,v in RESULT.items() if k!='pages'},ensure_ascii=False))
