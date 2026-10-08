from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle
ROOT=Path(__file__).resolve().parents[3]
fp=FontProperties(fname=str(ROOT/'tmp/chinese_font.ttf'))
plt.rcParams['font.family']=fp.get_name()
fig=plt.figure(figsize=(14,7),facecolor='#f7f8fa')
gs=fig.add_gridspec(1,2,width_ratios=[1.15,1],left=.025,right=.98,bottom=.14,top=.85,wspace=.07)
ax=fig.add_subplot(gs[0]);ax.imshow(plt.imread(ROOT/'tmp/full_section_upright.png'))
ax.set_xlim(380,1160);ax.set_ylim(660,310);ax.axis('off')
ax.add_patch(Rectangle((608,397),291,36,fill=False,edgecolor='#2563eb',lw=2))
ax.add_patch(Rectangle((485,450),531,81,fill=False,edgecolor='#d97706',lw=2))
def label(text,xy,at,color):
    ax.annotate(text,xy,xytext=at,fontproperties=fp,fontsize=12,color=color,ha='center',arrowprops={'arrowstyle':'->','color':color,'lw':1.8},bbox={'facecolor':'white','edgecolor':'none','alpha':.96,'pad':4})
label('四椽栿：上层较短的梁',(754,411),(750,344),'#2563eb')
label('下平槫斗栱：更外侧的承托区域',(500,499),(610,578),'#b45309')
label('上六椽栿',(756,476),(855,617),'#b45309')
ax.text(400,647,'原测绘剖面局部｜仅用于识别关系，不按像素定长',fontproperties=fp,fontsize=10,color='#475569')
bx=fig.add_subplot(gs[1]);bx.axis('off')
for y,t,c,size in [(.96,'本轮发现：先查梁长与轴线绑定','#0f172a',17),(.82,'现有四椽栿全长：7192 毫米','#2563eb',14),(.73,'快照已标为工作假设，不是实测全长','#475569',12),(.59,'只读敏感性检查：14 个样例／70 组','#0f172a',14),(.48,'缩小梁体副本的纵向延伸后，','#475569',13),(.41,'原有 10 处交叠可以全部消失。','#b45309',14),(.29,'这只说明交叠对梁长敏感，','#475569',12),(.22,'不能据此确定新梁长或宣布整榀通过。','#475569',12),(.09,'批准模型未改｜暂不削梁、移榀或改标高','#166534',13)]:
    bx.text(.02,y,t,transform=bx.transAxes,fontproperties=fp,fontsize=size,color=c,va='top')
fig.text(.035,.93,'前下平槫节点核对：问题可能在工作包络的轴线绑定',fontproperties=fp,fontsize=21,color='#0f172a')
fig.text(.035,.075,'下一项：核对四椽栿两端、上平槫轴线及上托脚落点；任何批准模型变更须另行审批。',fontproperties=fp,fontsize=13,color='#334155')
fig.text(.035,.035,'资料依据：测绘报告图纸06／11／12、图2-40、附件1-6；右侧为本轮计算结果，不是正式修订方案。',fontproperties=fp,fontsize=10,color='#64748b')
fig.savefig(ROOT/'Wanfo_Beam_Axis_Binding_Review_ZH.png',dpi=170)
