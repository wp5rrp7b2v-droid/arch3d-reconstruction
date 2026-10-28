"""Chinese review labels for actual C02 connected source meshes."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
O=Path(__file__).resolve().parent/'output'
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font=lambda s:ImageFont.truetype(F,s)
items=[
 ('head','东缝前柱头：栌斗、两跳华栱、交互斗、散斗、两道昂及横向栱'),
 ('spacer','前隔架局部：真实华栱／令栱／散斗及梁材连接位置'),
 ('overview','柱头与前隔架的同榀相对位置；保持PR75既有几何与接口')]
for key,subtitle in items:
 path=O/(key+'_CONNECTED_C02_ZH.png')
 im=Image.open(path).convert('RGB');w,h=im.size
 page=Image.new('RGB',(w,h+250),'#f3f1ec')
 page.paste(im,(0,150))
 d=ImageDraw.Draw(page)
 d.rectangle((0,0,w,150),fill='#294346')
 d.text((32,23),'镇国寺万佛殿｜连接优先重建 C02',font=font(43),fill='#ffffff')
 d.text((33,90),subtitle,font=font(23),fill='#d4e5e5')
 d.text((38,h+170),'棕：柱／栌斗　黄：斗与散斗　绿：栱　红：头昂和二昂　紫：梁',font=font(24),fill='#2e484c')
 d.text((38,h+214),'本图是PR75既有带接口几何的结构种子，未完成C01昂／V001栱替换，非历史形制批准。',font=font(22),fill='#a14f35')
 page.save(path)
 print('C02_ANNOTATED',key,path.stat().st_size)
