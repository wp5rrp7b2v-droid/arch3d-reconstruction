"""Add Chinese title + four-source color key to cloud Blender image output.
Runs in system Python (Pillow installed by Actions), not embedded Blender Python.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent/'output'
ft='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=lambda size:ImageFont.truetype(ft,size)
for tag,subtitle in [('iso','等轴试搭视图｜保持四件候选原始尺寸，独立刚体放置'),
 ('side','侧面｜外檐方向、两道下昂的倾斜及层次（试排）'),
 ('front','正面｜横向令栱与纵向华栱空间关系，令栱实际层位未核实')]:
 p=OUT/(tag+'_FOUR_COMPONENTS_ZH.png')
 im=Image.open(p).convert('RGB');w,h=im.size
 board=Image.new('RGB',(w,h+230),'#f3f3ef');board.paste(im,(0,140))
 d=ImageDraw.Draw(board)
 d.rectangle((0,0,w,140),fill='#243f47')
 d.text((35,20),'镇国寺万佛殿｜四类栱昂｜独立试搭 C01',font=f(43),fill='#ffffff')
 d.text((36,85),subtitle,font=f(24),fill='#d7e9e7')
 d.rectangle((0,h+140,w,h+230),fill='#f3f3ef')
 for x,color,txt in [(40,'#c78a47','第一跳华栱'),(350,'#429e8d','令栱（位置假设）'),
                     (785,'#d96040','头昂 C01'),(1150,'#6e79cf','二昂 C01')]:
  d.rectangle((x,h+154,x+36,h+187),fill=color)
  d.text((x+43,h+155),txt,font=f(22),fill='#243f47')
 d.text((35,h+197),'纯四件试排：不含第二跳华栱、斗、上梁及其他支撑；不代表完整历史装配。',font=f(20),fill='#923c30')
 board.save(p)
 print('Annotated',p.name,board.size)
