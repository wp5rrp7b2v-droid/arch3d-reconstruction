"""Render four evidence-bounded T-016 review diagrams from canonical result."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'production/zhenguo_wanfo'
OUT=BASE/'review/P3_2/representative_assembly_v001'
OUT.mkdir(parents=True,exist_ok=True)
DATA=json.loads((BASE/'assembly/P3_2_REPRESENTATIVE_DERIVED_RESULT_V001.json').read_text())
FONT='/System/Library/Fonts/PingFang.ttc'
BG='#f4f1e9';INK='#203035';MUTED='#52666b';BLUE='#287a86';GOLD='#b68542';RED='#a94939';WHITE='#fffdf8';LINE='#d3d7d0'
def f(n):return ImageFont.truetype(FONT,n)
def base(title,sub,tag):
 im=Image.new('RGB',(1600,900),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,1600,18),fill=BLUE);d.text((74,51),title,font=f(48),fill=INK);d.text((77,122),sub,font=f(24),fill=MUTED)
 d.rounded_rectangle((1300,61,1525,111),radius=15,fill=INK);d.text((1324,70),tag,font=f(22),fill=WHITE)
 d.line((75,168,1525,168),fill=LINE,width=2)
 return im,d
def chip(d,box,title,body,color=BLUE,body_size=20):
 d.rounded_rectangle(box,radius=18,fill=WHITE,outline=LINE,width=2)
 x0,y0,x1,y1=box;d.rounded_rectangle((x0+20,y0+22,x0+29,y0+49),radius=4,fill=color)
 d.text((x0+45,y0+17),title,font=f(25),fill=INK)
 for j,line in enumerate(body):d.text((x0+24,y0+62+j*34),line,font=f(body_size),fill=MUTED)
def foot(d,text):d.line((75,842,1525,842),fill=LINE,width=2);d.text((78,853),text,font=f(17),fill=MUTED)
# A: diagram is drawn at verified output proportions, with dimensions presented only as current realization.
im,d=base('A｜柱—柱头栌斗承托组合','显式接口推导位置 · 工程关系 · 非历史榫卯断言','CAN ASSEMBLE')
d.rounded_rectangle((75,192,770,820),radius=24,fill=WHITE,outline=LINE,width=2)
# column height scaled to 410 px; lodou height about 34 px
x=600;bottom=707;top=297
d.rectangle((x-42,top,x+42,bottom),fill='#a26e52',outline=INK,width=3)
d.polygon([(x-34,top-36),(x+34,top-36),(x+49,top),(x-49,top)],fill='#c99766');d.line((x-49,top,x+49,top),fill=INK,width=3)
d.line((x-130,top,x+130,top),fill=BLUE,width=4);d.ellipse((x-6,top-6,x+6,top+6),fill=BLUE)
d.line((x,top-70,x,bottom+35),fill=GOLD,width=2)
d.text((118,247),'柱头栌斗',font=f(28),fill=INK);d.text((118,282),'CMP-LUDOU-COLUMN-001',font=f(18),fill=MUTED)
d.text((118,617),'柱',font=f(28),fill=INK);d.text((118,652),'CMP-COLUMN-001',font=f(18),fill=MUTED)
d.text((118,357),'TOP-SUPPORT-PLANE',font=f(18),fill=BLUE);d.text((118,384),'= LOWER-SUPPORT-PLANE',font=f(18),fill=BLUE)
d.text((118,456),'SUPPORT ↑',font=f(27),fill=BLUE);d.text((118,494),'LOCATE：主轴对齐',font=f(23),fill=GOLD)
chip(d,(800,202,1525,344),'组合依据',['Registry + 接口 + 当前 Master 参数 → 派生位置'])
chip(d,(800,362,1525,521),'柱高证据边界',['Z-006 = UNKNOWN / null / DO_NOT_LOCK','Z-006-RC-01 = REASONABLE_COMPLETION','3534.3 mm · 可替换生产候选'],GOLD)
chip(d,(800,539,1525,693),'构造边界',['joinery = UNKNOWN','工程承托基准面 ≠ 已证实历史加工面'],RED)
chip(d,(800,711,1525,819),'重建验证',['Blender CLI · independent reopen · deterministic'])
foot(d,'T-016 / AU-COLUMN-LUDOU-001  ·  位置由局部接口求解，非人工世界坐标')
im.save(OUT/'A_COLUMN_LUDOU_SUPPORT.png')
# B: no beam silhouettes, no length scale, only semantic cards.
im,d=base('B｜上下六椽栿梁架层位关系','纯语义关系图 · 未生成实际全长梁架几何','SEMANTIC ONLY')
chip(d,(100,218,620,332),'上六椽栿',['CMP-FRAME-UPPER-SIX-CHUANFU-001'])
chip(d,(100,467,620,581),'下六椽栿',['CMP-FRAME-LOWER-SIX-CHUANFU-001'])
chip(d,(1030,218,1500,332),'梁架层位控制',['CTL-FRAME-001 = CONTROL_ONLY'],GOLD)
chip(d,(1030,467,1500,581),'梁架层位连接代理',['PRX-FRAME-CONNECTOR-001 = PROXY_ONLY'],GOLD,17)
d.rounded_rectangle((100,351,1500,435),radius=16,fill=WHITE,outline=LINE,width=2)
d.text((137,362),'CTL-FRAME-001 → 上/下六椽栿：LOCATE',font=f(22),fill=BLUE)
d.text((818,362),'上/下六椽栿 → PRX-FRAME-CONNECTOR-001：CONNECT',font=f(20),fill=BLUE)
d.rounded_rectangle((100,626,1500,801),radius=25,fill='#f8e9e6',outline=RED,width=3)
d.text((137,650),'FULL-LENGTH GEOMETRY BLOCKED',font=f(38),fill=RED)
d.text((139,712),'historical full length = UNKNOWN / null     ·     connector identity = UNKNOWN     ·     joinery = UNKNOWN',font=f(20),fill=INK)
d.text((139,751),'1000 mm = NON-HISTORICAL REFERENCE ONLY / NOT ACTUAL ASSEMBLY LENGTH',font=f(19),fill=RED)
foot(d,'T-016 / AU-FRAME-TIER-001  ·  SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED = expected')
im.save(OUT/'B_FRAME_TIER_SEMANTIC_BLOCKED.png')
# C
im,d=base('C｜柱网次间重复组合','一个正式柱 Master · 两个 runtime instance · 建筑级参数驱动','REPEAT × 2')
d.rounded_rectangle((75,192,1525,620),radius=24,fill=WHITE,outline=LINE,width=2)
for x,ordinal in ((420,1),(1130,2)):
 d.rectangle((x-39,258,x+39,525),fill='#a26e52',outline=INK,width=3)
 d.ellipse((x-42,246,x+42,269),fill='#bf8a60',outline=INK,width=2)
 d.text((x-144,541),f'INST-COLUMN-SIDEBAY-{ordinal:03}',font=f(22),fill=INK)
 d.text((x-112,574),'CMP-COLUMN-001',font=f(20),fill=MUTED)
d.line((420,236,1130,236),fill=BLUE,width=4);d.line((420,223,420,250),fill=BLUE,width=3);d.line((1130,223,1130,250),fill=BLUE,width=3)
d.text((590,193),'PM-005 = 3505.7 mm',font=f(26),fill=BLUE)
chip(d,(75,648,770,814),'参数证据',['PM-005 · CONFIRMED / observed_as_measured','DIRECT_PRIMARY · 文件解析值'],BLUE)
chip(d,(800,648,1525,814),'重复规则',['REPEAT = PROJECT_RULE · count = 2','2 → 3 → 2 rebuild / restore 已验证'],GOLD)
foot(d,'T-016 / AU-COLUMN-GRID-001  ·  runtime instance 不创建新的 component_id')
im.save(OUT/'C_COLUMN_GRID_REPEAT.png')
# Overview
im,d=base('P3.2｜代表性构件组合验证','三种系统行为 · 正式审核概览 V001','T-016')
for box,head,lines,color in [((75,220,525,749),'A｜能组合',['柱 → 柱头栌斗','SUPPORT / LOCATE / BELONG','接口驱动 Blender 重建','joinery = UNKNOWN'],BLUE),((575,220,1025,749),'B｜能正确阻断',['上/下六椽栿语义图','LOCATE / CONNECT / BELONG','FULL-LENGTH GEOMETRY BLOCKED','历史全长 = UNKNOWN'],RED),((1075,220,1525,749),'C｜能重复',['两柱 / 一个次间','REPEAT / BELONG','PM-005 = 3505.7 mm','2 → 3 → 2 恢复'],GOLD)]:
 d.rounded_rectangle(box,radius=24,fill=WHITE,outline=LINE,width=2);x0,y0,x1,y1=box
 d.rounded_rectangle((x0+20,y0+23,x1-20,y0+91),radius=16,fill=color);d.text((x0+38,y0+37),head,font=f(28),fill=WHITE)
 for i,line in enumerate(lines):d.text((x0+30,y0+135+i*78),line,font=f(21),fill=INK if i!=2 else color)
 d.line((x0+30,y1-51,x1-30,y1-51),fill=LINE,width=2)
 d.text((x0+30,y1-42),'PROJECT_RULE ≠ 历史确认',font=f(18),fill=MUTED)
foot(d,'T-016 工程候选 · P3.2 Gate 仍待 ChatGPT 与 Product Owner 审核；P3.3 保持 LOCKED')
im.save(OUT/'P3_2_REPRESENTATIVE_ASSEMBLY_OVERVIEW_V001.png')
print('\n'.join(str(p) for p in sorted(OUT.glob('*.png'))))
