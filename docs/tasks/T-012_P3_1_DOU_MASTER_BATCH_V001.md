# 【中国古建筑3D复原｜T-012｜P3_1_DOU_MASTER_BATCH_V001｜斗类三构件Master批次生产】

Status: **DRAFT / PRODUCT OWNER REVIEW REQUIRED / NOT AUTHORIZED**  
Think Level: **HIGH**  
Phase/Gate: P3 / P3.1  
Date: 2026-09-13

## 1. Objective

在已锁定的 `P3.1 Canonical Master Asset Contract V002`（D-036）和已批准的 T-011 柱 Master Pilot 方法基础上，仅对以下 3 个已批准 `MASTER_REQUIRED` 构件执行正式 Component Master 批次生产：

1. `CMP-LUDOU-COLUMN-001｜柱头栌斗`
2. `CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗`
3. `CMP-DOU-INTERACTIVE-001｜交互斗`

执行完整资产链：

> **evidence-aware params → deterministic generator → local-only canonical `.blend` → semantic QC → standard review package → Registry registration → independent reopen / mutation validation**

本任务的核心不是补齐“看起来像斗”的传统细节，而是把当前直接证据能够支持的几何范围正式转化为可复用、可验证、可替换的 evidence-bounded digital Masters。

T-012 COMPLETE 不等于 Product Owner 最终批准，也不等于 P3.1 PASS；上下六椽栿仍保持未授权。

---

## 2. Authoritative Inputs

必须完整读取并遵守：

1. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md`（LOCKED / D-036）；
2. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`（LOCKED / D-036）；
3. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002_CHANGE_PROPOSAL.md`；
4. `docs/production/zhenguo_wanfo/P3_1_DEFINITION_OF_DONE_V001.md`（LOCKED / D-032）；
5. `docs/production/zhenguo_wanfo/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.md/json`；
6. `docs/production/zhenguo_wanfo/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.md/json`；
7. P3.0 Ontology / Registry / Schema / Migration Audit；
8. P1 approved direct evidence package，特别是 `P1_2_DIRECT_PAGE_REVIEW_V001.md` D-007 / D-008；
9. P2 frozen parameter / dependency / integration baseline；
10. 已批准柱 Pilot 资产链与 Registry：T-011 / D-035，只作为方法参考，不得修改其结果；
11. `docs/project_control/project_state.json`、`decision_log.md`、`acceptance_matrix.md`、`governance.md`、`rules_change_log.md`；
12. D-028～D-036、CG-02～CG-06；
13. `RC-008｜LOCAL BLENDER EXECUTION RULE`。

### Contract precedence

- 后续 Master 生产唯一 authoritative Contract = **V002 / D-036**。
- `P3_1_MASTER_ASSET_CONTRACT_V001` 已被 V002 supersede，不得用于本任务生产参数。
- 如果真实实现与 V002 Contract 冲突，必须 HOLD 并提交 Project Control Review，不得自行修改 Contract。

---

## 3. Authorized Scope

### 3.1 CMP-LUDOU-COLUMN-001｜柱头栌斗

Geometry mode：

`MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

Canonical observed inputs（V002 corrected mapping）：

- `top_width_mm = 475.1`
- `bottom_width_mm = 327.1`
- `top_depth_mm = 446.3`
- `bottom_depth_mm = 305.5`
- `total_height_mm = 293.8`
- `flat_height_mm = 58.75`
- `sloped_height_mm = 116.2`

必须明确：

- `327.1 mm` = 面阔下宽 / bottom width；
- `446.3 mm` = 进深总深 / top depth；
- 不得再次采用 V001 中的错误字段映射。

### 3.2 CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗

Geometry mode：

`MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

Canonical observed inputs：

- `top_width_mm = 236.2`
- `bottom_width_mm = 162.7`
- `top_depth_mm = 256.2`
- `bottom_depth_mm = 177.2`
- `total_height_mm = 158.6`

### 3.3 CMP-DOU-INTERACTIVE-001｜交互斗

Geometry mode：

`MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

Canonical observed inputs：

- `top_width_mm = 255.2`
- `bottom_width_mm = 176.2`
- `top_depth_mm = 240.0`
- `bottom_depth_mm = 165.1`
- `total_height_mm = 148.5`

### 3.4 Evidence state common to all three

以上尺寸均来自当前实测 / report current-state measurement evidence，用于 evidence-bounded Master reference realization。

必须继续保留：

- current measured ≠ proven 963 original design；
- `HIS-002 = component originality unknown`；
- 构件替换、受压、磨损或形变可能影响现状尺寸；
- DG-114 继续 UNKNOWN，不得生成统一“小斗规格”。

---

## 4. Canonical Geometry Rule

三类 Master 的正式 V001 canonical body 统一采用：

> **centered rectangular bottom footprint at Z=0 → centered rectangular top footprint at Z=total_height → replaceable linear outer-envelope loft**

该 loft 是：

`PROJECT_RULE / REPLACEABLE_ENGINEERING_INTERPOLATION`

不是额外历史事实。

### 4.1 Coordinate / origin

每个 Master：

- unit = mm；
- right-handed local coordinates；
- `+X = canonical width`；
- `+Y = depth`；
- `+Z = gravity up / height`；
- origin = bottom footprint center；
- Location = `(0,0,0)`；
- Rotation = `(0,0,0)`；
- Scale = `(1,1,1)`。

正式尺寸只能由参数生成，不得通过 Object Scale 实现。

### 4.2 Required cross-section constraints

机器验证必须确认：

- `Z=0` 截面 = bottom width × bottom depth；
- `Z=total_height` 截面 = top width × top depth；
- `Z=total_height/2` 截面符合线性 interpolation；
- bounding box X/Y 最大值与 top footprint 一致；
- bounding box Z = total height。

### 4.3 柱头栌斗 flat/sloped heights 的使用边界

`flat_height_mm = 58.75` 与 `sloped_height_mm = 116.2` 必须进入 parameter/evidence metadata。

但在当前 V002 Contract 未提供足够完整纵向分段拓扑/顺序/剩余区段关系的情况下：

- 不得仅凭这两个数值自行发明台阶、耳瓣、斜面起止位置或中间分层；
- 本 T-012 canonical outer-envelope geometry 中，将两者标记为 `EVIDENCE_METADATA_ONLY_FOR_CURRENT_ENVELOPE`；
- 若后续直接证据明确纵向 profile，可通过新 Contract / Variant / Master revision 升级，不得在本任务静默补全。

---

## 5. Explicit Prohibited Geometry

三类 Master 全部禁止：

- 未量化耳瓣；
- 槽口 / 内切槽；
- 内部空腔；
- 榫卯；
- 隐蔽连接；
- 无证据曲面或雕削；
- 通过一般古建知识补造“标准斗”细部；
- 把现状变形直接重构为原始设计。

额外禁止：

- `单向长开斗`：不得因为名称“长开”而自动建出长槽；
- `交互斗`：不得因为名称“交互”而自动建十字槽、交叉内切或双向槽；
- `柱头栌斗`：不得根据 flat/sloped heights 自行创造未被 Contract 约束的多段 profile。

---

## 6. Independent Master Identity / Shared Code Boundary

允许建立共享 dou generator utility / renderer / validator，以减少重复代码。

但必须满足：

- 三个独立 `component_id`；
- 三套独立 parameter JSON；
- 三个独立 canonical `.blend`；
- 三套独立 semantic snapshot；
- 三套独立 review package；
- 三条独立 Registry Master record；
- 三个独立 canonical asset SHA256；
- mutation / reopen / deterministic validation 分别可追溯到每个 Master。

不得：

- 建一个 generic `DOU_MASTER` 后仅用名称标签区分三者；
- 用 Object Scale 从一个 Master 复制出另两个；
- 把 placement rotation 当作 Variant；
- 让三个 component_id 指向同一个 `.blend` binary。

---

## 7. Required Production Assets

每个 Component 至少生成：

### A. Parameter file

路径：

`production/zhenguo_wanfo/component_library/masters/<COMPONENT_ID>/<COMPONENT_ID>_MASTER_PARAMS_V001.json`

必须包含 Asset Contract common fields，并记录：

- component / master identity；
- V002 Contract source；
- geometry dimensions；
- evidence classification / source IDs；
- interpolation = replaceable project rule；
- known_unknowns；
- originality_status；
- reuse_scope；
- variant_axes；
- placement_only_attributes；
- prohibited geometry；
- generator / binary / semantic / review paths。

### B. Deterministic Blender generator

每个 Master 必须可被独立生成。

可以：

- 每个 Component 一个 wrapper generator；
- 调用共享 `dou_master_common` utility。

要求：

- Blender 3.6.23 CLI/background 可执行；
- 参数来自 JSON；
- 禁止裸写历史尺寸常量驱动正式 geometry；
- semantic result deterministic。

### C. Local-only canonical Blender asset

每个 Master：

`production/zhenguo_wanfo/component_library/masters/<COMPONENT_ID>/asset/<COMPONENT_ID>_MASTER_V001.blend`

要求：

- `.blend / .blend1` local-only；
- 不进入普通 Git；
- 独立 SHA256；
- independent reopen PASS。

### D. Semantic snapshot

每个 Master：

`<COMPONENT_ID>_MASTER_SEMANTIC_V001.json`

至少包括：

- object / collection names；
- object count / mesh count；
- local transforms；
- bounding box；
- bottom/top/mid cross-section dimensions；
- resolved parameters；
- evidence classes；
- geometry mode；
- interpolation status；
- known unknowns；
- prohibited details absent；
- generator version；
- input hashes；
- Contract V002 hash；
- Blender version；
- canonical `.blend` SHA256；
- semantic geometry signature。

---

## 8. Registry Registration

更新现有：

`production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`

要求：

1. 已批准 `CMP-COLUMN-001` record 必须 byte/semantic 保持不变，除非仅有不改变含义的 registry schema extension 且得到验证；
2. 新增 3 条 Master record：
   - `CMP-LUDOU-COLUMN-001`
   - `CMP-DOU-SINGLE-LONGKAI-001`
   - `CMP-DOU-INTERACTIVE-001`
3. 三条新记录在 T-012 工程完成时只能标记：
   - engineering complete / validation pass；
   - `approval_status = PENDING_CHATGPT_PRODUCT_OWNER_REVIEW` 或等价 pending 状态；
4. 不得提前标记 Product Owner Approved；
5. 不得登记上下六椽栿为已生产；
6. orphan Master / duplicate component_id = 0。

---

## 9. Standard Review Package

每个 Master 必须生成 6 项正式审核图：

目录：

`production/zhenguo_wanfo/review/P3_1/masters/<COMPONENT_ID>/`

每个 Master：

1. `FRONT.png`
2. `SIDE.png`
3. `TOP.png`
4. `AXON.png`
5. `DIMENSION_PARAMETER_SUMMARY.png`
6. `EVIDENCE_UNCERTAINTY_SUMMARY.png`

总计：**18 张单体审核图**。

统一要求：

- neutral grey；
- FRONT / SIDE / TOP = orthographic；
- AXON 显示上下 footprint 差异；
- 统一视图方向、构图语言与命名；
- 不使用影视材质、纹理、风化或戏剧灯光；
- 尺寸摘要明确 top/bottom width/depth 与 total height；
- 柱头栌斗额外显示 flat/sloped heights = evidence metadata only；
- evidence 摘要必须写明 current measured ≠ proven 963 original design；
- 明确 linear loft = replaceable engineering interpolation；
- 明确 no ears / notches / cavities / joinery modeled。

### 9.1 DOU_BATCH_OVERVIEW

额外生成：

`production/zhenguo_wanfo/review/P3_1/batches/DOU_MASTER_BATCH_V001_OVERVIEW.png`

要求：

- 三个 Master 同一画面并排；
- 保持真实相对尺度，不做独立 fit-to-frame 后再拼接；
- canonical axes / orientation 一致；
- 标 component_id / 中文名；
- 只用于批次视觉 QC，不替代各自 6 张正式审核图。

正式视觉审核总输入：**19 张**。

---

## 10. Mutation / Variant Validation

每个 Master 至少执行 1 次 synthetic mutation。

可选择改变一个 top/bottom footprint dimension 或 total height，但测试值必须：

- 标记 `ENGINEERING_TEST_ONLY`；
- 不覆盖 canonical params；
- 不进入历史 Variant 清单；
- 导致预期 cross-section / bbox / semantic signature 变化；
- 未变参数保持不漂移。

完成 mutation 后必须分别恢复 3 个 canonical reference 并 rebuild PASS。

本任务只验证 Variant architecture，不要求创建正式历史 Variant records。

---

## 11. Machine Validation Requirements

至少逐 Master 验证：

1. component_id / master_id 唯一；
2. required Asset Contract fields 完整；
3. Contract source = V002 / D-036；
4. unit = mm；
5. origin / axes / transform PASS；
6. body Scale = 1；
7. no world placement leakage；
8. no naked historical constants；
9. bottom cross-section 与参数一致；
10. top cross-section 与参数一致；
11. mid-height cross-section 符合 replaceable linear interpolation；
12. bbox 与 top footprint / total height 一致；
13. current measured evidence 未升级为 proven 963 design；
14. `HIS-002 = originality unknown` 保持；
15. DG-114 未参与 geometry；
16. unsupported ears / notches / cavities / mortise-tenon count = 0；
17. component-name-driven invented geometry count = 0；
18. semantic deterministic regeneration PASS；
19. independent reopen PASS；
20. synthetic mutation PASS；
21. canonical rebuild after mutation PASS；
22. `.blend/.blend1` 未进入 Git。

批次级额外验证：

23. V002 柱头栌斗字段映射 = PASS；
24. 3/3 canonical assets / semantic snapshots / parameter files 均存在；
25. review package = 18/18 + batch overview 1/1；
26. Registry 新增 3 条 pending review Master record；
27. approved column record 保持；
28. frame Masters 未被生产或登记为 complete；
29. P2 frozen baseline hashes unchanged；
30. Contract V002 files hash unchanged；
31. T-011 approved column canonical asset / committed source evidence 未被污染。

建议形成：

- `production/zhenguo_wanfo/validation/P3_1_DOU_MASTER_BATCH_VALIDATION_V001.json`
- `docs/production/zhenguo_wanfo/P3_1_DOU_MASTER_BATCH_VALIDATION_V001.md`

若任一 Master 失败，批次不得报告 COMPLETE；必须明确是单构件问题还是共享 pipeline 问题。

---

## 12. P2 / Existing Approved Asset Protection

T-012 不得修改：

- P2 frozen canonical `.blend`；
- P2 formal parameter / override / dependency / integration baseline；
- P2 review evidence；
- T-011 approved column canonical `.blend`；
- T-011 approved column params / semantic / review assets；
- Contract V002；
- Project Control files。

执行前后必须核验 frozen / approved evidence hashes。

---

## 13. Hard Fail Conditions

出现任一项，不得报告 COMPLETE / PASS：

- 使用 Contract V001 作为生产输入；
- 柱头栌斗再次出现 `top_depth=327.1 / bottom_width=446.3` 错映射；
- 使用 DG-114 推导统一小斗规格；
- 因“长开”名称自动建槽；
- 因“交互”名称自动建十字槽/交叉内切；
- 用 flat/sloped heights 发明未被证据约束的多段栌斗 profile；
- 建造无证据耳瓣、槽口、内部空腔、榫卯、隐蔽连接；
- 把 current measured 当成 proven 963 original design；
- 通过 Object Scale 产生正式尺寸 / Variant；
- 三个 component_id 共用同一个 canonical `.blend`；
- placement rotation 被登记为 Variant；
- mutation 污染 canonical parameters / historical evidence；
- 新 Registry records 被提前标为 Product Owner Approved；
- approved column Master 被改动；
- 上下六椽栿被顺带生产；
- P2 frozen baseline 被覆盖；
- LOCKED Contract V002 被本任务自行修改；
- `.blend/.blend1` 被提交普通 Git。

---

## 14. Completion Criteria

T-012 COMPLETE 至少要求：

- authorized scope：3 / 3 Masters；
- parameter contracts：3 / 3 PASS；
- deterministic generators：3 / 3 PASS；
- local-only canonical `.blend`：3 / 3 GENERATED；
- canonical `.blend` SHA256：3 / 3 RECORDED；
- semantic snapshots：3 / 3 PASS；
- standard review package：18 / 18 GENERATED；
- DOU_BATCH_OVERVIEW：1 / 1 GENERATED；
- Contract V002 validation：PASS；
- corrected ludou field mapping：PASS；
- transform validation：3 / 3 PASS；
- evidence boundary validation：3 / 3 PASS；
- naked historical constant scan：PASS；
- deterministic regeneration：3 / 3 PASS；
- independent reopen：3 / 3 PASS；
- synthetic mutation：3 / 3 PASS；
- canonical rebuild after mutation：3 / 3 PASS；
- Registry registration：3 new pending-review records / PASS；
- approved column Registry/asset preservation：PASS；
- P2 frozen baseline：UNCHANGED；
- Contract V002：UNCHANGED；
- unexplained validation errors：0。

T-012 COMPLETE 不等于：

- 三类斗 Product Owner 最终视觉批准；
- 上下六椽栿生产授权；
- P3.1 PASS。

完成后必须由 ChatGPT 审核工程结果与 19 张视觉资产，再由 Product Owner 决定三类斗是否 APPROVED。

---

## 15. Local Execution / Git Rules

执行前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git status
git pull --ff-only origin main
```

repository-local Git proxy 已配置；正常 `git pull / push` 即可。GitHub 443 网络失败先按网络/代理问题处理，不得误判为分支冲突，不得 force/reset/overwrite。

### 15.1 Local Blender Execution｜RC-008

固定 executable：

```bash
/Applications/Blender.app/Contents/MacOS/Blender
```

正式自动执行必须采用 CLI/background：

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --python <script.py>
```

强制：

- 禁止 `open -a Blender` 作为自动执行链；
- 禁止 Finder / AppleScript / 人工 GUI 点击作为自动工程前置；
- 不自行下载安装或切换其他 Blender 版本；
- 预期 Blender 3.6.23 / Intel x64；
- executable / version / CLI 失败则 STOP；
- review PNG、保存 `.blend`、reopen、mutation 与 QC 均应通过 background/CLI 完成。

### 15.2 Project Control / Git write boundary

T-012 执行期间不得修改：

`docs/project_control/`

Project Control 继续由 ChatGPT 维护。

若出现 unknown tracked changes、non-fast-forward 或同文件冲突，立即停止并报告。

完成后：

- 跑完所有 validation；
- `git status` 确认只包含 T-012 授权 text/script/JSON/review PNG；
- 确认 `.blend/.blend1` 未进入 Git；
- commit message 建议：`p3.1: implement dou master batch v001`；
- push `main`；
- 回传严格 Completion Report。

---

## 16. Completion Report Format

必须严格回报：

- STATUS: COMPLETE / BLOCKED / FAILED
- TASK: `T-012｜P3_1_DOU_MASTER_BATCH_V001`
- COMPONENTS: 3/3 + IDs
- MASTER_VERSION: `V001` each
- CONTRACT_VERSION: `P3_1_MASTER_ASSET_CONTRACT_V002 / D-036`
- BLENDER_VERSION:
- BLENDER_EXECUTION_MODE: CLI_BACKGROUND / OTHER
- BLENDER_EXECUTABLE_PATH:
- CANONICAL_PARAMS:
  - CMP-LUDOU-COLUMN-001: top/bottom width/depth + total/flat/sloped heights
  - CMP-DOU-SINGLE-LONGKAI-001: top/bottom width/depth + total height
  - CMP-DOU-INTERACTIVE-001: top/bottom width/depth + total height
- CANONICAL_BLEND_PATHS: 3/3
- CANONICAL_BLEND_SHA256: 3/3
- SEMANTIC_SNAPSHOT: 3/3 PASS / FAIL
- REVIEW_PACKAGE: x/18
- DOU_BATCH_OVERVIEW: PASS / FAIL
- CONTRACT_VALIDATION: PASS / FAIL
- LUDOU_V002_FIELD_MAPPING_VALIDATION: PASS / FAIL
- TRANSFORM_VALIDATION: 3/3 PASS / FAIL
- EVIDENCE_BOUNDARY_VALIDATION: 3/3 PASS / FAIL
- DG114_NON_USE_VALIDATION: PASS / FAIL
- UNSUPPORTED_DETAIL_VALIDATION: PASS / FAIL
- NAKED_HISTORICAL_CONSTANT_SCAN: PASS / FAIL
- DETERMINISTIC_REGENERATION: 3/3 PASS / FAIL
- INDEPENDENT_REOPEN: 3/3 PASS / FAIL
- SYNTHETIC_MUTATION: 3/3 PASS / FAIL
- CANONICAL_REBUILD_AFTER_MUTATION: 3/3 PASS / FAIL
- REGISTRY_REGISTRATION: PASS / FAIL
- APPROVED_COLUMN_PRESERVATION: PASS / FAIL
- P2_FROZEN_BASELINE: UNCHANGED / CHANGED
- CONTRACT_V002: UNCHANGED / CHANGED
- REQUIRES_PROJECT_CONTROL_REVIEW: NONE / [items]
- FILES_CREATED / UPDATED:
- COMMIT_SHA:
- UNRESOLVED / BLOCKERS:

---

## 17. Authorization Boundary

当前文件仅为 **Task Contract Draft**。

在 Product Owner 明确批准 T-012 前：

- Codex 不得执行；
- 不得生成三类斗正式 `.blend`；
- 不得修改 Registry；
- 不得创建上下六椽栿资产。

若 T-012 后续获批准，授权范围仅限本文件定义的三类斗 Master；任何 scope expansion 必须另行批准。