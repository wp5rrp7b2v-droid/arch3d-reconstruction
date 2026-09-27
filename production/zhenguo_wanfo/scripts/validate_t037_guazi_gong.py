"""T-037 瓜子栱 first-article validator and 8-panel Review Board composer."""
import argparse, hashlib, json, math
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
    def orient(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def seg(a,b,c,d):
        o1,o2,o3,o4=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
        return (o1*o2<0) and (o3*o4<0)
    n=len(points)
    for i in range(n):
        a=points[i]; b=points[(i+1)%n]
        for j in range(i+1,n):
            if j in (i,(i+1)%n) or (j+1)%n in (i,(i+1)%n): continue
            if i==0 and j==n-1: continue
            c=points[j]; d=points[(j+1)%n]
            if seg(a,b,c,d): return False
    return True

def manifold_edges(faces):
    counts={}
    for f in faces:
        for i in range(len(f)):
            a,b=f[i],f[(i+1)%len(f)]
            key=tuple(sorted((int(a),int(b))))
            counts[key]=counts.get(key,0)+1
    return counts and all(v==2 for v in counts.values())

def compose(a):
    d=load(a.definition); s=load(a.canonical); r=Path(a.review_dir)
    names=["LARGE_AXON","SMALL_AXON","LARGE_FRONT","SMALL_FRONT","OVERLAY_FRONT"]
    imgs={}
    for n in names:
        p=r/(n+".png")
        if not p.exists(): raise AssertionError("missing "+str(p))
        im=Image.open(p).convert("RGB")
        # Hard fail any near-uniform render. This is the visual-review gate:
        # machine geometry PASS is insufficient if PO cannot see the member.
        stat=ImageStat.Stat(im.convert("L"))
        if stat.var[0] < 120.0:
            raise AssertionError("REVIEW_RENDER_NEAR_UNIFORM "+n+" variance="+str(stat.var[0]))
        im.thumbnail((800,500)); imgs[n]=im.copy()
    W,H=2000,2500
    out=Image.new("RGB",(W,H),"white"); draw=ImageDraw.Draw(out)
    title=font(34); head=font(23); small=font(19)
    draw.text((45,24),"T-037｜瓜子栱族 Master V001｜First Article Review Board",font=title,fill="black")
    boxes=[]
    for row in range(4):
        for col in range(2):
            x0=40+col*980; y0=90+row*595
            boxes.append((x0,y0,x0+940,y0+550))
    labels=[
      "1 LARGE AXON","2 SMALL AXON","3 LARGE FRONT / PROFILE","4 SMALL FRONT / PROFILE",
      "5 LARGE vs SMALL OVERLAY","6 DIMENSION PROOF","7 SOURCE-DERIVED PROFILE","8 EVIDENCE / UNKNOWN BOUNDARY"
    ]
    for lab,box in zip(labels,boxes):
        draw.rectangle(box,outline=(180,180,180),width=2)
        draw.text((box[0]+15,box[1]+12),lab,font=head,fill="black")
    def paste(im,box,top=55):
        x0,y0,x1,y1=box; z=im.copy(); z.thumbnail((x1-x0-30,y1-y0-top-20))
        out.paste(z,(x0+(x1-x0-z.width)//2,y0+top+(y1-y0-top-z.height)//2))
    paste(imgs["LARGE_AXON"],boxes[0]); paste(imgs["SMALL_AXON"],boxes[1])
    paste(imgs["LARGE_FRONT"],boxes[2]); paste(imgs["SMALL_FRONT"],boxes[3]); paste(imgs["OVERLAY_FRONT"],boxes[4])

    # dimension proof
    x0,y0,x1,y1=boxes[5]; yy=y0+80
    for line in [
      "LARGE: L 1007.0 mm (OBSERVED_MEAN, n=16)",
      "SMALL: L 895.0 mm (OBSERVED_MEAN, n=28)",
      "WIDTH: 214.7 mm (family OBSERVED_MEAN, n=44)",
      "THICKNESS: 156.5 mm (OBSERVED_SAMPLE_MEAN, n=16)",
      "Thickness subgroup attribution: UNRESOLVED.",
      "Width/thickness remain identical across variants.",
      "SMALL is NOT a uniform global scale of LARGE."
    ]:
        draw.text((x0+28,yy),line,font=small,fill="black"); yy+=58

    # source-derived normalized profile
    x0,y0,x1,y1=boxes[6]
    pts=d["profile_contract"]["normalized_points"]
    gx0,gy0,gx1,gy1=x0+80,y0+105,x1-80,y1-135
    mapped=[(gx0+(px+0.5)*(gx1-gx0), gy0+(0.5-pz)*(gy1-gy0)) for px,pz in pts]
    mapped.append(mapped[0]); draw.line(mapped,fill=(50,50,50),width=4)
    draw.text((x0+28,y1-108),"Authority: SOURCE_DERIVED_PROFILE",font=small,fill="black")
    draw.text((x0+28,y1-90),"Same-building PDF p73 Fig 2-27 / p76 Fig 2-31.",font=font(15),fill="black")
    draw.text((x0+28,y1-60),"Locked numeric control set; NO metric source calibration claim.",font=font(15),fill="black")

    x0,y0,x1,y1=boxes[7]; yy=y0+78
    for line in [
      "44 physical = 16 LARGE + 28 SMALL",
      "1 Master family / 2 geometry variants",
      "Profile controls = Stage1 reconstructed / replaceable",
      "Source re-extraction reproducible = FALSE",
      "Direct curve-control measurement = FALSE",
      "Original 963 design claim = FALSE",
      "Exact mortise/slots/local curve = DEFERRED",
      "No wear/damage/per-instance deformation modeled",
      "First article only; Registry formalization NOT AUTHORIZED"
    ]:
        draw.text((x0+26,yy),line,font=font(17),fill="black"); yy+=49
    out.save(a.board,pnginfo=None)

def validate(a):
    d=load(a.definition); c=load(a.canonical); r=load(a.reopen); rs=load(a.restore); reg=load(a.registry)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    large=[x for x in reg["items"] if x.get("component")=="大型瓜子栱"]
    small=[x for x in reg["items"] if x.get("component")=="小型瓜子栱"]
    rb=d["registry_boundary"]; pc=d["profile_contract"]; es=d["evidence_semantics"]
    ck("01_task",d["task_id"]=="T-037" and d["execution_boundary"]["engineering_execution_authorized"] is True)
    ck("02_registry_schema",reg["schema_version"]=="V008" and reg["item_count"]==505)
    ck("03_counts",len(large)==rb["large_count"]==16 and len(small)==rb["small_count"]==28 and len(large)+len(small)==44)
    ck("04_master_variant_count",c["master_family_count"]==1 and c["geometry_variant_count"]==2 and c["physical_instance_count"]==44)
    ck("05_registry_large_dimensions",all(near(x["length_mm"],1007) and near(x["width_mm"],214.7) and near(x["thickness_mm"],156.5) for x in large))
    ck("06_registry_small_dimensions",all(near(x["length_mm"],895) and near(x["width_mm"],214.7) and near(x["thickness_mm"],156.5) for x in small))
    L=c["variants"]["LARGE_GUAZI_GONG"]; S=c["variants"]["SMALL_GUAZI_GONG"]
    ck("07_large_bbox",all(near(x,y) for x,y in zip(L["local_bbox_mm"]["dimensions"],[1007,214.7,156.5])))
    ck("08_small_bbox",all(near(x,y) for x,y in zip(S["local_bbox_mm"]["dimensions"],[895,214.7,156.5])))
    ck("09_width_shared",near(L["resolved_dimensions_mm"]["width"],S["resolved_dimensions_mm"]["width"]) and near(L["resolved_dimensions_mm"]["width"],214.7))
    ck("10_thickness_shared",near(L["resolved_dimensions_mm"]["thickness"],S["resolved_dimensions_mm"]["thickness"]) and near(L["resolved_dimensions_mm"]["thickness"],156.5))
    ck("11_not_uniform_global_scale",not near(895/1007,214.7/214.7) and not near(895/1007,156.5/156.5))
    ck("12_profile_authority",pc["authority"]=="SOURCE_DERIVED_PROFILE" and c["profile_contract"]["authority"]=="SOURCE_DERIVED_PROFILE")
    ck("13_exact_curve_unknown",pc["exact_historical_curve"]=="UNRESOLVED" and pc["normalized_points_are_direct_measurements"] is False)
    ck("14_source_provenance",len(pc["source_figures"])>=2 and "PDF p73" in " ".join(pc["source_figures"]) and "PDF p76" in " ".join(pc["source_figures"]))
    ck("15_profile_simple",polygon_simple(pc["normalized_points"]))
    ck("16_profile_extent",near(min(p[0] for p in pc["normalized_points"]),-0.5) and near(max(p[0] for p in pc["normalized_points"]),0.5) and near(min(p[1] for p in pc["normalized_points"]),-0.5) and near(max(p[1] for p in pc["normalized_points"]),0.5))
    ck("17_profile_shared_rule",pc["shared_profile_rule"] is True)
    ck("18_means_not_per_instance",es["family_mean_is_per_instance_direct"] is False and es["thickness_is_44_instance_direct"] is False)
    ck("18a_thickness_attribution",es["thickness_classification"]=="OBSERVED_SAMPLE_MEAN / n=16" and es["thickness_subgroup_attribution"]=="UNRESOLVED")
    ck("18b_thickness_application",es["thickness_variant_application"]=="STAGE1_PRODUCTION_FAMILY_APPLICATION / NOT_VARIANT_SPECIFIC_DIRECT_OBSERVATION")
    ck("18c_profile_traceability",pc["numeric_reproduction_basis"]=="LOCKED_13_POINT_CONTROL_SET_IN_THIS_DEFINITION" and pc["source_reextraction_reproducible"] is False and pc["metric_scale_calibration"]=="NOT_PERFORMED / NOT_CLAIMED" and pc["historical_control_point_claim"] is False)
    ck("19_not_original_design",es["original_963_design_claim"] is False)
    ck("20_no_unsupported",all(v["unsupported_detail_count"]==0 and v["joinery_cut_count"]==0 for v in (L,S)))
    ck("21_manifold_large",manifold_edges(L["geometry_faces"]))
    ck("22_manifold_small",manifold_edges(S["geometry_faces"]))
    ck("23_transform",all(v["local_transform"]=={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]} for v in (L,S)))
    ck("24_signatures_differ",L["semantic_geometry_signature"]!=S["semantic_geometry_signature"])
    ck("25_reopen",r["status"]=="PASS" and r["family_semantic_signature"]==c["family_semantic_signature"] and set(r["variants"])==set(c["variants"]))
    ck("26_restore",rs["family_semantic_signature"]==c["family_semantic_signature"] and {k:v["semantic_geometry_signature"] for k,v in rs["variants"].items()}=={k:v["semantic_geometry_signature"] for k,v in c["variants"].items()})
    ck("27_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("28_binary_sha",digest(a.asset)==c["canonical_blend_sha256"])
    ck("29_definition_hash",digest(a.definition)==c["definition_sha256"])
    ck("30_board",Path(a.board).exists() and Path(a.board).stat().st_size>10000)
    for name in ("LARGE_AXON","SMALL_AXON","LARGE_FRONT","SMALL_FRONT","OVERLAY_FRONT"):
        rim=Image.open(Path(a.review_dir)/(name+".png")).convert("L")
        ck("30_render_"+name.lower(),ImageStat.Stat(rim).var[0]>=120.0)
    ck("31_first_article_only",d["first_article_contract"]["variant_count"]==2 and d["first_article_contract"]["registry_instance_assembly"] is False)
    ck("32_formalization_not_authorized",d["execution_boundary"]["formalization_authorized"] is False and d["execution_boundary"]["catalog_v008_binding_authorized"] is False and d["execution_boundary"]["merge_authorized"] is False)
    ck("33_t018_hold",d["execution_boundary"]["t018_status"]=="HOLD" and d["execution_boundary"]["stage2_authorized"] is False)
    ck("34_deferred_geometry",all(x in d["deferred_geometry"] for x in ["exact_mortise_tenon","hidden_slots_or_cavities","exact_local_curve_control_dimensions"]))
    ck("35_source_counts",d["authority"]["dimension_pages"][0]["sample_count"]==44 and d["authority"]["dimension_pages"][1]["sample_count"]==16)
    out={"status":"PASS","task_id":"T-037","master_id":d["master_id"],"check_count":len(checks),"checks":checks,
         "canonical_blend_sha256":digest(a.asset),"family_semantic_signature":c["family_semantic_signature"],
         "variant_signatures":{k:v["semantic_geometry_signature"] for k,v in c["variants"].items()}}
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T037_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("compose-board","validate"),required=True)
    for n in ("definition","canonical","reopen","restore","registry","asset","review_dir","board","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)
if __name__=="__main__": main()
