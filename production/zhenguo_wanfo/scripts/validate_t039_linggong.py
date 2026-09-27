"""T-039 令栱 first-article validator and 8-domain Review Board composer."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,t=1e-3): return abs(float(a)-float(b))<=t

def font(size=24):
    for p in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"):
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def polygon_simple(points):
    def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def seg(a,b,c,d):
        o1,o2,o3,o4=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
        return (o1*o2<0) and (o3*o4<0)
    n=len(points)
    for i in range(n):
        a,b=points[i],points[(i+1)%n]
        for j in range(i+1,n):
            if j in (i,(i+1)%n) or (j+1)%n in (i,(i+1)%n): continue
            if i==0 and j==n-1: continue
            if seg(a,b,points[j],points[(j+1)%n]): return False
    return True

def manifold_edges(faces):
    counts={}
    for f in faces:
        for i in range(len(f)):
            k=tuple(sorted((int(f[i]),int(f[(i+1)%len(f)]))))
            counts[k]=counts.get(k,0)+1
    return counts and all(v==2 for v in counts.values())

def compose(a):
    d=load(a.definition); s=load(a.canonical); r=Path(a.review_dir)
    names=["AXON","FRONT_PROFILE","END_WIDTH"]; imgs={}
    for n in names:
        p=r/(n+".png")
        if not p.exists(): raise AssertionError("missing "+str(p))
        im=Image.open(p).convert("RGB"); var=ImageStat.Stat(im.convert("L")).var[0]
        if var<120.0: raise AssertionError("REVIEW_RENDER_NEAR_UNIFORM "+n+" variance="+str(var))
        im.thumbnail((820,480)); imgs[n]=im.copy()
    W,H=2000,2500; out=Image.new("RGB",(W,H),"white"); draw=ImageDraw.Draw(out)
    title=font(34); head=font(23); small=font(20)
    draw.text((45,24),"T-039｜令栱 Master V001｜First Article Review Board",font=title,fill="black")
    boxes=[(40+c*980,90+r0*595,980+c*980,640+r0*595) for r0 in range(4) for c in range(2)]
    labels=["1 AXON","2 FRONT / PROFILE","3 END / WIDTH","4 DIMENSION PROOF",
            "5 28 INSTANCES / ZERO VARIANT","6 PROFILE PROVENANCE","7 SOURCE vs RECONSTRUCTION","8 UNKNOWN / DEFERRED"]
    for lab,box in zip(labels,boxes):
        draw.rectangle(box,outline=(180,180,180),width=2); draw.text((box[0]+15,box[1]+12),lab,font=head,fill="black")
    def paste(im,box):
        z=im.copy(); z.thumbnail((box[2]-box[0]-30,box[3]-box[1]-75))
        out.paste(z,(box[0]+(box[2]-box[0]-z.width)//2,box[1]+60))
    paste(imgs["AXON"],boxes[0]); paste(imgs["FRONT_PROFILE"],boxes[1]); paste(imgs["END_WIDTH"],boxes[2])
    dims=d["canonical_reference_geometry_mm"]
    texts=[
      [f'L = {dims["length"]} mm',f'W = {dims["width"]} mm',f'T = {dims["thickness"]} mm',"DIRECT_PRIMARY / OBSERVED_MEAN / n=28","NOT per-instance exact / NOT 963 design"],
      ["28 Registry records","South 7 / North 7 / East 7 / West 7","1 shared Master / 0 geometry Variant","sample-to-instance mapping = UNKNOWN"],
      ["LINGGONG_PROFILE_CONTROL_SET_V001_C01","14 normalized points",d["profile_contract"]["classification"],"metric calibration = NOT PERFORMED"],
      ["DIRECT: L/W/T observed means","RECONSTRUCTION: 14-point simplified profile","same-building visual envelope only","no generic Song-template substitution"],
      ["exact historical curve = UNRESOLVED","exact end shaping = UNRESOLVED","mortise/tenon + grooves + slots = DEFERRED","wear / damage / deformation = DEFERRED"]
    ]
    for box,lines in zip(boxes[3:],texts):
        y=box[1]+72
        for line in lines:
            draw.text((box[0]+28,y),line,font=small,fill="black"); y+=52
    Path(a.board).parent.mkdir(parents=True,exist_ok=True); out.save(a.board)

def validate(a):
    d=load(a.definition); c=load(a.canonical); ro=load(a.reopen); rs=load(a.restore); reg=load(a.registry)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    items=reg["items"]; target=[x for x in items if x.get("component")=="令栱"]
    ids=[x["id"] for x in target]
    dirs={k:sum(1 for x in ids if f"令栱-{k}-" in x) for k in ("南","北","东","西")}
    body=c["canonical_body"]; dims=body["resolved_dimensions_mm"]; bb=body["local_bbox_mm"]["dimensions"]
    p=d["profile_contract"]["normalized_points"]
    ck("01_task",d["task_id"]=="T-039" and c["task_id"]=="T-039")
    ck("02_registry_schema",reg.get("schema_version")=="V008")
    ck("03_registry_total",len(items)==505)
    ck("04_target_count",len(target)==28)
    ck("05_direction_distribution",dirs=={"南":7,"北":7,"东":7,"西":7})
    ck("06_master_variant_count",c["master_family_count"]==1 and c["geometry_variant_count"]==0)
    ck("07_physical_count",c["physical_instance_count"]==28)
    ck("08_registry_dimensions",all(near(x["length_mm"],897) and near(x["width_mm"],217.4) and near(x["thickness_mm"],155.6) for x in target))
    ck("09_semantic_dimensions",near(dims["length"],897) and near(dims["width"],217.4) and near(dims["thickness"],155.6))
    ck("10_bbox",near(bb[0],897) and near(bb[1],217.4) and near(bb[2],155.6))
    ck("11_profile_authority",d["profile_contract"]["authority"]=="SAME_BUILDING_SOURCE_GUIDED_SIMPLIFIED")
    ck("12_profile_classification",d["profile_contract"]["classification"]=="SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT")
    ck("13_profile_control_set",d["profile_contract"]["candidate_id"]=="LINGGONG_PROFILE_CONTROL_SET_V001_C01" and d["profile_contract"]["point_count"]==14)
    ck("14_profile_signature",d["profile_contract"]["control_set_sha256"]=="0a3081110d36fea812739a942eca1522a510810f5ea52ee3b4c9ebaa51c1c1a7")
    ck("15_profile_approved",d["profile_contract"]["product_owner_approved"] is True)
    ck("16_profile_not_direct",d["profile_contract"]["normalized_points_are_direct_measurements"] is False)
    ck("17_metric_not_claimed",d["profile_contract"]["metric_scale_calibration"]=="NOT_PERFORMED / NOT_CLAIMED")
    ck("18_prior_reuse_false",d["profile_contract"]["t037_guazi_control_set_reused"] is False and d["profile_contract"]["t038_mangong_control_set_reused"] is False)
    ck("19_profile_simple",polygon_simple(p))
    ck("20_profile_extent",min(x for x,z in p)==-0.5 and max(x for x,z in p)==0.5 and min(z for x,z in p)==-0.5 and max(z for x,z in p)==0.5)
    ck("21_bilateral",d["profile_contract"]["bilateral_symmetry"] is True)
    ck("22_evidence_semantics",all("DIRECT_PRIMARY / OBSERVED_MEAN / n=28"==d["evidence_semantics"][k] for k in ("length_classification","width_classification","thickness_classification")))
    ck("23_not_per_instance",d["evidence_semantics"]["family_mean_is_per_instance_exact"] is False)
    ck("24_not_original_963",d["evidence_semantics"]["original_963_design_claim"] is False)
    ck("25_sample_mapping_unknown",d["registry_boundary"]["sample_to_instance_mapping"]=="UNKNOWN" and c["sample_to_instance_mapping"]=="UNKNOWN")
    ck("26_no_unsupported",body["unsupported_detail_count"]==0 and body["joinery_cut_count"]==0)
    ck("27_manifold",manifold_edges(body["geometry_faces"]))
    ck("28_transform",body["local_transform"]=={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]})
    ck("29_reopen",ro["status"]=="PASS" and ro["semantic_geometry_signature"]==body["semantic_geometry_signature"])
    ck("30_restore",rs["canonical_body"]["semantic_geometry_signature"]==body["semantic_geometry_signature"] and rs["family_semantic_signature"]==c["family_semantic_signature"])
    ck("31_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("32_binary_sha",c["canonical_blend_sha256"]==digest(a.asset))
    ck("33_definition_hash",c["definition_sha256"]==digest(a.definition))
    ck("34_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)
    for n in ("AXON","FRONT_PROFILE","END_WIDTH"):
        im=Image.open(Path(a.review_dir)/(n+".png")).convert("L")
        ck("35_render_"+n.lower(),ImageStat.Stat(im).var[0]>=120.0)
    ck("38_first_article_only",d["first_article_contract"]["canonical_body_count"]==1 and d["first_article_contract"]["registry_instance_assembly"] is False)
    ck("39_execution_authorized",d["execution_boundary"]["engineering_execution_authorized"] is True and d["execution_boundary"]["blender_execution_authorized"] is True)
    ck("40_formalization_not_authorized",d["execution_boundary"]["formalization_authorized"] is False and d["execution_boundary"]["catalog_v008_binding_authorized"] is False)
    ck("41_merge_close_not_authorized",d["execution_boundary"]["merge_authorized"] is False and d["execution_boundary"]["closure_authorized"] is False)
    ck("42_t018_stage2",d["execution_boundary"]["t018_status"]=="HOLD" and d["execution_boundary"]["stage2_authorized"] is False)
    ck("43_deferred",all(x in d["deferred_geometry"] for x in ["exact_mortise_tenon","grooves","slots","cavities","hidden_connection_cuts","exact_historical_profile_curve"]))
    out={"status":"PASS","task_id":"T-039","master_id":d["master_id"],"check_count":len(checks),"checks":checks,
         "canonical_blend_sha256":digest(a.asset),"family_semantic_signature":c["family_semantic_signature"],
         "geometry_signature":body["semantic_geometry_signature"],"profile_control_signature":d["profile_contract"]["control_set_sha256"]}
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T039_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("compose-board","validate"),required=True)
    for n in ("definition","canonical","reopen","restore","registry","asset","review_dir","board","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)
if __name__=="__main__": main()
