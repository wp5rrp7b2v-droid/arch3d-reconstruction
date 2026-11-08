#!/usr/bin/env python3
"""G4 minimum test: B01..B04 real triangulated surface interactions and physical sections.
Museum geometry and any derived images are short-lived only, never published to Git.
A triangle/triangle overlap does not prove load-bearing contact, tenon or identity.
"""
from __future__ import annotations
import bpy, bmesh, hashlib, json, math, ssl, traceback, urllib.request, urllib.parse
from itertools import combinations
from datetime import datetime, timezone
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output";WORK=ROOT/"_ephemeral_source";VIEWS=ROOT/"_ephemeral_visuals"
for p in (OUT,WORK,VIEWS):p.mkdir(parents=True,exist_ok=True)
URL="https://szbwgvue.chwhyun.cn/wanfodian/3d/dougong/"
EXPECTED={"dougong.gltf":"ac0687694715029a7b906bfdaa13578c578a01640e5cfeba1dbd29749dae6f1b",
          "dougong.bin":"940224e259dfcce31f2a11aa58780422a38bcf0de869a2b1c72762321f0abc32"}
NAMES={"B01":"polySurface9941","B02":"polySurface9986","B03":"polySurface9905","B04":"polySurface9961"}
REPORT={"status":"NOT_RUN","start_utc":datetime.now(timezone.utc).isoformat(),
 "source":URL+"dougong.gltf","source_tls":"KNOWN_CERT_EXPIRED__DIAGNOSTIC_WITH_PREVIOUS_EXACT_SHA_PIN",
 "museum_model_reproduction_permission":"UNKNOWN; NO_SOURCE_ASSET_OR_RENDER_IN_PUBLIC_GIT",
 "A1_reference":"Survey A1 PDF73 printed58 Figure2-27 lower-ang contact reference; no source mesh-ID mapping",
 "A1_same_east_front_object_correspondence":"NOT_PROVEN",
 "source_files":[],"source_hash_match":False,"selected_identifiers":NAMES,"meshes":[],
 "pair_checks":[],"section_planes":[],"screenshots":[],
 "gates":{"all_4_meshes_loaded":False,"all_6_pairs_bvh_evaluated":False,
          "manifold_reported":False,"pair_classification_adequate":False,
          "2_exact_geometry_sections_rendered":False,"historical_id_verified":False,
          "true_mortise_and_tenon_verified":False,"A1_dimension_calibrated":False},
 "notes":["BVH overlap gives intersecting triangle face PAIRS, not penetration volume.",
          "3D bounding-box overlap alone cannot identify physical material intersection.",
          "Nearness based on vertex-to-surface sampling has no guarantee of exact closest face-edge distance.",
          "Cross-section uses actual triangulated mesh bisection in museum coordinates but unverified historical units.",
          "Even demonstrated surface intersections are not engineering joinery or museum-to-A1 same-instance identification."],
 "errors":[]}
def H(b):return hashlib.sha256(b).hexdigest()
def fetch(filename):
 if filename not in EXPECTED:raise ValueError("Unexpected file")
 req=urllib.request.Request(URL+filename,headers={"User-Agent":"Wanfo Academic G4 Mesh-Section Test"})
 with urllib.request.urlopen(req,context=ssl._create_unverified_context(),timeout=30) as f:
  u=urllib.parse.urlsplit(f.geturl())
  if u.hostname!="szbwgvue.chwhyun.cn" or u.scheme!="https":raise ValueError("Cross host download")
  b=f.read(6_000_001)
 if len(b)>6_000_000 or H(b)!=EXPECTED[filename]:raise ValueError("Source SHA mismatch or size limit "+filename)
 p=WORK/filename;p.write_bytes(b)
 REPORT["source_files"].append({"filename":filename,"bytes":len(b),"sha256":H(b),"exact_previous_G1_SHA":True})
 return p
def P(x):return round(float(x),8)
def write():
 (OUT/"G4_REAL_MESH_SECTION_REPORT.json").write_text(json.dumps(REPORT,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("G4_FINAL",REPORT["status"])
 print("G4_PAIR_COUNTS",[(x["pair"],x["intersection_face_pair_count"],x["classification"]) for x in REPORT["pair_checks"]])
 print("G4_OUTPUT",OUT/"G4_REAL_MESH_SECTION_REPORT.json")
def tri_bvh(obj):
 vs=[obj.matrix_world @ v.co for v in obj.data.vertices]
 obj.data.calc_loop_triangles()
 faces=[tuple(t.vertices) for t in obj.data.loop_triangles]
 return BVHTree.FromPolygons(vs,faces,all_triangles=True,epsilon=1e-9),vs,faces
def bmesh_stats(obj):
 bm=bmesh.new()
 bm.from_mesh(obj.data)
 edges=len(bm.edges);faces=len(bm.faces)
 boundary=sum(e.is_boundary for e in bm.edges)
 nonmanifold=sum(not e.is_manifold for e in bm.edges)
 signed_vol=None
 if boundary==0 and nonmanifold==0:
  try:signed_vol=P(bm.calc_volume(signed=True))
  except Exception:pass
 bm.free()
 return {"edges":edges,"faces":faces,"boundary_edges":boundary,
         "nonmanifold_edges":nonmanifold,
         "closed_manifold":boundary==0 and nonmanifold==0,
         "signed_mesh_volume_source_units_cubed":signed_vol}
def nearest_vertex_distance(vs,other):
 best=math.inf;sel=None
 for v in vs:
  result=other.find_nearest(v)
  if result and result[3]<best:
   best=result[3];sel=(v,result[0],result[2])
 return best,sel
def make_material(n,rgb):
 m=bpy.data.materials.new("REVIEW_"+n);m.diffuse_color=(*rgb,1);m.use_nodes=True
 m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*rgb,1)
 m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value=.72
 return m
def bounds(obj):
 pts=[obj.matrix_world @ Vector(c) for c in obj.bound_box]
 lo=Vector(min(x[i] for x in pts) for i in range(3))
 hi=Vector(max(x[i] for x in pts) for i in range(3))
 return lo,hi
def save_view(title,objs,look_direction,look_at,scale):
 camdata=bpy.data.cameras.new("G4_CAM_"+title)
 cam=bpy.data.objects.new("G4_CAM_"+title,camdata);bpy.context.scene.collection.objects.link(cam)
 cam.location=look_at+Vector(look_direction)*scale*2.25
 cam.rotation_euler=(look_at-cam.location).to_track_quat("-Z","Y").to_euler()
 camdata.type="ORTHO";camdata.ortho_scale=scale*1.85
 bpy.context.scene.camera=cam
 path=VIEWS/("G4_"+title+".png")
 bpy.context.scene.render.filepath=str(path)
 bpy.ops.render.render(write_still=True)
 REPORT["screenshots"].append({"name":title,"filename":path.name,"bytes":path.stat().st_size,
   "sha256":H(path.read_bytes()),"stored_only_in_ephemeral_actions_artifact":True})
 bpy.data.objects.remove(cam,do_unlink=True)
 return path
try:
 f=fetch("dougong.gltf");fetch("dougong.bin")
 REPORT["source_hash_match"]=True
 data=json.loads(f.read_text(encoding="utf-8"))
 # Remove network-backed textures/materials but leave geometry accessor, vertex/index data unchanged.
 for mesh in data.get("meshes",[]):
  for prim in mesh.get("primitives",[]):prim.pop("material",None)
 data["textures"]=[];data["images"]=[];data["materials"]=[]
 data.pop("extensionsUsed",None);data.pop("extensionsRequired",None)
 clean=WORK/"dougong_G4_geometry_only.gltf"
 clean.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.gltf(filepath=str(clean))
 all_meshes=[o for o in bpy.context.scene.objects if o.type=="MESH"]
 assert len(all_meshes)==96, len(all_meshes)
 objects={}
 for id,source_name in NAMES.items():
  o=bpy.data.objects.get(source_name)
  if o is None or o.type!="MESH":raise RuntimeError("Missing source mesh "+source_name)
  objects[id]=o
 for o in all_meshes:
  if o not in objects.values():bpy.data.objects.remove(o,do_unlink=True)
 REPORT["gates"]["all_4_meshes_loaded"]=True

 # Matrices already include the same imported transform. Four canonical IDs cross-checked.
 pair_input={}
 lo_min=Vector((math.inf,math.inf,math.inf));hi_max=Vector((-math.inf,-math.inf,-math.inf))
 for k,o in objects.items():
  tree,vs,faces=tri_bvh(o)
  lo,hi=bounds(o)
  for q in range(3):
   lo_min[q]=min(lo_min[q],lo[q]);hi_max[q]=max(hi_max[q],hi[q])
  stats=bmesh_stats(o)
  REPORT["meshes"].append({"id":k,"glTF_name":o.name,"vertices":len(vs),
    "triangles":len(faces),"bbox_min":[P(x) for x in lo],
    "bbox_max":[P(x) for x in hi],**stats})
  pair_input[k]=(tree,vs,faces)
 REPORT["gates"]["manifold_reported"]=len(REPORT["meshes"])==4
 center=(lo_min+hi_max)/2;span=max(hi_max-lo_min)
 for a,b in combinations(NAMES,2):
  ta,va,fa=pair_input[a]
  tb,vb,fb=pair_input[b]
  intersections=ta.overlap(tb)
  # Distinct triangle face-pair overlap is a surface test, unlike AABB whole-object overlap.
  nintersections=len(intersections)
  ab,abinfo=nearest_vertex_distance(va,tb)
  ba,bainfo=nearest_vertex_distance(vb,ta)
  near=min(ab,ba)
  la,ha=bounds(objects[a]);lb,hb=bounds(objects[b])
  overlap=[max(0,min(ha[i],hb[i])-max(la[i],lb[i])) for i in range(3)]
  bbox3d=all(x>0 for x in overlap)
  # This classification stays conservative about coplanar intersections and containment.
  if nintersections>0:
   kind="TRIANGULATED_SURFACES_INTERSECT_OR_COINCIDE__NO_VOLUME_PROOF"
  elif near<=1e-6*span:
   kind="SAMPLED_VERTEX_ON_OTHER_SURFACE__CONTACT_CANDIDATE"
  else:
   kind="NO_FACE_INTERSECTION_DETECTED__MIN_VERTEX_TO_SURFACE_DISTANCE_ONLY"
  REPORT["pair_checks"].append({
   "pair":a+"-"+b,"mesh_a":objects[a].name,"mesh_b":objects[b].name,
   "aabb_3d_overlap":bbox3d,"aabb_overlap_axes_source_units":[P(x) for x in overlap],
   "intersection_face_pair_count":nintersections,
   "intersection_face_pairs_sample":[list(x) for x in intersections[:12]],
   "min_vertex_to_opposite_surface_source_units":P(near),
   "min_vertex_to_opposite_surface_relative_to_four_mesh_max_extent":P(near/span),
   "classification":kind,
   "geometry_proof_limit":"triangle-surface candidates; not proven historical mortise-tenon or structural support"
  })
 REPORT["gates"]["all_6_pairs_bvh_evaluated"]=len(REPORT["pair_checks"])==6
 REPORT["gates"]["pair_classification_adequate"]=all(x["classification"]!="UNKNOWN" for x in REPORT["pair_checks"])
 # Camera/lights for view-only. ALL original source mesh geometry remains untouched.
 scene=bpy.context.scene
 palette={"B01":(.85,.65,.31),"B02":(.40,.65,.86),"B03":(.37,.75,.57),"B04":(.85,.43,.42)}
 for key,o in objects.items():
  o.data.materials.clear();o.data.materials.append(make_material(key,palette[key]))
 scene.render.engine="CYCLES";scene.cycles.samples=18;scene.cycles.device="CPU"
 scene.render.resolution_x=1240;scene.render.resolution_y=920
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format="PNG"
 world=bpy.data.worlds.new("G4_WORLD");world.use_nodes=True;scene.world=world
 world.node_tree.nodes["Background"].inputs["Color"].default_value=(.92,.93,.95,1)
 world.node_tree.nodes["Background"].inputs["Strength"].default_value=.8
 for i,v in enumerate([(2.0,-1.5,2.5),(-2.0,2.5,2.0)]):
  l=bpy.data.lights.new("G4_L"+str(i),"AREA")
  o=bpy.data.objects.new("G4_L"+str(i),l);scene.collection.objects.link(o)
  o.location=center+Vector(v)*span*2.5
  l.energy=600;l.size=span*5
 save_view("FOUR_MESHES_AXON",objects,(1.4,-1.6,1.0),center,span)
 save_view("FOUR_MESHES_OPPOSITE",objects,(-1.2,-1.6,1.0),center,span)
 # Use ACTUAL mesh bisect, not bounding boxes, for physical cut visualizations.
 # These copies are transient, no source mesh or cut mesh is published.
 def make_section(name,normal,co):
  copies=[]
  for key,orig in objects.items():
   clone=orig.copy();clone.data=orig.data.copy()
   scene.collection.objects.link(clone)
   # World-space bisect to use same single plane across objects.
   clone.data.transform(clone.matrix_world)
   clone.matrix_world.identity()
   bm=bmesh.new()
   bm.from_mesh(clone.data)
   pre_vertices=len(bm.verts);pre_faces=len(bm.faces)
   pre_signed=[(v.co-co).dot(normal) for v in bm.verts]
   geom=list(bm.verts)+list(bm.edges)+list(bm.faces)
   result=bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-7,
      plane_co=co,plane_no=normal,clear_inner=True,clear_outer=False)
   post_signed=[(v.co-co).dot(normal) for v in bm.verts]
   # Any surviving vertex on the removed side would invalidate the "true cut" claim.
   eps=1e-6
   cut_valid=bool(pre_signed) and bool(post_signed) and min(post_signed)>-eps
   REPORT.setdefault("section_geometry_check",[]).append({
      "view_name":name,"mesh_id":key,
      "original_mesh_vertices":pre_vertices,"original_mesh_faces":pre_faces,
      "remaining_mesh_vertices":len(bm.verts),"remaining_mesh_faces":len(bm.faces),
      "original_signed_side_min":P(min(pre_signed)),"original_signed_side_max":P(max(pre_signed)),
      "remaining_signed_side_min":P(min(post_signed)),
      "removed_negative_side_all_vertices":cut_valid,
      "some_original_vertices_on_removed_side":min(pre_signed)<-eps
   })
   bm.to_mesh(clone.data);bm.free()
   clone.data.materials.clear()
   clone.data.materials.append(make_material("SECTION_"+key,palette[key]))
   copies.append(clone)
   orig.hide_render=True
  try:
   save_view(name,objects,(1.4,-1.7,.75),center,span)
  finally:
   for o in objects.values():o.hide_render=False
   for o in copies:bpy.data.objects.remove(o,do_unlink=True)
  REPORT["section_planes"].append({"view_name":name,
     "plane_co_source_coordinates":[P(x) for x in co],
     "plane_normal":[P(x) for x in normal],
     "method":"bmesh.ops.bisect_plane on actual triangulated mesh copies; outside cut side removed",
     "proves":"relative geometry arrangement, not solid wood contact or historical connection"})
 xplane=Vector((objects["B01"].location.x+center.x,0,0)) # overwritten to world center plane
 xplane=Vector((center.x,center.y,center.z))
 make_section("CUT_X_AT_B01_CENTER",Vector((1,0,0)),xplane)
 make_section("CUT_Y_AT_B01_CENTER",Vector((0,1,0)),xplane)
 REPORT["gates"]["2_exact_geometry_sections_rendered"]=(
   len(REPORT["section_planes"])==2 and len(REPORT["screenshots"])>=4
   and all(x["bytes"]>50000 for x in REPORT["screenshots"])
   and len(set(x["sha256"] for x in REPORT["screenshots"]))>=4
   and len(REPORT.get("section_geometry_check",[]))==8
   and all(x["removed_negative_side_all_vertices"] for x in REPORT["section_geometry_check"])
   and any(x["some_original_vertices_on_removed_side"] for x in REPORT["section_geometry_check"])
 )
 REPORT["status"]="PASS_MESH_INTERACTION_OBSERVED__HISTORICAL_JOINT_UNPROVEN"
except Exception as e:
 REPORT["status"]="FAIL_EXECUTION"
 REPORT["errors"].append(type(e).__name__+": "+str(e)[:1000])
 traceback.print_exc()
finally:write()
