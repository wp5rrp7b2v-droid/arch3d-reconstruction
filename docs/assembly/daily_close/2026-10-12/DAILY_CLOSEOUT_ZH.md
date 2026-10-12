# 万佛殿｜2026-10-12收尾登记

今日工程停止。状态：**PASS WITH KNOWN EXCEPTIONS**。本次完成批准身份绑定、验证结果归档与Project Control / Dashboard一致性同步；Mac同步待实际执行。

| 工作 | 当前状态 | 本阶段实际证明 |
|---|---|---|
| 三构件原图—网格核对V002 | 有界审核完成；完整形态NOT VERIFIED | 输入身份、原表与实际网格可追踪；条件性投影不能作实物轮廓真值 |
| 东前隔架V002 / 东后节点V001 | PO局部设计批准，D-288 / D-289 | 67 / 71实体工作版本及指定接口原验证；完整梁当时仍是片段 |
| 通长上六椽栿V001 | 候选待审 | 一根梁70实体工作版本、新梁69对及10接口原验证通过；10710mm为复原设计长度 |
| 叉手脚端 / 脊部接口修正 | PO局部批准，D-290 | 70实体、2415对及20接口原验证；编码精度修复不改源几何，隐藏榫卯及强度未验证 |
| 一端柱头铺作V004 | PO局部修正批准，D-291 | 本对话重跑GLB独立读回：82体封闭正体积单连通，3321对≤1mm³，最大0.270476620589mm³，17接口有正面积与向下接触投影；原70件源几何保持 |

## 字段纠正及批准边界

V002/V003误把交互斗欹高61.1mm当耳高或槽深；V004纠正为总148.5−平35.5−欹61.1=余耳51.9mm。此余耳为统计均值差推算；候选槽深尚未实测。两跳华栱上皮间距改为310.8mm。仅修正7个未批准候选，旧文件和既有批准快照保留。

V004批准不自动批准其中通长上六椽栿，也不认定完整铺作、完整外形、完整昂长、真实槽口、历史榫卯或承载力。后端与西缝柱头铺作未由此通过。不晋升Master，不改变505记录/25Master，正式Stage3未关闭。

本次核对东前/东后绑定的8份文件及叉手模型/审核图的2份SHA256与大小。V004交付manifest14/14身份一致，重新执行几何检查通过。前期验证按已交付报告引用，本次不声称全部重跑。原始资料本次收尾没有重新访问，不冒充独立来源复核。

## 已知例外

- Mac同步未执行，尚无用户本地HEAD或工作区输出。
- 通长上六椽栿仍待审；图纸方向绑定与未见端部保留复原设计边界。
- 完整形态、槽深、昂长及承载力未证实。
- 旧Dashboard折叠区仍为历史；当前首页为R362 / v216。
- D-287记录的T-039既有CI断言问题不在本次修改范围；不宣称全部CI通过。

无新Phase关闭，Phase Archive不新增；Governance和Rules Change Log核对后不变。公开仓库仅登记批准、SHA256、验证摘要及同步状态；完整模型和详细证据仍由交付包提供。旧候选内部NOT_PUBLISHED/待审标签保留历史意义，外部批准绑定接续状态。既有开放/HOLD PR不合并或关闭。

## 下一工作单元

先核验本地同步；下次核对斗体外轮廓及梁—昂接入形态。验收：可见形态与万佛殿照片/节点图相符；无法辨认部分保留明确可替换假设；发现直接冲突再提局部修改，不凭本轮几何PASS复制后端。

## Mac同步

在 /Users/caroline/中国古建筑3D复原 运行下面的安全同步命令；遇到已跟踪改动、分支分歧或快进失败则停止，不覆盖文件。

```bash
cd '/Users/caroline/中国古建筑3D复原'
bash <<'SYNC'
set -e
git status --short --branch
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo '发现已跟踪改动，停止同步并保留文件。'
  exit 1
fi
git switch main
git-proxy-auto fetch origin
git-proxy-auto pull --ff-only origin main
git rev-parse HEAD
git rev-parse origin/main
git status --short --branch
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
python3 scripts/check_dashboard_project_state.py
SYNC
```

两个HEAD相同、无已跟踪改动、检查输出R362 PASS后，才记本地登记同步PASS。original sources等未跟踪目录保留。Git同步取得登记与控制文件；完整今日二进制需另行下载交付包，不把元数据同步当作模型文件已下载。

## 发布授权补记

PO于2026-10-12 21:39:57（Asia/Shanghai）明确授权将本包收尾登记、Project Control、Dashboard及哈希/验证摘要发布到wp5rrp7b2v-droid/arch3d-reconstruction。完整模型二进制不上传。此前自动审批拒绝已由此明确授权解决。此提交仅发布已有批准及收尾记录，不改变工程批准范围或宣布Mac同步完成。
