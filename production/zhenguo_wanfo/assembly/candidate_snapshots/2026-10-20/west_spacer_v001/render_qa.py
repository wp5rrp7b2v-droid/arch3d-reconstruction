"""Check actual Blender renders are readable, add truthful Chinese candidate labels.
Runs in GitHub Actions only. Never touches the BLEND or mesh contents.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(sys.argv[1])
out=root/"output"
fonts=["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
       "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"]
font=next((p for p in fonts if Path(p).is_file()),None)
assert font,"Chinese font unavailable; do not archive unlabelled visualization"
titlefont=ImageFont.truetype(font,42,index=0)
descfont=ImageFont.truetype(font,24,index=0)
items=[
 ("WEST_SPACER_DETAIL.png","西缝隔架局部｜89实体候选 V001"),
 ("TWO_FRAME_OVERVIEW.png","东西两榀联合结构｜89实体候选 V001"),
]
records=[]
for file,title in items:
 path=out/file
 assert path.is_file() and path.stat().st_size>10000,("MISSING_RENDER",file)
 img=Image.open(path).convert("RGB")
 assert img.size==(1600,1000),("RENDER_SIZE_ERROR",file,img.size)
 a=np.asarray(img)
 sample=a[160:900,60:1540,:]
 mean=float(sample.mean())
 contrast=float(sample.std(axis=(0,1)).mean())
 dark_fraction=float(np.mean(np.all(sample<20,axis=2)))
 # A completely black, empty or flat image must never pass as visual proof.
 assert 35<mean<245 and contrast>13 and dark_fraction<0.80, \
      ("RENDER_HAS_NO_VISIBLE_GEOMETRY",file,mean,contrast,dark_fraction)
 draw=ImageDraw.Draw(img)
 draw.rectangle((0,0,1600,130),fill=(249,248,242))
 draw.rectangle((0,930,1600,1000),fill=(249,248,242))
 draw.text((44,14),title,font=titlefont,fill=(30,46,41))
 draw.text((46,78),"橙色：西缝新增7件（含2件散斗凹口调整）｜蓝灰：西缝原件｜褐色：东缝原件",
           font=descfont,fill=(53,70,61))
 draw.text((46,943),"形制与位置仅为装配候选，未获整体批准；几何验证结果另见WEST_SPACER_VALIDATION.json",
           font=descfont,fill=(68,72,65))
 img.save(path,format="PNG",compress_level=6)
 records.append({"file":file,"size_px":list(img.size),"raw_render_mean":mean,
                 "raw_render_std_mean":contrast,"raw_dark_fraction":dark_fraction,
                 "chinese_labels_applied":True,"qa":"PASS"})
(out/"RENDER_QA.json").write_text(json.dumps(
 {"status":"PASS_VISIBLE_CPU_RENDER","records":records,
  "view_only":"Visual images are schematic review renders; no historical or physical approval."},
 ensure_ascii=False,indent=2)+"\n")
print(json.dumps(records,ensure_ascii=False,indent=2))
