"""T-036 bottom-dou first-article validator and review-board composer."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,t=1e-3): return abs(float(a)-float(b))<=t

def font(size=24):
    for p in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"):
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def compose(defn_path, review_dir, board_path):
    d=load(defn_path); r=Path(review_dir)
    rendered={}
    for n in ("AXON","FRONT","SIDE","TOP"):
        p=r/(n+".png")
        if not p.exists(): raise AssertionError("missing review "+str(p))
        im=Image.open(p).convert("RGB")
        im.thumbnail((680,430))
        rendered[n]=im.copy()

    W,H=1800,2200
    out=Image.new("RGB",(W,H),"white")
    draw=ImageDraw.Draw(out)
    title=font(34); head=font(22); small=font(18)
    draw.text((50,28),"T-036｜补间铺作底斗 Master V001 Review Board",font=title,fill="black")

    panels=[
        ("AXON",(50,100,860,620)),
        ("FRONT_PROFILE",(940,100,1750,620)),
        ("SIDE_PROFILE_AND_DEPTH_BOUNDARY",(50,690,860,1210)),
        ("TOP_BOTTOM_FOOTPRINTS",(940,690,1750,1210)),
        ("EVIDENCE_VS_COMPLETION",(50,1280,860,2110)),
        ("PROFILE_STABILITY",(940,1280,1750,2110)),
    ]
    for name,(x0,y0,x1,y1) in panels:
        draw.rectangle((x0,y0,x1,y1),outline=(190,190,190),width=2)
        draw.text((x0+18,y0+14),name,font=head,fill="black")

    def paste_center(im,box,top_pad=60):
        x0,y0,x1,y1=box
        avail=(x1-x0-36,y1-y0-top_pad-20)
        z=im.copy(); z.thumbnail(avail)
        out.paste(z,(x0+(x1-x0-z.width)//2,y0+top_pad+(y1-y0-top_pad-z.height)//2))

    paste_center(rendered["AXON"],panels[0][1])
    paste_center(rendered["FRONT"],panels[1][1])
    paste_center(rendered["SIDE"],panels[2][1])

    x0,y0,x1,y1=panels[3][1]
    cx=(x0+x1)//2; cy=(y0+y1)//2+25
    scale=2.0
    tw,td=255.56,240.0; bw,bd=178.56,165.1
    def rect(w,d,outline,width):
        ww=w*scale; dd=d*scale
        draw.rectangle((cx-ww/2,cy-dd/2,cx+ww/2,cy+dd/2),outline=outline,width=width)
    rect(tw,td,(70,70,70),4); rect(bw,bd,(140,140,140),4)
    draw.text((x0+35,y1-100),"TOP 255.56 × 240.0 (depth reconstructed)",font=small,fill="black")
    draw.text((x0+35,y1-60),"BOTTOM 178.56 × 165.1 (depth reconstructed)",font=small,fill="black")

    x0,y0,x1,y1=panels[4][1]
    lines=[
      "12 physical / 9 measured / north 3 unmeasured",
      "A1 mean: top W 255.56 / bottom W 178.56 / H 161.78 mm",
      "A1 profile evidence: flat H 38.333 / qi H 65.6 mm",
      "A1 top/bottom depth: UNKNOWN",
      "Production depth: 240.0 / 165.1 mm",
      "= PARAMETRIC_COMPLETION / NOT_A1_DIRECT",
      "Profile: CURVED_QI_PROFILE",
      "Exact curvature: UNKNOWN",
      "curve_amount: engineering reconstruction / replaceable",
      "1 Master / 0 Geometry Variant",
      "No inferred ears / slots / cavities / mortise-tenon"
    ]
    yy=y0+70
    for line in lines:
        draw.text((x0+28,yy),line,font=small,fill="black"); yy+=54

    x0,y0,x1,y1=panels[5][1]
    gx0,gy0,gx1,gy1=x0+90,y0+100,x1-70,y1-150
    draw.line((gx0,gy1,gx0,gy0),fill=(100,100,100),width=2)
    draw.line((gx0,gy1,gx1,gy1),fill=(100,100,100),width=2)
    for amount,col in ((0.25,(80,80,80)),(0.50,(130,130,130)),(0.75,(180,180,180))):
        pts=[]
        for i in range(101):
            t=i/100
            smooth=3*t*t-2*t*t*t
            frac=(1-amount)*t+amount*smooth
            px=gx0+frac*(gx1-gx0); py=gy1-t*(gy1-gy0)
            pts.append((px,py))
        draw.line(pts,fill=col,width=4)
    draw.text((x0+30,y1-115),"curve_amount tests: 0.25 / 0.50 / 0.75",font=small,fill="black")
    draw.text((x0+30,y1-75),"Same top/bottom envelope; non-historical.",font=small,fill="black")

    out.save(board_path)

def validate(a):
    d=load(a.definition); c=load(a.canonical); r=load(a.reopen); lo=load(a.curve_low); hi=load(a.curve_high); rs=load(a.restore); reg=load(a.registry)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    ck("01_identity",c["component_id"]==d["component_id"]=="CMP-DOU-BOTTOM-LONGKAI-001" and c["master_id"]==d["master_id"])
    ck("02_counts",d["physical_instance_count"]==12 and d["measured_instance_count"]==9 and d["geometry_variant_count"]==0)
    items=[x for x in reg["items"] if x.get("component")=="补间铺作底斗"]
    ck("03_registry_12",len(items)==12)
    ck("04_locations",set(x["location"] for x in items)==set(d["registry_contract"]["locations"]))
    ck("05_direct_width_height",near(c["resolved_parameters"]["top_width_mm"],255.56) and near(c["resolved_parameters"]["bottom_width_mm"],178.56) and near(c["resolved_parameters"]["total_height_mm"],161.78))
    ck("06_profile_evidence",near(d["profile_evidence"]["flat_height_mm"]["value"],38.333) and near(d["profile_evidence"]["qi_height_mm"]["value"],65.6))
    ck("07_no_breakpoint_claim",d["profile_evidence"]["flat_height_mm"]["geometry_breakpoint_claim"] is False and d["profile_evidence"]["qi_height_mm"]["geometry_breakpoint_claim"] is False)
    ed=d["evidence_depth_contract"]; ck("08_a1_depth_unknown",ed["a1_top_depth_mm"] is None and ed["a1_bottom_depth_mm"] is None)
    ck("09_prod_depth",near(c["resolved_parameters"]["top_depth_mm"],240.0) and near(c["resolved_parameters"]["bottom_depth_mm"],165.1))
    ck("10_depth_class",ed["production_classification"].startswith("PARAMETRIC_COMPLETION") and ed["historical_claim"] is False)
    pc=d["profile_contract"]; pg=c["profile_geometry"]
    ck("11_profile_class",pc["profile_class"]=="CURVED_QI_PROFILE" and pg["profile_class"]=="CURVED_QI_PROFILE")
    ck("12_exact_curve_unknown",pc["exact_curvature"]=="UNKNOWN" and pg["exact_curvature_claim"] is False)
    ck("13_single_parameter",pc["parameter_count"]==1 and pc["parameter_name"]=="curve_amount")
    ck("14_default_curve",near(pg["curve_amount"],pc["default_curve_amount"]))
    ck("15_bbox",all(near(x,y) for x,y in zip(c["body"]["local_bbox_mm"]["dimensions"],[255.56,240.0,161.78])))
    ck("16_bottom_section",near(c["sections_mm"]["bottom"]["width"],178.56) and near(c["sections_mm"]["bottom"]["depth"],165.1))
    ck("17_top_section",near(c["sections_mm"]["top"]["width"],255.56) and near(c["sections_mm"]["top"]["depth"],240.0))
    ck("18_transform",c["body"]["local_transform"]=={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]})
    ck("19_reopen",r["status"]=="PASS" and r["semantic_geometry_signature"]==c["semantic_geometry_signature"])
    ck("20_restore",rs["semantic_geometry_signature"]==c["semantic_geometry_signature"] and rs["body"]==c["body"])
    ck("21_curve_mutations_identity",lo["component_id"]==hi["component_id"]==c["component_id"])
    ck("22_curve_mutations_values",near(lo["profile_geometry"]["curve_amount"],0.25) and near(hi["profile_geometry"]["curve_amount"],0.75))
    for label,x in (("low",lo),("high",hi)):
        ck("23_"+label+"_bbox",all(near(q,w) for q,w in zip(x["body"]["local_bbox_mm"]["dimensions"],c["body"]["local_bbox_mm"]["dimensions"])))
        ck("24_"+label+"_bottom",x["sections_mm"]["bottom"]==c["sections_mm"]["bottom"])
        ck("25_"+label+"_top",x["sections_mm"]["top"]==c["sections_mm"]["top"])
        verts=x["body"]["geometry_vertices_mm"]; rings=[verts[i:i+4] for i in range(0,len(verts),4)]
        widths=[max(v[0] for v in ring)-min(v[0] for v in ring) for ring in rings]
        depths=[max(v[1] for v in ring)-min(v[1] for v in ring) for ring in rings]
        ck("26_"+label+"_monotonic",all(widths[i+1]>=widths[i]-1e-6 and depths[i+1]>=depths[i]-1e-6 for i in range(len(rings)-1)))
    ck("27_curve_changes_signature",lo["semantic_geometry_signature"]!=c["semantic_geometry_signature"] and hi["semantic_geometry_signature"]!=c["semantic_geometry_signature"])
    ck("28_unsupported_zero",c["body"]["unsupported_detail_count"]==0 and d["unsupported_geometry"]==[])
    ck("29_deferred",all(x in d["deferred_geometry"] for x in ["exact_dou_ear_profile","exact_top_slots_or_cavities","exact_bottom_mortise_tenon"]))
    ck("30_not_963",d["historical_963_design_dimensions"]=="UNRESOLVED")
    ck("31_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("32_binary_sha",digest(a.asset)==c["canonical_blend_sha256"])
    ck("33_board",Path(a.board).exists() and Image.open(a.board).size[0]>=1200)
    out={"status":"PASS","task_id":"T-036","component_id":d["component_id"],"master_id":d["master_id"],"check_count":len(checks),"checks":checks,"canonical_blend_sha256":digest(a.asset),"semantic_geometry_signature":c["semantic_geometry_signature"]}
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T036_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("compose-board","validate"),required=True)
    ap.add_argument("--definition",required=True); ap.add_argument("--review-dir"); ap.add_argument("--board",required=True)
    ap.add_argument("--canonical"); ap.add_argument("--reopen"); ap.add_argument("--curve-low"); ap.add_argument("--curve-high")
    ap.add_argument("--restore"); ap.add_argument("--registry"); ap.add_argument("--asset"); ap.add_argument("--output")
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a.definition,a.review_dir,a.board)
    else: validate(a)
if __name__=="__main__": main()
