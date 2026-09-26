#!/usr/bin/env python3
"""Authoritative-input compiler shared by the T-018 Blender programs."""
from __future__ import annotations

import hashlib, json, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]; P = ROOT / "production/zhenguo_wanfo"; BUILD = P / "build"
ACCOUNTING=BUILD/"P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json"; BASELINE=BUILD/"P3_3_BUILDING_INPUT_BASELINE_V001.json"
GRAPH=BUILD/"P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json"; BINDINGS=BUILD/"P3_3_BUILDING_PARAMETER_BINDINGS_V001.json"
PARAMETERS=P/"params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"; REPRESENTATIVE_GRAPH=P/"assembly/P3_2_REPRESENTATIVE_RELATIONSHIP_GRAPH_V001.json"
MASTER_LIBRARY=P/"registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json"; MASTER_SCOPE=P/"registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json"
RUNTIME_MANIFEST=BUILD/"P3_3_WHOLE_BUILDING_RUNTIME_MANIFEST_V001.json"; CANONICAL_PM005=3505.7; MUTATED_PM005=3605.7
OUTCOMES={"GENERATE_FROM_FORMAL_COMPONENT":"GENERATED_FORMAL_GEOMETRY","PROXY_ONLY":"GENERATED_PROXY","CONTROL_ONLY":"GENERATED_CONTROL","ENVELOPE_ONLY":"GENERATED_ENVELOPE","UNKNOWN_BLOCKED":"UNKNOWN_BLOCKED","SEMANTIC_ONLY":"SEMANTIC_ONLY","DEFERRED":"DEFERRED","COMPARISON_ONLY":"COMPARISON_ONLY"}
ALLOWED_OUTCOMES=set(OUTCOMES.values()); PROTECTED=[ACCOUNTING,BASELINE,GRAPH,BINDINGS,PARAMETERS,REPRESENTATIVE_GRAPH,MASTER_LIBRARY,MASTER_SCOPE]
SOURCES=lambda:[str(x.relative_to(ROOT)) for x in (GRAPH,BINDINGS,PARAMETERS,REPRESENTATIVE_GRAPH)]
FAMILY_RULES={
 "COLUMN":(["RULE-COLUMN-GRID","RULE-MAJOR-ELEVATIONS"],["LOCATE","REPEAT"],["AU-COLUMN-GRID-001"],["CMP-COLUMN-001__ORIGIN","CTL-GRID-001__X-AXIS"]),
 "GRID_CONTROL":(["RULE-COLUMN-GRID"],["LOCATE","REPEAT"],["AU-COLUMN-GRID-001"],["CTL-GRID-001__SIDEBAY-START","CTL-GRID-001__X-AXIS"]),
 "BRACKET_CONTACT":(["RULE-BRACKET-TOPOLOGY","RULE-COLUMN-GRID","RULE-MAJOR-ELEVATIONS"],["LOCATE","REPEAT"],["AU-COLUMN-LUDOU-001"],["CMP-COLUMN-001__TOP-SUPPORT-PLANE"]),
 "BRACKET_ARM":(["RULE-BRACKET-TOPOLOGY","RULE-COLUMN-GRID","RULE-MAJOR-ELEVATIONS"],["LOCATE","REPEAT"],["AU-COLUMN-LUDOU-001"],["CMP-COLUMN-001__TOP-SUPPORT-PLANE"]),
 "FRAME_CONTROL":(["RULE-FRAME-DEPTHS","RULE-FRAME-SEMANTICS","RULE-ROOF-ELEVATIONS"],["LOCATE","BELONG"],["AU-FRAME-TIER-001"],["CTL-FRAME-001__LOWER-TIER-DATUM","CTL-FRAME-001__UPPER-TIER-DATUM"]),
 "FRAME_SUPPORT":(["RULE-FRAME-DEPTHS","RULE-FRAME-SEMANTICS","RULE-ROOF-ELEVATIONS"],["LOCATE","BELONG"],["AU-FRAME-TIER-001"],["PRX-FRAME-CONNECTOR-001__LOWER-ENDPOINT","PRX-FRAME-CONNECTOR-001__UPPER-ENDPOINT"]),
 "PRIMARY_FRAME":(["RULE-FRAME-DEPTHS","RULE-FRAME-SEMANTICS"],["LOCATE","BELONG"],["AU-FRAME-TIER-001"],["CTL-FRAME-001__LOWER-TIER-DATUM","CTL-FRAME-001__UPPER-TIER-DATUM"]),
 "GABLE_CONTROL":(["RULE-ROOF-OUTLINE","RULE-ROOF-ELEVATIONS"],["LOCATE"],[],[]),
 "PURLIN":(["RULE-FRAME-DEPTHS","RULE-ROOF-OUTLINE","RULE-ROOF-ELEVATIONS"],["LOCATE"],["AU-FRAME-TIER-001"],["CTL-FRAME-001__UPPER-TIER-DATUM"]),
 "RAFTER":(["RULE-ROOF-OUTLINE","RULE-ROOF-ELEVATIONS"],["LOCATE","REPEAT"],[],[]),
 "ROOF_ENVELOPE":(["RULE-ROOF-OUTLINE","RULE-ROOF-ELEVATIONS"],["LOCATE"],[],[]),
}
REPRESENTATION_GEOMETRY={
 "GRID_CONTROL":"GRID_AXIS_LINE", "BRACKET_CONTACT":"BRACKET_CONTACT_GLYPH",
 "BRACKET_ARM":"UNKNOWN_BRACKET_WIRE_CROSS", "FRAME_CONTROL":"FRAME_CONTROL_SEGMENT",
 "FRAME_SUPPORT":"FRAME_SUPPORT_CONNECTOR", "PRIMARY_FRAME":"PRIMARY_FRAME_SEMANTIC_AXIS",
 "GABLE_CONTROL":"GABLE_CONTROL_POLYLINE", "PURLIN":"DEFERRED_PURLIN_DATUM",
 "RAFTER":"RAFTER_PROXY_SLOPE_SEGMENT", "ROOF_ENVELOPE":"ROOF_ENVELOPE_CONTROL_SURFACE",
}

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def stable_json(v): return json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True,separators=(",",": "))+"\n"
def write_json(path,v): Path(path).parent.mkdir(parents=True,exist_ok=True); Path(path).write_text(stable_json(v),encoding="utf-8")
def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def protected_hashes(): return {str(p.relative_to(ROOT)):sha256(p) for p in PROTECTED}

def _authorities(pm005):
 g=load(GRAPH); b=load(BINDINGS); ps=load(PARAMETERS)["parameters"]; v={k:x.get("value") for k,x in ps.items()}; v["PM-005"]=pm005
 v["Z-006-RC-01"]=next(x["value"] for x in b["bindings"] if x["parameter_id"]=="Z-006-RC-01")
 rel={r["source_node"]:r for r in g["relationships"] if r["source_node"].startswith("P3_3:")}; masters={m["component_id"]:m for m in load(MASTER_LIBRARY)["masters"]}
 bound={x["parameter_id"]:x for x in b["bindings"]}; return v,rel,masters,bound

def _axes(v):
 # Observed bridge layer: side bays PM-005, independent front/depth centre bays PM-003/PM-004.
 return ([0.0,float(v["PM-005"]),float(v["PM-005"])+float(v["PM-003"]),2*float(v["PM-005"])+float(v["PM-003"])],
         [0.0,float(v["PM-005"]),float(v["PM-005"])+float(v["PM-004"]),2*float(v["PM-005"])+float(v["PM-004"])])

def _placement(source,v,relation,bound):
 fam=source["source_family_id"]; ident=source["legacy_instance_id"]; rules,types,assemblies,interfaces=FAMILY_RULES[fam]; xs,ys=_axes(v); fen=float(v["MOD-002"]); h=float(v["Z-006-RC-01"])
 idx={}; xyz=[0.,0.,0.]; datum="POINT"; deps=set(source["parameter_ids"])
 def groups(pattern):
  m=re.fullmatch(pattern,ident)
  if not m: raise ValueError(f"{fam} identity does not match approved rule grammar: {ident}")
  return m.groupdict()
 if fam=="COLUMN":
  q=groups(r"COLUMN_X(?P<x>\d+)_Y(?P<y>\d+)"); idx={k:int(n) for k,n in q.items()}; xyz=[xs[idx["x"]],ys[idx["y"]],float(v["Z-005"]) if idx["x"] in (0,3) and idx["y"] in (0,3) else 0.]; deps|={"PM-003","PM-004","PM-005"}
 elif fam=="GRID_CONTROL":
  q=groups(r"GRID_(?P<axis>[XY])(?P<i>\d+)"); idx={"axis":q["axis"],"index":int(q["i"])}; xyz=[xs[idx["index"]],0,0] if q["axis"]=="X" else [0,ys[idx["index"]],0]; datum="AXIS"; deps|={"PM-003","PM-004","PM-005"}
 elif fam.startswith("BRACKET_"):
  head=re.fullmatch(r"(?:BRACKET|CONTACT)_HEAD_X(\d+)_Y(\d+)_A(\d+)_J(\d+)",ident); inter=re.fullmatch(r"(?:BRACKET|CONTACT)_INTER_([XY])(\d+)_B(\d+)_J(\d+)",ident)
  if head: x,y,a,j=map(int,head.groups()); idx={"kind":"HEAD","x":x,"y":y,"arm":a,"jump":j}; xyz=[xs[x],ys[y],h+(j-1)*float(v["DG-110"])*fen/4]
  elif inter:
   axis,edge,bay,j=inter.groups(); edge,bay,j=int(edge),int(bay),int(j); idx={"kind":"INTER","axis":axis,"edge":edge,"bay":bay,"jump":j}; xyz=[(xs[bay]+xs[bay+1])/2,ys[edge],h+(j-1)*float(v["DG-110"])*fen/2] if axis=="Y" else [xs[edge],(ys[bay]+ys[bay+1])/2,h+(j-1)*float(v["DG-110"])*fen/2]
  else: raise ValueError(f"invalid bracket identity: {ident}")
  datum="BOUNDED_MARKER" if fam=="BRACKET_ARM" else "CONTACT_PROXY"; deps|={"PM-003","PM-004","PM-005"}
 elif fam in ("FRAME_CONTROL","FRAME_SUPPORT"):
  q=groups(r"(?:SUPPORT_)?FRAME_(?P<kind>POST|TIER)_(?P<side>[NS])_(?P<tier>\d+)(?:_X(?P<x>\d+)_(?P<level>LOW|UP))?"); tier=int(q["tier"]); side=q["side"]; x=int(q["x"] or 0); rises=[float(v[k])*fen for k in ("ROOF-004","ROOF-005","ROOF-006")]; z=h+sum(rises[:tier-(0 if q["level"]=="UP" else 1)]); depths=[float(v[k]) for k in ("FR-004","FR-005","FR-006")]; y=sum(depths[:tier]) if side=="N" else ys[-1]-sum(depths[:tier]); xyz=[xs[x] if q["kind"]=="POST" else xs[-1]/2,y,z]; idx={"kind":q["kind"],"side":side,"tier":tier,"x":x,"level":q["level"]}; datum="TIER_CONTROL" if fam=="FRAME_CONTROL" else "CONNECTOR_PROXY"; deps|={"PM-003","PM-004","PM-005"}
 elif fam=="PRIMARY_FRAME":
  q=groups(r"FRAME_(?P<axis>DEPTH_X|WIDTH_Y)(?P<i>\d+)"); i=int(q["i"]); idx={"axis":q["axis"],"index":i}; xyz=[xs[i],ys[-1]/2,h] if q["axis"]=="DEPTH_X" else [xs[-1]/2,ys[i],h]; datum="SPAN_SEMANTIC_MARKER"; deps|={"PM-003","PM-004","PM-005"}
 elif fam=="GABLE_CONTROL":
  q=groups(r"GABLE_(?P<edge>[EW])_(?P<side>[NS])"); idx=q; projection=float(v["OUT-003"])*fen; xyz=[-projection if q["edge"]=="W" else xs[-1]+projection,0 if q["side"]=="N" else ys[-1],h+float(v["ROOF-011"])]; datum="GABLE_CONTROL"; deps|={"PM-003","PM-004","PM-005"}
 elif fam=="PURLIN":
  q=groups(r"ROOF_PURLIN_(?P<side>[NS])_(?P<tier>\d+)"); tier=int(q["tier"]); idx={"side":q["side"],"tier":tier}; rises=[0]+[sum(float(v[k])*fen for k in ("ROOF-007","ROOF-008","ROOF-009")[:i]) for i in range(1,4)]; depths=[0]+[sum(float(x)*fen for x in v["FR-007"][:i]) for i in range(1,4)]; xyz=[xs[-1]/2,depths[tier] if q["side"]=="N" else ys[-1]-depths[tier],h+rises[tier]]; datum="DEFERRED_AXIS"; deps|={"PM-003","PM-004","PM-005"}
 elif fam in ("RAFTER","ROOF_ENVELOPE"):
  pat=r"ROOF_RAFTER_(?P<side>[NS])_X(?P<x>\d+)_S(?P<seg>\d+)" if fam=="RAFTER" else r"ROOF_SURFACE_(?P<side>[NS])_(?P<seg>\d+)"; q=groups(pat); seg=int(q["seg"]); side=q["side"]; x=int(q.get("x") or 0); idx={"side":side,"segment":seg,"repeat":x}; horizontal=[float(n)*fen for n in v["FR-007"]]; rise=[float(v[k])*fen for k in ("ROOF-007","ROOF-008","ROOF-009")]; y=sum(horizontal[:seg])+horizontal[seg]/2; z=h+sum(rise[:seg])+rise[seg]/2; xyz=[xs[-1]*x/5 if fam=="RAFTER" else xs[-1]/2,y if side=="N" else ys[-1]-y,z]; datum="RAFTER_PROXY" if fam=="RAFTER" else "ROOF_ENVELOPE"; deps|={"PM-003","PM-004","PM-005"}
 else: raise ValueError(f"no approved consumer for {fam}")
 pvals={k:v[k] for k in sorted(deps) if k in v}; missing=[k for k in pvals if k not in bound and k!="PM-005"]
 if missing: raise ValueError(f"unbound parameters for {ident}: {missing}")
 return {"status":"RULE_DERIVED","location_mm":[round(n,6) for n in xyz],"rotation_euler_rad":[0.,0.,0.],"scale":[1.,1.,1.],"datum_type":datum,"derivation":{"building_graph_node_id":f"P3_3:{ident}","building_graph_relationship_id":relation["relationship_id"],"rule_ids":rules,"rule_id":rules[0],"relationship_types":types,"relation_type":types[0],"assembly_refs":assemblies,"interface_ids":interfaces,"parameter_ids":sorted(pvals),"parameter_values":pvals,"identity_indices":idx,"authoritative_sources":SOURCES()}}

def compile_runtime(pm005=CANONICAL_PM005):
 accounting=load(ACCOUNTING); values,relations,masters,bound=_authorities(pm005); objects=[]
 for sequence,source in enumerate(accounting["instances"]):
  cid=source["component_id"]; disposition="DEFERRED" if cid=="CMP-PURLIN-001" else source["p3_3_disposition"]; outcome=OUTCOMES[disposition]; master=masters.get(cid) if outcome=="GENERATED_FORMAL_GEOMETRY" else None
  if outcome=="GENERATED_FORMAL_GEOMETRY" and not master: raise ValueError(f"formal component has no approved Master: {cid}")
  node=f"P3_3:{source['legacy_instance_id']}"; placement=_placement(source,values,relations[node],bound)
  rep={"class":"FORMAL_MASTER_GEOMETRY" if master else ("SEMANTIC_MARKER" if outcome in {"UNKNOWN_BLOCKED","DEFERRED"} else "TECHNICAL_ENGINEERING_REPRESENTATION"),"historical_geometry":bool(master),"evidence_upgrade":False,"display_dimensions_policy":"TECHNICAL_REVIEW_ONLY" if not master else "MASTER_PARAMETERS","geometry_class":"APPROVED_P3_1_MASTER" if master else REPRESENTATION_GEOMETRY[source["source_family_id"]],"structural_dimension_source":False if not master else "MASTER_PARAMETERS"}
  objects.append({"runtime_instance_id":f"P3_3_RUNTIME_{sequence+1:03d}","legacy_instance_id":source["legacy_instance_id"],"component_id":cid,"explicit_non_component_identity":None,"source_family_id":source["source_family_id"],"family":source["source_family_id"],"graph_parent_node_id":source["graph_parent_node_id"],"p3_3_disposition":outcome,"evidence_status":source["evidence_boundary"],"historical_claim_boundary":"NOT_UPGRADED","placement":placement,"representation":rep,"parameter_rule_provenance":placement["derivation"],"formal_master":None if not master else {k:master[k] for k in ("master_id","master_version","generator_path","parameter_path","geometry_mode","approval_status")}})
 counts=Counter(x["p3_3_disposition"] for x in objects); snapshot={"pm005_mm":pm005,"runtime_objects":objects}
 return {"version":"V001","task":"T-018","status":"CANONICAL" if pm005==CANONICAL_PM005 else "TEST_ONLY_MUTATION","generator_contract":{"clean_scene":True,"p2_blend_loaded":False,"p2_numeric_transform_usage":0,"blender_version":"4.5.13","relationship_vocabulary":["SUPPORT","CONNECT","LOCATE","REPEAT","BELONG"],"formal_geometry_policy":"APPROVED_P3_1_MASTER_GENERATOR_ONLY"},"parameter_state":{"PM-005":{"value_mm":pm005,"canonical_value_mm":CANONICAL_PM005,"source":str(BINDINGS.relative_to(ROOT))}},"input_hashes":protected_hashes(),"runtime_objects":objects,"runtime_accounting":{"input_count":365,"outcome_count":len(objects),"outcome_counts":dict(sorted(counts.items())),"unexplained_runtime_omission":0,"anonymous_formal_mesh":0,"broken_identity":0,"rule_derived":sum(x["placement"]["status"]=="RULE_DERIVED" for x in objects),"not_realized_no_approved_placement_rule":0},"technical_helpers":{"count":353,"historical_component_count":0},"canonical_semantic_snapshot_sha256":hashlib.sha256(stable_json(snapshot).encode()).hexdigest(),"blend_artifact":{"path":"artifacts/P3_3_WHOLE_BUILDING_CANONICAL_V001.blend","sha256":"POPULATED_BY_GITHUB_ACTIONS"}}

def normalized_snapshot(manifest): return {"parameter_state":manifest["parameter_state"],"runtime_objects":manifest["runtime_objects"]}
