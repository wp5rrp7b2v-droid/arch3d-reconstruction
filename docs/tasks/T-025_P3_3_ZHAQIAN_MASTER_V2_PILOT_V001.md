# T-025｜P3.3 剳牵 Master V2 Slim Pilot｜Lifecycle Record V001

Status: **VISUAL GATE PASS / V2 DEFINITION LOCKED / D-089 MINIMAL-SUFFICIENT RULE / D-090 ENGINEERING EXECUTION AUTHORIZED / FIRST ARTICLE RUNNING**  
Date: 2026-09-21  
Decisions: **D-088 / D-089 / D-090**  
Branch: `codex/t025-p3-3-zhaqian-master-v2-pilot-v001`  
Master: `CMP-FRAME-ZHAQIAN-001_MASTER`

## 1. Pilot objective

以剳牵作为 Stage1 第一个 V2 瘦身建模 Pilot，同时验证：

1. 构件 Master 几何/证据验证强度不下降；
2. 删除重复职责和冗余输出，使普通简单构件可由约 20 个文件收敛到最小充分文件集；剳牵当前预计约 6 个，但不设固定文件数；
3. 重复 review PNG 优先合并为 Review Board；Review Board 的 panel 数由构件 Definition 按复杂度声明，不设固定六宫格；
4. builder / validator / workflow 转为可复用共享基础设施，不再逐构件复制；
5. 输入 Definition、生成 Semantic、机器 Validation 继续保持独立，避免为了少文件而失去交叉验证。

## 2. D-076 visual-reference gate

**PASS / PRODUCT OWNER APPROVED / D-088**

同建筑视觉/结构参考：
- https://www.thepaper.cn/newsDetail_forward_27389245
- 该资料明确描述万佛殿两侧山面铺作经丁栿联系心间梁架，**其上再设剳牵、托脚**。
- 本来源仅用于构件结构层位与视觉审核，不作为截面尺寸、历史长度、榫卯尺寸权威。

尺寸与数量权威仍为：
`P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json / V008`

## 3. Locked current evidence boundary

- physical instances: 14
- east gable known: 2
- west gable known: 2
- remaining exact locations: 10 UNKNOWN
- canonical family section: 331.5 × 185.0 mm / V008 locked family mean
- historical full length: UNKNOWN / null
- canonical reference length: 1000 mm / NON_HISTORICAL_REFERENCE_ONLY
- sample-to-instance mapping: UNKNOWN
- exact endpoints: UNKNOWN
- hidden joinery / end profile: UNKNOWN / not modeled in Stage1

## 4. V2 minimal-sufficient package

原则：**不是追求固定 6 个文件，而是追求最小充分文件集。**

剳牵作为简单长构件，当前预计 formal outputs 为：

1. `MASTER_DEFINITION_V001.json`
2. `MASTER_SEMANTIC_V001.json`
3. `MASTER.blend` — Actions artifact + local only, not Git
4. `MASTER_REVIEW_BOARD_V001.png`
5. `MASTER_VALIDATION_V001.json`
6. this lifecycle record `T025_MASTER_RECORD_V001.md`

剳牵当前 Review Board 需要 6 个 panels：FRONT / SIDE / TOP / AXON / DIMENSION PARAMETER / EVIDENCE + UNCERTAINTY。

这只是剳牵本身的 required panels，不是全项目统一六宫格。后续构件可少可多，由各自 Master Definition 声明；复杂构件可增加 BOTTOM / SECTION / DETAIL / VARIANT COMPARISON 等。

Individual panel PNGs may be runtime temporary files only and must not become formal repository outputs.

### Minimal-sufficient rules

- 作用重复、内容冗余且合并后不损害追溯/验证/可读性的文件，应合并。
- Definition、generated Semantic、Validation 三者必须保持独立，因为它们构成输入—结果—验证的交叉校验。
- UNKNOWN、不确定性、来源绑定、参数边界、验收结论不得为了减少文件而删除。
- 构件复杂度确有需要时，允许增加 formal file / review board / review panel；不得为了数字好看而压缩。
- validator 检查“Definition 声明的信息域和 review panels 是否完整”，不检查全项目统一文件数或统一 panel 数。

## 5. Shared infrastructure target

T-025 execution should introduce or reuse shared V2 infrastructure:

- one reusable Blender builder for bounded long-member Masters;
- one reusable V2 validator driven by Master Definition;
- one reusable Stage1 Master V2 Actions workflow.

Do **not** create `zhaqian_master_common.py`, `validate_zhaqian_master.py`, and a dedicated Zhaqian-only workflow unless a genuine non-shareable geometry requirement is discovered and recorded.

## 6. Validation strength retained

The slim architecture must still machine-check at minimum:

- V008 identity and 14-instance count;
- known/unknown location boundary;
- 331.5 × 185 mm section;
- historical full length remains null;
- 1000 mm reference cannot leak into building assembly;
- canonical bbox / origin / transform;
- independent reopen;
- deterministic restore;
- length/width/thickness mutation isolation;
- no unsupported joinery/end geometry;
- Definition ↔ Semantic ↔ Validation identity;
- Review Board(s) cover every panel required by this Master Definition;
- no canonical .blend committed to Git.

## 7. Current authorization boundary

D-090 now authorizes:
- locked Zhaqian V2 Master Definition;
- shared V2 infrastructure implementation;
- GitHub Actions + Blender 4.5.13 first-article execution.

Still **not authorized / not yet approved**:
- final Master acceptance;
- Catalog/V008 approved binding;
- PR merge;
- Stage1 PASS;
- T-018 resume.

Current next decision:

> **Review the first-article machine evidence + Review Board and decide Product Owner acceptance.**
