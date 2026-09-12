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

## Current Execution State｜2026-09-12

- T-001：PASS
- T-002：PASS
- T-003：PASS / Class B
- T-004：PASS
- T-005 V001：ENGINEERING PASS
- T-005 V002：ENGINEERING PASS / COMPLETE / canonical evidence archived
- P0：CLOSED / APPROVED
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO
- P2：ACTIVE
- P2.0：**READY FOR PRODUCT OWNER DECISION**
- P2.0 Gate Review：7/7 PASS；Reviewer Recommendation = **APPROVE PASS**
- Formal Case：平遥镇国寺万佛殿
- Formal Blender geometry：LOCKED until Product Owner approves P2.0
