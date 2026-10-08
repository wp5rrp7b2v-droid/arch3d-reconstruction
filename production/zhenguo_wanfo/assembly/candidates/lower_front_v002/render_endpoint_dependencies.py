from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle,Polygon
import trimesh
ROOT=Path(__file__).resolve().parents[3]
fp=FontProperties(fname=str(ROOT/'tmp/chinese_font.ttf'))
a=json.loads((ROOT/'tmp/two_frames/west_v002/REOPENED_WEST_V002_MESHES.json').read_text())
o=next(o for o in a['objects'] if o['id']=='TUOJIAO_FRONT');m=trimesh.Trimesh(o['vertices'],o['faces'],process=False)
section=m.section(plane_normal=[1,0,0],plane_origin=[0,0,0])
fig,axes=plt.subplots(1,2,figsize=(13,6),facecolor='#f8fafc')
for ax,length,title in zip(axes,[7192,6000],['原批准试装：托脚接触面完整','只缩短梁的诊断副本：接触面被截断']):
    ax.set_facecolor('#ffffff');ax.add_patch(Rectangle((1600,-440),length/2-1600,440,color='#cbd5e1'))
    for poly in section.discrete:ax.add_patch(Polygon(poly[:,[1,2]],facecolor='#e9b45c',edgecolor='#8b5e21',lw=1.5))
    ax.plot([2818.213,3338.920],[0,0],color='#dc2626',lw=7,label='原托脚接触面')
    ax.plot([2818.213,min(length/2,3338.920)],[0,0],color='#16a34a',lw=4)
    ax.axvline(1836,ls='--',color='#2563eb',lw=1.1)
    ax.text(1848,855,'上平槫轴线',fontproperties=fp,color='#2563eb',fontsize=11)
    ax.text(1880,-260,'四椽栿工作包络',fontproperties=fp,color='#334155',fontsize=12)
    ax.text(2460,435,'上托脚',fontproperties=fp,color='#8b5e21',fontsize=13)
    ax.set_xlim(1600,3700);ax.set_ylim(-500,1000);ax.set_aspect('equal');ax.set_title(title,fontproperties=fp,fontsize=14,pad=15)
    ax.set_xlabel('局部进深坐标（毫米）',fontproperties=fp);ax.set_ylabel('局部标高（毫米）',fontproperties=fp)
    ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.15)
axes[0].text(2240,-470,'绿色：原接触面保留100%',fontproperties=fp,color='#15803d',fontsize=11)
axes[1].text(2140,-470,'绿色：仅保留约35%；红色：失去梁下承托',fontproperties=fp,color='#b91c1c',fontsize=10)
fig.suptitle('为什么不能只缩短梁？梁端与托脚需要联合复核',fontproperties=fp,fontsize=20,color='#0f172a',y=.98)
fig.text(.065,.08,'完整保留四处原接触面时，下平槫仍有两处干涉；不把接触面积比例当作承载能力结论。',fontproperties=fp,fontsize=12,color='#334155')
fig.text(.065,.035,'图为当前西端网格的局部截面｜6000毫米仅为诊断值，不是推荐梁长｜批准模型未修改',fontproperties=fp,fontsize=10,color='#64748b')
fig.subplots_adjust(left=.065,right=.98,bottom=.19,top=.86,wspace=.2)
fig.savefig(ROOT/'Wanfo_Beam_Foot_Endpoint_Review_ZH.png',dpi=170)
