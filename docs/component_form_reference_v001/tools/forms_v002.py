"""Evidence-bounded presentation drawings, not production geometry.

Coordinates are arbitrary illustration units. No mesh, BLEND or engineering
parameter is written. Every reconstructed outline is explicitly a candidate.
"""
from pathlib import Path
import html, json, hashlib, subprocess

OUT=Path(__file__).resolve().parents[1]
DEST=OUT/'assets/v002'
BASE='83cee5522b6f468677b2b42ced9f1f821500b9db'
IDS=['F003','F004','F005','F007','F008','F009','F030']
E=html.escape

FORMS={
 'F003':dict(title='下六椽栿',subtitle='深梁身 · 下缘肩部收削 · 榫区厚度另核',
  profile=[(0,115),(110,150),(310,160),(700,158),(890,145),(1000,115),(1000,50),(930,28),(835,0),(180,0),(70,27),(0,50)],
  feature='梁身较深，肩部有收削变化',end='榫区可收窄；不补造隐蔽槽',
  form='深而长的梁身，肩部有收削和厚薄变化；榫区与梁身分开表达。',
  difference='Master为8顶点直棱参考段；尚未表达梁身肩部、曲面及榫区收窄。',
  keep='保留下层身份、493.5mm材广均值；1000mm参考段不当作全梁长度。',
  change='候选方向：补肩部与梁身曲面，榫区按375mm与最厚444mm的统计分别约束；不凭示意锁定过渡长度。',
  unknown='整形为工程候选。端区长度、完整上下缘和隐蔽接口未知；本图非测绘坐标，不与图C同尺度比较。',
  source='A1 PDF81表2-38、PDF82图2-39；FG2022 PDF16明／草栿；DU1932 PDF54—55梁端卷杀。',
  same='本殿下梁可见曲面，榫厚与最厚统计不同；图2-39两端有遮挡。',
  analogous='佛光寺东大殿（857）明栿的加工轮廓、独乐寺山门（984）卷杀梁头支持类型比较；不复制月梁曲率。',
  common='可共用“长梁身＋局部端区收削”的绘图原型；上下梁的高度、曲线和接口不能共用。',
  refs=['assets/original/A1-p081.jpg','assets/original/A1-p082.jpg','assets/research/FG2021-p016.png','assets/research/DU1932-p054.png','assets/research/DU1932-p055.png'],
  foot='本殿照片支持梁身变化；端部延伸和曲线为时代形制候选。'),
 'F004':dict(title='上六椽栿',subtitle='较浅素平梁身 · 端部宽度过渡 · 独立于下梁',
  profile=[(0,109),(130,119),(400,122),(740,120),(920,116),(1000,109),(1000,10),(840,2),(580,0),(300,3),(100,8),(0,10)],
  feature='保持素平，不复制下梁弧肩',end='端区宽度过渡；不是高度拉伸',
  form='较浅、较素平的上层通长梁，保留木材边缘及端区厚度过渡。',
  difference='Master仅为直棱参考段；全梁端区过渡不足，C01仅代表已批准前端局部。',
  keep='保留334mm材广、209mm榫厚与240.5mm最厚统计；C01原批准边界保持。',
  change='以素平梁身为候选，另核端区厚度和压昂接触；不套下梁弧肩，不改已批准C01。',
  unknown='整形为工程候选。厚度是进深方向，不等于侧面材高；后端及全长未定，10710mm候选不作历史实测。',
  source='A1 PDF81—82文字、表2-38及图2-39；FG2022 PDF16明／草栿比较。',
  same='本殿上梁与下梁叠置、断面不同；端区压二下昂且停于柱心附近。',
  analogous='佛光寺东大殿（857）明栿与草栿的加工区别，支持上梁采用较素平候选，不证明本殿逐段曲线。',
  common='与下梁共用长梁表达方法；上梁单独确定断面、端区宽度和承托层位。',
  refs=['assets/original/A1-p081.jpg','assets/original/A1-p082.jpg','assets/research/FG2021-p016.png'],
  foot='本殿上梁可见段较素平；侧缘起伏、过渡长度均未作实测锁定。'),
 'F005':dict(title='四椽栿',subtitle='较短深梁 · 朴素边缘 · 两端置于隔架承托',
  profile=[(0,125),(100,149),(300,155),(650,153),(880,147),(1000,125),(1000,42),(910,19),(760,4),(300,0),(100,18),(0,42)],
  feature='较短深梁；端区轻度收削候选',end='梁端承托；托脚是另件',
  form='较短而深的梁身，边缘有变化，两端落在隔架承托上；不加华丽月梁装饰。',
  difference='Master为8顶点包络；未表达侧缘变化、梁端收削和承托区。',
  keep='保留426.5×302mm族均值；两个测量样本不擅自分配给东西缝。',
  change='候选增加朴素梁身轮廓和端区过渡；隔架栱、散斗和托脚保持独立，不刻成梁身。',
  unknown='端头部分遮挡，所画轻度收削是候选，非本殿实测闭合曲线；端榫、托脚切口与全长待核。',
  source='A1 PDF82图2-40及表2-39；FG2022 PDF16；DU1932 PDF55同名四椽栿比较。',
  same='本殿图2-40可辨较短梁身和端部承托；下方隔架单栱之下仅一散斗（A1正文）。',
  analogous='佛光寺东大殿（857）明四椽栿与独乐寺山门（984）四椽栿可比较梁端加工；不复制别殿强烈月梁曲率。',
  common='与六椽栿共用朴素梁身原型；跨度、深度及支承位置独立，不能直接整体缩放。',
  refs=['assets/original/A1-p082.jpg','assets/research/FG2021-p016.png','assets/research/DU1932-p055.png'],
  foot='图中承托仅解释梁端位置，不是已经验证的榫卯装配。'),
 'F007':dict(title='平梁 · 山面',subtitle='朴素短梁候选 · 不复制东西缝断面 · 端区未定',
  profile=[(0,110),(150,121),(380,124),(650,118),(850,120),(1000,108),(1000,24),(870,14),(640,4),(390,0),(150,13),(0,24)],
  feature='短梁原型；小幅边缘变化仅示意',end='两端承托，隐藏切口未定',
  form='提出朴素短梁候选：较平直梁身、局部边缘起伏，两端承托，上部支承脊部组合。',
  difference='山面Master仅有断面包络；245.4mm厚为参数补全，不能作为原物厚度。',
  keep='保留山面独立身份、346mm材广样本；厚度UNKNOWN继续保留。',
  change='可先按朴素短梁方向审核外形；长度、厚度、梁端与山面承托分别约束，不复制东西缝全几何。',
  unknown='本殿山面完整单体仍未证明。图示为同类短梁候选，轻微曲线和端区是工作假设；厚度、全长及隐蔽接口未知。',
  source='A1 PDF81山面构架、PDF83表2-40；DU1932 PDF55—56独乐寺山门平梁；本殿图2-41仅同殿家族比较。',
  same='本殿正文说明山面太平梁上构造与平梁上相同；表2-40山面材广346mm，厚度未及。',
  analogous='独乐寺山门（984）短平梁承脊部直立及斜向构件，支持短梁类型；不是与本殿山面位置完全同构的测量。',
  common='可与东西缝平梁共用“朴素短梁＋独立脊部垫座”类型；山面断面、全长、端区仍独立。',
  refs=['assets/original/A1-p081.jpg','assets/original/A1-p083.jpg','assets/research/DU1932-p055.png','assets/research/DU1932-p056.png'],
  foot='类型候选可浏览；本殿山面单件外形、尺寸仍缺直接证明。'),
 'F008':dict(title='驼峰 · 下层承托',subtitle='梁上低矮承托块候选 · 上承斗栱 · 单体身份待核',
  profile=[(0,0),(110,20),(205,60),(290,103),(390,130),(610,130),(710,103),(795,60),(890,20),(1000,0)],
  feature='低矮展开，中部形成承托面',end='上承斗栱，不把令栱并入',
  form='低矮展开的承托块候选，中部承斗栱，再托平梁；不再以两层台座当作历史外形。',
  difference='现Master是两层台座包络；台阶、比例及轮廓尚无本殿实测支持。',
  keep='保留下层承托角色、独立家族和数量未知；不假定与脊部共用一个实体。',
  change='候选采用低矮展开、中央承托面的块体；须先核清本殿单体与斗栱边界，再选具体肩部曲线。',
  unknown='官方文字证明名称与作用，但本殿下层单体未清晰分离；曲线、厚度、个数及接口未知，整形只作候选范围。',
  source='官方万佛殿梁架说明；A1 PDF83图2-41、PDF106图2-70；时代类比见页下单列来源。',
  same='官方明确四椽栿上有驼峰、令栱承平梁；A1该层有承托组合，但照片没有单独标名。',
  analogous='独乐寺山门（984）的脊部展开承托仅支持承托块类型，层位不同；下层候选需另有同作用图像核验。',
  common='只能共用“展开底座＋中央承托”的概念；下层上承斗栱，脊部上承蜀柱，不能共用全部几何。',
  refs=['assets/original/A1-p083.jpg','assets/original/A1-p106.jpg','assets/research/DU1932-p055.png','assets/research/DU1932-p056.png'],
  foot='身份与作用有据；下层本殿单体轮廓不足，保留证据缺口。'),
 'F009':dict(title='驼峰 · 脊部承托',subtitle='低矮展肩 · 中央承蜀柱 · 与下层分开',
  profile=[(0,0),(110,12),(170,35),(240,35),(300,73),(365,73),(405,108),(595,108),(635,73),(700,73),(760,35),(830,35),(890,12),(1000,0)],
  feature='低矮展肩，中央承短柱',end='蜀柱另件；脚部接口未定',
  form='低矮、向两侧展开的肩部，中央承蜀柱；肩部轮廓独立于下层承托。',
  difference='Master是对称阶状挤出体；可见肩部起伏未细化，深度和背面仍是未知。',
  keep='保留脊部身份及数量未知；蜀柱与脚下驼峰分为独立构件。',
  change='以本殿可见展肩作基本方向；细化曲折与过渡，柱脚接口、深度和背面另核。',
  unknown='A1图2-51补足一侧较清楚展肩，不能据此镜像证明背面；具体命名对应仍为推断，曲线为非量测提炼。',
  source='A1 PDF83图2-41、PDF90图2-51、PDF106图2-71；DU1932 PDF55—56山门脊部。',
  same='本殿图2-51右侧短柱脚下有展开起伏肩部；图2-41也见同层承托，官方说明该层有驼峰。',
  analogous='独乐寺山门（984）原调查脊部有展开式承托及直立短材；只比较类型，不搬其曲线和尺寸。',
  common='可共享展开承托类型，脊部中央对应蜀柱；下层中央对应斗栱，轮廓与接口分别调整。',
  refs=['assets/original/A1-p083.jpg','assets/original/A1-p090.jpg','assets/original/A1-p106.jpg','assets/research/DU1932-p055.png','assets/research/DU1932-p056.png'],
  foot='依据本殿可见肩部提炼；镜像、深度及隐藏连接不是测绘结论。'),
 'F030':dict(title='令栱',subtitle='独立横栱 · 两端卷杀 · 顶部交接口未定',
  profile=[(0,140),(1000,140),(1000,100),(978,74),(940,47),(880,19),(820,3),(180,3),(120,19),(60,47),(22,74),(0,100)],
  feature='两端卷杀，中段较深',end='顶面交接未知；不画假榫',
  form='横置短栱，两端下缘卷杀、中段较深；与出跳华栱保持方向区别。',
  difference='Master已有简化卷杀；端头分段、完整顶面交接和隐刻仍需核证。',
  keep='保留897×217.4×155.6mm族均值和既有基本卷杀；内外令栱分开识别。',
  change='可先审核卷杀类型及端部方直收束；精确瓣数、顶部开口和隐刻位置不能据同名栱照搬。',
  unknown='整件为时代形制参考示意，卷杀曲线非逐点实测；顶面开口与背面未知，图B与图C未配准。',
  source='A1 PDF60及PDF87图2-46；FG2022 PDF17标名令栱；DU1932 PDF49山门铺作。',
  same='本殿外檐最外跳横栱可见两端卷杀；内界面照片只辅助位置识别，不替代外檐单件。',
  analogous='佛光寺东大殿（857）标名令栱图和独乐寺山门（984）外端横栱，支持朴素横栱与卷杀类型。',
  common='同类可复用横栱卷杀原型；长度、材高、端头瓣数、顶面交接与内外位置独立。',
  refs=['assets/original/A1-p060.jpg','assets/original/A1-p087.jpg','assets/research/FG2021-p017.png','assets/research/DU1932-p049.png'],
  foot='剥离组合遮挡后的类型示意；没有补画未知槽孔与装饰。')
}

class Drawing:
 def __init__(self,title):
  self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img"><title>{E(title)}时代形制参考示意</title><rect width="1600" height="1000" fill="#faf9f3"/><g font-family="Noto Sans CJK SC,Microsoft YaHei,sans-serif" fill="#263c33">']
 def text(self,x,y,t,size=34,color='#263c33'):
  self.s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{E(t)}</text>')
 def poly(self,p,fill='#b49b6d',stroke='#665c45',width=3,dash=False):
  ds=' stroke-dasharray="12 9"' if dash else ''
  self.s.append(f'<polygon points="'+ ' '.join(f'{x:.2f},{y:.2f}' for x,y in p)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{ds}/>')
 def line(self,p,color='#8c6e3e',width=3,dash=False):
  ds=' stroke-dasharray="12 9"' if dash else ''
  self.s.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in p)+f'" fill="none" stroke="{color}" stroke-width="{width}"{ds}/>')
 def rect(self,x,y,w,h,fill='#f6ecd9',stroke='#b58339',dash=True):
  self.poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],fill,stroke,3,dash)
 def prism(self,profile,origin=(170,330),scale=1,depth=(110,-80)):
  ox,oy=origin;dx,dy=depth
  p=[(ox+scale*x,oy+scale*(.07*x-y)) for x,y in profile];q=[(x+dx,y+dy) for x,y in p]
  self.poly(q,'#d8c69c')
  for i in range(len(p)):
   j=(i+1)%len(p)
   self.poly([p[i],p[j],q[j],q[i]],'#cfbb8d' if profile[j][0]>=profile[i][0] else '#9b855f')
  self.poly(p,'#b59b6e')
  return p
 def save(self,path):path.write_text(''.join(self.s)+'</g></svg>')

def make(fid):
 f=FORMS[fid];d=Drawing(f['title'])
 d.text(60,64,f['title'],48);d.text(60,116,'时代形制参考示意 · 工程候选 · 非原物实测／非批准模型',31,'#916626')
 d.text(60,172,f['subtitle'],33)
 if fid=='F008':d.text(1180,64,'证据不足 · FAIL',34,'#a26d26')
 origin=(165,430)
 d.prism(f['profile'],origin=origin,scale=1.04,depth=(130,-85))
 d.text(90,537,f['feature'],35)
 # Unknown zones are clearly separate from the filled candidate envelope.
 if fid not in ['F008','F009']:
  d.rect(130,217,155,290,fill='none');d.rect(1120,292,180,215,fill='none')
  d.text(1170,246,'端区待核',30,'#986c35')
 else:
  d.line([(590,240),(590,305),(800,332),(800,268),(590,240)],'#9c793f',3,True)
  d.text(1020,238,'上部接触面待核',30,'#986c35')
 d.line([(60,580),(1540,580)],'#d3d8cc',2)
 d.text(65,630,'侧面类型轮廓（不代表实测比例）',31)
 p=[(95+x*.82,812-y*.82) for x,y in f['profile']]
 d.poly(p,'#e1d4b3','#6e694e')
 d.text(1070,630,'关键端部／承托',31)
 if fid in ['F003','F004']:
  # Plan diagram: width, rather than material height, changes at the tenon.
  d.poly([(1090,710),(1200,710),(1270,681),(1470,681),(1470,800),(1270,800),(1200,773),(1090,773)],'#e7d6ad','#b58339',3,True)
  d.text(1085,855,'俯视 · 过渡长度未知',29,'#916626')
 elif fid in ['F008','F009']:
  d.rect(1120,773,355,30,'#e7e8df','#8b9485',False)
  d.poly([(1140,773),(1220,749),(1270,705),(1350,705),(1405,749),(1460,773)],'#e1d4b3')
  if fid=='F008':d.rect(1250,665,125,35,'#e7e8df','#8b9485',True)
  else:d.rect(1275,657,70,49,'#e7e8df','#8b9485',True)
  d.text(1090,855,'灰色邻件仅解释层位',28)
 elif fid=='F030':
  d.rect(1120,705,330,70,'#e1d4b3','#6e694e',False)
  d.rect(1240,685,90,110,'none','#b58339',True)
  d.text(1100,855,'虚线区：交接位置待核',28,'#916626')
 else:
  d.poly([(1120,681),(1450,681),(1450,752),(1120,752)],'#e1d4b3')
  d.rect(1300,752,120,40,'#e7e8df','#8b9485',True)
  d.line([(1355,794),(1470,850)],'#b58339',4,True)
  d.text(1075,880,'承托及斜材为邻件示意',28)
 d.text(70,865,f['end'],31)
 d.text(60,935,f['foot'],30,'#6e6246')
 d.text(60,980,'全部轮廓为有边界的候选；虚线区细节未知。图B／C未作尺度或坐标配准。',28,'#6b7468')
 path=DEST/(fid+'-form.svg');d.save(path)
 return dict(id=fid,file=str(path.relative_to(OUT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),operation='CODE_DRAWN_CANDIDATE_TYPE_AXON_SIDE_DETAIL',coordinates='arbitrary illustration units; NOT measured geometry',source_refs=f['refs'],source_citation=f['source'],supported=f['same'],analogy=f['analogous'],unknown=f['unknown'],not_approved=True)

def main():
 DEST.mkdir(parents=True,exist_ok=True)
 items=[make(fid) for fid in IDS]
 for item in items:
  item['source_sha256']={p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in item['source_refs']}
 (DEST/'DERIVATION.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
 print('Drew seven independent candidate type illustrations; no engineering geometry written.')

if __name__=='__main__':main()
