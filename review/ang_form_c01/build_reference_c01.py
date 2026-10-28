"""Wanfo Hall: PO-selected illustration -> independent ANG C01 candidates.
VISUAL INFERENCE ONLY. Neither official point measurements nor approved Master geometry.
Geometry coordinates in millimetres, glTF export in metres. No production writes.
"""
import json, hashlib
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
GEO=ROOT/'geometry';OUT=ROOT/'output'
GEO.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def font(size,b=False):return ImageFont.truetype(BOLD if b else FONT,size)
def smooth(t):
 t=max(0.,min(1.,float(t)));return t*t*(3.-2.*t)
def section(name,L,x):
 d=x+L/2
 if name=='TOU_ANG':
  # 278.4 deep root => 187 single-cai body; lengths are visual INFERENCE.
  top=139.2-45.7*smooth((d-125.)/185.)
  bottom=-139.2+45.7*smooth((d-90.)/210.)
  tip=smooth((d-(L-168.))/168.)
  bottom+=(top-15.-bottom)*tip
 else:
  top=93.5;bottom=-93.5
  tip=smooth((d-(L-172.))/172.)
  bottom+=(top-13.-bottom)*tip
 return float(top),float(bottom)
def build(name,L):
 width=154.;half=width/2
 stations=list(np.linspace(-L/2,L/2,125))
 if name=='TOU_ANG':stations += [-L/2+v for v in (90,125,230,300,310,L-168,L-14,L)]
 else:stations += [-L/2+v for v in (L-172,L-14,L)]
 xs=sorted(set(round(float(x),9) for x in stations if -L/2-1e-6<=x<=L/2+1e-6))
 verts=[]
 for x in xs:
  top,bottom=section(name,L,x)
  bevel=min(4.,max(1.,(top-bottom)/5.))
  yz=[(-half+bevel,bottom),(half-bevel,bottom),(half,bottom+bevel),(half,top-bevel),
      (half-bevel,top),(-half+bevel,top),(-half,top-bevel),(-half,bottom+bevel)]
  verts.extend([[x,y,z] for y,z in yz])
 faces=[];n=8
 for j in range(len(xs)-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=(j+1)*n+i;d=(j+1)*n+(i+1)%n
   faces.extend([[a,b,c],[b,d,c]])
 for j in (0,len(xs)-1):
  ring=[j*n+i for i in range(n)]
  for i in range(1,n-1):
   faces.append([ring[0],ring[i],ring[i+1]] if j==0 else [ring[0],ring[i+1],ring[i]])
 mesh=trimesh.Trimesh(vertices=np.array(verts),faces=np.array(faces),process=False)
 mesh.fix_normals()
 if mesh.volume<0:mesh.invert()
 H=278.4 if name=='TOU_ANG' else 187.
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.is_volume
 assert mesh.euler_number==2 and mesh.volume>0 and min(mesh.area_faces)>.01
 assert max(abs(mesh.extents-np.array([L,width,H])))<.001
 data=dict(id=name+'_ILLUSTRATION_C01_candidate',units='mm',vertices=mesh.vertices.round(9).tolist(),
   faces=mesh.faces.tolist(),dimensions_mm=[L,width,H],work_design_length_only=True,
   source_kind='USER_SELECTED_ILLUSTRATION_NOT_OFFICIAL_MEASUREMENT',status='PENDING_PO_VISUAL_REVIEW',
   terminal_thickness_mm=15 if name=='TOU_ANG' else 13,
   outboard_underside_sweep_mm=168 if name=='TOU_ANG' else 172,
   design_class='INFERENCE',historical_full_length='UNKNOWN')
 path=GEO/(data['id']+'.json');path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 # Local fallback GLB; authoritative candidate is replaced by cloud Blender export.
 wm=mesh.copy();wm.apply_scale(.001);wm.visual.face_colors=[175,133,85,255]
 wm.export(GEO/(data['id']+'.glb'))
 check=trimesh.load(GEO/(data['id']+'.glb'),force='mesh',process=True)
 assert check.is_watertight and check.volume>0
 assert max(abs(check.extents*1000-mesh.extents))<.002
 qa=dict(id=name,dimensions_mm=[L,width,H],vertices=len(mesh.vertices),faces=len(mesh.faces),
         volume_mm3=round(float(mesh.volume),3),euler_number=mesh.euler_number,
         is_watertight=True,independent_glb_reimport='PASS',
         glb_bounds_error_mm=float(max(abs(check.extents*1000-mesh.extents))),
         historical_form_match='NOT_TESTED',po_visual='PENDING')
 return name,L,xs,mesh,qa
def side(draw,name,L,xs,rect):
 x0,y0,x1,y1=rect;H=278.4 if name=='TOU_ANG' else 187.
 up=[];down=[]
 for x in xs:
  top,bot=section(name,L,x);px=x0+(x+L/2)/L*(x1-x0)
  up.append((px,y0+(H/2-top)/H*(y1-y0)))
  down.append((px,y0+(H/2-bot)/H*(y1-y0)))
 draw.polygon(up+down[::-1],fill='#ba956a')
 draw.line(up,fill='#604d3a',width=4);draw.line(down,fill='#604d3a',width=4)
def iso(im,mesh,rect):
 d=ImageDraw.Draw(im);x0,y0,x1,y1=rect;v=mesh.vertices
 ux=.88*v[:,0]+.55*v[:,1];uy=.19*v[:,0]+.45*v[:,1]-1.65*v[:,2]
 lo=[np.min(ux),np.min(uy)];hi=[np.max(ux),np.max(uy)]
 scale=min((x1-x0-45)/(hi[0]-lo[0]),(y1-y0-35)/(hi[1]-lo[1]))
 xp=x0+20+(ux-lo[0])*scale;yp=y0+(y1-y0-(hi[1]-lo[1])*scale)/2+(uy-lo[1])*scale
 keys=np.mean(.25*v[mesh.faces,0]+.8*v[mesh.faces,1]+.7*v[mesh.faces,2],axis=1)
 for fi in np.argsort(keys)[::-1]:
  ids=mesh.faces[fi];n=mesh.face_normals[fi]
  light=.69+.22*abs(n[2])+.09*max(n[1],0)
  color=tuple(int(min(255,a*light)) for a in (191,152,103))
  d.polygon([(int(xp[i]),int(yp[i])) for i in ids],fill=color)
def make_figs(models):
 panel=Image.new('RGB',(2400,1500),'#f4f0e7');d=ImageDraw.Draw(panel)
 d.rectangle((0,0,2400,133),fill='#324e51')
 d.text((50,30),'镇国寺万佛殿｜头昂、二昂｜C01 候选视觉审核',font=font(45,True),fill='white')
 for idx,(name,L,xs,mesh,qa) in enumerate(models):
  x=40+idx*1205;zh='头昂 / 下层第一道' if idx==0 else '二昂 / 上层第二道'
  d.rounded_rectangle((x,155,x+1170,1325),radius=18,fill='#fffdf9')
  d.text((x+35,182),zh,font=font(36,True),fill='#324e51')
  iso(panel,mesh,(x+35,275,x+1135,655))
  d.text((x+40,695),'同轴侧面轮廓',font=font(26,True),fill='#364d4e')
  side(d,name,L,xs,(x+55,765,x+1125,983))
  d.text((x+40,1020),f'工作长 {L:.1f} mm / 厚度 154 mm',font=font(25),fill='#273b39')
  d.text((x+40,1073),'深头278.4 → 单材187 mm' if idx==0 else '材广187 mm（无深头段）',font=font(25),fill='#273b39')
  d.text((x+40,1140),'端部：下缘逐渐斜削收尖',font=font(25),fill='#855d44')
  d.text((x+40,1190),'待 PO 视觉审核',font=font(25,True),fill='#a14b3b')
 d.text((52,1357),'本轮将用户选定的示意图转化为 3D 候选；示意图并非官方测绘数据，不代表精确历史形制。',font=font(25,True),fill='#9b4b3c')
 d.text((52,1414),'正式 Master、原89实体与已批准栱件不变。安装接触、榫卯及承载力未验证。',font=font(25),fill='#39494a')
 panel.save(OUT/'ANG_C01_OVERVIEW_ZH.png')
 for name,L,xs,mesh,qa in models:
  im=Image.new('RGB',(2200,1250),'#f4f0e7');q=ImageDraw.Draw(im)
  q.rectangle((0,0,2200,130),fill='#324e51')
  q.text((60,30),f'万佛殿｜{"头昂" if name=="TOU_ANG" else "二昂"}｜C01独立候选',font=font(48,True),fill='white')
  iso(im,mesh,(75,170,2125,750))
  q.text((75,780),'侧面轮廓（本地构件轴向）',font=font(31,True),fill='#344c4f')
  side(q,name,L,xs,(120,859,2070,1060))
  q.text((75,1115),f'工作长 {L:.1f} mm；厚154 mm；材广'+('278.4 / 187 mm' if name=='TOU_ANG' else '187 mm'),font=font(28),fill='#334a4a')
  q.text((75,1180),'图像风格与削切参数为候选推断；非官方实测，未获视觉批准。',font=font(27),fill='#a14b3b')
  im.save(OUT/(name+'_C01_REVIEW_ZH.png'))
def main():
 models=[build('TOU_ANG',1440.62149385663),build('ER_ANG',1834.6484473864894)]
 make_figs(models)
 checks={'status':'PASS_GEOMETRY_ONLY_PO_PENDING','scope':'independent_uninstalled_candidates',
         'source':'PO_SELECTED_ILLUSTRATION_NOT_OFFICIAL_DATA','models':[a[4] for a in models],
         'unchanged':['formal Master','Registry','89-body BLEND/GLB','approved Hua/Ling Gong'],
         'not_tested':['historical geometry accuracy','mortise joints','assembly contact','structural strength']}
 (ROOT/'GEOMETRY_VALIDATION.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(checks,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
