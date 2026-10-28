"""C02 real-pixel gate; fail blank or all-dark CPU output, never treat save as visual QA."""
import json,statistics
from pathlib import Path
from PIL import Image,ImageStat
ROOT=Path(__file__).resolve().parent
D=ROOT/'output'
rows=[]
for key in ('head','spacer','overview'):
 p=D/(key+'_CONNECTED_C02_ZH.png')
 im=Image.open(p).convert('RGB')
 assert im.size[0]>=1200 and im.size[1]>=900
 # Cropping out header/footer prevents labels from disguising a blank 3D viewport.
 image_area=im.crop((0,170,im.width,im.height-260))
 st=ImageStat.Stat(image_area)
 spread=max(st.stddev)
 # Distinct shapes generate enough image texture in a large viewport.
 row=dict(file=p.name,pixels=im.size,viewport_stddev_rgb=list(map(float,st.stddev)),
   range_rgb=[float(x) for x in st.mean],visible_3d=bool(spread>=6.0))
 rows.append(row)
report=dict(gate='PASS' if all(x['visible_3d'] for x in rows) else 'FAIL_BLANK_VIEW',
  method='RGB channel spatial stddev of 3D viewport only; text headers excluded',
  images=rows)
(D/'RENDER_QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
assert report['gate']=='PASS','C02_REVIEW_IMAGES_VISUALLY_EMPTY'
