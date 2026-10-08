import ast,json
from pathlib import Path
import numpy as np
import trimesh,manifold3d
from functools import reduce
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.font_manager import FontProperties
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).resolve().parent
for node in ast.parse((ROOT/'lower_front/check_lower_front.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='boolean64':exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
font=FontProperties(fname=str(ROOT.parent/'chinese_font.ttf'))
g=json.loads((OUT/'GEOMETRY.json').read_text());m={k:trimesh.Trimesh(v['vertices'],v['faces'],process=False) for k,v in g.items() if k.startswith('west:')}
b=json.loads((ROOT/'west_v002/REOPENED_WEST_V002_MESHES.json').read_text());o=next(o for o in b['objects'] if o['id']=='FOUR_BEAM');beam=trimesh.Trimesh(o['vertices'],o['faces'],process=False)
fig,(ax,bx)=plt.subplots(1,2,figsize=(13.6,7.4),gridspec_kw={'width_ratios':[1.23,1]});fig.patch.set_facecolor('#faf9f5')
def draw(mesh,color,alpha=1):
 s=mesh.section(plane_origin=[0,3595.9,0],plane_normal=[0,1,0])
 if s is None:return
 for p in s.discrete:ax.add_patch(Polygon(p[:,[0,2]],closed=True,facecolor=color,edgecolor='#666',lw=.45,alpha=alpha))
draw(beam,'#aab2b9',.6)
for k,q in m.items():
 c='#dec899' if 'SIX' in k else '#b68251' if 'LUDOU' in k else '#bd9b73' if 'GONG' in k else '#e2b05e' if 'PANJIAN' in k else '#e8cc90'
 draw(q,c,.85)
rod=g['LOWER_PURLIN_FRONT'];q=trimesh.Trimesh(rod['vertices'],rod['faces'],process=False);draw(q,'#3980a5',.9)
for k in ['PANJIAN','LUDOU','HUAGONG','LINGGONG','CENTRE_DOU']:
 q=boolean64([m['west:'+k],beam],'intersection');draw(q,'#c84330',.85)
ax.set_xlim(-1150,1150);ax.set_ylim(-940,740);ax.set_aspect('equal');ax.set_xlabel('面阔方向（毫米）',fontproperties=font);ax.set_ylabel('局部高度（毫米）',fontproperties=font);ax.set_title('西端完整类别候选：实际网格切片',fontproperties=font,fontsize=14,pad=13)
for text,xy,where in [('前下平槫',(0,480),(500,570)),('替木及三枚小斗',(0,285),(580,300)),('襻间枋',(680,80),(580,150)),('令栱、华栱与中央斗',(280,-220),(560,-265)),('底部栌斗',(0,-490),(570,-490)),('上六椽栿试验参考体',(850,-750),(410,-880))]:
 ax.annotate(text,xy=xy,xytext=where,fontproperties=font,fontsize=10,color='#333',arrowprops={'arrowstyle':'-','color':'#777','lw':.7},bbox={'facecolor':'white','edgecolor':'none','alpha':.8})
ax.annotate('红色：与原四椽栿相交的部分',xy=(0,-130),xytext=(-1080,-80),fontproperties=font,fontsize=10,color='#b33222',arrowprops={'arrowstyle':'->','color':'#b33222','lw':1.1},bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
bx.axis('off');bx.set_title('本轮已证明什么？',fontproperties=font,fontsize=16,loc='left',pad=14)
items=[('已补齐类别','底部栌斗、华栱、令栱、襻间枋、\n中央斗、替木下三枚小斗及槫。'),('检验结果','1875组新增构件对检查：\n10处与四椽栿交叠，候选未通过。'),('失败集中位置','不是上部槫—替木槽：\n是下方斗栱与四椽栿梁端的对位。'),('模型边界','原批准63件形状保持；\n这版是借形、借参的定位试验。')]
for i,(h,t) in enumerate(items):
 y=.94-i*.205;bx.text(0,y,h,fontproperties=font,fontsize=13,color='#9d3926' if i in [1,2] else '#31596c',va='top');bx.text(0,y-.055,t,fontproperties=font,fontsize=12,linespacing=1.65,va='top',color='#333')
bx.text(0,.065,'不能由这次FAIL直接认定原梁架错误，\n也不据此擅自削梁或移动两榀。',fontproperties=font,fontsize=12,color='#9d3926',va='top',linespacing=1.6)
fig.suptitle('前下平槫承托组 V002：构件类别补齐，当前定位未通过',fontproperties=font,fontsize=19,y=.97)
fig.text(.04,.025,'切片位于西榀进深3595.9毫米；红色来自实际实体交集。小斗尺寸、隐刻槽形和标高含工作假设；未作承载能力验证。',fontproperties=font,fontsize=10,color='#666')
fig.tight_layout(rect=[.02,.07,.98,.92]);fig.savefig('/workspace/scratch/0ab7fd249ac6/Wanfo_Lower_Front_V002_Conflict_Review_ZH.png',dpi=170)
