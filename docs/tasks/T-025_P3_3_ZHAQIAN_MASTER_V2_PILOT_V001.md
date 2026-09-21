# T-025｜P3.3 剳牵 Master V2 Slim Pilot｜Lifecycle Record V001

Status: **VISUAL GATE PASS / V2 DEFINITION DRAFTED / ENGINEERING EXECUTION NOT AUTHORIZED**  
Date: 2026-09-21  
Decision: **D-088**  
Branch: `codex/t025-p3-3-zhaqian-master-v2-pilot-v001`  
Master: `CMP-FRAME-ZHAQIAN-001_MASTER`

## 1. Pilot objective

以剳牵作为 Stage1 第一个 V2 瘦身建模 Pilot，同时验证：

1. 构件 Master 几何/证据验证强度不下降；
2. 普通构件专属正式文件由约 20 个收敛到目标 6 个；
3. 6 张 review PNG 合并为 1 张 Review Board；
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

## 4. V2 six-file target

Component-specific formal outputs:

1. `MASTER_DEFINITION_V001.json`
2. `MASTER_SEMANTIC_V001.json`
3. `MASTER.blend` — Actions artifact + local only, not Git
4. `MASTER_REVIEW_BOARD_V001.png`
5. `MASTER_VALIDATION_V001.json`
6. this lifecycle record `T025_MASTER_RECORD_V001.md`

The Review Board must contain six panels:
FRONT / SIDE / TOP / AXON / DIMENSION PARAMETER / EVIDENCE + UNCERTAINTY.

Individual panel PNGs may be runtime temporary files only and must not become formal repository outputs.

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
- one Review Board exists and contains all six required panels;
- no canonical .blend committed to Git.

## 7. Current authorization boundary

D-088 approves only:
- D-076 visual gate;
- selection of 剳牵 as V2 Pilot;
- V2 Definition drafting and T-025 lifecycle-contract creation.

D-088 does **not** authorize:
- Blender execution;
- GitHub Actions production run;
- final Master approval;
- Catalog/V008 approved binding;
- PR merge;
- Stage1 PASS;
- T-018 resume.

Next decision required:

> **Product Owner approves/locks the V2 Master Definition and explicitly authorizes T-025 engineering execution.**
