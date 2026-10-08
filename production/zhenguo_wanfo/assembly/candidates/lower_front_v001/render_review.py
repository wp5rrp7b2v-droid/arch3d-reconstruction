from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle,Polygon
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1];O=Path(__file__).resolve().parent
font=FontProperties(fname=str(ROOT.parents[0]/'chinese_font.ttf'))
plt.rcParams['axes.unicode_minus']=False
geo=json.loads((O/'LOWER_FRONT_GEOMETRY.json').read_text())
meshes={k:trimesh.Trimesh(v['vertices'],v['faces'],process=False) for k,v in geo.items()}
raw=json.loads((ROOT/'west_v002/REOPENED_WEST_V002_MESHES.json').read_text());v=next(v for v in raw['objects'] if v['id']=='FOUR_BEAM');meshes['west:FOUR_BEAM']=trimesh.Trimesh(v['vertices'],v['faces'],process=False)
fig,(ax,bx)=plt.subplots(1,2,figsize=(13,6.5),gridspec_kw={'width_ratios':[1,1.4]});fig.patch.set_facecolor('#faf9f5')
col={'west:FOUR_BEAM':'#9aa3ab','west:LOWER_PANJIAN':'#ba8b57','west:LOWER_DOU':'#d59546','west:LOWER_TIEMU':'#edc26c','LOWER_PURLIN_FRONT':'#347cad'}
for k,c in col.items():
 sec=meshes[k].section(plane_origin=[0,0,0],plane_normal=[1,0,0])
 if sec is None:continue
 for ring in sec.discrete:
  ax.add_patch(Polygon(ring[:,[1,2]],closed=True,facecolor=c,edgecolor='#535353',lw=.6,alpha=.86))
ax.set_xlim(3350,3870);ax.set_ylim(-165,680);ax.set_aspect('equal');ax.set_xlabel('进深坐标（毫米）',fontproperties=font);ax.set_ylabel('局部高度（毫米）',fontproperties=font);ax.set_title('西端实际候选网格剖面',fontproperties=font,fontsize=15,pad=15)
for t,y,z in [('槫',3660,485),('新替木',3680,355),('借形斗',3730,285),('新襻间枋',3730,80),('原四椽栿梁端',3380,-125)]:ax.text(y,z,t,fontproperties=font,fontsize=11,color='#222')
ax.axhline(0,color='#555',ls=':',lw=1);ax.text(3370,10,'四椽栿顶：0',fontproperties=font,fontsize=10)
bx.axis('off');bx.set_title('检验结果与未通过项',fontproperties=font,fontsize=16,loc='left',pad=15)
rows=[('几何接口','两端各4处，共8处接触通过'),('周边碰撞','462组新增构件对，无超阈值交叠'),('重开复检','70实体重开，8处接触通过'),('批准模型','原63实体形状保持'),('原始资料复核','未通过：承托斗栱组表达不完整')]
for i,(a,b) in enumerate(rows):
 y=.9-i*.105;bx.text(.01,y,a,fontproperties=font,fontsize=12,color='#a34531' if i==4 else '#365b70',weight='bold');bx.text(.25,y,b,fontproperties=font,fontsize=12,color='#a34531' if i==4 else '#222')
bx.text(.01,.3,'需要补齐：底部栌斗、进深华栱、顺身令栱\n以及替木下小斗的实际对象与方位。',fontproperties=font,fontsize=13,linespacing=1.7,color='#a34531')
bx.text(.01,.16,'本候选只是试验副本，不进入正式采用。\n几何能贴合，不等于历史承托链正确。',fontproperties=font,fontsize=13,linespacing=1.7,color='#222')
fig.suptitle('前下平槫最小试装：几何通过，承托链完整性未通过',fontproperties=font,fontsize=19,y=.97)
fig.text(.05,.035,'剖面为模型真实坐标、同尺度。新槽形和借用参数属于探索性复原；未验证受力。原文依据：PDF第90—92页。',fontproperties=font,fontsize=11,color='#555')
fig.tight_layout(rect=[.02,.075,.98,.91]);fig.savefig('/workspace/scratch/0ab7fd249ac6/Wanfo_Lower_Front_Trial_Review_ZH.png',dpi=170)
