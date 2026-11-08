#!/usr/bin/env python3
"""Create two review sheets from temporary G3 mesh renders; no public museum images."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,math,os

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output";TMP=ROOT/"_temporary_23_thumbnails"
report=json.loads((OUT/"G3_BOTTOM23_OBJECT_REVIEW.json").read_text())
if report["status"]!="PASS_BOTTOM23_OBJECT_VIEWS__EXACT_MEMBERS_UNKNOWN":
 raise SystemExit("No successful 23-mesh inspection yet")
entries={x["review_id"]:x for x in report["selected_rows"]}
imgs={x["review_id"]:x for x in report["images"]}
assert len(entries)==23 and len(imgs)==24
fontfile="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not Path(fontfile).exists():fontfile="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font=lambda size:ImageFont.truetype(fontfile,size)
head=font(32);title=font(23);sub=font(17);tiny=font(16)
cellw,cellh=464,420
width=6*cellw+64;height=4*cellh+230
page=Image.new("RGB",(width,height),"#f8f9f7");d=ImageDraw.Draw(page)
d.text((35,24),"万佛殿数字博物馆｜底部23个匿名网格逐件检视",font=head,fill="#28343d")
d.text((35,73),"G3最小验证：每格为原网格独立渲染，视图自动放大以辨认形态；不能跨格比较真实尺寸",font=title,fill="#4b5358")
d.text((35,111),"B01–B23是本次分析编号；polySurface是模型原名；位置组1/2按网格质心相对高度分组，并非历史建筑铺作层级",font=sub,fill="#566168")
for idx,e in enumerate(report["selected_rows"]):
    rr,cc=divmod(idx,6);x=32+cc*cellw;y=153+rr*cellh
    d.rounded_rectangle((x,y,x+450,y+400),radius=16,fill="#ffffff",outline="#bfc6c8",width=2)
    f=TMP/imgs[e["review_id"]]["filename"]
    pic=Image.open(f).convert("RGB")
    # preserve render pixels, only fit full thumbnail in review tile.
    pic.thumbnail((424,296))
    page.paste(pic,(x+(450-pic.width)//2,y+10))
    main=f'{e["review_id"]}  ·  {e["gltf_mesh_name"]}'
    d.text((x+18,y+303),main,font=title,fill="#263238")
    fm={"horizontal":"细长","compact":"紧凑","vertical":"竖向","mixed":"混合"}[e["form_envelope"]]
    d.text((x+18,y+344),f'位置组{e["relative_band"]}  ·  {e["orientation_envelope"]}方向  ·  {fm}',font=sub,fill="#5a6268")
    d.text((x+18,y+373),"构件身份：尚未证明",font=tiny,fill="#945c37")
d.text((35,height-56),"来源：数字博物馆dougong.gltf；原数据按G1记录SHA-256核验。第三方图像仅作为短期审核证据，不提交公开Git。",font=sub,fill="#48545a")
atlas=TMP/"G3_BOTTOM23_INDEX_ATLAS.png";page.save(atlas,optimize=True)

# A "candidate adjacency table" is a derived-data schematic, no reproduced geometry.
pairs=report.get("possible_support_pairs",[])[:16]
W,H=1700,900
sheet=Image.new("RGB",(W,H),"#f7f8f6");dr=ImageDraw.Draw(sheet)
dr.text((45,28),"底部23对象｜潜在上下邻接编号（包络测试，不是实际榫卯）",font=head,fill="#2f3b42")
dr.text((45,86),"判据：上下Z包络端点接近且XY包络重叠；全部为 INFERENCE，不能据此确认“栌斗”“第一跳华栱”",font=sub,fill="#6a5351")
cols=[70,285,510,755,1060,1360]
headers=["序号","下部候选","上部候选","XY重叠比例","Z间隙/整体高度","证据等级"]
for x,h in zip(cols,headers):dr.text((x,158),h,font=sub,fill="#263641")
dr.line((55,196,W-55,196),fill="#94a0a3",width=2)
for i,p in enumerate(pairs):
 y=207+i*38
 if i%2==0:dr.rectangle((55,y-3,W-55,y+33),fill="#e9eded")
 values=[str(i+1),p["lower"]+" / "+p["lower_mesh"],p["upper"]+" / "+p["upper_mesh"],
         str(p["bbox_area_overlap_ratio"]),str(p["gap_as_model_height"]),"推断，未验证"]
 for x,z in zip(cols,values):
  dr.text((x,y),z,font=tiny,fill="#28363e" if x!=cols[-1] else "#8c5e4b")
if not pairs:dr.text((75,250),"底部23个网格内未满足本次AABB邻接阈值的对象对。不能据此证明实际完全无连接。",font=title,fill="#744e42")
note="以上是程序计算的包络候选，不包含接触面积或实测榫卯关系。构件身份和同一铺作位置仍 UNKNOWN。"
dr.text((55,H-90),note,font=sub,fill="#704f4d")
summary=TMP/"G3_BOTTOM23_AABB_CANDIDATES.png";sheet.save(summary,optimize=True)
for f in (atlas,summary):
 report["images"].append({"review_id":"BOARD","filename":f.name,"size_bytes":f.stat().st_size,
     "sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"temporary_review_only":True})
report["gates"]["G3_index_atlas_created"]=True
report["gates"]["G3_candidate_table_created"]=True
(OUT/"G3_BOTTOM23_OBJECT_REVIEW.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print("G3_ATLAS",atlas,"G3_PAIRS",len(pairs),"G3_BOARD",summary)
