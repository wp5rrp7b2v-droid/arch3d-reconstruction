"""Meaningful offline checks: resources, variants, counts, provenance and scope."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, hashlib, subprocess
import xml.etree.ElementTree as ET
from PIL import Image

OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for k in ['href','src','data-src']:
   if a.get(k):self.links.append(a[k])
  if tag=='img' and a.get('src'):self.images.append(a['src'])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 data=json.loads((OUT/'data.json').read_text());prov=json.loads((OUT/'assets/PROVENANCE.json').read_text())
 assert len(data)==16 and len({r['category'] for r in data})==12
 assert len({r['id'] for r in data})==16
 checked=0;images=set();htmlfiles=[p for p in OUT.rglob('*.html') if not p.is_relative_to(OUT/'assets')]
 for p in htmlfiles:
  q=Links();q.feed(p.read_text())
  for v in q.links:
   u=urlsplit(v)
   if u.scheme or u.netloc or not u.path:continue
   target=(p.parent/unquote(u.path)).resolve();assert target.is_relative_to(OUT),('outside gallery',p,v)
   assert target.exists(),('BROKEN_LOCAL_LINK',str(p),v);checked+=1
  images.update((p.parent/unquote(v)).resolve() for v in q.images if not urlsplit(v).scheme)
 for im in images:
  if im.suffix=='.svg':
   root=ET.parse(im).getroot();assert root.tag.endswith('svg') and root.attrib.get('viewBox')
   assert not root.findall('.//{http://www.w3.org/2000/svg}script')
  else:
   with Image.open(im) as img:img.verify()
 all_asset_images=[p for p in (OUT/'assets').rglob('*') if p.suffix.lower() in ['.jpg','.png','.webp']]
 for im in all_asset_images:
  with Image.open(im) as img:img.verify()
 for r in data:
  assert len(r['form'])>12 and len(r['difference'])>12 and r['bcite'] and r['analog']
  assert sha(OUT/r['c_original'])==r['model_provenance']['sha256'],('MODEL_RENDER_CHANGED',r['id'])
  assert len(r['registry_items'])>0
 # Each necessary variant has independent reference and model pixels.
 for pair in [('F006','F007'),('F008','F009'),('F028','F029'),('F035','F036')]:
  rr=[next(r for r in data if r['id']==k) for k in pair]
  for key in ['b','c']:assert sha(OUT/rr[0][key])!=sha(OUT/rr[1][key]),('REUSED_VARIANT_IMAGE',pair,key)
 for d in prov['derivatives']:assert sha(OUT/d['file'])==d['sha256'],d['file']
 for source,meta in prov['pr72_exact_assets'].items():
  p=OUT/'assets/original'/Path(source).name
  assert sha(p)==meta['sha256']
  b=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==meta['git_blob_sha']
 # Registry count flags are display semantics, not automatic physical totals.
 rows={r['id']:r for r in data}
 assert rows['F008']['count']=='未知' and rows['F009']['count']=='未知'
 assert all('子集' in rows[i]['count_kind'] for i in ['F028','F029'])
 assert '推导' in rows['F021']['count_kind']
 allowed=('.github/workflows/wanfo_component_form_sources.yml','.github/workflows/wanfo_component_form_qa.yml')
 diff=subprocess.check_output(['git','diff','--name-only','-z',prov['main_baseline'],'HEAD'],cwd=ROOT).decode('utf-8').strip('\0').split('\0')
 bad=[p for p in diff if not p.startswith('docs/component_form_reference_v001/') and p not in allowed]
 assert not bad,('PROTECTED_PATH_CHANGED',bad)
 result=dict(status='PASS',scope='16 views / 12 categories; static QA only',html_pages=len(htmlfiles),local_references_checked=checked,distinct_page_images_decoded=len(images),all_asset_images_decoded=len(all_asset_images),source_images_exact=len(prov['pr72_exact_assets']),derived_images_checked=len(prov['derivatives']),variant_images='FOUR_PAIRS_DISTINCT_B_AND_C',quantity_semantics='PASS',master_render_identity='PASS',protected_paths='PASS_NO_PROTECTED_PATH_CHANGED',changed_paths=diff,limitations='Static checks do not verify historical form or replace actual Google Chrome visual review.')
 (OUT/'qa/STATIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='changed_paths'},ensure_ascii=False))
if __name__=='__main__':main()
