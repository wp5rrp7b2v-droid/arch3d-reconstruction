import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def font(size,bold=False):
    ps=[
      "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for p in ps:
        if Path(p).exists():
            try:return ImageFont.truetype(p,size)
            except:pass
    return ImageFont.load_default()

def dist(a,b): return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))
def angle(a,b):
    dy=abs(b[1]-a[1]); dz=abs(b[2]-a[2])
    return math.degrees(math.atan2(dz,dy))

def compose(a):
    sem=load(a.semantic); c=load(a.contract)
    front=Image.open(Path(a.review_dir)/"MP01A_FRONT_ELEVATION.png").convert("RGB")
    axon=Image.open(Path(a.review_dir)/"MP01A_AXON.png").convert("RGB")
    W,H=2400,1600
    out=Image.new("RGB",(W,H),"white")
    d=ImageDraw.Draw(out)
    ft=font(38,True); fh=font(24,True); fb=font(18); fs=font(15)
    d.text((50,28),"MP-01A Gate D｜东缝上部脊部支撑 First Assembly",font=ft,fill="black")
    d.text((50,80),"Minimum Proof / evidence-classified reconstruction / hidden joinery UNKNOWN",font=fb,fill="black")
    boxes=[(50,125,1160,770),(1240,125,2350,770),(50,820,770,1530),(810,820,1580,1530),(1620,820,2350,1530)]
    titles=["1 FRONT ELEVATION","2 AXONOMETRIC","3 OBJECT PROVENANCE","4 NUMERIC / RELATION CHECK","5 UNKNOWN BOUNDARY"]
    for b,t in zip(boxes,titles):
        d.rectangle(b,outline="gray",width=2); d.text((b[0]+14,b[1]+12),t,font=fh,fill="black")
    def paste(im,b):
        z=im.copy(); z.thumbnail((b[2]-b[0]-24,b[3]-b[1]-64))
        out.paste(z,(b[0]+(b[2]-b[0]-z.width)//2,b[1]+58))
    paste(front,boxes[0]); paste(axon,boxes[1])
    y=boxes[2][1]+62
    for o in sem["objects"]:
        line=f'{o["instance_id"]} | {o["master_id"]}'
        d.text((boxes[2][0]+16,y),line,font=fs,fill="black"); y+=34
        d.text((boxes[2][0]+28,y),f'{o["record_type"]} / {o["evidence_class"]}'[:88],font=fs,fill="black"); y+=40
    y=boxes[3][1]+62
    br=c["building_realization"]
    lines=[
      f'Pingliang L = {br["pingliang"]["length_mm"]} mm (reconstructed)',
      f'Tuofeng = {br["tuofeng_upper"]["base_span_y_mm"]} x {br["tuofeng_upper"]["depth_x_mm"]} x {br["tuofeng_upper"]["height_z_mm"]} mm',
      f'Shuzhu endpoint L = {br["shuzhu"]["resolved_length_mm"]} mm',
      f'Chashou S/N L = {br["chashou_south"]["resolved_length_mm"]:.1f} mm',
      f'Chashou rise angle = {br["chashou_south"]["rise_angle_deg"]:.2f} deg',
      f'Ridge target Z = {br["ridge_target_datum"]["xyz_mm"][2]} mm',
      f'Ridge-purlin ref Z = {br["ridge_purlin_reference"]["z_mm"]} mm',
      'All relationship claims stop at support/contact region.'
    ]
    for line in lines:
        d.text((boxes[3][0]+18,y),line,font=fb,fill="black"); y+=48
    y=boxes[4][1]+62
    for line in [
      "UNKNOWN retained:",
      "• historical Pingliang full length",
      "• exact Tuofeng dimensions/profile",
      "• exact Shuzhu historical height",
      "• exact Chashou historical angle/length",
      "• East-Seam rear C (未及)",
      "• exact ridge-purlin segment-end owner",
      "• intermediate upper support block(s)",
      "• hidden joinery / exact contact faces",
      "",
      "PASS here ≠ historical exactness / whole-frame PASS."
    ]:
        d.text((boxes[4][0]+18,y),line,font=fb,fill="black"); y+=42
    Path(a.board).parent.mkdir(parents=True,exist_ok=True); out.save(a.board)
    print("MP01A_GATE_D_BOARD_PASS")

def validate(a):
    c=load(a.contract); s=load(a.semantic); r=load(a.reopen); rb=load(a.rebuild)
    checks={}
    def ck(n,cond):
        if not cond: raise AssertionError(n)
        checks[n]="PASS"
    objs={x["instance_id"]:x for x in s["objects"]}
    br=c["building_realization"]
    ck("01_scope",s["assembly_id"]=="MP-01A-UPPER-RIDGE-SUPPORT-EAST-SEAM" and s["scope"]=="MINIMUM_PROOF_ONLY")
    ck("02_five_bodies",len(s["objects"])==5)
    ck("03_v008_identities",set(k for k,v in objs.items() if v["record_type"]=="V008_PHYSICAL_INSTANCE")=={"平梁-东缝","蜀柱-东缝","叉手-东缝-南侧","叉手-东缝-北侧"})
    ck("04_tuofeng_reconstructed",objs["ASM-MP01A-TUOFENG-UPPER-01"]["record_type"]=="RECONSTRUCTED_ASSEMBLY_INSTANCE" and objs["ASM-MP01A-TUOFENG-UPPER-01"]["historical_metric_claim"] is False)
    ck("05_no_historical_recon",all(x["historical_metric_claim"] is False for x in s["objects"]))
    ck("06_no_joinery",all("UNKNOWN" in str(x["historical_joinery"]) for x in s["objects"]))
    ck("07_ping_bbox",all(abs(x-y)<1e-6 for x,y in zip(objs["平梁-东缝"]["bbox_mm"]["dimensions"],[395.5,3672.0,280.5])))
    ck("08_tuo_bbox",all(abs(x-y)<1e-6 for x,y in zip(objs["ASM-MP01A-TUOFENG-UPPER-01"]["bbox_mm"]["dimensions"],[395.5,1325.0,200.0])))
    sh=br["shuzhu"]; ck("09_shuzhu_length",abs(dist(sh["lower_endpoint_mm"],sh["upper_endpoint_mm"])-sh["resolved_length_mm"])<1e-6)
    cs=br["chashou_south"]; cn=br["chashou_north"]
    ck("10_chashou_s_length",abs(dist(cs["lower_endpoint_mm"],cs["upper_endpoint_mm"])-cs["resolved_length_mm"])<1e-5)
    ck("11_chashou_n_length",abs(dist(cn["lower_endpoint_mm"],cn["upper_endpoint_mm"])-cn["resolved_length_mm"])<1e-5)
    ck("12_mirror_endpoints",cs["lower_endpoint_mm"][1]==-cn["lower_endpoint_mm"][1] and cs["upper_endpoint_mm"]==cn["upper_endpoint_mm"])
    ck("13_angle_s",abs(angle(cs["lower_endpoint_mm"],cs["upper_endpoint_mm"])-cs["rise_angle_deg"])<1e-5)
    ck("14_angle_n",abs(angle(cn["lower_endpoint_mm"],cn["upper_endpoint_mm"])-cn["rise_angle_deg"])<1e-5)
    ck("15_ridge_target",br["ridge_target_datum"]["xyz_mm"]==[0,0,885])
    ck("16_ridge_ref",br["ridge_purlin_reference"]["z_mm"]==1245 and br["ridge_purlin_reference"]["physical_contact_claim"] is False)
    ck("17_reopen",r["status"]=="PASS")
    ck("18_reopen_count",r["object_count"]==5)
    ck("19_rebuild_signature",rb["assembly_signature"]==s["assembly_signature"])
    ck("20_rebuild_objects",{x["instance_id"]:x["geometry_signature"] for x in rb["objects"]}=={x["instance_id"]:x["geometry_signature"] for x in s["objects"]})
    # V5-like dependency perturbation: target +50, Pingliang/Tuofeng unchanged by contract; endpoint-driven members change.
    z2=br["ridge_target_datum"]["xyz_mm"][2]+50
    sh2=z2-br["shuzhu"]["lower_endpoint_mm"][2]
    cs2=[0,0,z2]
    ch2=dist(cs["lower_endpoint_mm"],cs2)
    ck("21_perturb_shuzhu_changes",abs(sh2-br["shuzhu"]["resolved_length_mm"]-50)<1e-6)
    ck("22_perturb_chashou_changes",abs(ch2-br["chashou_south"]["resolved_length_mm"])>1.0)
    ck("23_perturb_pingliang_invariant",br["pingliang"]["length_mm"]==3672)
    ck("24_perturb_tuofeng_invariant",br["tuofeng_upper"]["height_z_mm"]==200 and br["tuofeng_upper"]["base_span_y_mm"]==1325)
    ck("25_mp01b_not_claimed",s["mp01b_status"].startswith("NOT_INCLUDED"))
    ck("26_whole_hall_not_claimed",s["whole_hall_claim"] is False)
    ck("27_blender",str(s["blender_version"]).startswith("4.5.13"))
    ck("28_blend_sha",s["blend_sha256"]==sha(a.asset))
    for i,n in enumerate(["MP01A_FRONT_ELEVATION.png","MP01A_AXON.png"],start=29):
        p=Path(a.review_dir)/n
        im=Image.open(p).convert("L")
        ck(f"{i:02d}_render",p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    ck("31_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)
    out={"status":"PASS","assembly_id":s["assembly_id"],"check_count":len(checks),"checks":checks,
         "assembly_signature":s["assembly_signature"],"blend_sha256":sha(a.asset),
         "object_geometry_signatures":{k:v["geometry_signature"] for k,v in objs.items()},
         "perturbation":{"ridge_target_z_mm":z2,"shuzhu_length_mm":sh2,"chashou_length_mm":ch2,
                         "expected_changed":["蜀柱-东缝","叉手-东缝-南侧","叉手-东缝-北侧"],
                         "expected_invariant":["平梁-东缝","ASM-MP01A-TUOFENG-UPPER-01"]}}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01A_GATE_D_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("compose-board","validate"),required=True)
    for n in ("contract","semantic","reopen","rebuild","asset","review_dir","board","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)
if __name__=="__main__": main()
