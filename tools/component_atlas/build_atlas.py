"""Build the derived visual atlas; never writes registries or engineering state."""
from pathlib import Path
import json,html,hashlib,shutil,re,collections
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/component_atlas_v001'
BASE='414be293918fea2bf4138b1a8f4345272e8764a8'
OCT14='40de729cb6eaf774a006c76a66b2e566ec56d8e1'
REPO='https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'pages').mkdir(exist_ok=True)
registry=json.loads((ROOT/'docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json').read_text())
source_manifest=json.loads((OUT/'assets/sources/SOURCE_IMAGE_PROVENANCE.json').read_text())
source_by_file={x['file']:x for x in source_manifest}
master_root=ROOT/'production/zhenguo_wanfo/component_library/masters'
render_file=OUT/'assets/models/RENDER_PROVENANCE.json'
renders=json.loads(render_file.read_text()) if render_file.exists() else []
render_map={x['id']:x for x in renders if x['status']=='PASS_READONLY'}
e=html.escape
def gh(path,ref=BASE):return REPO+'/blob/'+ref+'/'+path
def copy_asset(path,folder='approved'):
    p=ROOT/path
    if not p.exists():return None
    target=OUT/'assets'/folder/(hashlib.sha256(str(path).encode()).hexdigest()[:10]+'-'+p.name)
    target.parent.mkdir(exist_ok=True,parents=True)
    if not target.exists():shutil.copyfile(p,target)
    return str(target.relative_to(OUT))
def source(file,label=None,boundary=''):
    m=source_by_file[file]
    return dict(image='assets/sources/'+file,label=label or (m['source']+' 原始资料'),caption=f"{m['source']} · PDF第{m['pdf_page']}页"+(f" / 印刷第{m['printed_page']}页" if m['printed_page'] else '')+(' · 原图局部裁切' if 'crop' in file else ' · 完整原页'),boundary=boundary,origin=m['source'])
def page(n,label='',boundary=''):return source(f'A1-p{n:03}.jpg',label,boundary)
def crop(key,label='',boundary=''):return source('A1-crop-'+key+'.jpg',label,boundary)
def paper(n,kind='A2',label='',boundary='同源测绘的分析/解释；不是独立复测，也不单独证明完整轮廓。'):return source(f'{kind}-p{n:03}.jpg',label or kind+' 交叉核对',boundary)
CONTEXT='这是同建筑的组合/环境图；仅按可见部分核对，不从遮挡推算完整单件外形。'
# Family-specific visual evidence, source context and differences. No synthesized ancient shapes.
S={
'柱':([page(292,'东缝实测剖面'),page(49,'柱径与柱高统计')],'圆形柱身有资料支持；卷杀、侧脚、生起、柱头及柱脚细部并未由这一圆柱 Master 完整表达。'),
'下六椽栿':([crop('beam-upper','梁架与铺作交接',CONTEXT),page(81),page(292)],'现有等截面参考体没有完整梁端、梁身变化与现场不规则轮廓；1000mm 为项目参考长度，不是整梁实长。'),
'上六椽栿':([crop('beam-six','梁架照片',CONTEXT),page(81),page(292)],'Master 为等截面参考体；全梁历史形态未成立。前端 C01 的批准仅覆盖局部端部设计，不能扩大到全梁及后端。'),
'四椽栿':([crop('beam-six','四椽栿与斗栱交接',CONTEXT),page(82,'表2-39 / 图2-40'),page(292)],'截面统计与层位可核对；Master 的直棱包络未表达照片中的端头、梁身变化与承托节点。'),
'平梁':([crop('pingliang','图2-41 平梁与斗栱交接',CONTEXT),page(83),page(292)],'东西缝与山面必须分开看；山面厚度未知。参考直棱体没有完整端部及现场形变；两种截面不能相互替代。'),
'驼峰':([crop('pingliang','脊部承托体系',CONTEXT),page(106,'图2-71'),page(109)],'上下承托角色有依据；两种现有外形属于来源引导的工程候选。尺寸、完整轮廓和隐蔽榫卯未知，不视为实测真值。'),
'丁栿':([page(83,'丁栿族截面统计'),page(294,'山面构架剖面'),paper(46)],'实测族截面不等于逐根尺寸；端部骑搭与隐刻未在等截面参考体中完整表达。'),
'乳栿':([crop('rufu','图2-42 乳栿与斗栱交接',CONTEXT),page(84),page(289)],'直棱参考体没有图中交接与端部细节；斜乳栿、平乳栿位置差别不自动构成已证实的形态变体。'),
'剳牵':([page(85),page(294),paper(49)],'已知构件族及山面位置；其余位置和端点仍有缺口。直棱参考长度不证明全殿各件轮廓。'),
'槫':([crop('purlin','槫与屋面木构关系',CONTEXT),page(97),page(292)],'Master 仍为矩形包络，不能当作真实槫身截面。跨榀三槫批准的是局部装配设计，不能替代逐件测绘外形。'),
'阑额':([crop('lane','阑额及檐部组合',CONTEXT),page(86),page(283)],'现有包络反映参考截面；柱间端部、收分、隐蔽交接与现状形变未完整表达。'),
'由额':([crop('youe','由额所在檐部',CONTEXT),page(88),page(283)],'族截面与分布有据；端部榫接、轮廓变化与后世修缮状态未完整落实到包络体。'),
'大角梁':([page(88),page(89),page(291)],'参考体不能显示翼角梁真实斜向、端头与承托变化；不可从单一包络推定四角完全同形。'),
'子角梁':([page(89),page(291),crop('taoshou','套兽与角端环境',CONTEXT)],'矩形包络没有角端起翘、套兽连接及隐蔽端部的完整证据。'),
'隐角梁':([page(89),page(291),page(300)],'登记存在与推定数量不等于已获得完整轮廓；不同来源对角部名物/边界的解释需分层，当前无法确认独立完整形态。'),
'托脚':([page(89,'§2.3.1.8 托脚与叉手'),page(90,'表2-45'),page(292)],'Master 为矩形包络，缺完整斜撑端部与实际承托切口。报告公布均值237.1×153.7与可见行复算234.1×154.1存在已登记冲突；本轮不改尺寸。'),
'叉手':([crop('chashou','平梁以上三角斜撑体系',CONTEXT),page(90,'表2-45'),page(292)],'矩形参考体未独立表达上下端与脊部连接。当前装配角度、收落面属于局部工程设计，不能当成原物榫卯。'),
'蜀柱':([crop('pingliang','蜀柱与脊部承托',CONTEXT),page(344,'附件1-7'),page(292)],'实测截面与出现位置有据；等截面参考体未完整落实柱端、承托座与历史全长。'),
'柱头栌斗':([page(295,'柱头铺作实测详图'),page(62,'斗族实测记录'),paper(31)],'现有 Master 仅为8顶点6面的长方体包络，未表现斗耳、欹面与开口。C02 局部轮廓批准不能自动升级为全殿 Master。'),
'补间铺作底斗':([page(297,'补间铺作实测详图'),page(64),paper(31)],'有分段轮廓的现有模型比单纯长方体更具体；槽口与隐藏连接仍缺直接证明，完整实物外形只部分符合。'),
'华栱':([crop('huagong','图2-27 华栱与昂交接',CONTEXT),page(50,'单材/足材类型'),page(336,'附件1-5 北东头R/L'),paper(36),paper(8,'A3')],'简化弧形有同建筑来源引导；单材/足材不能混同。214.2mm局部包络与完整足材之间缺切割范围证明，不能直接拉伸到316.4mm。'),
'令栱':([page(58,'令栱测量记录'),page(295),paper(36)],'Master 为简化曲线，尚未按原物精确拟合。局部装配中“进深华栱/进深令栱”的身份对应未闭合，不在此静默改名。'),
'大型瓜子栱':([page(58),page(295),paper(36)],'大/小型必须分别显示。现有曲线为来源引导简化轮廓，端部卷杀与榫槽未完成实测拟合。'),
'小型瓜子栱':([page(58),page(297),paper(36)],'小型不能以大型缩放图直接冒充；查看本 Master 的小型变体。端部和隐蔽交接仍待对应原图。'),
'大型慢栱':([page(60),page(295),paper(36)],'大型慢栱有独立尺寸和简化曲线；端部卷杀与精准历史轮廓未证明。'),
'小型慢栱':([page(60),page(297),paper(36)],'小型变体独立展示；形态由来源引导简化，未声称每件都与族均值一致。'),
'头昂':([page(336,'附件1-5 北东头R/L'),page(73),paper(39),paper(8,'A3')],'头昂与二昂分型；参考控制跨度不等于整材全长。隐蔽搭接与完整尾部未知。'),
'二昂':([page(336,'附件1-5 北东头R/L'),page(73),paper(39),paper(8,'A3')],'简化二昂不能以头昂截面替代。已登记族样本口径冲突仍保留；全材长与隐藏交接未证明。'),
'单向长开斗族':([page(64),page(295),paper(31)],'现有 Master 为长方体包络，尚未表达斗耳与单向开口；测量样本量不等于全殿件数。'),
'交互斗族':([page(64),page(295),paper(31)],'Master 的长方体包络没有交叉开口与斗耳；C02 仅局部批准，不自动形成全殿真实交互斗外形。'),
'散斗族':([page(64),page(297)],'可见斗栱组合中有小斗；未找到可闭合的独立散斗模型/全殿清单，不把统一小斗规则补成真值。'),
'柱头铺作':([page(295),page(296),paper(41)],'这是组合单元，不是一个木构件；现有局部接触验证没有证明完整七铺作形态与全部隐蔽连接。'),
'补间铺作':([page(297),page(298),paper(44)],'这是组合位置；不得把底斗、栱、斗和枋合算为一个真实物理木件。完整组合尚未批准。'),
'转角铺作':([page(291),page(300),crop('corner','角部构造环境',CONTEXT)],'正身双向与45°斜出需区分；四角对称不能直接证明每一件相同。现有局部装配不是完整转角铺作。'),
'铺作方向单元':([page(289),page(290),page(295)],'方向单元是立面计数及定位概念；转角同时服务两个方向，不能转成新增物理件。'),
'襻间枋':([crop('inner','内槽梁架与襻间区域',CONTEXT),page(345,'附件1-9'),page(292)],'不能把内槽栱件215.0×153.6mm统计作为襻间枋统一截面；独立完整形态和逐件模型未建立。'),
'内槽斗栱/隔架位置':([page(344),page(345),page(292)],'24处是装配位置，不是24个同形实体；应分别辨识栱、斗、替木和枋。'),
'替木测量边界':([page(344,'附件1-8'),page(345)],'23条是测量样本边界，不是23件完整实体；对应可浏览的“替木实体族”页面。'),
'替木实体族':([page(344,'附件1-8'),page(345),crop('purlin','槫下承托环境',CONTEXT)],'对称型与非对称半露长不能直接互换；样本到实例、端部形态和全殿件数未闭合。'),
'椽系':([page(291),page(292),crop('roof','屋面环境',CONTEXT)],'椽、飞子与翼角椽需要分别辨识；36个旧工程代理不代表真实椽数。截面、间距和翼角逐根几何未知。'),
'望板系统':([page(292),page(139,'屋面瓦作章节')],'存在及层位可确认；板厚、分板和拼接缺证，未建立可验证的逐板模型。'),
'台基整体':([crop('platform','台基边缘实物局部'),page(132),page(281)],'这是整体系统；边缘铺砌可见，内部构造未知，不能用台基盒体说明真实内部。'),
'角石':([page(132),page(281)],'可确认转角设置；当前无独立可验证角石模型和逐角完整轮廓，保留缺口。'),
'室内地面系统':([page(133),page(134),page(135)],'整体铺砖与材料统计有据；无逐砖批准模型，不能从统计值自动填满所有铺法。'),
'室内条砖族':([page(133),page(135)],'条砖长宽有测量支持，厚度未测；端部、磨损与铺法不能由矩形轮廓推定。'),
'室内方砖族':([page(134),page(135)],'约265见方与315×305mm两类需分别保留；完整厚度与逐砖映射未建立。'),
'神台':([page(134),page(135),page(281)],'神台周缘条砖及表面方砖属组合；当前没有独立完整形态模型。'),
'墙体':([crop('wall','南墙现状照片'),page(135),page(136)],'南墙局部820–880mm不能推广为四墙厚度；完整砌筑、内部与修缮叠加未建立。'),
'墙砖族':([page(135),page(138)],'族统计277.4×134×63.1mm不代表每块砖相同；当前没有逐块批准模型。'),
'南门洞':([page(283,'南立面实测图'),page(136)],'这是开口而非木件；现状分格可见，门框断面和完整门扇尺寸未知。'),
'北门洞':([page(284,'北立面实测图'),page(136)],'北门洞位置有据；不要用南门木作分格替代北门。独立木件断面与连接未知。'),
'南立面窗洞':([page(283),page(137)],'开口与实体木作区分；两窗及墙体关系有据，不能据立面锁定所有木框断面。'),
'门木作系统':([page(283),page(284),crop('door','南立面木作环境',CONTEXT)],'可见立面分格可供参考；木框截面、榫卯、门扇独立尺寸尚缺，未建立批准模型。'),
'窗木作系统':([page(283),page(137),crop('window','南立面窗木作环境',CONTEXT)],'以南立面原图观察分格；当前没有批准的逐杆件模型，截面不得凭空补实。'),
'透风孔':([page(137),page(136),page(283)],'孔洞是形态明确的开口；八星、四瓣、古钱、海棠等纹样不能统一替代。尚无各纹样独立模型。'),
'嵌墙石碑':([page(136),page(283)],'南立面门西侧两通碑有出处；无独立批准模型，碑身、额部与嵌入深度尚未闭合。'),
'正脊':([page(139),page(140),page(283)],'整条脊线与通脊砖不是同一粒度；真实脊饰、拼接和砖块独立几何未落实。'),
'垂脊':([page(141),page(142),page(285)],'每条垂脊与垂通脊砖数量分开；现有屋面代理不表达脊砖与端部构造。'),
'戗脊':([page(142),page(143),page(283)],'真实戗脊含找头与脊饰组合；未建立逐件可审核模型。'),
'正吻':([crop('chiwen','万佛殿正吻现状'),page(140)],'实物有龙吻形态；当前无对应雕塑几何模型，不用简单包络冒充外形。'),
'垂兽':([crop('chuishou','垂兽现状'),page(141)],'实物兽头及拼接可看；当前没有批准的对应兽件模型，完整背面和接缝仍缺。'),
'戗兽':([crop('ridge-corner','戗兽与脊线环境',CONTEXT),page(142)],'需与武士、背兽、套兽分清；当前无独立批准模型与闭合的背面形态。'),
'仙人':([crop('figure','脊端人物现状'),page(143)],'保留Registry“仙人”名称；官方专题使用“武士”。此处记录称谓差别，不据称谓改正式身份或塑造模型。'),
'板瓦':([page(144),page(145),page(139)],'处于待绑定来源列表；照片能显示瓦面组合，但单片完整轮廓、断面与批准模型仍缺。'),
'勾头':([crop('eave-tile','檐头瓦作局部'),page(144)],'可见檐头纹饰，但未完成逐片身份、完整断面及背面证明；没有批准模型。'),
'滴水':([crop('eave-tile','檐口瓦作环境'),page(144)],'图像不能自动锁定每一片滴水的独立边界与尺寸；未绑定独立模型。'),
'博风板':([page(285,'山面立面环境'),page(291)],'登记为待来源绑定；山面环境不等于独立博风板实测图，完整轮廓尚无法确认。'),
'悬鱼':([page(285,'山面环境')],'尚未取得可追溯、可明确指认万佛殿悬鱼的独立形态资料；不以别寺类比补作真值。'),
'惹草':([page(285,'山面环境')],'尚未取得可明确指认的万佛殿实物轮廓或独立模型；保留待绑定状态。'),
'生头木':([page(291),page(292)],'原有待绑定来源未闭合；不能把角梁或叉手端部局部设计直接称作生头木实测外形。'),
}
for direction in '东南西北':S[direction+'坡筒瓦']=([page(145),page(146),crop('roof','屋面瓦陇环境',CONTEXT)],f'{direction}坡的瓦陇登记是排列统计，不是筒瓦物理件数；当前没有逐瓦批准模型，端部、搭接与逐坡形变未建立。')

groups=collections.OrderedDict()
for item in registry['items']:groups.setdefault((item['system'],item['component']),[]).append(item)
for name in registry['pending_source_binding']:
    if not any(k[1]==name for k in groups):groups[('待绑定来源',name)]=[]
assert set(n for _,n in groups)<=set(S),set(n for _,n in groups)-set(S)
aliases={'内槽斗栱/隔架位置':'组合位置','替木测量边界':'测量样本边界','铺作方向单元':'方向计数','柱头铺作':'装配组合','补间铺作':'装配组合','转角铺作':'装配组合','南门洞':'洞口','北门洞':'洞口','南立面窗洞':'洞口','透风孔':'洞口/纹样','台基整体':'整体系统','神台':'设施组合','墙体':'整体系统','门木作系统':'木作组合','窗木作系统':'木作组合','椽系':'木构系统','望板系统':'木构系统','室内地面系统':'铺地系统','正脊':'瓦作组合','垂脊':'瓦作组合','戗脊':'瓦作组合'}
variants={'柱':[('普通柱','',lambda x:x.get('variant')=='普通柱'),('角柱','',lambda x:x.get('variant')=='角柱')],
 '平梁':[('东西缝型','EW',lambda x:x.get('variant')=='东西缝型'),('山面型','GABLE',lambda x:x.get('variant')=='山面型')],
 '华栱':[('一跳','JUMP_1',lambda x:'一跳' in x['location']),('二跳','JUMP_2',lambda x:'二跳' in x['location'])],
 '驼峰':[('下层承托角色','LOWER',lambda x:True),('脊部承托角色','UPPER',lambda x:True)],
 '室内方砖族':[('约265mm见方型','',lambda x:True),('约315×305mm型','',lambda x:True)]}
selectors={'大型瓜子栱':'LARGE','小型瓜子栱':'SMALL','大型慢栱':'LARGE','小型慢栱':'SMALL','头昂':'TOU','二昂':'ER'}
cards=[]
def mesh_nodes(d):
    if isinstance(d,dict):
        if 'geometry_vertices_mm' in d and 'geometry_faces' in d:yield d
        for v in d.values():yield from mesh_nodes(v)
    elif isinstance(d,list):
        for v in d:yield from mesh_nodes(v)
for (system,name),items in groups.items():
    for variant,selector,predicate in variants.get(name,[('',selectors.get(name,''),lambda x:True)]):
        scope=[x for x in items if predicate(x)];masters=list(dict.fromkeys(x.get('master_reference') for x in items if x.get('master_reference')))
        cid=masters[0].removesuffix('_MASTER') if masters else None
        semantics=list((master_root/cid).glob('*SEMANTIC*.json')) if cid else []
        selected_sem=[p for p in semantics if not selector or selector in p.name]
        if not selected_sem:selected_sem=semantics
        sems=[json.loads(p.read_text()) for p in selected_sem]
        bodies=[b for d in sems for b in mesh_nodes(d)]
        if selector:
            filtered=[b for b in bodies if selector in str(b.get('body_id',b.get('variant_id','')))]
            if filtered:bodies=filtered
        boxes=bool(bodies) and all(len(b['geometry_vertices_mm'])==8 and len(b['geometry_faces'])==6 for b in bodies)
        status='仍为占位包络' if boxes else ('仅部分符合' if cid else '尚无法确认')
        if name in aliases:status='组合/边界，形态未完整验证'
        model_imgs=[]
        record=render_map.get(cid,{})
        for im in record.get('images',[]):
            if selector and selector not in ' '.join(im['object_names']):continue
            model_imgs.append(dict(image='assets/models/'+im['file'],label='现有 BLEND · '+im['view'],caption=' / '.join(im['object_names']),boundary='云端只读渲染；原始二进制与网格/变换未改。',source_url=REPO+'/actions/runs/39010819727',mode='BINARY_RENDER'))
        if not model_imgs and record:
            for im in record.get('images',[]):model_imgs.append(dict(image='assets/models/'+im['file'],label='现有 Master 视图（含其变体）',caption=' / '.join(im['object_names']),boundary='具体变体见对象名；不得将全部图视为本实例同一外形。',mode='BINARY_RENDER'))
        if not model_imgs and cid:
            candidates=[]
            for phase in ['P3_1','P3_3']:
                p=ROOT/'production/zhenguo_wanfo/review'/phase/'masters'/cid
                for f in sorted(p.glob('*AXON.png')):
                    if selector and selector not in f.name:continue
                    candidates.append(f)
            if not candidates:candidates=list((master_root/cid).glob('*REVIEW_BOARD*.png'))
            for f in candidates:
                im=copy_asset(str(f.relative_to(ROOT)))
                model_imgs.append(dict(image=im,label='GitHub 已有审核渲染',caption=f.name,boundary='沿用原有审核图；批准范围及外形证据限制保持。',source_url=gh(str(f.relative_to(ROOT))),mode='EXISTING_REVIEW'))
        visual,note=S[name];visual=[dict(x) for x in visual]
        official_names={'柱':'01_SOURCE_柱.png','柱头栌斗':'02_SOURCE_栌斗.png','交互斗族':'04_SOURCE_交互斗.png','头昂':'06_SOURCE_头昂.png','二昂':'07_SOURCE_二昂.png','华栱':('03_SOURCE_第一跳华栱.png' if selector=='JUMP_1' else '05_SOURCE_第二跳华栱.png')}
        if name in official_names:
            opath='docs/assembly/source_review/2026-10-14/seven_source_forms/'+official_names[name]
            if (ROOT/opath).exists():visual.insert(0,dict(image=copy_asset(opath,'official'),label='官方数字模型形态参考',caption='2026-10-14 已归档提取视图',boundary='匿名节点的构件命名为对应推断；不证明实测尺寸、原物精确轮廓或历史原件。',origin='OFFICIAL',source_url=gh(opath,OCT14)))
        if name in ['悬鱼','惹草','博风板','生头木']:status='尚无法确认'
        card=dict(id=f'F{len(cards)+1:03}',name=name,title=name+(' · '+variant if variant else ''),variant=variant,system=system,kind=aliases.get(name,'实体构件族'),selector=selector,items=scope,all_items=items,masters=masters,cid=cid,status=status,note=note,sources=visual,models=model_imgs,semantic_paths=[str(p.relative_to(ROOT)) for p in selected_sem],box=boxes,
          geometry=[dict(vertices=len(b['geometry_vertices_mm']),faces=len(b['geometry_faces']),body=b.get('body_id',b.get('variant_id',b.get('name','参考体')))) for b in bodies])
        cards.append(card)

CSS='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f2efe7;color:#252a29;font:16px/1.65 system-ui,-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif}a{color:#305d66;text-decoration:none}a:hover{text-decoration:underline}header{background:#1c3236;color:#faf4e7;padding:24px max(5vw,20px)}header a{color:#e3c28d}header .brand{font-size:14px;letter-spacing:3px;color:#c4b79b}h1{font-family:serif;font-weight:500;font-size:clamp(28px,4vw,49px);line-height:1.3;margin:20px 0 12px}h2{font:500 27px/1.4 serif;margin:40px 0 16px}h3{font-size:20px;margin:14px 0 8px}p{margin:8px 0 16px}.lede{max-width:900px;color:#cbd4d0}.container{max-width:1500px;margin:auto;padding:26px max(4vw,18px)}.chips{display:flex;flex-wrap:wrap;gap:9px;margin:20px 0}.chip,.tag{display:inline-block;padding:5px 12px;border:1px solid #b8c6c2;border-radius:4px;font-size:13px}.tag{border:0;background:#e0e6df}.tag.warn{background:#f0d9bd;color:#69462b}.tag.unknown{background:#e5e2dc;color:#575951}.metrics{display:flex;gap:36px;flex-wrap:wrap;margin:25px 0 12px}.metrics b{font:34px serif;display:block;color:#e8c591}.metrics span{color:#d1d9d2;font-size:14px}.controls{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#f2efe7ee;backdrop-filter:blur(10px);padding:14px 0;z-index:10}input,select{font:inherit;padding:10px 14px;border:1px solid #b9c3bb;border-radius:4px;background:#fffdf8;color:#293533}input{flex:1;min-width:230px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));gap:20px}.card{background:#faf8f1;border:1px solid #d7d8ce;border-radius:5px;overflow:hidden;color:inherit;transition:transform .15s}.card:hover{transform:translateY(-3px);box-shadow:0 8px 25px #20352d14;text-decoration:none}.card img{width:100%;height:230px;object-fit:contain;background:#e7e5dc}.card .body{padding:18px}.eyebrow{color:#71746b;font-size:13px;letter-spacing:.5px}.card p{font-size:14px;color:#5c645d}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}figure{margin:0;background:#fffdf8;border:1px solid #d3d7cd;border-radius:4px;overflow:hidden}figure img{display:block;width:100%;height:470px;object-fit:contain;background:#eeede6;cursor:zoom-in}figure .caption{padding:16px;font-size:14px;overflow-wrap:anywhere}figure .caption strong{display:block;font-size:16px;margin-bottom:7px}.boundary{font-size:13px;color:#796244}.missing{min-height:470px;display:flex;justify-content:center;flex-direction:column;padding:36px;border:1px dashed #b7b7a8;background:#e9e7df}.missing strong{font:26px serif}.note{border-left:4px solid #b99b6a;background:#e9e3d5;padding:18px 24px;margin:24px 0}.notice{background:#e3e9e3;padding:20px 24px;margin:24px 0}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}.gallery figure img{height:300px}table{border-collapse:collapse;width:100%;font-size:15px;margin:18px 0;background:#fbf9f2}th,td{padding:13px 16px;border-bottom:1px solid #d8d9cf;text-align:left;vertical-align:top}th{background:#e4e8de;font-weight:600}code{font:12px monospace;word-break:break-all}details{margin:16px 0;padding:16px;background:#e7e9df}summary{cursor:pointer}.locations{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:9px;font-size:14px}.locations div{padding:9px;background:#f7f5ed}.sectionnav{display:flex;flex-wrap:wrap;gap:18px;border-bottom:1px solid #cfd4c9;padding:15px 0}.sectionnav a{font-size:14px}.footer{margin-top:40px;border-top:1px solid #cad0c5;padding:22px 0;font-size:13px;color:#74786d}.badge{color:#a27a3e}.sub{font-size:14px;color:#c7cfcb}button{font:inherit;border:1px solid #acb8ae;background:#fbf9f2;border-radius:4px;padding:8px 14px;cursor:pointer}.lightbox{position:fixed;inset:0;background:#111e;z-index:100;display:flex;align-items:center;justify-content:center;overflow:auto;padding:50px 20px}.lightbox img{max-width:96vw;max-height:93vh;object-fit:contain}.lightbox button{position:fixed;right:20px;top:15px}.evidence-label{padding:10px 16px;background:#dce5dd;font-size:13px}.model-label{background:#e8dcc8}.twocol{columns:2;column-gap:25px}@media(max-width:750px){.pair{grid-template-columns:1fr}figure img{height:360px}.metrics{gap:20px}.twocol{columns:1}.container{padding-top:15px}.card img{height:200px}th,td{padding:9px;font-size:13px}}@media print{.controls,.sectionnav,button{display:none}.pair{display:block}header{background:white;color:black}figure{break-inside:avoid}}'''
(OUT/'style.css').write_text(CSS)
JS='''document.querySelectorAll('figure img').forEach(im=>im.addEventListener('click',()=>{let box=document.createElement('div');box.className='lightbox';let close=document.createElement('button');close.textContent='关闭 ×';let big=new Image();big.src=im.src;big.alt=im.alt;box.append(close,big);document.body.append(box);close.onclick=()=>box.remove();box.onclick=e=>{if(e.target===box)box.remove()};document.addEventListener('keydown',e=>{if(e.key==='Escape')box.remove()},{once:true})}));let search=document.getElementById('search'),system=document.getElementById('system'),status=document.getElementById('status');function filter(){let n=0;document.querySelectorAll('.card').forEach(c=>{let yes=c.dataset.search.includes(search.value.toLowerCase())&&(!system.value||c.dataset.system===system.value)&&(!status.value||c.dataset.status===status.value);c.hidden=!yes;if(yes)n++});document.getElementById('resultcount').textContent=n+' 个页面'}[search,system,status].filter(Boolean).forEach(x=>x.addEventListener('input',filter));'''
(OUT/'app.js').write_text(JS)
def layout(title,body,detail=False):
    pre='../' if detail else ''
    return f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="万佛殿构件原始资料、当前模型及差异对照"><title>{e(title)}｜万佛殿构件库</title><link rel="stylesheet" href="{pre}style.css">{body}<script src="{pre}app.js" defer></script></html>'
def display_path(p):
    f=OUT/p
    if f.suffix.lower()=='.png' and f.with_suffix('.webp').exists():return str(f.with_suffix('.webp').relative_to(OUT))
    return p
def fig(x,pre='../',model=False):
    if not x:return ''
    origin=x.get('source_url')
    if not origin and x.get('origin') in ['A1','A2','A3']:
        origin={'A1':'https://drive.google.com/file/d/1sqCzyIaSIZ7r377nQCv_Drr7JOwICWU4/view','A2':'https://drive.google.com/file/d/1fBp2y7oKdpCcI0tGw78okehKoUf0SkR7/view','A3':'https://drive.google.com/file/d/1Gj--z9SKeGkN88nZ5mFm8rE9YNHMw47_/view'}[x['origin']]
    return f'<figure><div class="evidence-label {"model-label" if model else ""}">{"现有工程成果" if model else "资料证据 / 来源见下"}</div><img loading="lazy" src="{pre}{e(display_path(x["image"]))}" alt="{e(x["label"])}"><div class="caption"><strong>{e(x["label"])}</strong>{e(x.get("caption",""))} <a target="_blank" href="{pre}{e(display_path(x["image"]))}">全尺寸图 ↗</a><p class="boundary">{e(x.get("boundary",""))}</p>{f"<a href={e(origin)} target=_blank rel=noopener>打开来源 ↗</a>" if origin else ""}</div></figure>'
def thumb(p):
    dest=OUT/'assets/thumbs'/(hashlib.sha256(p.encode()).hexdigest()[:16]+'.webp')
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        im=Image.open(OUT/p).convert('RGB');im.thumbnail((550,380));im.save(dest,quality=86,method=4)
    return str(dest.relative_to(OUT))
def head(c):return f'<header><div class="brand">镇国寺 · 万佛殿 / 构件可视化参考</div><p><a href="../index.html">← 返回全部构件</a>　<a href="../sources.html">来源与证据边界</a></p><h1>{e(c["title"])}</h1><p class="sub">{e(c["system"])} / {e(c["kind"])} / {c["id"]}</p><div class="chips"><span class="chip">{e(c["status"])}</span><span class="chip">V001 · 待 PO 审核</span></div></header>'
def tags(c):return f'<span class="tag {"warn" if c["box"] else "unknown" if not c["cid"] else ""}">{e(c["status"])}</span>'
for c in cards:
    source_main=c['sources'][0];models=c['models'];model_main=models[0] if models else None
    # Prefer a front view next to measured sections; allow all other observations below.
    front=next((m for m in models if m.get('label','').endswith('front')),None)
    if front and source_main.get('origin')!='OFFICIAL':model_main=front
    missing='<div class="missing"><strong>尚无可对应的独立模型</strong><p>本次未找到可与此构件族直接对应的批准单件模型。系统包络、洞口、测量边界或装配位置不能替代该单件真实外形。</p><p>模型缺口保留；资料图仍可浏览和放大。</p></div>'
    notes=f'<div class="note"><b>当前结论：{e(c["status"])}</b><p>{e(c["note"])}</p></div>'
    compare=f'<h2 id="compare">资料与现有 Master 基准</h2><p>并排观察轮廓、截面和端部。视角不完全一致时，只作可见形态对照；不做像素尺寸测量或相似度百分比。</p><div class="pair">{fig(source_main)}{fig(model_main,model=True) if model_main else missing}</div>{notes}'
    table='<table><tr><th>核对部位</th><th>资料支持到哪里</th><th>当前模型 / 缺口</th></tr>'
    table+=f'<tr><td>① 轮廓</td><td>优先看原图可见边界；被遮挡部分不补成事实。</td><td>{e("8顶点、6面直棱包络；真实外形未完整表达。" if c["box"] else c["note"])}</td></tr>'
    table+='<tr><td>② 截面 / 尺寸</td><td>族统计、现状实测、报告理想模型分开理解。</td><td>登记的实例分配不自动证明逐件尺寸；模型参考长度不自动等于历史全长。</td></tr>'
    table+='<tr><td>③ 端部 / 构造</td><td>照片或实测详图可见的连接单列；看不到的保持未知。</td><td>接触/干涉通过仅证明该工程几何的接口结果；不证明完整历史榫卯和承载力。</td></tr></table>'
    visual='<h2 id="evidence">大图证据与其他观察方向</h2><div class="gallery">'+''.join(fig(x) for x in c['sources'][1:])+''.join(fig(x,model=True) for x in models if x is not model_main)+'</div>'
    if c['name'] in ['悬鱼','惹草','博风板','生头木']:
        visual='<div class="notice"><b>形态证据缺口</b><p>下列整页仅是建筑位置/环境线索，不能作为该独立构件外形已经确认的证明。</p></div>'+visual
    local_match={'柱':['COLUMN_CANDIDATE'],'上六椽栿':['UPPER6_FULL_BEAM'],'下六椽栿':['LOWER6_END_SEGMENT'],'柱头栌斗':['COLUMN_LUDOU','LUDOU_FRONT'],'交互斗族':['INTERACTIVE_DOU_LOCAL'],'华栱':['HUA1_LOCAL'] if c['selector']=='JUMP_1' else ['HUA2_LOCAL'],'大型瓜子栱':['NIDAO_GUAZI'],'小型瓜子栱':['NIDAO_GUAZI'],'散斗族':['SANDOU'],'襻间枋':['PANJIAN_FANG'],'替木实体族':['TIEMU'],'替木测量边界':['TIEMU'],'令栱':['LINGGONG_FRONT'],'托脚':['TUOJIAO_FRONT'],'叉手':['CHASHOU_FRONT'],'蜀柱':['SHUZHU'],'平梁':['PINGLIANG'],'四椽栿':['FOUR_BEAM'],'槫':['PURLIN'],'驼峰':['TUOFENG'],'头昂':['TOU_ANG_LOCAL'],'二昂':['ER_ANG_LOCAL']}.get(c['name'],[])
    localviews=[];shown=set()
    for rr in sorted(renders,key=lambda r:{'LOCAL_UPPER6_C01':0,'LOCAL_C02':1}.get(r['id'],2)):
        if rr['id'] not in ['ASSEMBLY_WORK_V003','LOCAL_C02','LOCAL_UPPER6_C01']:continue
        for v in rr.get('images',[]):
            nm=' '.join(v['object_names'])
            if v['view']!='axon' or not any(k in nm for k in local_match) or nm in shown:continue
            shown.add(nm)
            cap='前端局部设计已批准；全梁及后端未因此批准。' if rr['id']=='LOCAL_UPPER6_C01' else 'C02六处局部轮廓已批准；不晋升Master。' if rr['id']=='LOCAL_C02' else 'main工作V003：含局部批准和待审对象；此图不升级批准。'
            localviews.append(dict(image='assets/models/'+v['file'],label=nm,caption=rr['id'],boundary=cap,mode='BINARY_RENDER'))
    c['local_models']=localviews
    if localviews:visual+='<h2>现有局部装配版本</h2><p>以下与Master基准分开显示；用局部版本追溯已经修过的轮廓，保留各自批准范围。</p><div class="gallery">'+''.join(fig(v,model=True) for v in localviews)+'</div>'
    locpage=283 if c['system'] in ['围护','台基','瓦作','待绑定来源'] else 292
    locations='<h2 id="location">建筑位置与复用范围</h2><div class="pair">'+fig(page(locpage,'建筑位置参照 · '+('立面' if locpage==283 else '东缝剖面'),'此图用于层位和组合关系；具体实例位置见右侧。未在图中强行标注尚未完成身份对应的构件。'))+'<div><h3>'+e(c['kind'])+'</h3><p>'+e('；'.join(dict.fromkeys(x.get('location','未知') for x in c['items'])) or '尚未绑定到逐件位置；不据待绑定名单推定建筑必然存在该形态。')+'</p><h3>Master 与变体</h3><p>'+('<br>'.join('<code>'+e(m)+'</code>' for m in c['masters']) or '尚无独立批准 Master')+'</p><p>本页变体：'+e(c['variant'] or '当前登记口径，必要变化见原始资料')+'</p><p>登记记录：'+str(len(c['items']))+' 条，仅表示对应记录范围，不能直接解释为实际物理件数。</p><details><summary>展开实例登记位置及证据</summary><div class="locations">'+''.join('<div><b>'+e(x.get('id',''))+'</b><br>'+e(x.get('location',''))+'<br><small>'+e(x.get('evidence',''))+'</small></div>' for x in c['items'])+'</div></details></div></div>'
    refs='<h2 id="refs">模型引用与批准范围</h2><p><a href="'+gh('docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json')+'">本页范围依据：现行 Registry</a> · <a href="'+gh('docs/project_control/project_state.json')+'">正式状态与批准范围</a></p>'
    refs+=''.join('<p><a href="'+gh(p)+'">'+e(Path(p).name)+'</a></p>' for p in c['semantic_paths'])
    if c['cid'] in render_map:
        r=render_map[c['cid']];refs+='<p>本次读取 BLEND 的 SHA-256：<code>'+e(r['sha256'])+'</code>。<a href="../assets/models/RENDER_PROVENANCE.json">只读渲染与网格不变记录</a></p>'
    if c['name'] in ['上六椽栿','柱头栌斗','交互斗族','华栱','令栱']:
        refs+='<div class="notice"><b>局部装配与 Master 分开</b><p>10月9日曲线令栱V002、10月12日工作V003及10月13日C02/上六椽栿前端C01有各自批准边界。局部批准不升级整个Master。后端七件R01仍被退回，10月14日类型/截面身份门槛未闭合。</p><p><a href="'+REPO+'/tree/engineering/upper6-front-tenon-c01-20261013">C02及前端C01分支</a> · <a href="'+gh('docs/assembly/source_review/2026-10-14/REAR_HUAGONG_TYPE_SECTION_REVIEW_ZH.md',OCT14)+'">10月14日复核原文</a> · <a href="../working.html">浏览现有装配网格</a></p></div>'
    footer='<div class="footer">派生可视化审核材料。图库结论不改变原 Master、Registry、局部批准或正式工程结论。所有资料点击可放大。</div>'
    nav='<nav class="sectionnav"><a href="#compare">并排对比</a><a href="#evidence">大图证据</a><a href="#location">建筑位置</a><a href="#refs">模型与批准引用</a></nav>'
    (OUT/'pages'/f'{c["id"]}.html').write_text(layout(c['title'],head(c)+'<main class="container">'+nav+compare+table+visual+locations+refs+footer+'</main>',True))

systems=list(dict.fromkeys(c['system'] for c in cards));statuses=list(dict.fromkeys(c['status'] for c in cards))
header=f'<header><div class="brand">证据 · 外形 · 差异</div><h1>万佛殿<br>可参考可视化构件库</h1><p class="lede">从资料原图看构件应该长什么样，再对照当前模型。覆盖现行登记中的每个名称条目与待绑定来源项目，独立列出必要变体；如实显示占位包络和证据缺口。</p><div class="metrics"><div><b>{len(cards)}</b><span>实际详情页面</span></div><div><b>{len(groups)}</b><span>范围条目，含组合/边界</span></div><div><b>{len(set(c["cid"] for c in cards if c["cid"]))}</b><span>关联 Master 家族</span></div></div><p class="sub">V001 · 2026-10-17 · 待 PO 审核　/　不代表整殿完整形态已获验证</p></header>'
controls='<div class="controls"><input id="search" aria-label="搜索构件" placeholder="搜索构件、Master、变体…"><select id="system" aria-label="建筑系统"><option value="">全部建筑系统</option>'+''.join('<option>'+e(s)+'</option>' for s in systems)+'</select><select id="status" aria-label="当前结论"><option value="">全部形态状态</option>'+''.join('<option>'+e(s)+'</option>' for s in statuses)+'</select></div>'
intro='<nav class="sectionnav"><a href="sources.html">资料来源与独立性</a><a href="working.html">现有装配模型图</a><a href="'+REPO+'/tree/visualization/wanfo-component-atlas-v001-20261017">GitHub工作分支</a></nav><div class="notice">读图顺序：<b>资料原图 → 当前模型 → 轮廓/截面/端部差异</b>。已批准不等于外形完全正确；“尚无法确认”也不表示构件必然不存在。</div>'
grid='<p id="resultcount">'+str(len(cards))+' 个页面</p><div class="grid">'
for c in cards:
    grid+=f'<a class="card" href="pages/{c["id"]}.html" data-search="{e((c["title"]+" "+str(c["masters"])).lower())}" data-system="{e(c["system"])}" data-status="{e(c["status"])}"><img loading="lazy" src="{e(thumb(c["sources"][0]["image"]))}" alt="{e(c["title"])}资料图"><div class="body"><div class="eyebrow">{e(c["system"])} · {e(c["kind"])}</div><h3>{e(c["title"])}</h3>{tags(c)}<p>{e(c["note"][:82])}</p></div></a>'
grid+='</div>'
(OUT/'index.html').write_text(layout('可参考可视化构件库 V001',header+'<main class="container">'+intro+controls+grid+'<div class="footer">'+str(len(registry['items']))+'条登记记录不等于整殿物理构件总数。重复实例共用形态页，必要变体独立显示。本轮未进行新的构件建模、整殿装配或正式模型变更。</div></main>'))
srcbody='''<header><div class="brand">万佛殿可视化构件库 V001</div><a href="index.html">← 全部构件</a><h1>来源与证据边界</h1></header><main class="container"><h2>资料之间是什么关系</h2><table><tr><th>来源</th><th>本轮实际使用</th><th>独立性与限制</th></tr><tr><td>A1 精细测绘报告</td><td>完整434页原PDF；选取实测表、同建筑照片、图录和附件原页。</td><td>主测绘资料。现状实测、报告推定与理想模型分开；不把别寺图2-28～2-31当万佛殿外形。</td></tr><tr><td>A2 大木结构测量研究</td><td>《中国建筑史论汇刊》第5辑，当前文件PDF第10–57页为目标文章；本轮展示相关正文与图表。</td><td>与A1共享测绘研究脉络，不能算新增独立复测。旧记录中的“A2”有时指官方数字专题；本图库统一将论文称A2，官方专题单列。</td></tr><tr><td>A3 尺度规律研究</td><td>肖旻，2024；原文明确使用精细测绘报告数据。展示原页、尺度表和解释边界。</td><td>同源数据的竞争性解释；321mm等模数及推算长度不自动成为后端单件实测尺寸。</td></tr><tr><td>官方数字模型 / 专题</td><td>沿用10月14日归档的官方模型提取图、节点对应说明和哈希。</td><td>形态展示参考；匿名polySurface名称没有直接构件语义，部分身份为推断。来源链不够明确，不能按独立实测计票。</td></tr><tr><td>C1 营造法式</td><td>已取得原PDF作为传统构造类比边界。</td><td>不是万佛殿实测。图库未使用类比形状冒充万佛殿真值。</td></tr><tr><td>GitHub现有模型</td><td>现行Registry、26个Master目录、已有审核图、main工作BLEND与相关分支。</td><td>模型是被核对对象，不是新的实物证据；局部批准不能扩大成全殿批准。</td></tr></table><h2>已核实的Drive目录范围</h2><p>项目根目录“万佛殿3D复原”及“01_万佛殿直接资料”“02_唐五代比较资料”“03_制度与参考资料”“04_研究报告与证据摘录”和“修缮与保护资料”子目录已列取。相关原始资料是A1/A2/A3/C1及五份既有研究摘录；本轮列取的比较资料、修缮资料子目录为空，没有发现额外独立现场照片集。A1包含大量同建筑现场照片；这些照片和其测绘表仍属于同一来源链。</p><h2>本轮证明到哪里</h2><p>页面覆盖和图像可浏览性可以验证；登记计数、批准范围与网格/二进制一致性可追溯。完整历史外形、全部逐件尺寸、隐蔽榫卯和承载力没有因此自动通过。</p><p>FACT：原页、网格与正式记录直接支持的内容。INFERENCE：官方匿名节点与构件的语义对应等。WORKING HYPOTHESIS：简化轮廓、参考长度及部分局部端部设计。UNKNOWN：缺失的完整外形、全长与样本对应。</p><h2>原始来源入口</h2><p><a href="https://drive.google.com/drive/folders/1mHLKizFfU7qwgeCHQWKnrvmetaXfB-E4">A1/A2/A3原始PDF</a> · <a href="https://drive.google.com/file/d/1wnQz5sdEMNTVeCFsMupVMrj93WNDLqeC/view">C1营造法式</a> · <a href="https://szbwgvue.chwhyun.cn/wanfodian/">官方数字专题</a></p><p><a href="assets/sources/SOURCE_IMAGE_PROVENANCE.json">原图页码、裁切范围与SHA-256</a> · <a href="assets/models/RENDER_PROVENANCE.json">现有模型只读渲染记录</a></p><h2>跨分支查阅</h2>'''
for ref,label in [('evidence/rear-huagong-type-review-20261014','10月14日后端形态复核'),('engineering/upper6-front-tenon-c01-20261013','上六椽栿前端C01局部批准'),('engineering/dou-contour-c02-20261013','C02六处局部轮廓批准'),('archive/20261013-form-review-and-rejected-candidates','10月13日退回候选与研究归档'),('engineering/master-section-direction-candidates-2026-10-09','截面方向候选，未整体批准')]:srcbody+='<p><a href="'+REPO+'/tree/'+ref+'">'+label+'</a></p>'
srcbody+='<div class="footer">页面解释只用于可视化审核，不替代正式工程决策。</div></main>'
(OUT/'sources.html').write_text(layout('资料来源',srcbody))
work='<header><a href="index.html">← 全部构件</a><h1>现有装配网格 · 只读视图</h1><p class="lede">main工作V003含局部批准及待审对象；下列渲染不改变任何对象的批准状态。用对象名追溯，不能据整页观看作整殿批准。</p></header><main class="container"><div class="gallery">'
for r in renders:
    if r['id']=='ASSEMBLY_WORK_V003':
        for x in r['images']:
            if x['view']=='axon':work+=fig(dict(image='assets/models/'+x['file'],label=' / '.join(x['object_names']),caption='工作V003现有网格',boundary='只读原模型；对象批准范围见正式状态。'),pre='',model=True)
work+='</div><div class="footer">此处为模型图，不是现场照片或实测真值。</div></main>'
(OUT/'working.html').write_text(layout('现有装配网格',work))
data=[{k:v for k,v in c.items() if k not in ['all_items']} for c in cards]
(OUT/'atlas_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(json.dumps(dict(pages=len(cards),scope_entries=len(groups),registry_records=len(registry['items']),linked_master_families=len(set(c['cid'] for c in cards if c['cid'])),with_model_images=sum(bool(c['models']) for c in cards),box_pages=sum(c['box'] for c in cards)),ensure_ascii=False))
