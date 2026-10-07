"""Read-only checks on approved exported geometry; no intermediate inputs required."""
import argparse,itertools,json
from pathlib import Path
from importlib.metadata import version
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

def planar(mesh,normal,point):
    n=np.asarray(normal,dtype=float);n/=np.linalg.norm(n)
    p=np.asarray(point,dtype=float);u=np.cross(n,[1,0,0])
    if np.linalg.norm(u)<.1:u=np.cross(n,[0,1,0])
    u/=np.linalg.norm(u);v=np.cross(n,u);polys=[]
    for t in mesh.triangles:
        if np.max(np.abs((t-p)@n))<.003:
            q=Polygon(np.column_stack(((t-p)@u,(t-p)@v)))
            if q.area>.001:polys.append(q)
    return unary_union(polys)

def check(folder,mesh_name,check_name):
    data=json.loads((folder/mesh_name).read_text())
    recorded=json.loads((folder/check_name).read_text())
    meshes={o['id']:trimesh.Trimesh(o['vertices'],o['faces'],process=True) for o in data['objects']}
    assert len(meshes)==len(data['objects'])==33
    contacts=[]
    for item in data['interfaces']:
        area=planar(meshes[item['a']],item['normal'],item['point']).intersection(planar(meshes[item['b']],item['normal'],item['point'])).area
        contacts.append({'a':item['a'],'b':item['b'],'area_mm2':round(float(area),3),'pass':bool(area>20)})
    curved=[]
    for a,b in [('TIEMU_FRONT','UPPER_PURLIN_FRONT'),('TIEMU_REAR','UPPER_PURLIN_REAR'),('RIDGE_TIEMU','RIDGE_PURLIN')]:
        _,dist,_=trimesh.proximity.closest_point_naive(meshes[b],meshes[a].triangles_center)
        area=float(meshes[a].area_faces[dist<.003].sum())
        curved.append({'a':a,'b':b,'area_mm2':area,'pass':area>100})
    intersections=[];boolean_tests=0
    for a,b in itertools.combinations(meshes,2):
        ma,mb=meshes[a],meshes[b]
        overlap=np.minimum(ma.bounds[1],mb.bounds[1])-np.maximum(ma.bounds[0],mb.bounds[0])
        if np.any(overlap<=.003):continue
        boolean_tests+=1
        volume=abs(trimesh.boolean.intersection([ma,mb],engine='manifold').volume)
        if not np.isfinite(volume):raise ValueError('Non-finite intersection volume: '+a+' / '+b)
        if volume>1:intersections.append({'a':a,'b':b,'volume_mm3':float(volume)})
    closed={k:bool(m.is_watertight and m.volume>0 and len(m.split(only_watertight=False))==1) for k,m in meshes.items()}
    matching=len(contacts)==len(recorded['contacts'])==42 and len(curved)==len(recorded['curved_contacts'])==3
    for new,old in zip(contacts,recorded['contacts']):
        matching=matching and new['a']==old['a'] and new['b']==old['b'] and abs(new['area_mm2']-old['actual_contact_area_mm2'])<=.01
    for new,old in zip(curved,recorded['curved_contacts']):
        matching=matching and new['a']==old['a'] and new['b']==old['b'] and abs(new['area_mm2']-old['area_mm2'])<=.01
    passed=matching and all(closed.values()) and all(x['pass'] for x in contacts+curved) and not intersections and recorded['status']=='PASS'
    return {'status':'PASS' if passed else 'FAIL','entities':len(meshes),'pairs_checked':528,'boolean_narrow_phase_tests':boolean_tests,'planar_contacts':contacts,'curved_contacts':curved,'closed_positive_single_connected':closed,'intersections_above_1mm3':intersections,'recorded_contact_areas_match':bool(matching)}

parser=argparse.ArgumentParser();parser.add_argument('--snapshot-root',type=Path,required=True);args=parser.parse_args()
results={'scope':'Read-only recheck of hash-verified archived exported meshes; not a fresh BLEND reopen or historical/structural certification. No deterministic reconstruction or mutation test claimed.','dependencies':{x:version(x) for x in ['numpy','trimesh','shapely','manifold3d']}}
results['east_v011']=check(args.snapshot_root/'east_v011','REOPENED_V11_MESHES.json','V011_GEOMETRY_CHECKS.json')
results['west_v002']=check(args.snapshot_root/'west_v002','REOPENED_WEST_V002_MESHES.json','WEST_V002_GEOMETRY_CHECKS.json')
results['status']='PASS' if all(results[x]['status']=='PASS' for x in ['east_v011','west_v002']) else 'FAIL'
print(json.dumps(results,ensure_ascii=False,indent=2))
raise SystemExit(0 if results['status']=='PASS' else 1)
