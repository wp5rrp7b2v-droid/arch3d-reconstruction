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
label('更正：上层短梁是平梁',(754,411),(750,344),'#2563eb')
label('下平槫斗栱：更外侧的承托区域',(500,499),(610,578),'#b45309')
label('四椽栿：位于平梁下方',(756,476),(855,617),'#b45309')
ax.text(400,647,'原测绘剖面局部｜仅用于识别关系，不按像素定长',fontproperties=fp,fontsize=10,color='#475569')
bx=fig.add_subplot(gs[1]);bx.axis('off')
for y,t,c,size in [(.96,'本轮更正：平梁与四椽栿不能混同','#0f172a',16),(.82,'此前蓝框误标为四椽栿，现已更正。','#b91c1c',13),(.73,'蓝框是平梁；橙框区域是四椽栿。','#475569',12),(.59,'撤回按“上层短梁”截短四椽栿的方向','#0f172a',13),(.48,'裁切能消除交叠，只是几何敏感性；','#475569',12),(.41,'不是历史处理方法或正确梁长的证据。','#475569',12),(.29,'下一项：四椽栿端与下平槫栱枋穿插。','#b45309',12),(.22,'原 10 处交叠仍有效，候选仍未通过。','#475569',12),(.09,'批准快照与正式方案未改｜旧解释已撤回','#166534',12)]:
    bx.text(.02,y,t,transform=bx.transAxes,fontproperties=fp,fontsize=size,color=c,va='top')
fig.text(.035,.93,'定位更正：先区分平梁与四椽栿，再处理下平槫节点',fontproperties=fp,fontsize=21,color='#0f172a')
fig.text(.035,.075,'下一项：核对下平槫节点中的梁端与栱枋关系，不按错误层级改梁长或翻转托脚。',fontproperties=fp,fontsize=13,color='#334155')
fig.text(.035,.035,'更正依据：测绘报告PDF82／83、图2-40／2-41、图纸06／11／12；旧敏感性数值保留，不作为方案推荐。',fontproperties=fp,fontsize=10,color='#64748b')
fig.savefig(ROOT/'Wanfo_Beam_Axis_Binding_Review_ZH.png',dpi=170)
