# 【中国古建筑3D复原｜T-012｜P3_1_DOU_MASTER_BATCH_V002｜斗类三构件Master精益批次生产】

Status: **AUTHORIZED / READY_FOR_LOCAL_EXECUTION**  
Execution Mode: **LEAN_PRODUCTION_MODE_V001**  
Think Level: **HIGH for first-article / MEDIUM for proven batch repetition**  
Phase/Gate: P3 / P3.1  
Date: 2026-09-13  
Authorization: **PRODUCT OWNER APPROVED**  
Supersedes for execution: `T-012_P3_1_DOU_MASTER_BATCH_V001.md`

## 1. Objective

在不降低任何 P3.1 Master 验收标准的前提下，将 T-011 已验证的完整 Master 资产链转入精益生产模式：

> **共享生产工具链 + 首件验证 + 批量参数驱动 + 逐资产独立验收**

只生产：

1. `CMP-LUDOU-COLUMN-001｜柱头栌斗`
2. `CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗`
3. `CMP-DOU-INTERACTIVE-001｜交互斗`

上下六椽栿不在本任务授权范围。

本 V002 改变的是**执行方式与 Codex 资源使用策略**，不降低 V001 的资产、证据、验证、审核或审批标准。

---

## 2. Lean Production Principle

允许节省：

- 重复读取已锁定且与本批次无直接变化的大量历史文件；
- 三套重复 generator 主逻辑；
- 三套重复 validator；
- 三套重复 renderer；
- 重复的 Blender 启动与人工解释；
- 成功过程中的长篇推理/过程报告。

不得节省：

- 3 套独立 parameter JSON；
- 3 个独立 canonical `.blend`；
- 3 个独立 SHA256；
- 3 套独立 semantic snapshot；
- 每个 Master 的 deterministic regeneration；
- 每个 Master 的 independent reopen；
- 每个 Master 的 synthetic mutation；
- 每个 Master 的 canonical rebuild after mutation；
- 每个 Master 的 evidence / transform / unsupported-detail validation；
- 18 张单体审核图 + 1 张 batch overview；
- Registry 中 3 条独立 pending-review Master record；
- P2 / approved column / Contract V002 的保护性 hash check。

原则：**reduce duplicated reasoning/code, not acceptance evidence.**

---

## 3. Minimal Authoritative Read Set

执行前只要求优先读取以下直接相关输入；不要无目的重新通读全部 P1/P2/P3 文档：

1. 本文件：`docs/tasks/T-012_P3_1_DOU_MASTER_BATCH_V002.md`
2. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`
3. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md` 中 7.2–7.4、8–13 节
4. `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md` 中 D-007 / D-008
5. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`
6. T-011 已批准的 generator/review/validation 代码，仅用于复用通用资产链方法；不得继承柱几何逻辑
7. `docs/project_control/project_state.json` 仅核对当前授权状态
8. `RC-008` 本地 Blender CLI/background 规则

P2 frozen baseline、Contract V002、T-011 approved column 的完整内容不要求重复分析；通过既有 hash manifest / 当前文件 SHA 做执行前后保护性比较。只有 hash mismatch 才展开调查并 STOP。

若上述直接输入之间出现矛盾，以 `P3_1_MASTER_ASSET_CONTRACT_V002 / D-036` 为最高生产合同，不得自行改 Contract。

---

## 4. Canonical Inputs / Evidence Boundary

### 4.1 CMP-LUDOU-COLUMN-001｜柱头栌斗

- `top_width_mm = 475.1`
- `bottom_width_mm = 327.1`
- `top_depth_mm = 446.3`
- `bottom_depth_mm = 305.5`
- `total_height_mm = 293.8`
- `flat_height_mm = 58.75`
- `sloped_height_mm = 116.2`

V002 corrected mapping 是硬约束：

- `327.1` = 面阔下宽 / bottom width
- `446.3` = 进深总深 / top depth

`flat_height / sloped_height` 当前仅为 `EVIDENCE_METADATA_ONLY_FOR_CURRENT_ENVELOPE`，不得自行生成多段 profile。

### 4.2 CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗

- `top_width_mm = 236.2`
- `bottom_width_mm = 162.7`
- `top_depth_mm = 256.2`
- `bottom_depth_mm = 177.2`
- `total_height_mm = 158.6`

不得因为“长开”名称自动建槽。

### 4.3 CMP-DOU-INTERACTIVE-001｜交互斗

- `top_width_mm = 255.2`
- `bottom_width_mm = 176.2`
- `top_depth_mm = 240.0`
- `bottom_depth_mm = 165.1`
- `total_height_mm = 148.5`

不得因为“交互”名称自动建十字槽、交叉内切或双向槽。

### 4.4 Common evidence boundary

三者均为 current measured evidence 的 evidence-bounded reference realization：

- current measured ≠ proven 963 original design
- `HIS-002 = originality unknown`
- `DG-114 = UNKNOWN`，不得参与统一小斗规格推导
- 替换、受压、磨损、形变可能影响现状尺寸

---

## 5. Shared Geometry / Toolchain Rule

三类 Master 共用一种正式 canonical geometry rule：

> centered rectangular bottom footprint at Z=0 → centered rectangular top footprint at Z=total_height → replaceable linear outer-envelope loft

标记：`PROJECT_RULE / REPLACEABLE_ENGINEERING_INTERPOLATION`

允许建立一套共享：

- `dou_master_common` geometry utility
- batch runner
- validator
- review renderer
- semantic snapshot helper

建议结构：

```text
shared dou utility
  ├── params: CMP-LUDOU-COLUMN-001
  ├── params: CMP-DOU-SINGLE-LONGKAI-001
  └── params: CMP-DOU-INTERACTIVE-001
```

但最终资产必须独立：3 component IDs / 3 params / 3 blends / 3 semantic snapshots / 3 hashes / 3 review packages / 3 Registry records。

禁止：

- generic `DOU_MASTER` 作为三个正式 Master 的共同 binary
- Object Scale 复制另外两个 Master
- placement rotation 形成 Variant

---

## 6. First-Article Gate｜先柱头栌斗，后批量

为了控制共享代码的 common-mode error，执行顺序固定：

### Stage A｜Shared pipeline setup

只建立一次共享 generator utility、validator、renderer 和 batch orchestration。

### Stage B｜First Article = CMP-LUDOU-COLUMN-001

只生成柱头栌斗 canonical asset，并完成以下首件验证：

- V002 field mapping
- bottom/top/mid cross-section
- bbox / total height
- transform / Scale=1 / no world placement
- evidence semantics
- unsupported detail = 0
- DG-114 non-use
- deterministic regeneration
- independent reopen
- one synthetic mutation
- canonical rebuild after mutation
- 6/6 review assets
- `.blend` local-only

**任何一项失败：立即 STOP。不得继续另外两类斗。**

失败时只报告：失败项、最小复现、相关日志、是否共享 pipeline 问题；不得自动进行无上限反复尝试。

### Stage C｜Batch expansion

Stage B 全部 PASS 后，同一共享 pipeline 一次性参数驱动生成：

- `CMP-DOU-SINGLE-LONGKAI-001`
- `CMP-DOU-INTERACTIVE-001`

不要重新设计第二、第三套 generator/validator/renderer。

### Stage D｜Final batch validation

对 3 个独立资产执行完整逐资产验收 + 批次级保护检查。

---

## 7. Retry / Token Budget Discipline

为避免 Codex 额度被无效调试消耗：

- 同一根因最多允许 **2 次有证据的修正重试**；
- 第 2 次后仍失败，STOP 并回报，不继续猜测式修改；
- Blender 成功命令不重复解释；
- 正常 PASS 日志保持简短，只保存机器结果；
- 不为每个 Master 重写相同代码；
- 不重复全文总结已锁定 P1/P2/Contract 内容；
- 不生成额外非验收所需图、报告或临时资产；
- 不使用 Codex 视觉分析 19 张 review PNG；Codex 只负责生成与机器检查，视觉判断由 ChatGPT / Product Owner 完成。

该规则只减少工程执行冗余，不允许跳过 Hard Fail / Completion Criteria。

---

## 8. Independent Asset Requirements

每个 Component 必须生成：

- `<COMPONENT_ID>_MASTER_PARAMS_V001.json`
- 独立 wrapper / entrypoint（可调用共享 utility）
- local-only `asset/<COMPONENT_ID>_MASTER_V001.blend`
- `<COMPONENT_ID>_MASTER_SEMANTIC_V001.json`
- 6 张正式 review PNG
- 独立 canonical SHA256
- Registry 独立 record

Canonical transform：Location `(0,0,0)` / Rotation `(0,0,0)` / Scale `(1,1,1)`；unit = mm；+X width / +Y depth / +Z height；origin = bottom footprint center。

`.blend/.blend1` 不进入普通 Git。

---

## 9. Validation Matrix｜质量标准不降

每个 Master 必须逐项 PASS：

1. component_id / master_id unique
2. Contract source = V002 / D-036
3. required fields complete
4. unit / axes / origin / transform correct
5. body Scale = 1
6. no world placement leakage
7. no naked historical constants
8. bottom section = params
9. top section = params
10. mid section = linear interpolation
11. bbox / height correct
12. current measured not promoted to proven 963 design
13. `HIS-002` originality unknown
14. DG-114 geometry use = 0
15. unsupported ears/notches/cavities/mortise-tenon = 0
16. component-name-driven invented geometry = 0
17. deterministic regeneration PASS
18. independent reopen PASS
19. synthetic mutation PASS
20. canonical rebuild after mutation PASS
21. `.blend/.blend1` absent from Git

批次级必须 PASS：

22. ludou V002 field mapping
23. 3/3 params / blends / semantic snapshots / hashes
24. review = 18/18 + overview 1/1
25. Registry = 3 new independent pending-review records
26. approved column record/assets unchanged
27. frame Masters not produced
28. P2 frozen baseline hashes unchanged
29. Contract V002 hashes unchanged
30. T-011 approved column committed source/review evidence unchanged

---

## 10. Review Package｜保持 19 张

每个 Master：

1. FRONT
2. SIDE
3. TOP
4. AXON
5. DIMENSION_PARAMETER_SUMMARY
6. EVIDENCE_UNCERTAINTY_SUMMARY

总计 18 张。

另生成：

`production/zhenguo_wanfo/review/P3_1/batches/DOU_MASTER_BATCH_V001_OVERVIEW.png`

要求三个 Master 同画面、真实相对尺度、同轴向、清楚标识。

Codex 不进行逐图美学/历史视觉判断；只确认文件存在、尺寸可打开、对应 component_id 正确。最终 19 张由 ChatGPT / Product Owner 视觉审核。

---

## 11. Registry Rule

更新：`production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`

- approved `CMP-COLUMN-001` 保持语义不变
- 新增 3 条独立 Master record
- 新记录只能为 engineering/validation complete + `PENDING_CHATGPT_PRODUCT_OWNER_REVIEW`
- 不得提前 Product Owner Approved
- 不得登记上下六椽栿 complete
- orphan / duplicate = 0

---

## 12. Protected Assets / Hash-only Recheck

执行前后只做 hash / manifest 比较，不重新分析其全文：

- P2 frozen baseline
- T-011 approved column params / semantic / review / committed source
- Contract V002 md/json

若 hash 完全一致：记录 PASS 后继续。

若任一 hash mismatch：STOP，列出变化文件，不自动修复或重写。

`docs/project_control/` 仍不得由 Codex 修改。

---

## 13. Hard Fail Conditions

任一发生不得 COMPLETE：

- 使用 Contract V001
- 栌斗字段再次错映射
- DG-114 参与 geometry
- “长开/交互”名称驱动无证据槽
- flat/sloped heights 被用于发明多段 profile
- 无证据耳瓣、槽、空腔、榫卯、隐蔽连接
- current measured 被写成 proven 963 design
- Object Scale 形成正式尺寸 / Variant
- 三 component 共用一个 canonical binary
- mutation 污染 canonical/evidence
- Registry 提前标为 Product Owner Approved
- approved column / P2 / Contract V002 被修改
- 上下六椽栿被顺带生产
- `.blend/.blend1` 进入 Git
- First Article 未 PASS 就继续 Stage C

---

## 14. Completion Criteria

T-012 COMPLETE 必须保持与 V001 同等质量门槛：

- 3/3 params / independent Masters / semantic snapshots
- 3/3 canonical `.blend` + SHA256
- 3/3 deterministic regeneration / reopen / mutation / rebuild
- 3/3 transform / evidence / unsupported-detail validation
- 18/18 review + 1/1 batch overview
- Registry 3 new pending-review records
- approved column preserved
- P2 frozen baseline unchanged
- Contract V002 unchanged
- unexplained validation errors = 0

COMPLETE 不等于 Product Owner APPROVED，不授权六椽栿，也不等于 P3.1 PASS。

---

## 15. Local Blender / Git

执行前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git status
git pull --ff-only origin main
```

固定 Blender：

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --python <script.py>
```

遵守 RC-007 / RC-008；禁止 `open -a Blender` 自动链；禁止 force/reset/overwrite。

完成后：

- 全部 validation PASS
- `.blend/.blend1` 未进 Git
- commit 建议：`p3.1: implement dou master lean batch v001`
- push main
- 只回传 Completion Report，不写冗长过程复盘，除非存在失败/异常

---

## 16. Completion Report Format

- STATUS: COMPLETE / BLOCKED / FAILED
- TASK: `T-012｜P3_1_DOU_MASTER_BATCH_V002`
- EXECUTION_MODE: `LEAN_PRODUCTION_MODE_V001`
- FIRST_ARTICLE: `CMP-LUDOU-COLUMN-001` PASS / FAIL
- SHARED_PIPELINE: PASS / FAIL
- COMPONENTS: 3/3 + IDs
- CONTRACT_VERSION: `P3_1_MASTER_ASSET_CONTRACT_V002 / D-036`
- BLENDER_VERSION:
- BLENDER_EXECUTION_MODE: CLI_BACKGROUND / OTHER
- CANONICAL_PARAMS: 3 components
- CANONICAL_BLEND_PATHS: 3/3
- CANONICAL_BLEND_SHA256: 3/3
- SEMANTIC_SNAPSHOT: 3/3 PASS / FAIL
- REVIEW_PACKAGE: x/18
- DOU_BATCH_OVERVIEW: PASS / FAIL
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
- RETRY_COUNTS: first-article / batch
- REQUIRES_PROJECT_CONTROL_REVIEW: NONE / [items]
- FILES_CREATED / UPDATED:
- COMMIT_SHA:
- UNRESOLVED / BLOCKERS:

---

## 17. Future Reuse Boundary

本任务同时作为 Lean Production Mode 的首次正式生产验证。

若 T-012 最终工程 + 视觉审核均 PASS，则后续同类生产默认可采用 Lean Production Mode，条件是：

- 已有代表性 Pilot 或 First Article 验证了共享 pipeline；
- 批次构件共享明确的生成方法/Contract；
- 每个正式资产仍独立生成和逐资产验收；
- 首件失败即停止批量扩展；
- 不因省 token/额度降低 DoD、Hard Fail、Evidence Boundary 或 Visual Review。

若构件几何方法、证据语义或执行环境发生实质变化，则必须回到 standalone / pilot mode，不得机械套用 Lean。
