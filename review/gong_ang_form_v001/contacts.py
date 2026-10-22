"""Read-only contact patch extraction from PR75 GLB; locations, not load validation."""
from build_review import *
from shapely.ops import unary_union
from shapely.geometry import Polygon

def world_mesh(n):
 t,g=SCENE.graph[n];m=SCENE.geometry[g].copy();m.apply_transform(t);m.vertices=m.vertices[:,[0,2,1]]*np.array([1,-1,1]);return m

def patches(a,b):
 A=world_mesh(a);B=world_mesh(b);ta=A.triangles;tb=B.triangles;nb=B.face_normals
 pieces=[]
 for t,n in zip(ta,A.face_normals):
  inds=np.flatnonzero((abs(nb@n)>.99999)&(np.max(abs((tb-t[0])@n),axis=1)<.01))
  ax=int(np.argmax(abs(n)));keep=[i for i in range(3) if i!=ax];pa=Polygon(t[:,keep])
  if pa.area<1e-6:continue
  for j in inds:
   pb=Polygon(tb[j][:,keep]);q=pa.intersection(pb)
   if q.area<.01:continue
   # Location boundaries retain GLB world mm. Separate fragments are intentionally not counted as distinct contacts.
   for shape in ([q] if q.geom_type=='Polygon' else getattr(q,'geoms',[])):
    if shape.geom_type!='Polygon' or shape.area<.01:continue
    pp=[]
    for uv in shape.exterior.coords:
     v=np.zeros(3);v[keep]=uv;v[ax]=(np.dot(n,t[0])-sum(n[i]*v[i] for i in keep))/n[ax];pp.append(v.tolist())
    pieces.append(dict(area_mm2=shape.area/abs(n[ax]),boundary_world_mm=pp,normal=n.tolist()))
 area=sum(p['area_mm2'] for p in pieces)
 if not pieces:return dict(a=a,b=b,status='NO_COPLANAR_PATCH_AT_0_01_MM',area_mm2=0)
 vs=np.vstack([p['boundary_world_mm'] for p in pieces]);cent=np.mean(vs,axis=0)
 return dict(a=a,b=b,status='FOUND_READ_ONLY_GEOMETRY_PATCH',area_mm2=area,patch_bbox_world_mm=[vs.min(0).tolist(),vs.max(0).tolist()],visual_centroid_world_mm=cent.tolist(),fragments=pieces)

if __name__=='__main__':
 d=json.loads((ROOT/'production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WEST_SPACER_VALIDATION.json').read_text());pairs=[x['target'].split(' | ') for x in d['contact_details'] if any(k in x['target'] for k in ['HUAGONG','LINGGONG'])]
 pairs += [['trial:EAST_UPPER6_FULL_BEAM_CANDIDATE','trial:EAST_FRONT_ER_ANG_LOCAL'],['trial:EAST_FRONT_ER_ANG_LOCAL','trial:EAST_FRONT_TOU_ANG_LOCAL'],['trial:EAST_FRONT_TOU_ANG_LOCAL','trial:EAST_FRONT_HUA2_LOCAL'],['trial:EAST_FRONT_HUA2_LOCAL','trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL'],['trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL','trial:EAST_FRONT_HUA1_LOCAL'],['trial:EAST_FRONT_HUA1_LOCAL','trial:EAST_FRONT_COLUMN_LUDOU']]
 res=[patches(*p) for p in pairs]
 write(TASK/'CONTACT_LOCATIONS.json',dict(source=REF75,source_glb_sha256=sha(GLB),units='mm',frame='Blender world XYZ, converted from glTF Y-up',plane_tolerance_mm=.01,scope='Current source geometry locations only; candidate contacts NOT validated; not historical joinery or strength',contacts=res))
 print([(r['a'].split(':')[-1],r['b'].split(':')[-1],round(r['area_mm2'],2)) for r in res])
