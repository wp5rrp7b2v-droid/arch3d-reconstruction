"""Independent WEST spacer proof: original-82 identity, 7 copied meshes, contacts and overlaps.
Requires external pip numpy==2.5.3 trimesh==5.1.1 manifold3d==3.5.4 shapely==2.1.2.
"""
import json,math,itertools,sys
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as mf
from shapely.geometry import Polygon

root=Path(sys.argv[1]);out=root/"output"
baseline=json.loads((out/"BASELINE82.json").read_text())
current=json.loads((out/"REOPENED89.json").read_text())
build=json.loads((out/"BUILD_INPUT_REPORT.json").read_text())
aa={o["id"]:o for o in baseline["objects"]}
bb={o["id"]:o for o in current["objects"]}
mapping=build["copy_map"]
delta=np.asarray(build["delta_mm"])
assert len(aa)==82 and len(bb)==89, (len(aa),len(bb))
assert set(bb)==set(aa)|set(mapping.values()) and set(aa).isdisjoint(mapping.values())
# Exact original mesh/face/local-transform identity, independent save-reopen.
max_error=0.
for key,src in aa.items():
 dst=bb[key]
 assert src["faces"]==dst["faces"], ("ORIGINAL_FACES_CHANGED",key)
 assert src["local"]==dst["local"], ("ORIGINAL_LOCAL_VERTICES_CHANGED",key)
 assert src["matrix"]==dst["matrix"], ("ORIGINAL_TRANSFORM_CHANGED",key)
 d=float(np.max(abs(np.asarray(src["vertices"])-np.asarray(dst["vertices"]))))
 assert d<.001, ("ORIGINAL_WORLD_COORDINATE_DRIFT",key,d)
 max_error=max(max_error,d)
for src,dst in mapping.items():
 one,two=aa[src],bb[dst]
 assert one["faces"]==two["faces"] and one["local"]==two["local"], ("COPY_NOT_SAME_MESH",dst)
 actual=np.array(two["vertices"]);expected=np.array(one["vertices"])+delta
 d=float(np.max(abs(actual-expected)))
 assert d<.001, ("WEST_CLONE_OFFSET_WRONG",dst,d)
 max_error=max(max_error,d)
assert abs(delta[0]+4437)<1 and abs(delta[1])<1 and abs(delta[2]+27)<1,delta

mesh={k:trimesh.Trimesh(v["vertices"],v["faces"],process=False) for k,v in bb.items()}
for k in mapping.values():
 assert mesh[k].is_volume and len(mesh[k].split(only_watertight=False))==1, ("NOT_CLOSED_POSITIVE_SINGLE_MESH",k)
def man(v,f):
 return mf.Manifold(mf.Mesh64(vert_properties=np.asarray(v,dtype="f8",order="C"),
                               tri_verts=np.asarray(f,dtype="u8",order="C")))
bad=[];n=0;greatest=0.
for a,b in itertools.combinations(mesh,2):
 ma,mb=mesh[a],mesh[b]
 lo=np.maximum(ma.bounds[0],mb.bounds[0]);hi=np.minimum(ma.bounds[1],mb.bounds[1]);volume=0.
 if np.all(hi>lo):
  centre=(hi+lo)/2
  volume=abs(float((man(ma.vertices-centre,ma.faces)^man(mb.vertices-centre,mb.faces)).volume()))
 n+=1;greatest=max(greatest,volume)
 if volume>1.:bad.append({"a":a,"b":b,"overlap_mm3":volume})
def surface(ma,mb):
 result=0.
 for i,tri in enumerate(ma.triangles):
  normal=ma.face_normals[i]
  axis=tri[1]-tri[0]; axis=axis/np.linalg.norm(axis)
  other=np.cross(normal,axis);origin=tri[0]
  pa=Polygon(np.column_stack([(tri-origin)@axis,(tri-origin)@other]))
  for j,t in enumerate(mb.triangles):
   if np.dot(normal,mb.face_normals[j])>-1+1e-7 or np.max(np.abs((t-origin)@normal))>.001:continue
   pb=Polygon(np.column_stack([(t-origin)@axis,(t-origin)@other]))
   result+=pa.intersection(pb).area
 return result
east_pairs=[
 ("trial:EAST_UPPER6_FULL_BEAM_CANDIDATE","trial:EAST_FRONT_SPACER_HUAGONG"),
 ("trial:EAST_UPPER6_FULL_BEAM_CANDIDATE","trial:EAST_FRONT_SPACER_LINGGONG"),
 ("trial:EAST_FRONT_SPACER_HUAGONG","trial:EAST_FRONT_SPACER_LINGGONG"),
 ("trial:EAST_FRONT_SPACER_LINGGONG","trial:EAST_FRONT_SANDOU"),
 ("trial:EAST_UPPER6_FULL_BEAM_CANDIDATE","trial:EAST_REAR_SPACER_DEPTH_LINGGONG"),
 ("trial:EAST_UPPER6_FULL_BEAM_CANDIDATE","trial:EAST_REAR_SPACER_LONGITUDINAL_LINGGONG"),
 ("trial:EAST_REAR_SPACER_DEPTH_LINGGONG","trial:EAST_REAR_SPACER_LONGITUDINAL_LINGGONG"),
 ("trial:EAST_REAR_SPACER_LONGITUDINAL_LINGGONG","trial:EAST_REAR_SANDOU"),
]
contact_rows=[]
for a,b in east_pairs:
 orig=surface(mesh[a],mesh[b])
 transplanted=surface(mesh[mapping[a]],mesh[mapping[b]])
 contact_rows.append({"source":a+" | "+b,"target":mapping[a]+" | "+mapping[b],
                       "east_mm2":orig,"west_mm2":transplanted,
                       "pass":bool(orig>100 and transplanted>100 and abs(orig-transplanted)<max(0.02,orig*.0001))})
for a,b in [
 ("trial:EAST_FRONT_SANDOU","east:FOUR_BEAM"),
 ("trial:EAST_REAR_SANDOU","east:FOUR_BEAM")
]:
 west_a=mapping[a]
 east=surface(mesh[a],mesh[b])
 west=surface(mesh[west_a],mesh["west:FOUR_BEAM"])
 contact_rows.append({"source":a+" | "+b,"target":west_a+" | west:FOUR_BEAM",
                      "east_mm2":east,"west_mm2":west,
                      "pass":bool(east>100 and west>100),
                      "note":"West support area need only be positive: section differs by the measured 27 mm."})
good=not bad and all(c["pass"] for c in contact_rows)
report={
 "status":"PASS_ASSEMBLY_CANDIDATE_ONLY" if good else "FAIL_HOLD_CANDIDATE",
 "source_blend_sha256":build["baseline_sha256"],
 "new_blend_sha256":current["blend_sha256"],
 "blender":current["blender"],
 "base_meshes":82,"added_new_candidate_meshes":7,"total_meshes":89,
 "original_82_exact_mesh_and_matrix":True,"new_seven_derived_rigid_copy":True,
 "max_world_delta_error_mm":max_error,"world_tolerance_mm":.001,
 "source_to_target_translation_mm":list(delta),
 "pair_count":n,"max_overlap_mm3":greatest,"max_permitted_overlap_mm3":1,
 "overlap_failures":bad,
 "new_contact_count":len(contact_rows),"contact_details":contact_rows,
 "source_43_interface_regression":"PRESERVED_BY_EXACT_IDENTITY_OF_ALL_82_SOURCE_MESHES_NOT_RECALCULATED",
 "note":"PASS is only tested CAD spatial compatibility; it is NOT historical exact form, strength, west-specific measurement, or PO approval.",
 "existing_approval_boundaries_unchanged":True,"po_west_assembly_approval":False}
(out/"WEST_SPACER_VALIDATION.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k not in ("contact_details","overlap_failures")},ensure_ascii=False,indent=2))
assert good, "WEST_SPACER_ASSEMBLY_GATE_FAILED"
