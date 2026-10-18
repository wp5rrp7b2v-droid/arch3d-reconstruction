"""Build a self-contained file:// reference gallery from verified archived images.

This script never writes a model, Registry or Project Control file. Image
operations are crops, resampling and locator marks; no hidden outline is filled.
"""
from pathlib import Path
import sys, json, hashlib, html, shutil, collections, re, os, subprocess
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops
from content import ROWS

OUT=Path(__file__).resolve().parents[1]
REPO=OUT.parents[1]
ATLAS=Path(os.environ.get('WANFO_ATLAS_INPUT','/workspace/scratch/4967bcf52682/arch3d-reconstruction/docs/component_atlas_v001'))
TREE=Path(os.environ.get('WANFO_ATLAS_TREE','/workspace/scratch/837958840904/research/pr72_tree.txt'))
BASE='414be293918fea2bf4138b1a8f4345272e8764a8'
ATLAS_SHA='54fac54578340918c78d65e973933b54090893a1'
GH='https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction'
e=html.escape
PROV=[];VERIFIED={};SOURCE_PAGES={}
for f in ['assets/original','assets/views','pages','qa']:(OUT/f).mkdir(parents=True,exist_ok=True)
atlas={c['id']:c for c in json.loads((ATLAS/'atlas_data.json').read_text())}
deriv=json.loads((ATLAS/'assets/v002/DERIVATION_PROVENANCE.json').read_text())
source_prov=json.loads((ATLAS/'assets/sources/SOURCE_IMAGE_PROVENANCE.json').read_text())
render_prov=json.loads((ATLAS/'assets/models/RENDER_PROVENANCE.json').read_text())
tree={}
for line in TREE.read_text().splitlines():
 meta,path=line.split('\t');tree[path]=meta.split()[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blobsha(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save_webp(im,target):
 stream=BytesIO();im.save(stream,format='WEBP',quality=91,method=6)
 raw=stream.getvalue();assert len(raw)>40,('EMPTY_WEBP_ENCODER',target)
 with Image.open(BytesIO(raw)) as check:check.verify()
 temp=target.with_suffix('.writing');temp.write_bytes(raw);temp.replace(target)
 assert target.stat().st_size==len(raw)
def original(spec):
 if spec.startswith('research:'):
  path=OUT/'assets/research'/spec.split(':',1)[1]
  assert path.exists(),path
  return path
 path=ATLAS/('assets/official/'+spec.split(':',1)[1] if spec.startswith('official:') else 'assets/sources/'+spec)
 return preserve(path)
def preserve(path):
 if not path.exists() and path.suffix=='.png':path=path.with_suffix('.webp')
 rel=str(path.relative_to(ATLAS));expected=tree['docs/component_atlas_v001/'+rel]
 target=OUT/'assets/original'/path.name
 local_match=blobsha(path)==expected
 if not local_match:
  # A stale scratch copy must never become the authoritative current image.
  raw=subprocess.check_output(['git','show',ATLAS_SHA+':docs/component_atlas_v001/'+rel],cwd=REPO)
  target.write_bytes(raw)
  assert blobsha(target)==expected,('REMOTE_ASSET_MISMATCH',rel)
 elif target.exists():assert sha(target)==sha(path)
 else:shutil.copyfile(path,target)
 VERIFIED[rel]=dict(git_blob_sha=expected,sha256=sha(target),source_commit=ATLAS_SHA,initial_scratch_match=local_match,stale_scratch_retrieved_from_exact_commit=not local_match)
 return target
def crop(path,name,box=None,marks=()):
 im=Image.open(path).convert('RGB');size=im.size
 bounds=(0,0,*size) if box is None else tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(box))
 im=im.crop(bounds);im.thumbnail((1400,1000),Image.Resampling.LANCZOS)
 if marks:
  d=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
  for x,y,num in marks:
   px=(x*size[0]-bounds[0])*im.width/(bounds[2]-bounds[0]);py=(y*size[1]-bounds[1])*im.height/(bounds[3]-bounds[1])
   assert 0<=px<im.width and 0<=py<im.height,(name,px,py)
   d.ellipse((px-18,py-18,px+18,py+18),fill='#166955',outline='white',width=3)
   d.text((px,py),num,anchor='mm',font=font,fill='white')
 target=OUT/'assets/views'/f'{name}.webp';save_webp(im,target)
 PROV.append(dict(file=str(target.relative_to(OUT)),source=str(path.relative_to(OUT)),source_sha256=sha(path),crop_normalized=box,marks=marks,operation='CROP_RESAMPLE_WITH_LOCATOR_NUMBERS' if marks else 'CROP_RESAMPLE_ONLY',sha256=sha(target),pixels=list(im.size)))
 return str(target.relative_to(OUT))
def model_crop(path,name,rotate=False):
 im=Image.open(path).convert('RGB')
 bg=Image.new('RGB',im.size,im.getpixel((0,0)));diff=ImageChops.difference(im,bg).convert('L').point(lambda x:255 if x>23 else 0)
 box=diff.getbbox()
 if box:box=(max(0,box[0]-30),max(0,box[1]-30),min(im.width,box[2]+30),min(im.height,box[3]+30))
 if box:im=im.crop(box)
 if rotate:im=im.transpose(Image.Transpose.ROTATE_90)
 im.thumbnail((1400,1000),Image.Resampling.LANCZOS);target=OUT/'assets/views'/f'{name}.webp';save_webp(im,target)
 PROV.append(dict(file=str(target.relative_to(OUT)),source=str(path.relative_to(OUT)),source_sha256=sha(path),operation='EXISTING_AXON_RENDER_CROP_RESAMPLE_ONLY',crop_pixels=box,display_rotation_deg=90 if rotate else 0,sha256=sha(target),pixels=list(im.size)))
 return str(target.relative_to(OUT))
def fig(src,title,caption,prefix='../',cls='',original_path=None):
 return f'<figure class="{cls}"><h2>{e(title)}</h2><button class="zoom" data-src="{prefix+src}" data-caption="{e(caption)}" aria-label="放大{e(title)}"><img src="{prefix+src}" alt="{e(caption)}"></button><figcaption>{e(caption)}</figcaption>'+(f'<a class="small" href="{prefix+original_path}">查看未经裁切的原图 ↗</a>' if original_path else '')+'</figure>'
def start(title,prefix=''):
 return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}｜万佛殿构件形制</title><link rel="stylesheet" href="{prefix}style.css"></head><body><nav><a class="brand" href="{prefix}index.html">万佛殿 <span>构件形制参考 V001</span></a><div><a href="{prefix}sources.html">依据与边界</a><a href="{prefix}qa/index.html">浏览验证</a></div></nav>'
def end(prefix=''):
 return f'<footer>形制研究与建模参考 · 建议尚未批准 · 已批准Master与局部设计保持各自原范围。</footer><dialog id="viewer"><div class="viewer-head"><p id="viewer-caption"></p><button id="close-viewer" aria-label="关闭放大">关闭 ×</button></div><div class="viewer-tools"><button id="zoom-in">＋ 放大</button><button id="zoom-out">－ 缩小</button><button id="zoom-reset">适合窗口</button><a id="open-original" target="_blank">新页打开原图 ↗</a></div><div class="viewer-scroll"><img id="viewer-image" alt="放大图"></div></dialog><script src="{prefix}app.js"></script></body></html>'

sources=[
 dict(id='A1',name='刘畅、廖慧农、李树盛《山西平遥镇国寺万佛殿与天王殿精细测绘报告》',date='现状测绘；本殿基准963年',url=GH+'/blob/'+BASE+'/docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md',role='本殿实证',scope='PDF81—85、87、90—91、106、292、294—295及相关既有统计与照片；PDF74—80比较图复核。不是全434页本轮精读。',boundary='照片、现状剖面、点云与报告理想推算分开；图2-28／29／31为佛光寺／保国寺／独乐寺类比，不能当本殿原物。',sha256='94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472'),
 dict(id='A2',name='刘畅、刘梦雨、王雪莹《平遥镇国寺万佛殿大木结构测量数据解读》',date='《中国建筑史论汇刊》第5辑',url='https://drive.google.com/file/d/1fBp2y7oKdpCcI0tGw78okehKoUf0SkR7/view',role='本殿实证／解释',scope='57页文件相关PDF28、36、39、41、44、46；单材／足材及交接图。',boundary='与A1同批测绘链，不算第二次独立复测。旧项目“A2”也曾指官方专题，本图库两者分列。',sha256='5c91a3ef7731aaf98d5bcd877376d34379b51a7f67790f248ac26b98567b9bee'),
 dict(id='A3',name='肖旻《镇国寺大殿尺度规律研究》',date='2024',url='https://drive.google.com/file/d/1Gj--z9SKeGkN88nZ5mFm8rE9YNHMw47_/view',role='本殿分析',scope='相关PDF7—11尺寸及解释，沿用16页文件。',boundary='主要数据来自A1；尺度解释与推算长度不是额外实测。',sha256='d5782b216a4c4b5ad2c88ab034aa4e271c9c964e31bcbe21e0a9bb13c47bd643'),
 dict(id='OFFICIAL',name='山西文物数字博物馆·万佛殿官方专题及已归档数字展示提取件',date='既有2026-10-14归档',url='https://szbwgvue.chwhyun.cn/wanfodian/',role='本殿展示参考',scope='本轮复核既有栌斗、一跳／二跳华栱、头昂／二昂独立提取图；沿用已登记四段动画代表帧核对结果。',boundary='匿名节点身份为推断；数字建模是否来自独立实测未知。本轮实时抓取因站点证书过期失败，未绕过证书；使用的是经GitHub精确核验的既有归档。'),
 dict(id='FG2022',name='张荣《中国五台山佛光寺东大殿建筑数字化勘察数据分析与唐代材分°营造法式研究》',date='报告末页2022-03-19；建筑857年',url='https://www.kaah.or.kr/download/mailing/kaah_seminar_presentation1_1.pdf',role='时代类比｜研究者原报告',scope='40页文件索引；重点PDF16—19、26—28、33—34、40。明／草栿区别、栌斗及双下昂、测绘与解释边界。',boundary='只能支持同类基本形态及异同判断；佛光寺栌斗截直造、无蜀柱脊部等特例不能套用本殿。旧获取文件前缀FG2021只是下载标识，实际报告日期按末页2022年。',sha256='26dc883207ce05d48c77018dd11825a33eca670ae60f02dbfbf9f6f4776e069b'),
 dict(id='DU1932',name='梁思成《蓟县独乐寺观音阁山门考》原载《中国营造学社汇刊》3卷2期',date='1932；建筑辽984年',url='https://upload.wikimedia.org/wikipedia/commons/3/3a/NLC404-01J000317-23024_中國營造學社彙刊_1932年3卷2期.pdf',role='时代类比｜原始调查',scope='203页整期索引；重点PDF10、45、49、52、54—56：山门梁枋、斗栱及脊部照片。没有声称全203页逐字精读。',boundary='山门及观音阁分别看；旧图实测也不证明每根都是984年原件，不迁移尺寸、曲线或槽深。',sha256='7ecfaeaa2014ce9ac568d100a568b7c0eda07515f2e25787f9432a79362a0314'),
 dict(id='WEN2017',name='温静《殿堂——解读佛光寺大殿的斗栱设计》讲座原文及图19、20',date='2017-07-11',url='https://www.archiposition.com/items/20180525111400',role='本殿实物照片／比较解释',scope='本轮核对令栱界面论述及图19／20；图29南北体系不同作为不照搬的参照。',boundary='图19／20拍摄的就是万佛殿，不能误标佛光寺照片；图19题记964与本项目963不同，仅记录此差异，不改项目年代基准。'),
 dict(id='HL964',name='福州市委党史方志室《全国重点文保｜华林寺大殿》',date='2023-05-17；吴越964年',url='https://fz.fjdsfzw.org.cn/wap/2023-05-17/content_125335.html',role='时代／地域比较｜官方',scope='核对年代、月梁及内外不等高构架等特征。',boundary='南方特殊构架，列为可比较但不整件移植的来源；未用其云形或圆截面替换本殿。'),
 dict(id='C1',name='李诫《营造法式》',date='北宋1103年刊行；本项目2006年版',url='https://drive.google.com/file/d/1wnQz5sdEMNTVeCFsMupVMrj93WNDLqeC/view',role='术语及制度参照',scope='沿用已登记卷四／五相关条目边界。',boundary='晚于万佛殿约140年，不能当作963年原始标准；本图库没有依其统一生产尺寸。'),
]

def make():
 enriched=[]
 # Preserve small supporting pages with the original page and provenance.
 for n in [50,51,60,62,81,82,83,85,87,90,106,292,294,295]:
  key=f'A1-p{n:03}.jpg'
  if (ATLAS/'assets/sources'/key).exists():original(key)
 for n in [28,39,41,44,46]:
  key=f'A2-p{n:03}.jpg'
  if (ATLAS/'assets/sources'/key).exists():original(key)
 for n in [7,8,9,10,11]:
  key=f'A3-p{n:03}.jpg'
  if (ATLAS/'assets/sources'/key).exists():original(key)
 for row in ROWS:
  c=atlas[row['id']];fid=row['id'];braw=original(row['bsource']);araw=original(row['araw'])
  a=crop(araw,fid+'-A',row['acrop'],row['marks']);b=crop(braw,fid+'-B',row['bcrop'])
  m=c['models'][0]
  if m.get('mode')=='BINARY_RENDER':
   craw=preserve(ATLAS/m['image']);ci=model_crop(craw,fid+'-C',fid=='F021')
   bm=dict(source=m['image'],sha256=sha(craw),render_label=m['label'],model_id=c['cid'],source_commit=ATLAS_SHA)
  else:
   craw=preserve(ATLAS/'assets/v002'/f'{fid}-model-clear.jpg');ci=crop(craw,fid+'-C')
   bm=next((x for x in deriv if x['file']==f'assets/v002/{fid}-model-clear.jpg'),None)
  model_id=c['cid'];identity='Master V001'
  if fid=='F006':identity+=' · EW_SEAM'
  if fid=='F007':identity+=' · GABLE（厚度参数补全）'
  if fid=='F008':identity+=' · LOWER_SUPPORT'
  if fid=='F009':identity+=' · UPPER_RIDGE_SUPPORT'
  if fid in ['F028','F029','F035','F036']:identity+=' · '+{'F028':'JUMP_1','F029':'JUMP_2','F035':'TOU_ANG','F036':'ER_ANG'}[fid]
  side=[]
  for j,lm in enumerate(c['local_models'][:2] if fid not in ['F007','F009'] else []):
   src=preserve(ATLAS/lm['image']);side.append(dict(image=crop(src,fid+f'-local{j+1}'),label=lm['label'],identity=lm['caption'],boundary=lm['boundary']))
  r={**row,'a':a,'b':b,'c':ci,'a_original':str(araw.relative_to(OUT)),'b_original':str(braw.relative_to(OUT)),'c_original':str(craw.relative_to(OUT)),'master_id':model_id,'model_identity':identity,'model_provenance':bm,'model_origin_url':m.get('source_url',GH+'/blob/'+ATLAS_SHA+'/docs/component_atlas_v001/'+m['image'].replace('.png','.webp')),'local_models':side,'registry_items':c['items'],'geometry':c['geometry']}
  enriched.append(r)
 # Main page: exactly the six requested information columns.
 h=start('构件形制参考图库')+'<header><div class="eyebrow">平遥镇国寺 · 万佛殿</div><h1>先看形，再看模型。</h1><p class="intro">12类关键构件，16个独立视图。原物证据、建议外观与现有模型放在一起比较。</p><div class="legend"><span>本殿实证</span><span>时代类比</span><span>工程建议 · 未批准</span><span class="gap">待确认</span></div><p class="scope-note">“应有形制”是有边界的本轮参考建议；没有证据的完整外形会明确留空。图像各自适配显示，不代表同尺度或配准比较。</p></header><main><section class="toolbar"><label>查找构件<input id="search" type="search" placeholder="输入名称、位置或形态"></label><label>显示范围<select id="group"><option value="">全部12类</option><option value="梁架">梁架</option><option value="斗栱">斗栱</option><option value="gap">完整形制待确认</option></select></label><span id="result-count" aria-live="polite">16个视图</span></section><div class="table-wrap"><table class="gallery"><colgroup><col class="col-family"><col class="col-name"><col class="col-place"><col class="col-count"><col class="col-form"><col class="col-model"></colgroup><thead><tr><th>家族</th><th>构件</th><th>位置</th><th>个数</th><th>应有形制</th><th>当前模型</th></tr></thead><tbody>'
 for r in enriched:
  group='斗栱' if r['category'] in ['柱头栌斗','华栱','令栱','昂'] else '梁架';gap='gap' if '待确认' in r['level'] else ''
  h+=f'<tr data-group="{group}" data-gap="{gap}"><td><span class="family">{group}</span><strong>{e(r["category"])}</strong></td><td><a class="name" href="pages/{r["id"]}.html">{e(r["name"])} <span>↗</span></a><span class="badge {gap}">{e(r["level"])}</span></td><td>{e(r["position"])}</td><td><strong class="count">{e(r["count"])}</strong><small>{e(r["count_kind"])}</small></td><td><button class="zoom thumb" data-src="{r["b"]}" data-caption="{e(r["bcite"])}" aria-label="放大{e(r["name"])}参考图"><img src="{r["b"]}" alt="{e(r["name"])}参考外观"></button><p>{e(r["form"])}</p></td><td><button class="zoom thumb model" data-src="{r["c"]}" data-caption="{e(r["model_identity"])}" aria-label="放大{e(r["name"])}模型图"><img src="{r["c"]}" alt="{e(r["name"])}现有模型"></button><p>{e(r["difference"])}</p></td></tr>'
 h+='</tbody></table></div><p class="small">数量只沿用已登记口径：家族记录、子集、图纸推导与实际件数分列；驼峰两角色共用一条家族记录，不能合计为两件。</p></main>'+end();(OUT/'index.html').write_text(h)
 for i,r in enumerate(enriched):
  gap='gap' if '待确认' in r['level'] else ''
  h=start(r['name'],'../')+f'<main class="detail"><div class="crumb"><a href="../index.html">← 返回六栏图库</a><span>{i+1:02} / 16</span></div><header class="detail-head"><div class="eyebrow">{e(r["category"])} · {e(r["position"])}</div><h1>{e(r["name"])}</h1><p class="lead">{e(r["form"])}</p><div class="detail-meta"><span class="badge {gap}">{e(r["level"])}</span><span>{e(r["count"])} · {e(r["count_kind"])}</span></div></header><div class="triad">'
  h+=fig(r['a'],'图A｜万佛殿自身证据','标记1为目标可见区域；“?”为角色或个体对应待确认，标记不等于完整轮廓。',original_path=r['a_original'])
  h+=fig(r['b'],'图B｜建议参考的基本形制',r['bcite'],cls='recommended',original_path=r['b_original'])
  h+=fig(r['c'],'图C｜当前3D模型',r['master_id']+' / '+r['model_identity'],cls='model-panel',original_path=r['c_original'])
  h+=f'</div><div class="key-note {gap}"><strong>{e(r["bkind"])} · 推荐边界</strong><p>{e(r["unknown"])}</p></div><section class="findings"><article><h2>当前差异</h2><p>{e(r["difference"])}</p></article><article><h2>建议保留</h2><p>{e(r["keep"])}</p></article><article><h2>建议修改／补查</h2><p>{e(r["change"])}</p></article></section><section class="comparison-notes"><h2>时代与出处</h2><p>{e(r["analog"])}</p><p class="small">唐末—五代—辽及宋初实例只约束形制类型；不把地域特例、模数或《营造法式》直接变成本殿963年标准。<a href="../sources.html">查看来源与采用范围 ↗</a></p>'
  if r['id'] in ['F006','F008','F009','F020','F021']:
   h+=fig('assets/views/DU1932-ridge.webp','辽代类比｜独乐寺山门脊部','DU1932 PDF56，图17：平梁、蜀柱及两侧斜材；不能替代万佛殿单件实测。',original_path='assets/research/DU1932-p056.png')
  elif r['id'] in ['F003','F004','F005']:
   h+=fig('assets/views/FG2022-beams.webp','晚唐类比｜明栿与草栿分别看','张荣报告PDF16：佛光寺东大殿857年梁架；不同加工方式，不整件照搬。',original_path='assets/research/FG2021-p016.png')
  elif r['id'] in ['F026','F028','F029','F035','F036']:
   h+=fig('assets/views/FG2022-bracket.webp','晚唐类比｜栌斗、华栱与双下昂','张荣报告PDF17：佛光寺东大殿；其中栌斗截直为该殿特征。',original_path='assets/research/FG2021-p017.png')
  elif r['id']=='F030':
   h+=fig('assets/research/WEN2017-20.jpg','本殿另一视角｜令栱所在界面','温静讲座图20：万佛殿；保留作者原标色。本图不是佛光寺。',original_path='assets/research/WEN2017-20.jpg')
  h+='</section>'
  if r['local_models']:
   h+='<details><summary>另看现有局部工作版本（身份独立，不升级批准）</summary><div class="locals">'
   for lm in r['local_models']:h+=fig(lm['image'],lm['identity']+' · 局部',lm['label']+'；'+lm['boundary'])
   h+='</div></details>'
  h+=f'<details><summary>位置、数量和模型回查</summary><p><a href="{e(r["model_origin_url"])}">GitHub原模型渲染 ↗</a> · <a href="{GH}/blob/{BASE}/{atlas[r["id"]]["semantic_paths"][0]}">Master语义定义 ↗</a> · <a href="../data.json">本页完整显示数据</a></p><p class="small">图C复用PR72已归档的现有模型渲染并核验Git blob与SHA-256；没有新建或改写几何。局部对象保持其原有批准／待审边界。</p><ul>'
  for it in r['registry_items']:h+='<li>'+e(it['id']+'｜'+it['location']+'｜'+it['count_status'])+'</li>'
  h+='</ul></details><div class="page-nav">'
  if i:h+=f'<a href="{enriched[i-1]["id"]}.html">← {e(enriched[i-1]["name"])}</a>'
  if i+1<len(enriched):h+=f'<a href="{enriched[i+1]["id"]}.html">{e(enriched[i+1]["name"])} →</a>'
  h+='</div></main>'+end('../');(OUT/'pages'/f'{r["id"]}.html').write_text(h)
 (OUT/'data.json').write_text(json.dumps(enriched,ensure_ascii=False,indent=2))
 (OUT/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
 (OUT/'assets/PROVENANCE.json').write_text(json.dumps(dict(main_baseline=BASE,atlas_commit=ATLAS_SHA,pr73_commit='c770088e04216588eb9bcae02fa16a2b54199697',pr72_exact_assets=VERIFIED,derivatives=PROV,original_page_records=[p for p in source_prov if p['file'] in [Path(x).name for x in VERIFIED]],original_model_render_records=[p for p in render_prov if p['id'] in {r['master_id'] for r in enriched}],interpretation='Crops and locator marks only. No synthesized hidden shapes, no model edits.'),ensure_ascii=False,indent=2))
 h=start('来源与采用边界')+'<main class="sources"><header><div class="eyebrow">按用途取证</div><h1>有出处，也有边界。</h1><p>本殿照片与测绘是优先依据；其他建筑用于检查时代兼容和形制差别。没有统一的唐五代“标准构件”可直接替换本殿所有变体。</p></header><div class="evidence-key"><p><strong>本殿实证</strong>：本殿原图直接可见。</p><p><strong>时代类比</strong>：其他建筑支持的形态特征。</p><p><strong>工程建议</strong>：综合证据提出，尚未获准。</p><p><strong>待确认</strong>：现有资料不足或对应仍是推断。</p></div>'
 for s in sources:h+=f'<article id="{s["id"]}"><h2>{e(s["id"])}｜{e(s["name"])}</h2><p class="small">{e(s["date"])} · {e(s["role"])}</p><p>{e(s["scope"])}</p><p class="boundary">{e(s["boundary"])}</p><a href="{e(s["url"])}">原始资料／正式登记入口 ↗</a></article>'
 h+='<article><h2>采用与不采用的决定</h2><ul><li>佛光寺857年：采用明／草栿区分和简单批竹式昂的类型比较；不移植其栌斗泥道截直特例。</li><li>独乐寺984年：采用山门脊部短柱、斜材与承托块的角色比较；不移植曲线和尺寸。</li><li>华林寺964年、保国寺1013年：地域与构架不同，用于检验“早期都应同形”的假设；未用其特殊月梁／云形做法补本殿缺口。保国寺图源已在A1图2-29复核，未重复收集。</li><li>本殿下六椽栿、上六椽栿、四椽栿：优先保留原照片能看出的差别，未将所有梁画成同一种月梁。</li><li>山面平梁与两种驼峰：完整可信单体仍不足；图B保留定位或局部可见形态，不提供臆造整件。</li></ul></article><p><a href="assets/PROVENANCE.json">逐图来源、裁切及模型核验记录</a> · <a href="assets/research/FETCH_LOG.json">新来源获取的实际结果</a> · <a href="qa/STATIC_VALIDATION.json">静态验证</a></p></main>'+end();(OUT/'sources.html').write_text(h)
 print(json.dumps(dict(pages=len(enriched),categories=len({r['category'] for r in enriched}),verified_source_assets=len(VERIFIED),derivative_images=len(PROV)),ensure_ascii=False))

if __name__=='__main__':
 # These crops keep the original primary drawings/photos, with no redrawing.
 crop(OUT/'assets/research/DU1932-p056.png','DU1932-ridge',[.49,.0,.99,.425])
 crop(OUT/'assets/research/FG2021-p016.png','FG2022-beams',[.31,.02,.99,.98])
 crop(OUT/'assets/research/FG2021-p017.png','FG2022-bracket',[.44,.0,.99,.71])
 make()
