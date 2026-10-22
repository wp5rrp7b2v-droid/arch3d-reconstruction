"""Read exact GitHub geometry; generate independent review meshes and CPU orthographic views.
No Blender execution, no writes to production, registry or canonical geometry.
"""
from pathlib import Path
import json,hashlib,math,sys,subprocess,shutil
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import triangulate
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2];TASK=Path(__file__).resolve().parent
SRC=TASK/'sources';OUT=TASK/'output';GEO=TASK/'geometry'
for p in [SRC,OUT,GEO]:p.mkdir(exist_ok=True)
FONT=Path('/tmp/NotoSansSC.ttf')
BLUE='#235666';GREEN='#276958';INK='#23363e';ORANGE='#a35e26'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def font(n):
 f=ImageFont.truetype(str(FONT),n);f.set_variation_by_axes([450]);return f
def txt(im,xy,s,size=26,fill=INK):ImageDraw.Draw(im).text(xy,s,font=font(size),fill=fill)
def wrap(im,xy,s,width,size=25,fill=INK):
 d=ImageDraw.Draw(im);x,y=xy;line=''
 for c in s:
  if d.textlength(line+c,font=font(size))>width:
   txt(im,(x,y),line,size,fill);y+=int(size*1.55);line=''
  line+=c
 if line:txt(im,(x,y),line,size,fill)
 return y+int(size*1.55)
def getfile(ref,path,dst):
 p=SRC/dst
 if not p.exists():p.write_bytes(subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT))
 return p
REF72='54fac54578340918c78d65e973933b54090893a1';REF74='8a47daa343efde62d28cef62370d0185da3f6abe';REF75='f8f72d40dd47ab61abc3103c396c855f5c4c3865'
# Full original pages, copied byte for byte; each source ref fixed.
for n in [60,73,87,106]:
 dst=SRC/f'A1-p{n:03}.jpg'
 if not dst.exists():
  p=Path('/tmp/A1-p073.jpg') if n==73 else ROOT/f'docs/component_form_reference_v001/assets/original/A1-p{n:03}.jpg'
  shutil.copyfile(p,dst)
# Official images supplement the primary photos, never constitute measured truth.
for fn in ['0d6e55efe9-06_SOURCE_头昂.png','2a94b0e852-07_SOURCE_二昂.png','6fd13f56b4-05_SOURCE_第二跳华栱.png']:
 p=ROOT/'docs/component_form_reference_v001/assets/original'/fn
 if p.exists():shutil.copyfile(p,SRC/fn)
MP='production/zhenguo_wanfo/component_library/masters/'
MASTERS={}
for k in ['HUAGONG','LINGGONG','ANG']:
 path=MP+f'CMP-GONG-{k}-001/CMP-GONG-{k}-001_MASTER_SEMANTIC_V001.json'
 p=getfile('414be293918fea2bf4138b1a8f4345272e8764a8',path,f'{k}_MASTER_SEMANTIC.json')
 d=json.loads(p.read_text());bodies=d.get('canonical_bodies',[d.get('canonical_body')])
 for b in bodies:MASTERS[b['body_id']]=b
GLBPATH='production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WANFO_WEST_SPACER_89_TRIAL_V001.glb'
GLB=ROOT/GLBPATH
assert sha(GLB)=='ed686f2ed81dc0ad0139a320bdd0c99709419c1c401bc1dff3b3635867f5a151'
SCENE=trimesh.load(GLB,force='scene',process=False)
assert len(SCENE.graph.nodes_geometry)==89

def poly_mesh(points,width):
 poly=Polygon(points);assert poly.is_valid and poly.area>0
 pts=list(poly.exterior.coords)[:-1];n=len(pts)
 v=np.array([[x,-width/2,z] for x,z in pts]+[[x,width/2,z] for x,z in pts])
 faces=[]
 for t in triangulate(poly):
  if not poly.covers(t.representative_point()):continue
  inds=[pts.index(tuple(p)) for p in list(t.exterior.coords)[:3]]
  faces.extend([inds[::-1],[i+n for i in inds]])
 for i in range(n):j=(i+1)%n;faces.extend([[i,j,j+n],[i,j+n,i+n]])
 m=trimesh.Trimesh(v,faces,process=False);m.fix_normals();return m

def master_mesh(key):
 b=MASTERS[key];v=np.array(b['geometry_vertices_mm']);n=len(v)//2
 m=poly_mesh(v[:n][:,[0,2]],np.ptp(v[:,1]))
 # Triangulation changes faces only; all original vertices are retained exactly.
 assert np.allclose(np.sort(m.vertices,axis=0),np.sort(v,axis=0),atol=1e-9)
 return m

def trial_mesh(name,axes):
 tf,g=SCENE.graph[name];m=SCENE.geometry[g].copy();m.apply_transform(tf)
 # glTF Y up; export uses millimetre numeric coordinates (verified validation).
 v=m.vertices[:,[0,2,1]]*np.array([1,-1,1]);world=v.copy()
 v=v[:,axes]
 if axes==[1,0,2]:v[:,1]*=-1  # preserve right-handedness; observation transform is rigid
 v-= (v.max(0)+v.min(0))/2
 m.vertices=v
 return m,world

def render(mesh,w=880,h=320,view='iso',color=(159,127,87),scale=None):
 # Deterministic CPU z-buffer rasterisation of actual triangle geometry, 2x AA.
 w0,h0=w,h;w*=2;h*=2
 v=mesh.vertices.copy();v-=(v.max(0)+v.min(0))/2
 eye={'iso':np.array([.68,-1,.65]),'profile':np.array([0,-1,0]),'top':np.array([0,0,1]),'end':np.array([1,0,0])}[view];eye=eye/np.linalg.norm(eye)
 up=np.array([0,0,1]) if view!='top' else np.array([0,1,0])
 right=np.cross(up,eye);right/=np.linalg.norm(right);up=np.cross(eye,right)
 proj=np.column_stack((v@right,v@up,v@eye));span=np.ptp(proj[:,:2],axis=0)
 sc=min((w-90)/max(span[0],1),(h-55)/max(span[1],1)) if scale is None else scale*2
 p=np.column_stack((proj[:,0]*sc+w/2,-proj[:,1]*sc+h/2,proj[:,2]))
 arr=np.zeros((h,w,3),dtype=np.uint8)+np.array([247,247,243],dtype=np.uint8);depth=np.full((h,w),-np.inf)
 light=np.array([-.35,-.6,.9]);light/=np.linalg.norm(light)
 for f in mesh.faces:
  t=p[f];x0=max(0,int(np.floor(t[:,0].min())));x1=min(w-1,int(np.ceil(t[:,0].max())));y0=max(0,int(np.floor(t[:,1].min())));y1=min(h-1,int(np.ceil(t[:,1].max())))
  if x0>x1 or y0>y1:continue
  den=(t[1,1]-t[2,1])*(t[0,0]-t[2,0])+(t[2,0]-t[1,0])*(t[0,1]-t[2,1])
  if abs(den)<1e-8:continue
  yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
  a=((t[1,1]-t[2,1])*(xx-t[2,0])+(t[2,0]-t[1,0])*(yy-t[2,1]))/den
  b=((t[2,1]-t[0,1])*(xx-t[2,0])+(t[0,0]-t[2,0])*(yy-t[2,1]))/den;c=1-a-b
  z=a*t[0,2]+b*t[1,2]+c*t[2,2];dep=depth[y0:y1+1,x0:x1+1]
  mask=(a>=-1e-6)&(b>=-1e-6)&(c>=-1e-6)&(z>dep)
  normal=np.cross(v[f[1]]-v[f[0]],v[f[2]]-v[f[0]]);norm=np.linalg.norm(normal)
  if norm<1e-12:continue
  shade=.62+.38*abs(np.dot(normal/norm,light))
  rgb=np.clip(np.array(color)*shade,0,255).astype('uint8')
  arr[y0:y1+1,x0:x1+1][mask]=rgb;dep[mask]=z[mask]
 return Image.fromarray(arr).resize((w0,h0),Image.Resampling.LANCZOS)

def candidate_gong(key):
 m=master_mesh(key);L,W,H=m.extents
 # Source-guided shoulder + concentrated end roll; no joinery inferred.
 # Central-flat ratio is an explicitly editable hypothesis, not a measured coordinate.
 a=.31 if key=='JUMP_1_HUAGONG' else .355 if key=='JUMP_2_HUAGONG' else .30
 pts=[(-L/2,H/2),(L/2,H/2),(L/2,H*.17)]
 for t in np.linspace(0,math.pi/2,33)[1:]:
  x=L/2-(L/2-a*L)*(1-math.cos(t));z=H*.17-H*.67*math.sin(t);pts.append((x,z))
 pts.append((-a*L,-H/2))
 for t in np.linspace(math.pi/2,0,33)[1:]:
  x=-(L/2-(L/2-a*L)*(1-math.cos(t)));z=H*.17-H*.67*math.sin(t);pts.append((x,z))
 return poly_mesh(pts,W)

def candidate_ang(key):
 m=master_mesh(key);L,W,H=m.extents
 if key=='TOU_ANG':
  # Straight upper datum; single-cai tail, deep lower head and unilateral shaving.
  xs=np.array([-.5,-.15,.05,.20,.31,.40,.47,.5])*L
  upper=np.array([.5,.5,.5,.5,.5,.5,.38,.08])*H
  lower=np.array([.5-187/278.4,.5-187/278.4,-.34,-.5,-.5,-.36,-.10,.08])*H
 else:
  xs=np.array([-.5,-.10,.25,.34,.40,.46,.5])*L
  upper=np.array([.5,.5,.5,.5,.48,.32,.06])*H
  lower=np.array([-.5,-.5,-.5,-.5,-.40,-.20,.06])*H
 pts=list(zip(xs,upper))+list(zip(xs[:-1][::-1],lower[:-1][::-1]))
 return poly_mesh(pts,W)

def ang_work_candidate(key):
 name='trial:EAST_FRONT_'+('TOU' if key=='TOU_ANG' else 'ER')+'_ANG_LOCAL'
 m,_=trial_mesh(name,[1,0,2]);a=math.radians(24.075498255078834)
 T=np.eye(4);T[:3,:3]=[[math.cos(a),0,-math.sin(a)],[0,1,0],[math.sin(a),0,math.cos(a)]];m.apply_transform(T)
 L,W,H=m.extents;end=L/2
 if key=='TOU_ANG':
  xs=np.array([-L/2,end-520,end-390,end-280,end-170,end-95,end-30,end])
  upper=np.array([.5,.5,.5,.5,.5,.5,.35,.06])*H
  lower=np.array([.5-187/278.4,.5-187/278.4,-.32,-.5,-.5,-.36,-.10,.06])*H
 else:
  xs=np.array([-L/2,end-450,end-200,end-150,end-90,end-30,end])
  upper=np.array([.5,.5,.5,.5,.46,.28,.04])*H
  lower=np.array([-.5,-.5,-.5,-.5,-.39,-.18,.04])*H
 cand=poly_mesh(list(zip(xs,upper))+list(zip(xs[:-1][::-1],lower[:-1][::-1])),W)
 assert np.allclose(cand.extents,m.extents,atol=.001)
 return cand

SPECS={
'huagong':dict(zh='华栱',keys=['JUMP_1_HUAGONG','JUMP_2_HUAGONG'],trials=[('trial:EAST_FRONT_HUA1_LOCAL',[1,0,2]),('trial:EAST_FRONT_HUA2_LOCAL',[1,0,2]),('trial:WEST_FRONT_SPACER_HUAGONG',[1,0,2])],problem='正式两跳参考体沿全长连续变浅，端部卷杀与中段直腹区分不足。隔架候选另有非对称端部和顶面承托凹口，身份及截面不能直接等同两跳。',change='两跳分别保留原长、宽、高包络；把下缘变化集中到端部，中段改为较平直的深栱身。二跳单独生成端区比例，不缩放复制一跳。',fact='图2-27照片可见卷杀转折；同页报告解释图显示两层华栱下缘与承托组合。',inference='左右对称、卷杀起点、弧线及中段比例为本轮候选推断。',unknown='整材隐蔽端、上口切割、各跳历史全长及隔架华栱的历史型号。',photo=73,crop=(.16,.13,.79,.39),diagram=(.22,.52,.70,.67)),
'linggong':dict(zh='令栱',keys=['LINGGONG'],trials=[('trial:WEST_FRONT_SPACER_LINGGONG',[0,1,2]),('trial:WEST_REAR_SPACER_DEPTH_LINGGONG',[1,0,2]),('trial:WEST_REAR_SPACER_LONGITUDINAL_LINGGONG',[0,1,2])],problem='正式Master中段仅短小平底，整段呈浅弧。西缝三件另有不同截面、方向及中部开口；后部进深令栱的命名不能证明它是外檐令栱。',change='保留897×217.4×155.6毫米参考包络，改为较宽的深中段与集中端卷杀；不照搬西缝试装槽口，不把三件强行统一为同一外檐类型。',fact='PDF60记令栱仅施最外跳；图2-46上部最外跳横栱可见两端卷杀。',inference='中段直腹长度、端曲线与侧面厚度连续处理为候选；照片有透视及遮挡。',unknown='卷杀分瓣、上口、背面和三件隔架令栱准确历史身份。',photo=87,crop=(.29,.405,.66,.49),diagram=(.17,.40,.82,.69)),
' touang':{},
 'touang':dict(zh='头昂',keys=['TOU_ANG'],trials=[('trial:EAST_FRONT_TOU_ANG_LOCAL',[1,0,2])],problem='正式Master是787.6毫米控制段，头部近上下对称鼓起；东缝局部候选已经延长并有较钝多折昂头，不能视作同一网格。',change='在原控制段包络内保留154毫米厚、278.4毫米深头及187毫米单材尾部。改为上缘较直、加深集中在下缘，昂头向外单侧收削。',fact='PDF73图2-27照片可见斜昂及外端削尖；资料记录的头昂材广与二昂有别。',inference='深头过渡位置、削尖段长度及曲面均是来源引导候选；非逐点测绘。',unknown='真实整材全长、后尾隐藏部分、上六椽栿接口和全部榫卯。',photo=73,crop=(.21,.20,.63,.34),diagram=(.22,.43,.69,.61)),
'erang':dict(zh='二昂',keys=['ER_ANG'],trials=[('trial:EAST_FRONT_ER_ANG_LOCAL',[1,0,2])],problem='正式Master是独立的单材控制段，现端部上下对称收尖仍较钝；东缝局部候选较长且有独立切口、尾部变化。',change='保留787.6毫米控制跨度、154毫米厚及187毫米材广。保持单材昂身，以较短外端收削区别头昂深头，不由头昂整体缩放。',fact='PDF73上层斜昂的外端收削与双昂层位可见；187与154毫米沿用既有尺寸记录。',inference='上层对应二昂的识别结合原报告与官方提取图；精确削尖与曲线为本轮候选。',unknown='历史尾部全长、内部切口、各实例变形及样本口径冲突。',photo=73,crop=(.20,.17,.63,.31),diagram=(.21,.40,.70,.57))}
SPECS.pop(' touang')

PROVENANCE=[];EXTRACTION=[];CANDIDATES=[]
def arrow(im,a,b,label):
 d=ImageDraw.Draw(im);d.line([a,b],fill='#e4a129',width=5)
 vec=np.array(a)-np.array(b);vec=vec/(np.linalg.norm(vec)+1e-9);perp=np.array([-vec[1],vec[0]])
 d.polygon([tuple(b),tuple(np.array(b)+vec*19+perp*9),tuple(np.array(b)+vec*19-perp*9)],fill='#e4a129')
 bb=d.textbbox(a,label,font=font(22));d.rectangle((bb[0]-5,bb[1]-4,bb[2]+5,bb[3]+4),fill='white');d.text(a,label,font=font(22),fill=INK)
def crop(p,box,w,h):
 im=Image.open(p).convert('RGB');im=im.crop(tuple(int(q*z) for q,z in zip(box,[im.width,im.height]*2)))
 return ImageOps.contain(im,(w,h),Image.Resampling.LANCZOS)
def pastecenter(im,sub,box):
 x,y,w,h=box;im.paste(sub,(int(x+(w-sub.width)/2),int(y+(h-sub.height)/2)))
def dims(m):return ' × '.join(f'{v:.1f}' for v in m.extents)+' 毫米'
def add_view(im,m,box,label,color=(161,132,95),view='iso'):
 x,y,w,h=box;txt(im,(x,y),label,20 if '图示高' in label else 23,BLUE);im.paste(render(m,w,h-36,view,color),(x,y+36))
def export_mesh(m,key,kind):
 p=GEO/f'{key}_{kind}.json';write(p,dict(id=key,kind=kind,units='mm',vertices=m.vertices.tolist(),faces=m.faces.tolist(),dimensions_mm=m.extents.tolist(),status='PENDING_PO_REVIEW' if kind=='candidate' else 'READ_ONLY_EXTRACT'))
 # metres in standard glTF, preserving meaningful portable dimensions.
 portable=m.copy();portable.apply_scale(.001);portable.export(GEO/f'{key}_{kind}.glb')
 if kind=='candidate':
  check=trimesh.load(GEO/f'{key}_{kind}.glb',force='mesh',process=False);assert np.max(abs(check.extents*1000-m.extents))<.001
 return p

def detail(k):
 s=SPECS[k];im=Image.new('RGB',(3000,2180),'#eef0ed');d=ImageDraw.Draw(im)
 d.rectangle((0,0,3000,150),fill='#203b46');txt(im,(60,26),f'镇国寺万佛殿｜{s["zh"]}形制修正候选 V001',48,'white');txt(im,(60,97),'真实模型提取  /  本殿资料对应  /  独立三维候选 · 等待PO视觉审核',25,'#d2e0df')
 for x,title,c in [(40,'左｜现有正式Master与PR #75试装件',BLUE),(1035,'中｜历史资料与可见特征',ORANGE),(2030,'右｜修正候选 · 非批准模型',GREEN)]:
  d.rounded_rectangle((x,174,x+930,1755),radius=16,fill='white');txt(im,(x+22,192),title,32,c)
 keys=s['keys'];rows=len(keys)
 for j,key in enumerate(keys):
  m=master_mesh(key);cand=candidate_gong(key) if 'GONG' in key else candidate_ang(key)
  assert np.allclose(m.extents,cand.extents,atol=1e-5),(key,m.extents,cand.extents)
  assert not np.isclose(m.volume,cand.volume,rtol=1e-4)
  assert cand.is_watertight and cand.volume>0
  jp=export_mesh(m,key,'master');cp=export_mesh(cand,key,'candidate')
  CANDIDATES.append(dict(id=key,preserved_master_dimensions_mm=m.extents.tolist(),candidate_dimensions_mm=cand.extents.tolist(),master_volume_mm3=m.volume,candidate_volume_mm3=cand.volume,watertight=bool(cand.is_watertight),geometry_class='INFERENCE_SOURCE_GUIDED_REVIEW_ONLY',not_installable_without_further_contact_validation=True))
  y=250+j*505 if rows==2 else 250
  nm={'JUMP_1_HUAGONG':'第一跳','JUMP_2_HUAGONG':'第二跳','LINGGONG':'正式参考体','TOU_ANG':'正式参考控制段','ER_ANG':'正式参考控制段'}[key]
  add_view(im,m,(65,y,880,210 if rows==2 else 280),nm+'｜真实网格轴测')
  add_view(im,cand,(2055,y,880,210 if rows==2 else 280),nm+'｜候选轴测',(111,143,112))
  py=y+(215 if rows==2 else 300)
  add_view(im,m,(65,py,880,180), '正面轮廓｜长×侧宽×图示高：'+dims(m),view='profile')
  add_view(im,cand,(2055,py,880,180),'候选轮廓｜包络与左侧一致',(111,143,112),view='profile')
  if rows==2:
   add_view(im,m,(735,py+165,195,115),'端面',view='end');add_view(im,cand,(2725,py+165,195,115),'端面',(111,143,112),view='end')
  if rows==1:
   add_view(im,m,(65,py+195,420,175),'侧面／端面',view='end');add_view(im,cand,(2055,py+195,420,175),'侧面／端面',(111,143,112),view='end')
   add_view(im,m,(510,py+195,420,175),'顶面',view='top');add_view(im,cand,(2500,py+195,420,175),'顶面',(111,143,112),view='top')
  m.export(OUT/f'{key}_master_preview.ply') if False else None
  cand_preview=render(cand,900,280,color=(111,143,112));cand_preview.save(OUT/f'{key}_candidate.png')
 # Actual target trial geometry, independent from Master.
 ty=1260 if rows==2 else 1010
 for j,(name,axes) in enumerate(s['trials']):
  m,world=trial_mesh(name,axes);ex=export_mesh(m,name.split(':')[-1],'trial')
  h=105 if len(s['trials'])==3 else 220
  add_view(im,m,(65,ty+j*(h+65),880,h+35),'PR75｜'+('装配投影包络' if 'ANG_LOCAL' in name else name.split('_')[-2])+'｜'+dims(m),(187,131,81))
  member_dimensions=m.extents.tolist()
  if 'ANG_LOCAL' in name:
   aligned=m.copy();a=math.radians(24.075498255078834);T=np.eye(4);T[:3,:3]=[[math.cos(a),0,-math.sin(a)],[0,1,0],[math.sin(a),0,math.cos(a)]];aligned.apply_transform(T);member_dimensions=aligned.extents.tolist()
   txt(im,(65,ty+h+45),'轴向长×厚×材广：'+dims(aligned),23,BLUE)
  EXTRACTION.append(dict(member_axis_dimensions_mm=member_dimensions,id=name,glb_node=name,source_glb_sha256=sha(GLB),normalized_axes=axes,normalized_axis_signs=([1,-1,1] if axes==[1,0,2] else [1,1,1]),dimensions_mm=m.extents.tolist(),world_bbox_mm=[world.min(0).tolist(),world.max(0).tolist()],vertices=len(m.vertices),triangles=len(m.faces),local_export=str(ex.relative_to(TASK))))
 # Primary source panels
 p=SRC/f'A1-p{s["photo"]:03}.jpg';sub=crop(p,s['crop'],870,450);pastecenter(im,sub,(1065,275,870,450))
 txt(im,(1060,238),f'A1 PDF第{s["photo"]}页｜'+('图2-46 实物照片' if k=='linggong' else '图2-27 实物照片'),25,ORANGE)
 if k=='linggong':
  arrow(im,(1090,340),(1325,473),'最外跳横栱：左端卷杀');arrow(im,(1550,340),(1840,473),'右端卷杀')
 elif k=='huagong':arrow(im,(1090,350),(1580,440),'可见栱端｜与斜昂交叠')
 elif k=='touang':arrow(im,(1520,330),(1303,642),'下层斜昂外端｜削尖')
 else:arrow(im,(1520,330),(1116,655),'上层斜昂外端｜削尖')
 sub=crop(p,s['diagram'],870,400);pastecenter(im,sub,(1065,800,870,400))
 txt(im,(1060,752),'照片定位范围' if k=='linggong' else '同页图2-27｜报告交接关系解释图',25,ORANGE)
 if k=='huagong':
  arrow(im,(1090,900),(1480,1090),'下层：第一跳（层位识别）');arrow(im,(1430,825),(1740,980),'上层：第二跳')
 elif k in ['touang','erang']:arrow(im,(1090,815),(1470,1020),'斜材｜结合照片识别，非单件实测')
 # full page locator with box
 full=Image.open(p).convert('RGB');fd=ImageDraw.Draw(full);box=s['crop'];fd.rectangle(tuple(int(q*z) for q,z in zip(box,[full.width,full.height]*2)),outline='#d5822b',width=12);full.thumbnail((270,420));im.paste(full,(1070,1260))
 wrap(im,(1380,1280),'FACT｜'+s['fact'],530,26)
 wrap(im,(1380,1440),'页码按项目434页PDF计；PDF73＝印刷58页，PDF87＝印刷72页。原页未改，框箭头只作定位。',530,23)
 wrap(im,(1065,1630),'图纸与模型未做比例配准，不能按屏幕大小推断长度。',865,23,ORANGE)
 cy=1300 if rows==2 else 1020
 cy=wrap(im,(2055,cy),'修正：'+s['change'],875,28,GREEN)+24
 cy=wrap(im,(2055,cy),'推断：'+s['inference'],875,25)+24
 cy=wrap(im,(2055,cy),'未知：'+s['unknown'],875,25,ORANGE)+25
 if k in ['touang','erang']:
  cy=wrap(im,(2055,cy),'斜度沿用报告设计三角形24.0755°；主图按构件局部轴展示。787.6毫米仅是控制段，非整材。',875,25)+12
  # Full existing-work-length variant; hidden tail length remains a working assumption.
  full=ang_work_candidate(keys[0]);export_mesh(full,keys[0]+'_WORK_LENGTH','candidate')
  add_view(im,full,(2055,1440,880,135),'沿用试装轴向长度的完整外形候选',(111,143,112))
  mm=full.copy();a=-math.radians(24.075498255);T=np.eye(4);T[:3,:3]=[[math.cos(a),0,-math.sin(a)],[0,1,0],[math.sin(a),0,math.cos(a)]];mm.apply_transform(T)
  add_view(im,mm,(2055,1585,880,145),'沿用24.0755°斜度｜工作长度，非历史全长',(111,143,112),'profile')
 d.rectangle((40,1790,2960,2115),fill='#e1e8e6')
 txt(im,(65,1810),'本页判断与证据边界',30,BLUE)
 wrap(im,(65,1870),'当前问题：'+s['problem'],1390,27)
 wrap(im,(1540,1870),'FACT｜只限资料可见特征与原模型数据。INFERENCE｜完整候选轮廓；数字坐标不是实测。UNKNOWN｜遮挡端部与榫卯。候选不替换89件，不承接原模型的碰撞PASS。',1350,27)
 txt(im,(60,2135),'来源与精确网格、尺寸、差异清单见同目录 README_ZH.md / TRACEABILITY.json / geometry/',22,BLUE)
 out=OUT/f'{k.upper()}_COMPARISON_ZH.png';tmp=out.with_suffix('.part');im.save(tmp,format='PNG');tmp.replace(out)
 return out

if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'all'
 targets=['huagong'] if mode=='pilot' else list(SPECS)
 for k in targets:print(detail(k),flush=True)
 write(TASK/'CANDIDATE_VALIDATION.json',CANDIDATES);write(TASK/'MODEL_EXTRACTION.json',EXTRACTION)
 write(TASK/'TRACEABILITY.json',dict(PR72=REF72,PR74=REF74,PR75=REF75,main='414be293918fea2bf4138b1a8f4345272e8764a8',glb_path=GLBPATH,glb_sha256=sha(GLB),source_pdf_sha256='94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472',sources=[dict(path=str(p.relative_to(TASK)),sha256=sha(p)) for p in SRC.iterdir() if p.is_file()],font_url='https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf',font_sha256=sha(FONT),candidate_status='PENDING_PO_REVIEW',renderer='CPU_ORTHOGRAPHIC_TRIANGLE_ZBUFFER_2X_AA',blender_executed=False))
