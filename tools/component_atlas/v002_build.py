"""Produce image-first revisions of the existing atlas, without touching models.

Only crops, image resampling, transparent locator boxes, and evidence-bound open
edge traces are made. No synthetic historical geometry is generated.
"""
from pathlib import Path
import json, hashlib, html, re, shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from v002_specs import S
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/component_atlas_v001'
DER=OUT/'assets/v002'; DER.mkdir(exist_ok=True,parents=True)
D=json.loads((OUT/'atlas_data.json').read_text())
PROV=json.loads((OUT/'assets/sources/SOURCE_IMAGE_PROVENANCE.json').read_text())
PM={x['file']:x for x in PROV}
REND=json.loads((OUT/'assets/models/RENDER_PROVENANCE.json').read_text())
REPO='https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction'
BASE='e4109b3b78c503880458c820b755313f6ef90dbe'
e=html.escape
FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
COL={'partial':'#a77727','different':'#b94435','unknown':'#70747b','similar':'#207b67'}
NAMES={'partial':'可见部分／部分表达','different':'可见差异／模型缺失','unknown':'尚无法判断','similar':'可见形态相近'}
DERIV=[]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def path_display(path):
    p=OUT/path
    if p.suffix=='.png' and p.with_suffix('.webp').exists():return p.with_suffix('.webp')
    return p
def rect_px(im,box):return tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(box))
def save_image(im,name,origin,operation,**meta):
    q=DER/name; im.convert('RGB').save(q,quality=93,subsampling=0)
    DERIV.append(dict(file=str(q.relative_to(OUT)),source=str(origin.relative_to(OUT)),source_sha256=sha(origin),operation=operation,sha256=sha(q),**meta))
    return str(q.relative_to(OUT))
def dot(draw,xy,num,color):
    x,y=xy;r=20
    draw.ellipse((x-r,y-r,x+r,y+r),fill=color,outline='white',width=3)
    draw.text((x,y-1),str(num),font=FONT,fill='white',anchor='mm')
def dashed(draw,box,fill,width=4):
    x0,y0,x1,y1=box
    for x in range(int(x0),int(x1),24):
        draw.line((x,y0,min(x+13,x1),y0),fill=fill,width=width)
        draw.line((x,y1,min(x+13,x1),y1),fill=fill,width=width)
    for y in range(int(y0),int(y1),24):
        draw.line((x0,y,x0,min(y+13,y1)),fill=fill,width=width)
        draw.line((x1,y,x1,min(y+13,y1)),fill=fill,width=width)
def source_images(c,s):
    raw=OUT/s['source']; im=Image.open(raw).convert('RGB');box=rect_px(im,s['crop'])
    assert box[2]>box[0] and box[3]>box[1]
    # The locator is the unchanged source page with an explicitly non-contour box.
    locator=im.copy();locator.thumbnail((1700,1700));ld=ImageDraw.Draw(locator)
    dashed(ld,rect_px(locator,s['crop']),'#d28b2b',max(3,locator.width//330))
    loc=save_image(locator,c['id']+'-locator.jpg',raw,'ORIGINAL_WITH_DASHED_SEARCH_REGION',crop=s['crop'],identity_inference=s['inferred'])
    crop=im.crop(box);scale=min(2.5,1300/max(crop.width,1),900/max(crop.height,1))
    crop=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.LANCZOS)
    base=crop.copy();dr=ImageDraw.Draw(crop)
    def tr(x,y):return ((x*im.width-box[0])*scale,(y*im.height-box[1])*scale)
    for points in s['traces']:
        pts=[tr(*v) for v in points];dr.line(pts,fill='#ffffff',width=7,joint='curve');dr.line(pts,fill='#00866f',width=4,joint='curve')
    for i,(x,y,label) in enumerate(s['parts'],1):
        px,py=tr(x,y)
        # Never put an annotation outside the clipped source image.
        px=max(23,min(crop.width-23,px));py=max(23,min(crop.height-23,py))
        dot(dr,(px,py),i,'#a77727' if s['inferred'] else '#207b67')
    clear=save_image(base,c['id']+'-source-clear.jpg',raw,'CROP_RESAMPLE_ONLY',crop=s['crop'])
    annotated=save_image(crop,c['id']+'-source.jpg',raw,'CROP_WITH_NUMBERED_VISIBLE_FEATURES_AND_OPEN_EDGE_TRACES',crop=s['crop'],traces=s['traces'],parts=s['parts'])
    return annotated,loc,clear
def selected_model(c):
    if not c['models']:return None
    return next((m for m in c['models'] if m.get('label','').endswith('front')),c['models'][0])
def model_image(c,m):
    if not m:return None
    raw=path_display(m['image']);im=Image.open(raw).convert('RGB');before=sha(raw)
    if S[c['id']]['model_crop']:
        box=rect_px(im,S[c['id']]['model_crop']);im=im.crop(box)
    elif '/approved/' in str(raw) and raw.name.endswith('AXON.png') and im.height>650:
        im=im.crop(rect_px(im,(.025,.13,.975,.90)))
    # The sole operation on model pixels is a crop/resample. No mesh, lighting,
    # shape or material adjustment is permitted here.
    ar=np.asarray(im).astype(float);bg=np.median(np.vstack([ar[:12,:].reshape(-1,3),ar[-12:,:].reshape(-1,3)]),axis=0)
    mask=np.max(np.abs(ar-bg),axis=2)>24
    ys,xs=np.where(mask)
    if len(xs)>60:
        b=(max(0,int(xs.min())-22),max(0,int(ys.min())-22),min(im.width,int(xs.max())+23),min(im.height,int(ys.max())+23));im=im.crop(b)
    im.thumbnail((1200,750),Image.Resampling.LANCZOS)
    plain=save_image(im,c['id']+'-model-clear.jpg',raw,'EXISTING_RENDER_CROP_RESAMPLE_ONLY',model_id=c['cid'],render_label=m['label'])
    ann=im.copy();dr=ImageDraw.Draw(ann)
    dot(dr,(max(22,ann.width*.50),max(22,min(ann.height-22,ann.height*.48))),1,'#43576b')
    if ann.width>130 and ann.height>45:dot(dr,(min(ann.width-22,ann.width*.84),max(22,min(ann.height-22,ann.height*.55))),2,'#43576b')
    decorated=save_image(ann,c['id']+'-model.jpg',raw,'EXISTING_RENDER_CROP_WITH_SUBJECT_NUMBERS_NOT_REGISTERED_PIXELS',model_id=c['cid'],render_label=m['label'])
    assert sha(raw)==before
    return decorated,plain
def label_source(path):
    pm=PM.get(Path(path).name)
    if pm:return f"{pm['source']} · PDF第{pm['pdf_page']}页"+(f" / 印刷第{pm['printed_page']}页" if pm.get('printed_page') else '')
    if '/official/' in path:return '10月14日归档的官方展示模型提取图｜不是独立实测'
    return '现有归档原始资料'
def url_source(path):
    pm=PM.get(Path(path).name)
    if pm:
        ids={'A1':'1sqCzyIaSIZ7r377nQCv_Drr7JOwICWU4','A2':'1fBp2y7oKdpCcI0tGw78okehKoUf0SkR7','A3':'1Gj--z9SKeGkN88nZ5mFm8rE9YNHMw47_'}
        return f"https://drive.google.com/file/d/{ids[pm['source']]}/view#page={pm['pdf_page']}"
    return REPO+'/blob/'+BASE+'/docs/component_atlas_v001/'+path
def fig(path,title,caption='',pre='../',cls='',clear=None):
    if path:
        image=f'<img src="{pre}{e(path)}" alt="{e(title)}" loading="lazy" decoding="async"'+(f' data-clear="{pre}{e(clear)}"' if clear else '')+'>'
    else:image='<div class="no-model"><b>没有可对应的独立模型</b><span>未以占位长方体、组合图或推测模型代替。</span></div>'
    return f'<figure class="{cls}"><figcaption><b>{e(title)}</b><span>{caption}</span></figcaption>{image}</figure>'
def shell(title,body,pre=''):
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+e(title)+'｜万佛殿构件图库</title><link rel="stylesheet" href="'+pre+'v002.css"></head><body>'+body+'<script src="'+pre+'v002.js"></script></body></html>'
def header(c):
    return '<header class="page-head"><div><a class="brand" href="../index.html">镇国寺 · 万佛殿</a><span class="edition">构件图库 V001 / 审核整改 V002</span></div><nav><a href="../index.html">全部构件</a><a href="#details">形态细节</a><a href="#location">原图定位</a><a href="#refs">出处与边界</a></nav><h1>'+e(c['title'])+'</h1><div class="meta">'+e(c['system'])+' · '+e(c['kind'])+' · '+c['id']+' <span class="status">原登记：'+e(c['status'])+'</span></div></header>'
def feature_html(s,model_exists):
    return '<div class="differences">'+''.join(f'<article class="difference {state}"><span class="state">{NAMES[state]}</span><b>{e(src)}</b><p>{e(model)}</p></article>' for state,src,model in s['features'])+'</div>'
def extra_figs(c,s):
    out=[];used={s['source']}
    for j,(path,box,label) in enumerate(s['extra']):
        raw=OUT/path;im=Image.open(raw).convert('RGB');im=im.crop(rect_px(im,box));im.thumbnail((1500,1000),Image.Resampling.LANCZOS)
        derived=save_image(im,c['id']+f'-detail-{j+1}.jpg',raw,'SOURCE_DETAIL_CROP_RESAMPLE_ONLY',crop=box)
        cap=label_source(path)+' · <a href="../'+e(path)+'">原图</a>'
        out.append(fig(derived,label,cap));used.add(path)
    for m in c['models']:
        if m is selected_model(c):continue
        raw=path_display(m['image']);out.append(fig(str(raw.relative_to(OUT)),'模型其他方向 · '+m['label'],e(m.get('caption',''))+' · 原渲染'))
    # Long repetitive full source pages are retained under their citations, not
    # promoted as single-member evidence in the main visual comparison.
    return ''.join(out)
def build():
    coverage=[]
    for c in D:
        s=S[c['id']];source,locator,clear=source_images(c,s);m=selected_model(c);model=model_image(c,m)
        kind=s['kind'];cap=e(kind)+' · '+e(label_source(s['source']))
        if s['inferred']:cap+='<em>框选含身份或位置推断，不能当作已确认的完整单件。</em>'
        subparts='　'.join(f'{i} {e(v[2])}' for i,v in enumerate(s['parts'],1))
        body=header(c)+'<main><section class="first-screen" aria-label="形态及差异对照"><div class="compare-head"><h2>先看形，再看差异</h2><button class="annotations" type="button" aria-pressed="true">隐藏数字／描线</button></div><div class="comparison">'
        body+=fig(source,s['label'],cap+'<small>'+subparts+'</small>',cls='source-panel',clear=clear)
        body+=fig(model[0] if model else None,'现有 Master · '+('原模型只读图' if model else '缺口'),e(c['cid'] or '尚未绑定独立Master')+'<small>数字标记主题部位，不代表视角或像素已经配准。</small>',cls='model-panel',clear=model[1] if model else None)
        body+='</div>'+feature_html(s,bool(m))+'<p class="view-limit">定性对照：两侧未做比例归一或像素叠加。'+('绿色实线只描原图可辨边缘；' if s['traces'] else '')+'橙色虚框只表示原图查找范围。</p></section>'
        local=c.get('local_models',[])
        body+='<section id="details"><div class="section-title"><span>02 / 形态细节</span><h2>其他角度、截面与现有局部版本</h2></div><div class="gallery">'+extra_figs(c,s)+'</div>'
        if local:
            body+='<h3>现有局部工作模型 · 与 Master 分开看</h3><div class="gallery local-models">'
            for lm in local:
                raw=path_display(lm['image'])
                body+=fig(str(raw.relative_to(OUT)),lm['label'],e(lm.get('boundary',''))+'<small>'+e(lm.get('caption',''))+'</small>')
            body+='</div>'
        body+='</section><section id="location"><div class="section-title"><span>03 / 原图与位置</span><h2>目标在原始资料的哪里</h2></div><div class="location-grid">'
        body+=fig(locator,c['title']+'｜原图查找区域','橙色虚框＝本页放大范围；不是完整实体轮廓。 <a href="../'+e(s['source'])+'">打开未标注原图</a>')
        body+='<div class="location-text"><h3>安装位置与复用</h3><p>'+e('；'.join(dict.fromkeys(x.get('location','未知') for x in c['items'])))+'</p><p><b>变体：</b>'+e(c['variant'] or '沿用现行登记口径')+'</p><p><b>Master：</b>'+e('；'.join(c['masters']) or '无独立批准Master')+'</p><details><summary>对应实例范围（'+str(len(c['items']))+'条登记记录，不是物理件数）</summary><ul>'+''.join('<li>'+e(x.get('id',''))+' · '+e(x.get('location',''))+'</li>' for x in c['items'])+'</ul></details></div></div></section>'
        body+='<section id="refs"><div class="section-title"><span>04 / 证据与边界</span><h2>出处、模型身份与未知部分</h2></div><p class="unknown"><b>仍然未知：</b>'+e(s['unknown'])+'</p>'
        if c['id'] in ['F026','F069','F070']:
            body+='<p class="correction"><b>V001文字纠正：</b>原页“长方体”说法不准确。该Master的网格坐标和原渲染都显示上宽下窄的收分，8顶点、6面不能作为长方体判断依据。仍保留原“占位包络”登记标签；正式模型与批准结论未变。</p>'
        body+='<p class="baseline"><b>原工程记录（按原文保留）：</b>'+e(c['note'])+'</p><div class="source-links"><h3>资料出处</h3>'
        paths=list(dict.fromkeys([s['source']]+[x[0] for x in s['extra']]+[x['image'] for x in c['sources']]))
        for path in paths:
            body+='<p><a href="'+e(url_source(path))+'">'+e(label_source(path))+'</a> · <a href="../'+e(path)+'">归档原图 '+e(Path(path).name)+'</a></p>'
        body+='</div><details><summary>模型原始渲染、网格身份与批准范围</summary>'
        for md in c['models']+local:
            rp=path_display(md['image']);body+='<p><a href="../'+e(str(rp.relative_to(OUT)))+'">'+e(md['label'])+'</a> '+e(md.get('boundary',''))+'</p>'
        for path in c['semantic_paths']:body+='<p><a href="'+REPO+'/blob/'+BASE+'/'+e(path)+'">'+e(Path(path).name)+'</a></p>'
        body+='<p><a href="../assets/models/RENDER_PROVENANCE.json">既有只读BLEND哈希、对象名与不变校验</a> · <a href="../assets/v002/DERIVATION_PROVENANCE.json">本轮裁切、数字与描线记录</a></p></details><p>A1、A2、A3共享测绘数据脉络，不作为三次独立复测。官方展示只作形态参考；推断、遮挡与未知不升级为实测事实。</p></section>'
        idx=int(c['id'][1:]);prev=f'F{idx-1:03d}.html' if idx>1 else '../index.html';nxt=f'F{idx+1:03d}.html' if idx<79 else '../index.html'
        body+='<footer><a href="'+prev+'">← 上一页</a><a href="../index.html">全部79页</a><a href="'+nxt+'">下一页 →</a><span>审核整改 V002 · 待PO审核 · 不更改正式工程基线</span></footer></main>'
        (OUT/'pages'/f'{c["id"]}.html').write_text(shell(c['title'],body,'../'))
        coverage.append(dict(id=c['id'],title=c['title'],kind=c['kind'],source=s['source'],source_crop=s['crop'],identity_inference=s['inferred'],visible_edge_trace_count=len(s['traces']),model_id=c['cid'],model=m['image'] if m else None,source_panel=source,locator=locator,model_panel=model[0] if model else None))
    # Index cards use the annotated crop rather than a whole scanned page.
    systems=list(dict.fromkeys(c['system'] for c in D));cards=[]
    for c in D:
        s=S[c['id']];img='assets/v002/'+c['id']+'-source.jpg'
        cards.append('<a class="card" href="pages/'+c['id']+'.html" data-system="'+e(c['system'])+'" data-search="'+e((c['title']+' '+str(c['masters'])).lower())+'" data-status="'+e(c['status'])+'"><img src="'+img+'" alt="'+e(c['title'])+'资料局部" loading="lazy"><div><small>'+e(c['system'])+' · '+c['id']+'</small><h2>'+e(c['title'])+'</h2><p>'+e(s['kind'])+'</p><span class="card-status">'+e('无独立Master' if not c['models'] else 'Master＋局部版本' if c.get('local_models') else '有现有Master')+'</span></div></a>')
    body='<header class="index-head"><a class="brand" href="index.html">镇国寺 · 万佛殿</a><span class="edition">构件图库 V001 / 审核整改 V002</span><h1>看清每一种构件</h1><p>资料中的可见形态，现有模型的具体表达。<br>点击图片进入：目标高亮、可辨边缘、模型差异和未知部分。</p><div class="counts"><span><b>79</b>个浏览页</span><span><b>58</b>个实体构件族页面</span><span><b>26</b>个Master家族</span></div></header><main><div class="index-nav"><a href="sources.html">来源与独立性</a><a href="qa/index.html">浏览验证</a><a href="'+REPO+'/pull/72">Draft PR #72</a><span>仅视觉整改 · 正式模型未改动</span></div><div class="controls"><label>查找构件<input id="search" placeholder="例如：六椽栿、华栱、滴水" type="search"></label><label>建筑系统<select id="system"><option value="">全部系统</option>'+''.join('<option>'+e(s)+'</option>' for s in systems)+'</select></label><label>原登记状态<select id="status"><option value="">全部状态</option>'+''.join('<option>'+e(s)+'</option>' for s in dict.fromkeys(c['status'] for c in D))+'</select></label><output id="resultcount">79 个页面</output></div><div class="legend"><span>绿线：仅描可辨边缘</span><span>橙框：原图查找范围</span><span>灰色：遮挡或未知</span></div><div class="grid">'+''.join(cards)+'</div><p class="view-limit">范围条目含系统、洞口和测量边界，数量不等于实际物理件数。大型／小型、一跳／二跳及其他必要变体分别保留。</p></main>'
    (OUT/'index.html').write_text(shell('构件浏览',body))
    (DER/'DERIVATION_PROVENANCE.json').write_text(json.dumps(DERIV,ensure_ascii=False,indent=2))
    (DER/'PAGE_COVERAGE.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
    print(json.dumps(dict(pages=len(coverage),derivative_images=len(DERIV),masters=len(set(c['cid'] for c in D if c['cid'])),open_edge_traces=sum(len(s['traces']) for s in S.values())),ensure_ascii=False))
if __name__=='__main__':build()
