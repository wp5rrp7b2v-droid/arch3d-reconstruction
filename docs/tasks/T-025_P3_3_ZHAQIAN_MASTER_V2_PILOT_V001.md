# T-025｜P3.3 剳牵 Master V2 Slim Pilot｜Lifecycle Record V001

Status: **PRODUCT OWNER APPROVED / D-091 / FORMAL DELIVERY AUTHORIZED / PR MERGE PENDING**  
Date: 2026-09-21  
Decisions: **D-088 / D-089 / D-090 / D-091**  
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

## 7. Authorization boundary

D-090 authorized first-article engineering execution. D-091 subsequently approved the first article and formal-delivery closure.

Still not authorized:
- PR #12 merge;
- Stage1 PASS;
- Stage2;
- T-018 resume.


## 8. First-article engineering result

**Run #3 PASS / ENGINEERING COMPLETE / PRODUCT OWNER REVIEW REQUIRED**

- GitHub Actions Run: `35572874173`
- reviewed head: `834765fede99325b3e53cc8b298e00613c810c96`
- Blender: `4.5.13 LTS`
- machine validation: **35/35 PASS**
- canonical .blend SHA-256: `d8636ae910d286f3629b3ab0b087a18f6e70dbbc8f967ef30d79c4454f4e4cd6`
- semantic geometry signature: `bab035240ac2fe82117dc66b8da388d5cf1484081e608ef872e9da53890ecf1e`
- Review Board SHA-256: `b53f38d58dd697c293b65a59862a780690bd12b963340c213e5d51ec30e2a7fd`
- Artifact ID: `10626941998`
- Artifact ZIP SHA-256: `86d7defe94d64deddc2eb4020f69dffbec352e56bf2f49ec66d222cf853a325a`
- Artifact size: 1,321,991 bytes
- Review Board: 3600 × 1880 px / 6 Definition-required panels

Formal generated artifact contains exactly four files:

1. `CMP-FRAME-ZHAQIAN-001_MASTER_V001.blend`
2. `CMP-FRAME-ZHAQIAN-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-ZHAQIAN-001_MASTER_REVIEW_BOARD_V001.png`
4. `CMP-FRAME-ZHAQIAN-001_MASTER_VALIDATION_V001.json`

Together with the two component-specific repository files:

5. `CMP-FRAME-ZHAQIAN-001_MASTER_DEFINITION_V001.json`
6. `T-025_P3_3_ZHAQIAN_MASTER_V2_PILOT_V001.md`

the Zhaqian Pilot currently resolves to **6 component-specific formal files**. This is a result of the minimal-sufficient analysis, **not a universal file-count rule**.

### Superseded failed runs

- Run `35572328310`: FAILED only at validator check `31_no_tracked_blend`.
- Run `35572381543`: same superseded validator boundary / FAILED.
- Root cause: validator incorrectly prohibited any tracked `.blend` anywhere in the repository, while main legitimately retains historical P0.2 roundtrip asset `poc/P0_2_cloud_roundtrip/input/P0_2_CLOUD_INPUT_V001.blend`.
- Correction: the guard now checks only that the **current V2 Master directory** contains no tracked canonical `.blend`.
- No geometry, Definition, Semantic, mutation, reopen, Review Board, or evidence rule was weakened to obtain Run #3 PASS.

## 9. Product Owner review result

**PASS / superseded by D-091 acceptance.**

The reviewed Board, geometry boundary, evidence/UNKNOWN boundary and minimal-sufficient package were accepted without requesting geometry changes.


## 10. Product Owner acceptance / D-091

**PRODUCT OWNER APPROVED / FIRST ARTICLE ACCEPTED / FORMAL DELIVERY AUTHORIZED**

Product Owner approved the T-025 Zhaqian V2 first article on 2026-09-21.

Accepted evidence:
- Run: `35572874173` / SUCCESS
- validation: **35/35 PASS**
- accepted engineering head: `834765fede99325b3e53cc8b298e00613c810c96`
- canonical .blend SHA-256: `d8636ae910d286f3629b3ab0b087a18f6e70dbbc8f967ef30d79c4454f4e4cd6`
- semantic geometry signature: `bab035240ac2fe82117dc66b8da388d5cf1484081e608ef872e9da53890ecf1e`
- Review Board SHA-256: `b53f38d58dd697c293b65a59862a780690bd12b963340c213e5d51ec30e2a7fd`
- Artifact ID: `10626941998`
- Artifact ZIP SHA-256: `86d7defe94d64deddc2eb4020f69dffbec352e56bf2f49ec66d222cf853a325a`

D-091 authorizes materialization of the exact approved Artifact's Semantic / Validation / Review Board, Stage1 Catalog registration, V008/CURRENT + derived Excel synchronization, and final regression / pre-merge cross-check.

D-091 does **not** authorize PR #12 merge, Stage1 PASS, Stage2 authorization, or T-018 resume.


## 11. Formal materialization

**PASS / EXACT APPROVED ARTIFACT MATERIALIZED**

- publication workflow run: `35574922533`
- job: `publish-approved-artifact` = SUCCESS
- materialization commit: `b4ccd8c37eb7166e3a4ed340ce83c242a541d187`
- source Artifact ID: `10626941998`
- source Artifact ZIP SHA-256: `86d7defe94d64deddc2eb4020f69dffbec352e56bf2f49ec66d222cf853a325a`
- exact-source verification: PASS before copy
- materialized files: Semantic / Validation / single adaptive Review Board
- canonical .blend remains Actions Artifact + local-only and is not tracked in the Master directory.

The locked Master Definition was restored to the exact bytes used by accepted Run 35572874173. Acceptance/publication metadata stays in this Lifecycle Record and Decision Log so the generated Semantic's `definition_sha256` remains valid.

## 12. Registry / Catalog closure

**PASS / JSON AUTHORITIES UPDATED**

- Stage1 Catalog: **11 approved Masters**
- V008/CURRENT Zhaqian rows: **14/14 bound** to `CMP-FRAME-ZHAQIAN-001_MASTER`
- Stage1 Master progress: **11 / 28 = 39.3%**
- approved-Master-covered registry rows: **66**
- pending Masters: **17**
- derived Excel remains a derived view and must sync from these JSON authorities before final record closure.

Final regression and PR #12 pre-merge cross-check are still required before requesting merge authorization.
