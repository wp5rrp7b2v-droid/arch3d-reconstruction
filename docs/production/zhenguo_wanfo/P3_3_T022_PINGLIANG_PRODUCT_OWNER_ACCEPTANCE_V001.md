# P3.3｜T-022 平梁 Master 首件｜Product Owner Acceptance V001

Date: 2026-09-20  
Decision: **D-074**  
Task: `T-022｜P3_3_PINGLIANG_MASTER_FIRST_ARTICLE_V001`  
Master: `CMP-FRAME-PINGLIANG-001_MASTER`

## 1. Formal Decision

**PRODUCT OWNER APPROVED / FIRST ARTICLE ACCEPTED**

T-022 平梁 Master V001 的工程验证、视觉审核与证据边界审核均通过。该首件自 D-074 起正式获得 Product Owner 批准。

本批准不等于：
- P3.3 Stage 1 整体 PASS；
- PR #9 已合并；
- Stage 2 已授权；
- T-018 恢复；
- 山面平梁实测厚度已被发现或历史化。

## 2. Accepted Evidence

- PR：#9
- Branch：`codex/t022-p3-3-pingliang-master-first-article-v001`
- Reviewed head：`0ddf8290345e4087b7173e89993d3022e2ba730c`
- GitHub Actions Run：`35483530705` / Run #2 / **SUCCESS**
- Validation：**56 / 56 PASS**
- Blender：**4.5.13 LTS**
- Independent reopen：EW_SEAM + GABLE = **PASS**
- Mutations：Length / EW Width / EW Thickness / GABLE Completion Thickness = **PASS**
- Canonical restore：**PASS**
- Review images：**10 / 10 PASS**
- Artifact ID：`10597296654`
- Artifact ZIP SHA-256：`31670f3654fa2f088900b06c0d7d5d7c1b8a1dbeb221dce692bb85cce4f40839`

## 3. Accepted Variant Geometry

### EW_SEAM

- instances：平梁-东缝 / 平梁-西缝
- raw samples：390×280 mm / 401×281 mm
- sample-to-instance mapping：UNKNOWN
- production section：**395.5 × 280.5 mm**
- classification：DIRECT_MEASURED_FAMILY_MEAN
- canonical binary SHA-256：
  `5c077efe8d39299c8f0a0da39b02b460d3116a204888a17a203dccd189e5d8f4`
- semantic geometry signature：
  `5805215c4aa4a18bc3f100af855c2442efdb8d4cb07d334a1aeabbf39b74fdb7`

### GABLE

- instances：平梁-东山 / 平梁-西山
- observed sample：width 346 mm / thickness UNKNOWN
- production section：**346 × 245.4 mm**
- 245.4 mm classification：**PARAMETRIC_COMPLETION / PROJECT_RULE / REPLACEABLE / historical_claim=false**
- 346 mm generalized to both gable instances：replaceable production completion
- observed thickness：**UNKNOWN / null**
- canonical binary SHA-256：
  `f2ecff85c6179481ba156f5f2a249cc7e060be623e3e99a6ee03d8d2ad22f59a`
- semantic geometry signature：
  `262f8493b7656f94e4112a8405be565893d89be7c099d83f63bde149d7993c40`

## 4. Locked Boundaries

- historical full length：UNKNOWN / null
- canonical reference length：1000 mm / non-historical Master reference only
- building instance length：later derived from explicit assembly endpoints
- no unsupported joinery / groove / end profile / camber / hidden connection
- report fen analysis remains metadata only
- GABLE 245.4 mm must never be restated as observed/report/historical value

## 5. Publication Instruction

D-074 additionally authorizes formal-delivery materialization:
1. correct T-021 Stage1 Catalog status to Product Owner Approved / D-072;
2. register T-022 Pingliang Master as Product Owner Approved / D-074;
3. materialize approved T-022 semantic / validation / engineering review / 10 review PNG;
4. perform final cross-check;
5. request PR #9 merge only after cross-check PASS.

PR #9 merge remains a separate authorization boundary.

**T-022 FIRST ARTICLE = PRODUCT OWNER APPROVED / D-074**  
**P3.3 Stage 1 = ACTIVE / NOT YET PASSED**  
**T-018 = HOLD**
