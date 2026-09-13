# 【中国古建筑3D复原｜T-012｜P3_1_DOU_MASTER_BATCH_V001｜斗类三构件Master批次生产】

Status: **AUTHORIZED / READY_FOR_LOCAL_EXECUTION**  
Think Level: **HIGH**  
Phase/Gate: P3 / P3.1  
Date: 2026-09-13  
Authorization: **PRODUCT OWNER APPROVED**

## 1. Objective

在已锁定的 `P3.1 Canonical Master Asset Contract V002`（D-036）和已批准的 T-011 柱 Master Pilot 方法基础上，仅生产以下 3 个 `MASTER_REQUIRED` 构件：

1. `CMP-LUDOU-COLUMN-001｜柱头栌斗`
2. `CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗`
3. `CMP-DOU-INTERACTIVE-001｜交互斗`

执行完整资产链：

> evidence-aware params → deterministic generator → local-only canonical `.blend` → semantic QC → standard review package → Registry registration → independent reopen / mutation validation

本任务只把当前直接证据支持的几何范围转化为 evidence-bounded digital Masters；不得为了“更像斗”而补造传统构造细节。

T-012 COMPLETE 不等于 Product Owner 最终批准，也不等于 P3.1 PASS；上下六椽栿继续未授权。

---

## 2. Authoritative Inputs

必须完整读取并遵守：

1. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md`（LOCKED / D-036）
2. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`（LOCKED / D-036）
3. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002_CHANGE_PROPOSAL.md`
4. `docs/production/zhenguo_wanfo/P3_1_DEFINITION_OF_DONE_V001.md`（D-032）
5. `P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.md/json`
6. `P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.md/json`
7. P3.0 Ontology / Registry / Schema / Migration Audit
8. P1 approved direct evidence，特别是 `P1_2_DIRECT_PAGE_REVIEW_V001.md` D-007 / D-008
9. P2 frozen baseline
10. T-011 / D-035 approved column Master，只作方法参考，不得修改
11. Project Control files
12. D-028～D-036、CG-02～CG-06
13. `RC-008｜LOCAL BLENDER EXECUTION RULE`

Contract precedence：后续 Master 生产唯一 authoritative Contract = **V002 / D-036**。V001 已 superseded，不得作为 T-012 生产输入。若真实实现与 V002 冲突，必须 HOLD 并提交 Project Control Review，不得自行改 Contract。

---

## 3. Authorized Scope / Canonical Inputs

### 3.1 CMP-LUDOU-COLUMN-001｜柱头栌斗

Geometry mode：`MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

- `top_width_mm = 475.1`
- `bottom_width_mm = 327.1`
- `top_depth_mm = 446.3`
- `bottom_depth_mm = 305.5`
- `total_height_mm = 293.8`
- `flat_height_mm = 58.75`
- `sloped_height_mm = 116.2`

必须明确：`327.1` = 面阔下宽 / bottom width；`446.3` = 进深总深 / top depth。再次使用 V001 错映射为 HARD FAIL。

### 3.2 CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗

Geometry mode：`MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

- `top_width_mm = 236.2`
- `bottom_width_mm = 162.7`
- `top_depth_mm = 256.2`
- `bottom_depth_mm = 177.2`
- `total_height_mm = 158.6`

### 3.3 CMP-DOU-INTERACTIVE-001｜交互斗

Geometry mode：`MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

- `top_width_mm = 255.2`
- `bottom_width_mm = 176.2`
- `top_depth_mm = 240.0`
- `bottom_depth_mm = 165.1`
- `total_height_mm = 148.5`

### 3.4 Evidence state

上述尺寸均为 current-state measured evidence，用于 evidence-bounded reference realization。必须保持：

- current measured ≠ proven 963 original design；
- `HIS-002 = component originality unknown`；
- 替换、受压、磨损、形变可能影响现状尺度；
- `DG-114 = UNKNOWN`，不得推导统一“小斗规格”。

---

## 4. Canonical Geometry Rule

三类 Master 的 V001 canonical body 统一采用：

> centered rectangular bottom footprint at Z=0 → centered rectangular top footprint at Z=total_height → replaceable linear outer-envelope loft

该 loft 必须标记：`PROJECT_RULE / REPLACEABLE_ENGINEERING_INTERPOLATION`，不是历史事实。

每个 Master：

- unit = mm
- right-handed local coordinates
- `+X = canonical width`
- `+Y = depth`
- `+Z = height / gravity up`
- origin = bottom footprint center
- Location = `(0,0,0)`
- Rotation = `(0,0,0)`
- Scale = `(1,1,1)`
- 正式尺寸只由参数生成，不得通过 Object Scale 实现

机器必须核对 bottom / top / mid-height cross-section 与线性 interpolation、bbox 和 total height。

### 柱头栌斗 flat/sloped heights

`58.75 / 116.2` 必须进入 parameter/evidence metadata，但在 V002 未提供完整纵向分段拓扑的情况下，仅标记为：

`EVIDENCE_METADATA_ONLY_FOR_CURRENT_ENVELOPE`

不得据此自行发明台阶、耳瓣、斜面起止或多段 profile。

---

## 5. Explicit Prohibited Geometry

三类全部禁止：

- 未量化耳瓣
- 槽口 / 内切槽
- 内部空腔
- 榫卯 / 隐蔽连接
- 无证据曲面、雕削或标准斗细节
- 把现状变形直接重构为原始设计

额外禁止：

- 单向长开斗：不得因名称“长开”自动建长槽
- 交互斗：不得因名称“交互”自动建十字槽、交叉内切或双向槽
- 柱头栌斗：不得用 flat/sloped heights 发明未被 Contract 约束的多段 profile

---

## 6. Independent Master / Shared Code Boundary

允许共享 dou generator utility / renderer / validator，但三个 Master 必须保持：

- 3 个独立 component_id
- 3 套独立 parameter JSON
- 3 个独立 canonical `.blend`
- 3 套独立 semantic snapshot
- 3 套独立 review package
- 3 条独立 Registry Master record
- 3 个独立 canonical asset SHA256
- mutation / reopen / deterministic validation 分别可追溯

不得建立 generic `DOU_MASTER` 后仅靠名称区分；不得 Object Scale 复制；不得三个 component_id 指向同一 `.blend`。

---

## 7. Required Production Assets

每个 Component 至少生成：

- `<COMPONENT_ID>_MASTER_PARAMS_V001.json`
- 独立可调用 deterministic generator（可调用共享 utility）
- local-only `asset/<COMPONENT_ID>_MASTER_V001.blend`
- `<COMPONENT_ID>_MASTER_SEMANTIC_V001.json`

Semantic snapshot 至少包括：object / collection、transform、bbox、bottom/top/mid cross-section、resolved params、evidence class、geometry mode、interpolation status、known unknowns、prohibited details absent、generator version、input hashes、Contract V002 hash、Blender version、blend SHA256、semantic signature。

`.blend / .blend1` 不进入普通 Git。

---

## 8. Registry Registration

更新：`production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`

要求：

- 已批准 `CMP-COLUMN-001` record 保持语义不变
- 新增三类斗 3 条 Master record
- 新记录只能标记 engineering complete / validation pass + `PENDING_CHATGPT_PRODUCT_OWNER_REVIEW`（或等价）
- 不得提前 Product Owner Approved
- 不得登记上下六椽栿为 complete
- orphan / duplicate component_id = 0

---

## 9. Standard Review Package

每个 Master 6 张：

1. FRONT.png
2. SIDE.png
3. TOP.png
4. AXON.png
5. DIMENSION_PARAMETER_SUMMARY.png
6. EVIDENCE_UNCERTAINTY_SUMMARY.png

总计 **18 张单体审核图**。

统一要求：neutral grey；正交视图；AXON 能看出上下 footprint 差异；统一方向/命名；尺寸摘要明确 top/bottom width/depth + height；柱头栌斗额外说明 flat/sloped heights 仅为 evidence metadata；evidence 摘要明确 current measured ≠ proven 963 design、linear loft = replaceable engineering interpolation、no ears/notches/cavities/joinery modeled。

额外生成：

`production/zhenguo_wanfo/review/P3_1/batches/DOU_MASTER_BATCH_V001_OVERVIEW.png`

三个 Master 同画面、真实相对尺度、同轴向、标 component_id / 中文名。正式视觉审核输入共 **19 张**。

---

## 10. Mutation / Variant Validation

每个 Master 至少 1 次 synthetic mutation，可改变一个 footprint dimension 或 total height；必须标记 `ENGINEERING_TEST_ONLY`，不覆盖 canonical params，不进入历史 Variant，且引起预期 cross-section / bbox / signature 变化。完成后分别恢复 3 个 canonical reference 并 rebuild PASS。

本任务只验证 Variant architecture，不创建正式历史 Variant records。

---

## 11. Machine Validation Requirements

逐 Master 至少验证：

1. component_id / master_id 唯一
2. Contract fields 完整，source = V002 / D-036
3. unit / origin / axes / transform / Scale=1
4. no world placement leakage
5. no naked historical constants
6. bottom / top / mid cross-section 与参数及线性插值一致
7. bbox / total height 正确
8. current measured 未升级为 proven 963 design
9. HIS-002 保持 unknown
10. DG-114 未参与 geometry
11. unsupported ears / notches / cavities / mortise-tenon = 0
12. component-name-driven invented geometry = 0
13. deterministic regeneration PASS
14. independent reopen PASS
15. synthetic mutation PASS
16. canonical rebuild PASS
17. `.blend/.blend1` 未进入 Git

批次级还必须验证：

- V002 栌斗字段映射 PASS
- 3/3 canonical assets / params / semantic 存在
- review = 18/18 + overview 1/1
- Registry 新增 3 条 pending-review records
- approved column record / asset / committed evidence 未被污染
- frame Masters 未生产或登记 complete
- P2 frozen baseline hashes unchanged
- Contract V002 files hash unchanged

建议输出：

- `production/zhenguo_wanfo/validation/P3_1_DOU_MASTER_BATCH_VALIDATION_V001.json`
- `docs/production/zhenguo_wanfo/P3_1_DOU_MASTER_BATCH_VALIDATION_V001.md`

任一 Master 失败则批次不得 COMPLETE；必须说明是单构件还是共享 pipeline 问题。

---

## 12. Protected Assets

T-012 不得修改：

- P2 frozen baseline
- T-011 approved column `.blend` / params / semantic / review assets
- Contract V002
- `docs/project_control/`

执行前后核验 frozen / approved hashes。

---

## 13. Hard Fail Conditions

出现任一项不得 COMPLETE / PASS：

- 使用 Contract V001
- 栌斗字段再次错映射
- DG-114 推导统一小斗规格
- 因“长开/交互”名称自动建槽
- 用 flat/sloped heights 发明多段栌斗 profile
- 建无证据耳瓣、槽、空腔、榫卯、隐蔽连接
- current measured 冒充 proven 963 design
- Object Scale 产生正式尺寸 / Variant
- 三 component 共用同一 canonical `.blend`
- placement rotation 登记为 Variant
- mutation 污染 canonical / historical evidence
- Registry 提前 Product Owner Approved
- approved column Master 被改动
- 上下六椽栿被顺带生产
- P2 frozen baseline 被覆盖
- Contract V002 被修改
- `.blend/.blend1` 被提交 Git

---

## 14. Completion Criteria

T-012 COMPLETE 至少要求：

- authorized scope 3/3
- parameter contract / generator / semantic snapshot 3/3 PASS
- local-only `.blend` 3/3 GENERATED，SHA256 3/3 RECORDED
- review 18/18 + overview 1/1
- Contract V002 / corrected ludou mapping PASS
- transform / evidence boundary 3/3 PASS
- naked historical constant scan PASS
- deterministic regeneration / reopen / mutation / canonical rebuild 3/3 PASS
- Registry 3 new pending-review records PASS
- approved column preservation PASS
- P2 frozen baseline UNCHANGED
- Contract V002 UNCHANGED
- unexplained validation errors = 0

T-012 COMPLETE 不等于：三类斗最终视觉批准、六椽栿授权或 P3.1 PASS。完成后必须由 ChatGPT 审核工程结果与 19 张视觉资产，再由 Product Owner 决定三类斗是否 APPROVED。

---

## 15. Local Execution / Git / Blender Rules

执行前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git status
git pull --ff-only origin main
```

repository-local Git proxy 已配置。443 网络失败先按网络/代理问题处理，不得误判分支冲突，不得 force/reset/overwrite。

RC-008 固定 Blender executable：

```bash
/Applications/Blender.app/Contents/MacOS/Blender
```

自动执行必须：

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --python <script.py>
```

禁止 `open -a Blender`、Finder / AppleScript / GUI 自动链；不自行下载安装/切换 Blender。预期 Blender 3.6.23 / Intel x64。CLI/background 失败才算 runtime blocker。

T-012 执行期间不得修改 `docs/project_control/`。若出现 unknown tracked changes、non-fast-forward 或同文件冲突，立即停止并报告。

完成后运行全部 validation，确认 `.blend/.blend1` 未进入 Git，commit 建议：

`p3.1: implement dou master batch v001`

push `main` 后回传 Completion Report。

---

## 16. Completion Report Format

- STATUS: COMPLETE / BLOCKED / FAILED
- TASK: `T-012｜P3_1_DOU_MASTER_BATCH_V001`
- COMPONENTS: 3/3 + IDs
- MASTER_VERSION: `V001` each
- CONTRACT_VERSION: `P3_1_MASTER_ASSET_CONTRACT_V002 / D-036`
- BLENDER_VERSION:
- BLENDER_EXECUTION_MODE: CLI_BACKGROUND / OTHER
- BLENDER_EXECUTABLE_PATH:
- CANONICAL_PARAMS: 三构件全部尺寸与 evidence metadata
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

**T-012 已由 Product Owner 明确批准并正式授权。**

授权范围仅限：

- `CMP-LUDOU-COLUMN-001`
- `CMP-DOU-SINGLE-LONGKAI-001`
- `CMP-DOU-INTERACTIVE-001`

不得顺带生产上下六椽栿或任何 Deferred / Proxy / Control / Envelope 对象。任何 scope expansion 必须另行批准。
