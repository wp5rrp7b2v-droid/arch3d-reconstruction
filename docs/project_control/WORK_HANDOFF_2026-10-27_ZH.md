# 平遥镇国寺万佛殿3D复原｜新工作窗口交接 V001

**状态截至：2026-10-27（Asia/Shanghai）**  
**性质：事实回查／只读工程状态总结，不产生新的Product Owner批准或更改正式设计结论。**  
**本文处于独立状态更新分支；未经单独批准，不视作已经合入main的正式Project Control。**

## 0. 新窗口首先应当做什么

1. 先读取 GitHub `main` 当前事实源和本文所属状态更新分支，而非依赖对话记忆；确认 `main` 提交、PR #75和#76的最新状态。
2. 本次恢复的**下一项完整工作单元是PO对PR #76四类栱昂的视觉审核**。四类：华栱、令栱、头昂、二昂。每件须明确接受/退回及修正位置；**未批准前不直接替换Master或89实体工作模型**。
3. 若PO接受某一明确形制方向，才另行授权/启动**一处最小局部替换试装**：证据对应→指定构件与位置→Blender云端生成→保存重开→源件保护→接触、穿插复验→PO局部外形审核。未获批准的形状与历史尺寸不静默升级。
4. **不重启开放式历史形制调研**。已有PR #72、#73、#74的资料应优先复用；资料缺口仍按UNKNOWN与可替换工程补全分别记录。

## 1. 项目目标和正式基线

- 正式案例：山西平遥镇国寺万佛殿；目标为**基于可追溯资料与真实构件装配关系，建立结构自洽、可重复生成的3D复原模型**，不是证明963年所有不可见细节。
- GitHub：`wp5rrp7b2v-droid/arch3d-reconstruction`；核验时 `main` 提交为 `414be293918fea2bf4138b1a8f4345272e8764a8`。
- `main`正式Project State是 `R366 / 2026-10-13`。本文与新的工作状态候选仅补足随后分支事实，**不追溯改写10月13日批准含义**。未经单独合并批准，main仍可比本分支旧。
- P3：`P3.0 / P3.1 / P3.2` CLOSED，`P3.3 构件驱动整殿重建` ACTIVE；阶段门进度3/4，**不是整殿完成75%**；P3.3 Stage3未正式关闭，T-018继续HOLD。
- 已登记Master家族基线25，Registry V008包含**505条记录而非505件已装配实体**。不得以本次新候选修改Master、Registry或已批准哈希。
- P2及既有正式局部装配快照、已有批准的东缝V011、西缝V002、两榀三道槫V002的63实体成果保留。
- 10月13日工作分支局部批准：斗形C02相关六处局部修改、上六椽栿前端C01；不代表后端/整梁/整体模型外形批准。后端七件R01外形已被PO退回，历史记录保留。

## 2. 10月17日至22日新增事实（仓库已回查）

| PR | 成果 | 现在的审批含义 |
| --- | --- | --- |
| [#72](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/72) | 79页构件图库、26个Master家族的形态可视化整改、已登记图源与Chrome浏览核验 | `OPEN DRAFT`，图库及显示工程可用，不代表单件历史几何获批 |
| [#73](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/73) | 58类实体六栏精简速览 | `OPEN DRAFT`，方便查阅，不晋升工程模型 |
| [#74](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/74) | 7页形制参考V002：F003/004/005/030/007/008/009 | `OPEN DRAFT`；形制类型方向部分有边界参考；F008下层驼峰无可信完整单件形态，仍FAIL。所画曲线非实测 |
| [#75](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/75) | 89实体联合工作候选 + BLEND/GLB + 西缝局部试装 | `OPEN DRAFT`；几何与文件核验PASS，**PO栱、昂视觉形制FAIL**，不能视为获批整体模型 |
| [#76](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/76) | 四类栱昂修正V001、五张高清审图、候选GLB与证据 | `OPEN DRAFT`；76文件公开上传及核验完成，**等待PO视觉审核**；未做替换后碰撞/接触测试 |

本次GitHub只读核验：PR #72–#76均未合并，状态为Draft。最新的内容性成果在PR #76，而非main的10月13日Dashboard旧首页。

## 3. PR #75｜89实体的工程验证范围

输入：2026-10-13的82实体上六椽栿前端C01工作BLEND；西缝新增7个候选：
- 上六椽栿候选 **1件**；
- 前华栱1件、前令栱1件、后隔架令栱2件，**共4件栱**；
- 前后散斗2件；**新增七件中不含昂**。
原82件的东缝前柱头候选包含头昂、二昂，不要误认它们是新增七件。

云端GitHub Actions运行 [39354404647](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/actions/runs/39354404647) 结果为PASS：
- 原82件模型几何及变换保持；新增5件原型刚性平移，2件散斗为适配西缝梁宽295→309mm，在承托凹口每侧各扩7mm的**试装工程处理**；
- 89实体，3916对交叠检查；最大交叠 `0.7532755588978135 mm³`，小于 `1mm³` 阈值；
- 新增10项承托接触：10/10 PASS；
- 云端Blender4.5.13保存／独立重开通过；
- BLEND SHA256 `5c81c836cc7ca3a229eebe5ac9cb4c62a744b9a1eeb10b0e9683cf0ccd097f13`；
- GLB云端重新导入89件，14460三角面，尺寸包络未变化；SHA256 `ed686f2ed81dc0ad0139a320bdd0c99709419c1c401bc1dff3b3635867f5a151`。

**上述PASS只证明限定的工程几何相容，不证明完整历史形制、隐藏榫卯、真实受力或PO视觉通过。** PO随后指出栱/昂外形不符，本PR视觉Gate明确FAIL。保留工作候选二进制，不改正式Master。

- [89实体BLEND](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/assembly/west-spacer-from-east-v001-20261020/production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WANFO_WEST_SPACER_TRIAL_V001.blend)
- [89实体GLB](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/assembly/west-spacer-from-east-v001-20261020/production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WANFO_WEST_SPACER_89_TRIAL_V001.glb)
- [接触/交叠验证](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/assembly/west-spacer-from-east-v001-20261020/production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WEST_SPACER_VALIDATION.json)

## 4. PR #76｜最新视觉审核交付

分支 `review/gong-ang-form-v001-20261021`；基于PR #75的 `f8f72d40dd47ab61abc3103c396c855f5c4c3865` 提交；审核成果提交 `028517cbdada6cb266feae17f58ae0a7888c4a93`。

- **76个新增审核文件，总计10,275,157字节**；PR #76记录了公开原始下载76/76 HTTP 200，逐文件字节和SHA-256 76/76一致。PR文件对比为**新增76、修改0、删除0**。此为实际发布验证，不代表候选外形验收。
- 交付五张图：总览3000×2700，四张详细图3000×2180，含中文标注、实际Master/试装网格/参考图/修正候选的可见轮廓。
- 提取真实试装网格8件、原Master参照体5件、独立候选7个（华栱第一/二跳、令栱、头昂、二昂、两件昂的工作长版本），候选GLB可读取，封闭正体积；并有13+接触定位原始记录。
- 保留原Master基线参数（华栱第一/二跳898.8/1630mm的参考长，令栱897×217.4×155.6mm参考包络，昂的控制段与工作长另分），不将Master控制段擅称历史整木全长。
- 显式区分 `FACT` / `INFERENCE` / `UNKNOWN`，并明确栱广/材厚轴映射在Master和局部试装件间存在差异，尚未统一裁定。隔架中的“令栱”名称不能自动证明它等于外檐最外跳令栱。
- `DELIVERY_VALIDATION.json` 为交付/提取范围PASS；`VISUAL_REVIEW.json`为 `READY_FOR_PO_VISUAL_REVIEW_NOT_FORM_APPROVAL`；**PO未批准**；未测试候选替换后接触/碰撞、榫卯与承载。

审核图按建议顺序：
1. [总览](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/output/OVERVIEW_ZH.png)
2. [华栱](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/output/HUAGONG_COMPARISON_ZH.png)
3. [令栱](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/output/LINGGONG_COMPARISON_ZH.png)
4. [头昂](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/output/TOUANG_COMPARISON_ZH.png)
5. [二昂](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/output/ERANG_COMPARISON_ZH.png)

[PR #76审核说明与数值边界](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/README_ZH.md)

## 5. 尚未完成/风险

| 项目 | 当前状态 | 不能宣称的内容 |
| --- | --- | --- |
| PR #76四类栱昂修正 | **PO视觉审核待定** | 不能宣称通过或改动Master |
| PR #75原89实体外观 | **PO视觉FAIL** | 不能作为最终批准装配模型 |
| 头昂/二昂实际长度与隐藏端 | 工作设计值与候选；完整历史外形UNKNOWN | 不能称为原物精确复原 |
| 栱、昂Master与试装件截面轴 | 映射差异已识别，仍需具体安装实例判定 | 不能简单整体镜像/缩放 |
| PR #74 F008下层驼峰 | 现有类型信息可读，完整形制仍FAIL | 不应据示意升级历史真形 |
| 89实体新候选替换后接口 | 未测试 | 不因原V001几何PASS自动批准新候选 |
| Stage3、整殿完成率、结构强度 | 未闭合/未验证 | 不扩大局部试装结论 |
| 本地Mac同步 | 当前未取得2026-10-27终端同步证据 | 不宣称本地已同步 |
| main Project Control | R366/10月13日；本次为状态更新审核分支 | 不宣称R367已合入main |

## 6. 审批、安全及操作边界

- PO决定停止开放式形制调研、保留成果、继续模型装配；但后来明确判定已有栱、昂外观不符，应先审核新形制候选。**没有将PR #76候选视觉通过的授权**。
- 正式Master、89实体BLEND/GLB、505 Registry及历史已批准快照不覆盖、不删除、不修改。本次是状态文字同步，不是几何生产。
- `main`合并、正式基线变化、删除批准成果仍需PO另行审批。PR #75/#76以及本次状态更新PR保持Draft。
- Blender脚本化操作只走GitHub Actions云端；不能因工作转移而要求PO下载/安装Blender。
- 所有工程/研究成果保留GitHub分支；Mac只从GitHub拉取，**不提供每日ZIP替代同步**。
- 工程PO仍只需要看具有明确证据边界的候选视觉结论与必要工作单元结果；不再为简单步骤反复发起继续确认。

## 7. 本次状态更新的核验结论与停止点

- 本轮工作是**把GitHub已有工作分支事实总结为跨对话交接和拟更新的项目状态**，不创建新构件、不执行模型生成、不重跑历史验证。
- GitHub PR #72–#76、main状态及既有记录已经实际读取。PR #76的文件完整性/公开下载验证引用其原有验证档案；本轮不会伪称重新逐字节下载全部76文件。
- 合并前保持 `MAIN_PUBLICATION_PENDING`：若新窗口以main为唯一输入，会继续读到R366和10月13日看板。**新窗口应首先读取本文分支及对应Draft PR，并与main交叉核对。**
- 下一工作单元需等PO针对华栱、令栱、头昂、二昂逐项给出形制方向；建议仅对**一处**批准范围开展局部装配试验，验收为源几何保护、接触／交叠、保存重开与视觉审核四项均通过。
