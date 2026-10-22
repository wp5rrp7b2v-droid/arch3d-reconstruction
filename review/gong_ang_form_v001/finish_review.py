from build_review import *
from shapely.ops import unary_union
import importlib.metadata

def silhouette(mesh):
 v=mesh.vertices[:,[0,2]];pieces=[]
 for f in mesh.faces:
  p=Polygon(v[f]);
  if p.area>1e-8:pieces.append(p)
 return unary_union(pieces)
def normalized(p):
 from shapely import affinity
 x,y,X,Y=p.bounds;p=affinity.translate(p,-x,-y);return affinity.scale(p,1/(X-x),1/(Y-y),origin=(0,0))
comparisons=[]
for k,s in SPECS.items():
 for name,axes in s['trials']:
  t,w=trial_mesh(name,axes)
  if 'ANG_LOCAL' in name:
   a=math.radians(24.075498255078834);T=np.eye(4);T[:3,:3]=[[math.cos(a),0,-math.sin(a)],[0,1,0],[math.sin(a),0,math.cos(a)]];t.apply_transform(T)
  keys=s['keys']
  if 'HUA1' in name:keys=['JUMP_1_HUAGONG']
  if 'HUA2' in name:keys=['JUMP_2_HUAGONG']
  for key in keys:
   m=master_mesh(key);p=normalized(silhouette(m));q=normalized(silhouette(t));iou=p.intersection(q).area/p.union(q).area
   comparisons.append(dict(master=key,trial=name,master_dimensions_length_sidewidth_displayheight_mm=m.extents.tolist(),trial_dimensions_length_sidewidth_displayheight_mm=t.extents.tolist(),master_vertices=len(m.vertices),trial_vertices=len(t.vertices),normalized_side_silhouette_iou=float(iou),same_local_geometry=False,comparison_note='Size-normalized silhouette comparison only; NOT evidence of historical type equality. Different parameter axes and connection cuts are retained.'))
write(TASK/'MODEL_COMPARISON.json',comparisons)
# Compact primary visual overview: four rows, literal existing/reference/candidate.
im=Image.new('RGB',(3000,2700),'#edf0ee');d=ImageDraw.Draw(im)
d.rectangle((0,0,3000,170),fill='#203b46');txt(im,(60,30),'镇国寺万佛殿｜四类栱昂形制修正 V001',54,'white');txt(im,(60,112),'现有模型 → 本殿原始资料 → 独立候选｜仅供视觉审核，未替换89实体',28,'#dce8e5')
for x,t in [(60,'现有Master／试装真实网格'),(1055,'本殿资料｜有遮挡，非完整真值'),(2050,'修正候选｜推断，等待PO审核')]:txt(im,(x,197),t,31,BLUE)
for i,(k,s) in enumerate(SPECS.items()):
 y=255+i*575;d.rounded_rectangle((40,y,2960,y+545),radius=14,fill='white');txt(im,(65,y+15),f'{i+1:02}  {s["zh"]}',35,BLUE)
 if len(s['keys'])==2:
  for j,key in enumerate(s['keys']):
   add_view(im,master_mesh(key),(65+j*440,y+75,425,200),'第一跳' if j==0 else '第二跳')
   add_view(im,candidate_gong(key),(2055+j*440,y+75,425,200),'第一跳候选' if j==0 else '第二跳候选',(111,143,112))
  m,_=trial_mesh(s['trials'][-1][0],s['trials'][-1][1]);add_view(im,m,(65,y+290,870,165),'PR75隔架华栱｜与两跳分开',(187,131,81))
 else:
  key=s['keys'][0];add_view(im,master_mesh(key),(65,y+75,870,210),'正式参考体／控制段')
  m,_=trial_mesh(*s['trials'][0]);add_view(im,m,(65,y+300,870,150),'PR75试装件',(187,131,81))
  c=candidate_gong(key) if 'GONG' in key else ang_work_candidate(key)
  add_view(im,c,(2055,y+75,870,245),('完整工作长候选｜非历史全长' if 'ANG' in key else '独立候选轴测'),(111,143,112));add_view(im,c,(2055,y+330,870,115),'侧向轮廓',(111,143,112),'profile')
 # Reuse inspected and annotated source panel, pixel-identical to individual board.
 board=Image.open(OUT/f'{k.upper()}_COMPARISON_ZH.png');sub=board.crop((1055,235,1940,730));sub.thumbnail((880,390));pastecenter(im,sub,(1055,y+55,880,390))
 cap=s['change'] if k not in ['touang','erang'] else ('主控制段仍为787.6毫米；此处完整候选沿用试装轴向长度'+('1440.6' if k=='touang' else '1834.6')+'毫米，非历史全长。深头／单材、外端加工分别生成。')
 wrap(im,(2055,y+460),cap,860,22,GREEN)
 txt(im,(1060,y+470),'PDF87 图2-46' if k=='linggong' else 'PDF73 图2-27｜照片；解释图另见详情',24,ORANGE)
wrap(im,(60,2588),'FACT｜真实几何与资料可见特征。INFERENCE｜完整候选轮廓与曲线。UNKNOWN｜隐藏端部、榫卯和历史全长。尺寸与批准记录保留，候选需PO逐类审核。',2870,26)
im.save(OUT/'OVERVIEW_ZH.png')
# Main input file and every archival source retained as checksums.
source72=json.loads((SRC/'PR72_PAGE_PROVENANCE.json').read_text()) if (SRC/'PR72_PAGE_PROVENANCE.json').exists() else json.load(open('/tmp/sources.json'))
for n in [60,73,87,106]:
 p=SRC/f'A1-p{n:03}.jpg';entries=[x for x in source72 if x.get('file')==p.name]
 if entries:assert sha(p)==entries[0]['sha256'],(n,sha(p),entries)
# PR74 target assertions, omit large physical registry lists.
fd=json.loads((SRC/'PR74_TARGET_SUMMARY.json').read_text()) if (SRC/'PR74_TARGET_SUMMARY.json').exists() else json.load(open('/tmp/formdata.json'));wanted=['F028','F029','F030','F035','F036']
compact=[{k:v for k,v in x.items() if k not in ['registry_items']} for x in fd if x.get('id') in wanted]
write(SRC/'PR74_TARGET_SUMMARY.json',compact)
write(SRC/'PR72_PAGE_PROVENANCE.json',[x for x in source72 if x.get('file') in [f'A1-p{n:03}.jpg' for n in [60,73,87,106]]])
write(TASK/'RUNTIME.json',dict(python=sys.version,packages={n:importlib.metadata.version(n) for n in ['numpy','trimesh','shapely','pillow']},font_sha256=sha(FONT)))
print('overview, independent silhouette comparisons and source hashes PASS')
