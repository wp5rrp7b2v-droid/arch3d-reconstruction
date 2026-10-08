"""Inspect actual horizontal foot bearing, not nominal interface points."""
import ast, json, hashlib, math
from pathlib import Path
import numpy as np
import trimesh, manifold3d
from functools import reduce
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).resolve().parent
for node in ast.parse((ROOT/'lower_front/check_lower_front.py').read_text()).body:
    if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
def clip(poly,axis,bound,greater):
    result=[]
    for a,b in zip(poly,np.roll(poly,-1,axis=0)):
        ina=(a[axis]>=bound) if greater else (a[axis]<=bound)
        inb=(b[axis]>=bound) if greater else (b[axis]<=bound)
        if ina:result.append(a)
        if ina!=inb:result.append(a+(b-a)*(bound-a[axis])/(b[axis]-a[axis]))
    return np.array(result)
def area(poly):
    return abs(float(np.sum(poly[:,0]*np.roll(poly[:,1],-1)-poly[:,1]*np.roll(poly[:,0],-1))))/2 if len(poly)>=3 else 0.
results=[];nominal=[];geometry=[];hashes={}
for side,folder,file in [('east','east_v011','REOPENED_V11_MESHES.json'),('west','west_v002','REOPENED_WEST_V002_MESHES.json')]:
    p=ROOT/folder/file;raw=p.read_bytes();hashes[str(p)]=hashlib.sha256(raw).hexdigest();a=json.loads(raw)
    objs={o['id']:trimesh.Trimesh(o['vertices'],o['faces'],process=False) for o in a['objects']}
    beam=objs['FOUR_BEAM']
    for end in ['FRONT','REAR']:
        foot=objs['TUOJIAO_'+end]
        triangles=foot.triangles[(foot.face_normals[:,2]<-.999)&(abs(foot.triangles[:,:,2]).max(axis=1)<.001)]
        assert len(triangles)>0
        patch_area=sum(area(t[:,:2]) for t in triangles)
        bb=np.array([triangles.reshape(-1,3).min(0),triangles.reshape(-1,3).max(0)])
        geometry.append({'side':side,'end':end,'actual_bearing_bounds_mm':bb.tolist(),'actual_bearing_area_mm2':patch_area,'upper_axis_Y_mm':1836. if end=='FRONT' else -1836.,'four_beam_end_Y_mm':3596. if end=='FRONT' else -3596.})
        iface=next(i for i in a['interfaces'] if i['a']=='FOUR_BEAM' and i['b']=='TUOJIAO_'+end)
        point=np.array([iface['point']],float)
        _,d,_=trimesh.proximity.closest_point_naive(foot,point)
        nominal.append({'side':side,'end':end,'nominal_point_mm':iface['point'],'distance_to_actual_foot_surface_mm':float(d[0]),'point_on_foot_surface':bool(d[0]<.001)})
        for length in [7192.,7000.,6703.44921875,6600.,6000.,5000.,4400.,4200.]:
            retained=0.
            for tri in triangles:
                poly=tri[:,:2].copy()
                for axis,bound,gt in [(0,beam.bounds[0,0],True),(0,beam.bounds[1,0],False),(1,-length/2,True),(1,length/2,False)]:
                    if len(poly)<3:break
                    poly=clip(poly,axis,bound,gt)
                retained+=area(poly)
            results.append({'side':side,'end':end,'diagnostic_length_mm':length,'retained_area_mm2':retained,'retained_fraction':retained/patch_area,'full_original_patch_retained':abs(retained-patch_area)<.01})
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in hashes.items())
minimum_length=2*max(abs(v) for g in geometry for b in g['actual_bearing_bounds_mm'] for v in [b[1]])
new={k:trimesh.Trimesh(o['vertices'],o['faces'],process=False) for k,o in json.loads((OUT/'GEOMETRY.json').read_text()).items()}
bad=json.loads((OUT/'CHECKS.json').read_text())['bad_pairs'];boundary_tests=[]
for side,folder,file in [('east','east_v011','REOPENED_V11_MESHES.json'),('west','west_v002','REOPENED_WEST_V002_MESHES.json')]:
    o=next(o for o in json.loads((ROOT/folder/file).read_text())['objects'] if o['id']=='FOUR_BEAM')
    beam=trimesh.Trimesh(o['vertices'],o['faces'],process=False);x=4437 if side=='east' else 0;beam.apply_translation([x,0,0])
    shortened=boolean64([beam,box([1000,minimum_length,2000],[x,0,-500])],'intersection')
    for p in bad:
        if p['b']==side+':FOUR_BEAM':boundary_tests.append({'a':p['a'],'b':p['b'],'length_mm':minimum_length,'overlap_mm3':vol(new[p['a']],shortened)})
report={'status':'SINGLE_BEAM_LENGTH_CHANGE_NOT_VALIDATED','scope':'32 diagnostic horizontal foot bearing checks and 10 boundary collision tests; no revised assembly exported','bearing_geometry':geometry,'nominal_interface_audit':nominal,'cases':results,'minimum_centered_length_preserving_all_original_foot_patches_mm':minimum_length,'collision_tests_at_preservation_boundary':boundary_tests,'failed_at_boundary':sum(p['overlap_mm3']>1 for p in boundary_tests),'approved_files_unchanged':True,'conclusion':'6000mm clipping removes the ten known V002 overlaps but retains only about34-35percent of each original foot bearing patch;5000mm removes all. Preserving all original foot patches requires at least6703.449mm centered beam length and still leaves collisions. NominalY=+/-3500 markers are not actual foot-surface locations. No centered single-length solution preserves all original patches and eliminates known collisions, with all other geometry held fixed. This is not a capacity judgement or a historical endpoint claim.'}
(OUT/'ENDPOINT_DEPENDENCY_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'geometry':geometry,'nominal':nominal,'cases':results},ensure_ascii=False))
