"""Read-only primary-source retrieval. No model creation or modification."""
from pathlib import Path
import urllib.request, urllib.parse, hashlib, json, time
import fitz
from PIL import Image, ImageDraw

OUT=Path(__file__).resolve().parents[1]/'assets'/'research'
OUT.mkdir(parents=True, exist_ok=True)
sources=[
 ('DU1932','https://upload.wikimedia.org/wikipedia/commons/3/3a/NLC404-01J000317-23024_中國營造學社彙刊_1932年3卷2期.pdf','pdf'),
 ('WEN2017-19','https://www.archiposition.com/images/lecture/foguangsi_80/佛光寺_温静_19.jpg','jpg'),
 ('WEN2017-20','https://www.archiposition.com/images/lecture/foguangsi_80/佛光寺_温静_20.JPG','jpg'),
 ('WEN2017-29','https://www.archiposition.com/images/lecture/foguangsi_80/佛光寺_温静_29.JPG','jpg'),
 ('OFFICIAL','https://szbwgvue.chwhyun.cn/wanfodian/','html'),
]
log=[]
for ident,url,ext in sources:
 rec={'id':ident,'url':url,'retrieved_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 try:
  enc=urllib.parse.quote(url,safe=':/?=&%')
  req=urllib.request.Request(enc,headers={'User-Agent':'Mozilla/5.0 (compatible; research reference retrieval)'})
  b=urllib.request.urlopen(req,timeout=120).read()
  rec.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status='FETCHED')
  if ext=='pdf':
   d=fitz.open(stream=b,filetype='pdf'); rec['pages']=len(d)
   for start in range(0,len(d),12):
    sheet=Image.new('RGB',(1600,1500),'#eeeeee');dr=ImageDraw.Draw(sheet)
    for j,n in enumerate(range(start,min(start+12,len(d)))):
     pg=d[n].get_pixmap(matrix=fitz.Matrix(.7,.7));im=Image.frombytes('RGB',(pg.width,pg.height),pg.samples);im.thumbnail((390,460))
     x=j%4*400;y=j//4*500;sheet.paste(im,(x,y+24));dr.text((x+5,y+5),f'DU1932 PDF {n+1}',fill='black')
    sheet.save(OUT/f'DU1932-contact-{start+1:03}.jpg',quality=88)
   # Preserve only original selected figure pages, not an entire scanned volume.
   for n in [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]:
    pix=d[n-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5));pix.save(OUT/f'DU1932-p{n:03}.png')
  elif ext=='jpg':
   q=OUT/f'{ident}.jpg';q.write_bytes(b);im=Image.open(q);im.verify()
  else:
   text=b.decode('utf-8');(OUT/'OFFICIAL-current.html.txt').write_text(text)
 except Exception as ex:
  rec.update(status='FAILED',error=str(ex))
 log.append(rec);print(json.dumps(rec,ensure_ascii=False),flush=True)
(OUT/'FETCH_LOG.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
