"""Bounded augmentation of seven V001 pages. Nine pages stay byte-identical."""
from pathlib import Path
import subprocess,json,re,hashlib,html
from forms_v002 import FORMS,IDS,BASE,OUT,main as draw

ROOT=OUT.parents[1];E=html.escape
def old(path):return subprocess.check_output(['git','show',BASE+':'+str((OUT/path).relative_to(ROOT))],cwd=ROOT).decode()
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
CSS='''
.v002 .triad{grid-template-columns:24fr 48fr 28fr}.v002 .triad .zoom{height:390px}
.v002 .detail-head{padding-top:26px}.v002 .detail-head .lead{font-size:18px}
.v002 .key-note{font-size:13px;padding:12px 17px}.v002 .findings{padding-top:6px}
.v002 .comparison-notes{display:none}.v002 .evidence-v002{margin-top:24px}
.v002 .evidence-v002 h3{font-size:14px;color:#216651}.v002 .source-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px;margin-top:16px}
.v002 .source-cards img{width:100%;height:240px;object-fit:contain;background:#eee}
.v002 .source-cards figure{margin:0;background:white;padding:12px;border:1px solid #d9dfd7}.v002 .source-cards figcaption{font-size:12px}
.v002 .source-cards button{width:100%;height:240px;border:0;background:#eee}
.v002 .checkline{font-size:12px;color:#805c2d}.v002 .findings h2{font-size:14px}
@media(max-width:1050px){.v002 .triad{grid-template-columns:1fr 1.35fr}.v002 .triad .zoom{height:320px}}
@media(max-width:620px){.v002 .triad{grid-template-columns:1fr}.v002 .triad .zoom,.v002 .triad figure:last-child .zoom{height:290px}.v002 .triad .recommended .zoom{height:320px}.v002 .source-cards{grid-template-columns:1fr}}
'''
def main():
 draw()
 data=json.loads(old(Path('data.json')));byid={r['id']:r for r in data}
 baseline=dict(commit=BASE,target_ids=IDS,nine_pages={},models_and_counts={})
 keys=['c','c_original','master_id','model_identity','model_provenance','model_origin_url','local_models','registry_items','geometry','count','count_kind','position']
 for r in data:
  baseline['models_and_counts'][r['id']]=hashlib.sha256(json.dumps({k:r[k] for k in keys},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
  if r['id'] not in IDS:baseline['nine_pages'][r['id']]=sh(OUT/'pages'/(r['id']+'.html'))
 for fid,f in FORMS.items():
  r=byid[fid];r.update({k:f[k] for k in ['form','difference','keep','change','unknown']})
  r.update(b=f'assets/v002/{fid}-form.svg',b_original=f'assets/v002/{fid}-form.svg',bkind='工程候选',bcite=f['source']+' 图B为时代形制参考示意。',level='类型候选 · 细节待确认' if fid in ['F007','F008'] else '基本形制参考 · 候选',v002=dict(same_building=f['same'],analogy=f['analogous'],reuse=f['common'],source_refs=f['refs']))
  h=old(Path('pages')/(fid+'.html')).replace('<body>','<body class="v002">').replace('</head>',f'<style>{CSS}</style></head>')
  h=h.replace('构件形制参考 V001','构件形制参考 V002')
  if fid=='F008':
   h=h.replace('<header class="detail-head">','<header class="detail-head"><p class="checkline">本轮证据验收：FAIL｜下层完整可信单体仍不足；下图仅解释候选范围。</p>')
  h=re.sub(r'<p class="lead">.*?</p>',f'<p class="lead">{E(f["form"])}</p>',h,count=1)
  h=re.sub(r'<span class="badge[^\"]*">.*?</span>',f'<span class="badge">{E(r["level"])}</span>',h,count=1)
  b=f'''<figure class="recommended"><h2>图B｜建议采用的基本形制</h2><button class="zoom" data-src="../{r['b']}" data-caption="{E(r['bcite'])}" aria-label="放大{E(f['title'])}形制图"><img src="../{r['b']}" alt="{E(f['title'])}：单体轴测、侧面轮廓、关键端部；时代形制参考示意，非原物实测"></button><figcaption>时代形制参考示意 · 工程候选 · 未批准。<br>{E(f['source'])}</figcaption><a class="small" href="../{r['b']}">打开清晰矢量图 ↗</a></figure>'''
  h=re.sub(r'<figure class="recommended">.*?</figure>',lambda _:b,h,count=1,flags=re.S)
  h=re.sub(r'<div class="key-note[^\"]*">.*?</div>',lambda _:f'<div class="key-note"><strong>候选边界 · 图B／C未作尺寸或坐标配准</strong><p>{E(f["unknown"])}</p></div>',h,count=1,flags=re.S)
  findings='<section class="findings">'+''.join(f'<article><h2>{title}</h2><p>{E(f[key])}</p></article>' for title,key in [('当前模型缺少什么','difference'),('当前模型可保留什么','keep'),('推荐修改方向','change')])+'</section>'
  h=re.sub(r'<section class="findings">.*?</section>',lambda _:findings,h,count=1,flags=re.S)
  ev='<details class="evidence-v002"><summary>展开证据、时代类比与共用形制边界</summary>'
  ev+=f'<h3>本殿直接支持</h3><p>{E(f["same"])}</p><h3>时代类比支持什么</h3><p>{E(f["analogous"])}</p><h3>可共用什么、位置需另调什么</h3><p>{E(f["common"])}</p>'
  ev+='<p class="checkline">事实：来源可见特征及已登记测量。推断：照片中个体与构件名的对应。工作假设：图B完整候选轮廓、未量测的过渡。未知：隐藏榫卯及逐件几何。网页通过不等于历史复原正确。</p><div class="source-cards">'
  for p in f['refs']:
   label=('A1本殿原资料' if '/original/' in p else '时代类比原资料')+' · '+Path(p).stem
   ev+=f'<figure><button class="zoom" data-src="../{p}" data-caption="{E(label)}" aria-label="放大证据"><img src="../{p}" alt="{E(label)}"></button><figcaption>{E(label)} · <a href="../{p}">完整原图</a></figcaption></figure>'
  ev+='</div><p><a href="../assets/v002/DERIVATION.json">逐图派生记录</a> · <a href="../V002_EVIDENCE_ZH.md">7页判断与逐项依据</a> · <a href="../sources.html">原始来源入口</a></p></details>'
  h=h.replace('<div class="page-nav">',ev+'<div class="page-nav">')
  # Supporting V001 comparison remains intact in the file but folded into evidence.
  h=re.sub(r'(<section class="comparison-notes">.*?</section>)',r'<details><summary>V001已归档比较说明</summary>\1</details>',h,flags=re.S)
  h=h.replace('.v002 .comparison-notes{display:none}','.v002 .comparison-notes{padding-top:10px}')
  (OUT/'pages'/(fid+'.html')).write_text(h)
 # Update only seven table rows. Their six-column structure is preserved.
 h=old(Path('index.html')).replace('构件形制参考 V001','构件形制参考 V002')
 h=h.replace('12类关键构件，16个独立视图。','V002：7项单体形制补强，保留12类、16个独立视图。')
 def row(m):
  s=m.group(0);hit=re.search(r'href="pages/(F\d+)\.html"',s)
  if not hit or hit[1] not in FORMS:return s
  fid=hit[1];r=byid[fid];f=FORMS[fid]
  s=s.replace(f'assets/views/{fid}-B.webp',r['b'])
  s=re.sub(r'<span class="badge[^\"]*">.*?</span>',f'<span class="badge">{E(r["level"])}</span>',s,count=1)
  if fid=='F008':s=s.replace('类型候选 · 细节待确认','证据不足 · 本轮FAIL')
  s=re.sub(r'<p>.*?</p>',lambda _:f'<p>{E(f["form"])}</p>',s,count=1)
  pp=list(re.finditer(r'<p>.*?</p>',s))
  if len(pp)>1:s=s[:pp[1].start()]+f'<p>{E(f["difference"])}</p>'+s[pp[1].end():]
  return s
 h=re.sub(r'<tr data-group=.*?</tr>',row,h,flags=re.S)
 (OUT/'index.html').write_text(h)
 (OUT/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 (OUT/'assets/v002/BASELINE.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2))
 # Append a V002 explanation without changing any of the nine old pages.
 s=old(Path('sources.html'));extra='<article><h2>V002：7项单体形制提炼</h2><p>图B改为明确标识的工程候选示意，不是新实测或批准模型。采用范围、完整证据和未知部分见各页折叠区。</p><p><a href="V002_EVIDENCE_ZH.md">逐项依据与共用边界</a> · <a href="assets/v002/DERIVATION.json">图形派生记录</a></p></article>'
 s=s.replace('</main>',extra+'</main>');s=s.replace('完整可信单体仍不足；图B保留定位或局部可见形态，不提供臆造整件。','V001完整可信单体不足；V002另给有边界的类型候选，仍未证明本殿完整单件。')
 (OUT/'sources.html').write_text(s)
 for fid,digest in baseline['nine_pages'].items():assert sh(OUT/'pages'/(fid+'.html'))==digest
 print('Updated exactly seven detail pages; nine detail pages byte-identical.')

if __name__=='__main__':main()
