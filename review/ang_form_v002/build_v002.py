"""Offline, source-guided ANG V002 candidates; no production writes. Units mm."""
from pathlib import Path
import ast,json,hashlib,math,subprocess,sys,shutil
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import triangulate,unary_union
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[2]; TASK=Path(__file__).resolve().parent
OLD=ROOT/'review/gong_ang_form_v001'; OUT=TASK/'output'; GEO=TASK/'geometry';SRC=TASK/'sources'
for p in [OUT,GEO,SRC]:p.mkdir(exist_ok=True)
FONT=Path('/tmp/NotoSansSC.ttf');INK='#23363e';BLUE='#235666';GREEN='#276958';ORANGE='#a35e26'
BASE='028517cbdada6cb266feae17f58ae0a7888c4a93'
# Reuse audited rasterizer and extrusion implementation, without executing V001 build.
names={'sha','write','font','txt','wrap','poly_mesh','render','arrow','pastecenter','crop'}
tree=ast.parse((OLD/'build_review.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(OLD/'build_review.py'),'exec'))
def readmesh(name):
 d=json.loads((OLD/'geometry'/f'{name}.json').read_text());return trimesh.Trimesh(d['vertices'],d['faces'],process=False)
def profile(m):
 return unary_union([Polygon(m.vertices[f][:,[0,2]]) for f in m.faces if Polygon(m.vertices[f][:,[0,2]]).area>1e-8])
def smooth(t):return t*t*(3-2*t)
def build(key,L):
 H=278.4 if key=='TOU_ANG' else 187.;W=154.;end=L/2
 # Independent definitions. Source constrains shaving direction; all numeric cut parameters INFERENCE.
 if key=='TOU_ANG':cut=270.;lip=8.;rise=3.;blend=28.;transition=(end-590,end-390)
 else:cut=205.;lip=6.;rise=2.;blend=18.;transition=None
 start=end-cut
 xs=sorted(set([-L/2,end,start,start+blend,end-20]+list(np.linspace(start,end,55))+([] if transition is None else list(np.linspace(*transition,35)))))
 upper=[];lower=[]
 for x in xs:
  # C1 blend into a planar shaving face, deliberately not a symmetric point.
  d=max(0,x-start);slope=(H-lip-rise)/(cut-blend/2)
  drop=slope*(d*d/(2*blend) if d<blend else d-blend/2)
  upper.append((x,H/2-drop))
  z=-H/2
  if transition:
   a,b=transition;t=np.clip((x-a)/(b-a),0,1);z=H/2-187-(H-187)*smooth(t)
  z+=rise*smooth(np.clip((x-(end-20))/20,0,1))
  lower.append((x,z))
 pts=upper+lower[::-1];p=Polygon(pts).simplify(1e-8,preserve_topology=True);m=poly_mesh(list(p.exterior.coords)[:-1],W)
 assert p.is_valid and p.exterior.is_simple
 assert np.allclose(m.extents,[L,W,H],atol=1e-7)
 assert m.is_watertight and m.is_winding_consistent and m.volume>0
 assert np.min(m.area_faces)>1e-8 and m.euler_number==2
 # Simple nonintersecting planar polygon x constant positive-width extrusion proves no self-intersections.
 assert abs(m.volume-p.area*W)<.01
 assert abs(upper[-1][1]-lower[-1][1]-lip)<1e-8
 return m,dict(shaving_start_from_outer_end_mm=cut,upper_blend_mm=blend,terminal_thickness_mm=lip,lower_lip_rise_mm=rise,deep_transition_x_mm=transition,upper_points_mm=upper,lower_points_mm=lower,parameter_class='INFERENCE_NOT_HISTORIC_MEASUREMENT')
def export(key,m,params,work=False):
 name=key+'_V002'+('_WORK_LENGTH' if work else '')+'_candidate'
 write(GEO/(name+'.json'),dict(id=name,units='mm',vertices=m.vertices.tolist(),faces=m.faces.tolist(),dimensions_mm=m.extents.tolist(),parameters=params,status='PENDING_PO_VISUAL_REVIEW',historical_full_length='UNKNOWN',work_design_length_only=work))
 # Initial GLB for local QA; authoritative cloud export replaces these via Blender.
 c=m.copy();c.apply_scale(.001);c.export(GEO/(name+'.glb'))
 return name

def source_panel(im,x,y,key,width=1120):
 # Full original photograph, no tight crop; normalized anchors checked against original 1312x1902 page.
 p=Image.open(OLD/'sources/A1-p073.jpg').convert('RGB');box=(.16,.128,.775,.373)
 a=p.crop(tuple(int(q*z) for q,z in zip(box,[p.width,p.height]*2)));a=ImageOps.contain(a,(width,510));im.paste(a,(x,y))
 # Original normalized image positions. Lower front head at (.322,.309), upper at (.237,.291).
 anchor=(.322,.309) if key=='TOU_ANG' else (.237,.291)
 b=(x+(anchor[0]-box[0])/(box[2]-box[0])*a.width,y+(anchor[1]-box[1])/(box[3]-box[1])*a.height)
 arrow(im,(x+width-340,y+45),b,'头昂外端（下层）' if key=='TOU_ANG' else '二昂外端（上层）')
 txt(im,(x,y+a.height+12),'A1 PDF73／印刷58 图2-27：上侧削面收向下缘',25,ORANGE)
 return dict(path='review/gong_ang_form_v001/sources/A1-p073.jpg',crop_normalized=box,anchor_normalized=anchor)

def view(im,m,box,label,kind='profile',color=(111,143,112)):
 x,y,w,h=box;txt(im,(x,y),label,25,BLUE);im.paste(render(m,w,h-38,kind,color),(x,y+38))
def outline(im,m1,m2,box):
 x,y,w,h=box;d=ImageDraw.Draw(im);d.rectangle((x,y,x+w,y+h),fill='#f7f7f3')
 allv=np.vstack([m1.vertices,m2.vertices]);lo=allv[:,[0,2]].min(0);hi=allv[:,[0,2]].max(0);s=min((w-80)/(hi[0]-lo[0]),(h-110)/(hi[1]-lo[1]))
 for m,c in [(m1,'#b78351'),(m2,GREEN)]:
  ps=np.asarray(profile(m).exterior.coords);xy=[(x+40+(a-lo[0])*s,y+h-30-(b-lo[1])*s) for a,b in ps];d.line(xy,fill=c,width=5)
 txt(im,(x+22,y+8),'同尺度轮廓叠图：棕 V001 ／ 绿 V002；外端 →',23)

def detail(key,m,work,params):
 zh='头昂' if key=='TOU_ANG' else '二昂';im=Image.new('RGB',(3400,2580),'#eef0ed');d=ImageDraw.Draw(im)
 d.rectangle((0,0,3400,148),fill='#203b46');txt(im,(55,24),f'镇国寺万佛殿｜{zh}形制修正 V002',49,'white');txt(im,(55,93),'独立审核候选 · 技术核验与PO视觉批准分开 · 仅修改外形，不替换装配',26,'#d2e0df')
 for x,w,title in [(35,1060,'一｜真实旧模型与V001'),(1120,1100,'二｜V002候选 · 实际网格'),(2245,1120,'三｜同殿原图与来源边界')]:
  d.rounded_rectangle((x,175,x+w,2220),radius=14,fill='white');txt(im,(x+20,196),title,33,BLUE)
 old=readmesh(key+'_candidate');master=readmesh(key+'_master');trial=readmesh('EAST_FRONT_'+('TOU' if key=='TOU_ANG' else 'ER')+'_ANG_LOCAL_trial')
 view(im,old,(55,260,1020,270),'V001控制段｜侧视 · 外端 →',color=(187,131,81))
 view(im,old,(55,560,1020,330),'V001控制段｜轴测',kind='iso',color=(187,131,81))
 view(im,old,(55,920,470,270),'V001端视（沿轴投影）','end',(187,131,81))
 view(im,master,(55,1230,1020,300),'正式Master｜真实控制段侧视',color=(150,155,159))
 view(im,trial,(55,1570,1020,380),'PR75东缝试装件｜完整网格轴测','iso',(187,131,81))
 wrap(im,(65,1990),'Master、V001与东缝试装件身份独立。试装件仅只读提取，保持原网格与89实体文件。',970,27)
 view(im,m,(1140,260,1060,270),'V002控制段｜侧视 · 外端 →')
 view(im,m,(1140,560,1060,330),'V002控制段｜轴测','iso')
 view(im,m,(1140,920,470,270),'V002端视（沿轴投影）','end')
 # Exact outer end face, not a misleading full-axis silhouette.
 lip=params['terminal_thickness_mm'];endface=poly_mesh([(0,0),(154,0),(154,lip),(0,lip)],1)
 view(im,endface,(1650,920,540,270),f'最外端面｜厚154 × 端厚{lip:g}毫米','profile')
 outline(im,old,m,(1140,1240,1060,320))
 view(im,work,(1140,1600,1060,340),'V002工作长度｜完整轴测（工作设计值）','iso')
 H=278.4 if key=='TOU_ANG' else 187
 wrap(im,(1150,1980),f'控制段787.6158 × 厚154 × 材广{H:g}毫米。'+('单材区187毫米；深头278.4毫米。' if key=='TOU_ANG' else '全身为单材187毫米，独立端部。')+f'工作轴长{work.extents[0]:.4f}毫米，非历史实测全长。',1020,27)
 loc=source_panel(im,2265,265,key,1080)
 off=OLD/'sources'/('0d6e55efe9-06_SOURCE_头昂.png' if key=='TOU_ANG' else '2a94b0e852-07_SOURCE_二昂.png')
 sub=ImageOps.contain(Image.open(off).convert('RGB'),(1080,715));im.paste(sub,(2265,850));txt(im,(2265,1580),'既有官方展示提取图：身份含推断，非单件实测',25,ORANGE)
 # Full source page locator preserves exact context, photo and explanation diagram distinguished.
 sub=ImageOps.contain(Image.open(OLD/'sources/A1-p073.jpg').convert('RGB'),(350,510));im.paste(sub,(2265,1650))
 wrap(im,(2650,1660),'完整原页定位：上半为实物照片，下半为报告交接关系解释图。 A2 PDF39／印刷130图22及文字复核头昂、上层下昂的上下皮交接关系。 A2 PDF46上半图是奉国寺，本候选不采用。',670,27)
 wrap(im,(55,2270),'FACT｜固定材广、厚度、控制跨度来自已有Master；原图可见两层斜昂、方向性斜削。V001上下缘末点同高属代码事实，不能单独解释PO全部退回原因。',3270,27)
 wrap(im,(55,2360),f'INFERENCE｜上侧主削面、深头过渡与收削控制点；削切长{params["shaving_start_from_outer_end_mm"]:g}毫米、端厚{lip:g}毫米仅为本次候选参数，非历史真值。',3270,27,GREEN)
 wrap(im,(55,2450),'UNKNOWN｜历史整材全长、背面与隐藏尾端、全部榫卯、准确削切曲线及实例差异。PO视觉审核：待定；安装适配与承载力：未验证。',3270,27,ORANGE)
 im.save(OUT/(key+'_V001_V002_SOURCE_ZH.png'))
 return loc

def run(only=None):
 # Fetch only pre-existing, fixed project evidence; no new historical research.
 for n in [28,39,46]:
  p=SRC/f'A2-p{n:03}.jpg'
  if not p.exists():p.write_bytes(subprocess.check_output(['git','show',f'8a47daa343efde62d28cef62370d0185da3f6abe:docs/component_form_reference_v001/assets/original/A2-p{n:03}.jpg'],cwd=ROOT))
 results=[];models={};locators={}
 for key,Lw in [('TOU_ANG',1440.62149385663),('ER_ANG',1834.6484473864894)]:
  if only and key!=only:continue
  m,params=build(key,787.6158);w,pw=build(key,Lw);name=export(key,m,params);export(key,w,pw,True)
  old=readmesh(key+'_candidate');p=profile(m);op=profile(old);diff=p.symmetric_difference(op).area
  assert diff>1000
  assert abs(m.extents[1]-154)<1e-7
  locators[key]=detail(key,m,w,params);models[key]=w
  results.append(dict(id=name,dimensions_mm=m.extents.tolist(),work_dimensions_mm=w.extents.tolist(),volume_mm3=float(m.volume),watertight=bool(m.is_watertight),positive_volume=True,winding_consistent=bool(m.is_winding_consistent),euler_number=m.euler_number,minimum_triangle_area_mm2=float(m.area_faces.min()),self_intersection='PASS_SIMPLE_POLYGON_CONSTANT_WIDTH_EXTRUSION',section_axes='X轴向/Y厚度/Z材广；非安装世界坐标',v001_symmetric_difference_mm2=diff,v001_profile_IoU=p.intersection(op).area/p.union(op).area,terminal_thickness_mm=params['terminal_thickness_mm'],parameters_class='INFERENCE',PO_VISUAL='PENDING'))
 write(TASK/('TOU_ANG_PILOT.json' if only else 'TECHNICAL_VALIDATION.json'),dict(scope='CONTROL_AND_WORK_LENGTH_OFFLINE_CANDIDATES',geometry_gate='PASS',blender_gate='PENDING_SEPARATE_PROCESS',PO_visual_gate='PENDING',models=results,source_locators=locators))
 if only:return
 # Layer comparison, rigid observation transforms only; NO assembly replacement.
 im=Image.new('RGB',(3200,2300),'#eef0ed');d=ImageDraw.Draw(im);d.rectangle((0,0,3200,150),fill='#203b46');txt(im,(55,30),'镇国寺万佛殿｜头昂、二昂 V002：层位与形态区别',49,'white');txt(im,(55,103),'资料层位对照 + 独立候选；未做装配替换或接触验证',27,'#d2e0df')
 source_panel(im,60,230,'TOU_ANG',1450);source_panel(im,1630,230,'ER_ANG',1450)
 txt(im,(60,880),'下层头昂｜深头278.4 → 单材187；厚154毫米',32,BLUE);txt(im,(1630,880),'上层二昂｜独立细长单材187；厚154毫米',32,BLUE)
 for key,x in [('TOU_ANG',60),('ER_ANG',1630)]:
  w=models[key];view(im,w,(x,960,1450,330),'工作长度完整侧视 · 外端 →（各图自适应缩放）')
  view(im,w,(x,1330,1450,410),'工作长度完整轴测','iso')
  m,_=build(key,787.6158);view(im,m,(x,1790,920,280),'控制段侧视｜两类保留相同控制跨度');view(im,m,(x+960,1790,470,280),'沿轴端视','end')
 wrap(im,(60,2130),'层位依据：A1图2-27实物照片 + A2 PDF39图22及文字。头昂在下、二昂在上；候选只供外形比较，图示间距不是安装标高。工作长为既有工程设计值；历史完整尾端、榫卯与全长UNKNOWN。',3050,29)
 im.save(OUT/'ANG_V002_LEVEL_FORM_OVERVIEW_ZH.png')
 write(TASK/'SOURCE_TRACEABILITY.json',dict(base=BASE,main='414be293918fea2bf4138b1a8f4345272e8764a8',PR74='8a47daa343efde62d28cef62370d0185da3f6abe',PR75='f8f72d40dd47ab61abc3103c396c855f5c4c3865',technical_comment='https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/76#issuecomment-6459911371',locators=locators,sources=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in list(SRC.glob('*'))+list((OLD/'sources').glob('*')) if p.is_file()],FACT=['原归档网格、控制尺寸及两层斜昂照片','A2 PDF39头下昂与上层下昂交接文字'],INFERENCE=['所有新轮廓控制点、上侧斜削参数、末端有限端厚','官方展示件身份'],UNKNOWN=['历史整材全长','精确端厚与斜削起点','隐藏尾端与榫卯','安装适配与承载力'],excluded='A2 PDF46图30奉国寺、图31梅庵，不作本殿端部依据'))
if __name__=='__main__':run('TOU_ANG' if '--pilot' in sys.argv else None)
