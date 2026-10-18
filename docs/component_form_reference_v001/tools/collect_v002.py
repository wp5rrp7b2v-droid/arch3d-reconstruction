"""Targeted read-only retrieval; original author photographs and repair report."""
from pathlib import Path
import urllib.request,urllib.parse,re,json,hashlib,time
import fitz
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[1]/'assets/research/v002';OUT.mkdir(parents=True,exist_ok=True)
log=[]
def get(key,url,ext):
 rec=dict(id=key,url=url,time_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
 try:
  req=urllib.request.Request(urllib.parse.quote(url,safe=':/?=&%'),headers={'User-Agent':'Mozilla/5.0'})
  b=urllib.request.urlopen(req,timeout=45).read();p=OUT/(key+'.'+ext);p.write_bytes(b)
  rec.update(status='FETCHED',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),file=str(p.name))
  return b
 except Exception as ex:rec.update(status='FAILED',error=str(ex));return None
 finally:log.append(rec)
html=get('DAYUN2011','https://blog.sina.com.cn/s/blog_4a877d4d0102e10e.html','html')
if html:
 s=html.decode('utf-8','replace');urls=[]
 for u in re.findall(r'(?:real_src|src)=["\']([^"\']+)',s):
  if ('sinaimg.cn' in u or 'sinajs.cn' in u) and ('mw690' in u or 'orignal' in u or 'bmiddle' in u or 'middle' in u):
   u=u.replace('&amp;','&');u=('https:'+u) if u.startswith('//') else u
   if u not in urls:urls.append(u)
 for i,u in enumerate(urls[:40]):
  b=get(f'DAYUN2011-{i+1:02}',u,'jpg')
  if b:
   try:Image.open(OUT/f'DAYUN2011-{i+1:02}.jpg').verify()
   except Exception as ex:log[-1]['image_error']=str(ex)
b=get('NC1980','https://www.3d-wonders.com/wp-content/uploads/2020/02/南禅寺大殿修复_祁英涛.pdf','pdf')
if b:
 try:
  d=fitz.open(stream=b,filetype='pdf');log[-1]['pages']=len(d)
  for n in range(len(d)):d[n].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(OUT/f'NC1980-p{n+1:02}.png')
  (OUT/'NC1980.pdf').unlink() # selected-page image archive; upstream remains retrievable
 except Exception as ex:log[-1]['pdf_error']=str(ex)
files=[p for p in OUT.glob('*.jpg') if 'DAYUN2011-' in p.name]+list(OUT.glob('NC1980-p*.png'))
for k in range(0,len(files),12):
 sheet=Image.new('RGB',(1600,1500),'#ddd');dr=ImageDraw.Draw(sheet)
 for j,f in enumerate(files[k:k+12]):
  try:
   im=Image.open(f).convert('RGB');im.thumbnail((390,460));x=j%4*400;y=j//4*500;sheet.paste(im,(x,y+25));dr.text((x+5,y+4),f.name,fill='black')
  except Exception:pass
 sheet.save(OUT/f'contact-{k//12+1}.jpg',quality=90)
(OUT/'FETCH_LOG.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
print(json.dumps(log,ensure_ascii=False))
