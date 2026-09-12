# Execution Log｜ARCH3D-001

本文件记录实际工程执行结果，只保留足以追溯结论的关键事实、证据、失败原因和最终结果；完整脚本、Workflow、Commit 与历史版本由 GitHub 保存。

## T-001｜PROJECT_WORKSPACE_INIT_V001｜PASS

- Think Level: LOW
- 目标：建立本地项目工作区。
- 根目录：`/Users/caroline/中国古建筑3D复原`
- 结果：项目目录结构建立完成，无 blocker。

## T-002｜LOCAL_BLENDER_POC_V002｜PASS

- Think Level: MEDIUM
- Local Blender：3.6.23 macOS x64。
- Blender 4.2.23 macOS x64：Platform Unsupported，不作为本机基线。
- `P0_1_MINIMAL_GREYBOX_V001.blend` 与 PNG 生成、保存、独立重开、Geometry Integrity、人工审核：PASS。

## T-003｜LOCAL_CLOUD_ROUNDTRIP_POC｜PASS / CLASS B

- Codex Cloud 因网络代理无法取得 Blender，停止作为 Blender Executor。
- GitHub Actions `ubuntu-latest` + Blender 4.5.13 LTS 成功成为 Cloud Executor。
- Local 3.6 → GitHub → Blender 4.5.13 → Artifact → Local 3.6 完整往返：PASS。
- Cloud Marker、Local Marker、Metadata、Geometry Integrity：PASS。
- Blender 3.6 会移除部分不支持的 4.5 UI region 数据；未发现核心几何或所需 Metadata 损失。
- 最终分类：**Class B｜ROUNDTRIP_WITH_LIMITATIONS**。
- 关键证据：GitHub Actions full roundtrip commit `e26d5d600ed693a8e86a914e24dfbe652d718ed3`。

## T-004｜PARAMETRIC_ARCHITECTURE_POC_V001｜PASS

- Think Level: MEDIUM
- Local Blender：3.6.23 macOS x64。
- 独立 JSON 参数驱动同一 Blender Python 脚本稳定生成最小结构灰模。
- Baseline 3×2 → 12柱 / 21主要对象；Variant 4×3 → 20柱 / 31主要对象。
- 只修改 JSON 即驱动柱位、梁、台基、屋顶尺寸变化；无逐柱硬编码。
- 独立重开与 Determinism：PASS。
- Lightweight Evidence Archive commit：`63a0c506f98d843376361421cf88e1e74c807dc7`。
- `.blend / .blend1` 保持 Local-only。

## P0 Gate Review｜APPROVED / CLOSED｜2026-09-11

- P0.0–P0.3：4/4 PASS。
- Product Owner 批准 P0 关闭；进入 P1。
- P0.2 Class B 兼容性限制继续生效。
- P0.3 只证明参数驱动技术链路，不代表历史正确性或正式古建构造精度。

## P1 Research / Gate Execution Summary｜CLOSED｜2026-09-12

- 正式案例：山西平遥镇国寺万佛殿。
- `SRC-ZG-WF-001` 完整精细测绘报告直接核读完成。
- P1.2：10/10 PASS / Product Owner APPROVED。
- P1.3：85/85关键参数完成四级分类；46 CONFIRMED / 32 HIGH_CONFIDENCE_INFERENCE / 4 REASONABLE_COMPLETION / 3 UNKNOWN。
- P1.3 Gate Review：6 PASS + 2 PASS WITH CONDITION + 0 FAIL。
- Product Owner 2026-09-12 批准 CONDITIONAL GO；P1 4/4 PASS并关闭。
- P1研究与Gate Review本身不占用T-###。

## 【中国古建筑3D复原｜T-005｜P2_0_SCHEMA_VALIDATION_V001｜证据感知参数架构验证】｜ENGINEERING PASS / GATE HOLD

- Think Level: MEDIUM
- Python：3.10.2；`jsonschema`：4.26.0 / Draft 2020-12。
- Positive four-class validation：PASS。
- `UNKNOWN + DO_NOT_LOCK` 数字硬锁负例：按预期 FAIL / test PASS。
- `REASONABLE_COMPLETION + is_replaceable=false` 负例：按预期 FAIL / test PASS。
- Reader smoke test：PASS；无 `bpy` / 无几何生成。
- V001 automated suite：4 tests PASS。
- Gate 暂 HOLD 原因：V001 未显式验证三层语义同时并存且不串层；工程证据当时尚未进入 canonical GitHub。
- 因任务目标未改变，继续同一任务 V002，不创建 T-006。

## 【中国古建筑3D复原｜T-005｜P2_0_SCHEMA_VALIDATION_V002｜证据感知参数架构验证】｜ENGINEERING PASS / COMPLETE

- Think Level: MEDIUM。
- V001 regression：**PASS 4/4**。
- V002 three-layer coexistence：**PASS**。
- V002 reader preservation：**PASS**；精确保留：
  - `PM-TL-OBS → observed_as_measured`
  - `MOD-TL-IDEAL → report_ideal_model`
  - `Z-TL-963 → reconstructed_963_candidate`
- 自动化完整 suite：6 tests PASS。
- 三层 ID / `time_layer` 映射若发生 merge、overwrite、relabel、missing 或 silent conversion，测试会失败。
- 无 `bpy` import；无 Blender 几何生成。
- P0 POC、P1 evidence/classification、`.blend`、已知本地 PDF/P0 untracked 资产均未触碰。
- 本地 Codex engineering commit：`0f3e0ef0bbadcea4c42ca912cfa219b1d596281d`；因本机无法连接 GitHub 未能 push。
- 用户已上传全部 T-005 工程证据；ChatGPT 通过 GitHub connector 将等价内容作为单一 canonical evidence commit 写入 `main`：`a938d9fe96c579c21fb3a16734f9b74efcd7d8bc`。
- canonical evidence includes validator、reader、V001/V002 automated tests、两个负例 fixture、三层并存 fixture、V001/V002 validation reports。
- T-005 V002 最终工程结论：**PASS / COMPLETE**。

## P2.0 Gate Review｜APPROVED / PASS｜2026-09-12

- P2.0 Gate Review：**7/7 PASS**。
- Product Owner 明确批准 `P2.0｜PASS`。
- CG-01｜Evidence-aware Parameter Schema 前置条件正式满足。
- T-005 V001/V002：COMPLETE。
- 正式几何不再受 P2.0 阻断，但 CG-02～CG-06 持续生效。
- 在创建下一项正式几何 T-### 前，必须先定义并锁定 P2.1–P2.3 Gate 架构。

## 【中国古建筑3D复原｜T-006｜P2_1_PRODUCTION_PARAMETER_SET_V001｜正式生产参数集建立与几何依赖预检】｜ENGINEERING HOLD

- Think Level: HIGH。
- Python：3.10.2；`jsonschema`：4.26.0。
- Formal Production Parameter Set：**85/85**；classification = 46 CONFIRMED / 32 HIGH_CONFIDENCE_INFERENCE / 4 REASONABLE_COMPLETION / 3 UNKNOWN。
- Geometry Dependency Matrix：**85/85**。
- Machine validation：**PASS**。
- Automated tests：**PASS 11/11**。
- Production preflight：**HOLD / exit 1**。
- UNKNOWN dependency：
  - `Z-006 / column_height_963_design_mm` → `BLOCKS_P2_2_GEOMETRY`；
  - `DG-114 / small_dou_unified_design_rule` → `BOUNDED_NON_BLOCKING`；
  - `HIS-002 / component_level_963_originality` → `METADATA_ONLY_BLOCK`。
- Geometry-critical unresolved blocker count：**1**。
- blocker：`Z-006`。P2.2 的柱、主要梁架与屋顶绝对 Z 定位需要柱高；P1 未锁定合法的 963 原设计柱高，现状或二手高度不得静默代填。
- 无静默补值、无 UNKNOWN 重分类、无 `bpy`、无 Blender 几何生成。
- T-006 engineering commit：`1ccf08aeed6f5bb6ae3ed0e0ccd25cd8346055f0`，已进入 GitHub `main` canonical repo。
- T-006 最终工程建议：**HOLD**。P2.1 不得 PASS；P2.2 不得启动，直到 `Z-006` blocker 通过新证据或 Product Owner 明确批准的独立、可替换、可追溯 REASONABLE_COMPLETION 得到处理。

## 【中国古建筑3D复原｜T-006｜P2_1_PRODUCTION_PARAMETER_SET_V002｜Z-006批准候选接入与阻断清零验证】｜ENGINEERING PASS / COMPLETE

- Think Level: HIGH。
- Python：3.10.2；`jsonschema`：4.26.0。
- V001 regression：**11/11 PASS**。
- Automated tests：**21/21 PASS**。
- Formal Production Parameter Set：**85/85 unchanged**；46 CONFIRMED / 32 HIGH_CONFIDENCE_INFERENCE / 4 REASONABLE_COMPLETION / 3 UNKNOWN。
- `Z-006`：继续保持 `UNKNOWN / null / DO_NOT_LOCK`；dependency 继续为 `BLOCKS_P2_2_GEOMETRY`。
- `Z-006-RC-01`：独立 approved override sidecar；`REASONABLE_COMPLETION`；`is_replaceable=true`；traceable to D-023。
- Formula resolution：`11 × MOD-006 = 11 × 321.3 = 3534.3mm`。
- Historical geometry-critical unknown count：**1**。
- Approved candidate resolution count：**1**。
- Geometry-critical unresolved blocker count：**0**。
- Production preflight：**PASS / exit 0**。
- Mutation tests 验证缺失/额外 override、Z-006 改写、dependency 改写、candidate身份/公式/审批/可替换性篡改、stale resolved value、证据边界缺失、RC-01混入历史85项等均触发 HOLD/FAIL。
- 无 Blender、无 `bpy`、无正式几何生成。
- canonical engineering commit：`fc124922d5c0c1674548f9b99968f9848ffbb332`。
- T-006 V002 最终工程结论：**PASS / COMPLETE**。

## P2.1 Gate Review｜APPROVED / PASS / CLOSED｜2026-09-12

- Gate Review：**9/9 PASS**。
- Hard PASS condition：`geometry-critical unresolved blocker = 0`，**PASS**。
- Product Owner 明确批准：`P2.1｜PASS`。
- P2.1 正式 CLOSED；P2.2 解锁。
- P2.1 PASS 不改变 Z-006 历史 UNKNOWN；Z-006-RC-01 继续作为独立、可替换 production override。
- Gate Review：`docs/production/zhenguo_wanfo/P2_1_GATE_REVIEW_2026-09-12.md`。

## 【中国古建筑3D复原｜T-007｜P2_2_STRUCTURAL_SKELETON_V001｜第一版正式主体结构候选模型】｜ENGINEERING PASS / COMPLETE

- Think Level: HIGH。
- Blender：3.6.23；Blender Python：3.10.13；host test Python：3.10.2。
- 正式输入 hash 已锁定并写入 build manifest；P2.1 production preflight 继续 PASS。
- Structural scope：**6/6**；共 **217** 个稳定命名 mesh 对象：GRID 8 / COLUMN 12 / FRAME 62 / BRACKET 88 / ROOF 43 / GABLE 4。
- `Z-006` 继续 `UNKNOWN / null / DO_NOT_LOCK`；`Z-006-RC-01 = 11 × MOD-006 = 3534.3mm` 以独立、可替换 REASONABLE_COMPLETION 进入几何。
- Machine geometry validation：**PASS / 0 errors**；声明 tolerance = 0.01mm。
- Naked historical constant scan：**PASS**。
- Deterministic rebuild：**PASS**；两次 clean build 的对象集合、数量、family counts、关键尺寸、topology、geometry-input snapshot 与 validation summary 一致；`.blend` 二进制序列化不要求 byte-identical。
- Independent reopen：**PASS / PASS**。
- Replaceability：synthetic test-only MOD-006 change 使实际柱高由 3534.3mm 重建为 3702.6mm，reopen PASS；Z-006 保持 null。其他合理补全替换测试亦 PASS。
- Automated tests：**32/32 PASS**。
- Review PNG：PLAN / ELEVATION / AXON 三张已生成并归档。
- 本地正式 `.blend`：`production/zhenguo_wanfo/output/P2_2_STRUCTURAL_SKELETON_V001.blend`；SHA256 `3b61ccbaca17836bd63d9369ebc3a4c6e25fb27f0d274ea67e64f732ad3000e4`；2,466,272 bytes；local-only。
- Canonical engineering commit：`a5a4181499c0494d16fbaf59d29337fa7d688e9d`，已进入 `origin/main`。
- 独立复核：generator / validator / tests / manifest / machine validation / engineering report 一致，未发现新的工程 blocker。
- T-007 最终工程结论：**PASS / COMPLETE**；**不等于 P2.2 Gate PASS**，仍需 Product Owner 人工结构审核。

## Current Execution State｜2026-09-12

- T-001：PASS
- T-002：PASS
- T-003：PASS / Class B
- T-004：PASS
- T-005 V001：ENGINEERING PASS
- T-005 V002：ENGINEERING PASS / COMPLETE / canonical evidence archived
- T-006 V001：ENGINEERING HOLD / canonical evidence archived
- T-006 V002：ENGINEERING PASS / COMPLETE / canonical evidence archived
- T-007 V001：**ENGINEERING PASS / COMPLETE / canonical evidence archived**
- P0：CLOSED / APPROVED
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO
- P2：ACTIVE
- P2.0：PASS / APPROVED
- P2.1：PASS / APPROVED / CLOSED
- P2.2：**IN PROGRESS / ENGINEERING PASS / PRODUCT OWNER STRUCTURAL REVIEW REQUIRED**
- P2.3：LOCKED / WAITING FOR P2.2 PASS
- Formal Case：平遥镇国寺万佛殿
- Formal Blender geometry：**FIRST FORMAL CANDIDATE GENERATED / LOCAL-ONLY BLEND**
- Current blocker：**NONE**
- Next action：Product Owner 视觉审核 PLAN / ELEVATION / AXON 三张结构审核图；审核前不得宣布 P2.2 Gate PASS。
