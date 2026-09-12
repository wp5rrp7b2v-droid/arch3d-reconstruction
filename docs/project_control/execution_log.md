# Execution Log｜ARCH3D-001

本文件记录实际工程执行结果，只保留足以追溯结论的关键事实、证据、失败原因和最终结果；完整脚本、Workflow、Commit 与历史版本由 GitHub 保存。

## T-001｜PROJECT_WORKSPACE_INIT_V001｜PASS

- Think Level: LOW。
- 本地项目工作区建立完成；无 blocker。

## T-002｜LOCAL_BLENDER_POC_V002｜PASS

- Think Level: MEDIUM。
- Local Blender 3.6.23 macOS x64。
- 最小灰模生成、保存、独立重开、Geometry Integrity、PNG 审核：PASS。

## T-003｜LOCAL_CLOUD_ROUNDTRIP_POC｜PASS / CLASS B

- Codex Cloud 因网络代理无法取得 Blender，不作为 Blender Executor。
- GitHub Actions Hosted Runner + Blender 4.5.13 成为 Cloud Executor。
- Local 3.6 → GitHub → Blender 4.5.13 → Artifact → Local 3.6：PASS。
- 核心几何、Marker 与所需 Metadata 保留；3.6 会移除部分不支持的 4.5 UI region 数据。
- 分类：**Class B｜ROUNDTRIP_WITH_LIMITATIONS**。
- 关键 commit：`e26d5d600ed693a8e86a914e24dfbe652d718ed3`。

## T-004｜PARAMETRIC_ARCHITECTURE_POC_V001｜PASS

- Think Level: MEDIUM。
- 独立 JSON 参数驱动同一 Blender Python 脚本。
- Baseline 3×2 → 12柱 / 21主要对象；Variant 4×3 → 20柱 / 31主要对象。
- 参数响应、独立重开与 Determinism：PASS。
- 证据归档 commit：`63a0c506f98d843376361421cf88e1e74c807dc7`。
- `.blend / .blend1` local-only。

## P0 Gate Review｜APPROVED / CLOSED｜2026-09-11

- P0.0–P0.3：4/4 PASS。
- Product Owner 批准 P0 关闭；P0.2 Class B 限制继续生效。

## P1 Research / Gate Execution Summary｜CLOSED｜2026-09-12

- 正式案例：山西平遥镇国寺万佛殿。
- `SRC-ZG-WF-001` 完整精细测绘报告直接核读完成。
- P1.2：10/10 PASS / Product Owner APPROVED。
- P1.3：85/85关键参数分级完成；46 CONFIRMED / 32 HIGH_CONFIDENCE_INFERENCE / 4 REASONABLE_COMPLETION / 3 UNKNOWN。
- Product Owner 批准 `CONDITIONAL GO`；P1 4/4 PASS / CLOSED。

## T-005 V001｜P2_0_SCHEMA_VALIDATION_V001｜ENGINEERING PASS / GATE HOLD

- Think Level: MEDIUM。
- UNKNOWN/DO_NOT_LOCK、RC可替换等基础 Schema 机械约束 PASS；4 tests PASS。
- HOLD 原因：V001 尚未显式验证三层语义并存且不串层。

## T-005 V002｜P2_0_SCHEMA_VALIDATION_V002｜ENGINEERING PASS / COMPLETE

- V001 regression 4/4 PASS；完整 suite 6 tests PASS。
- `observed_as_measured / report_ideal_model / reconstructed_963_candidate` 三层 reader preservation PASS。
- Canonical evidence commit：`a938d9fe96c579c21fb3a16734f9b74efcd7d8bc`。

## P2.0 Gate Review｜APPROVED / PASS｜2026-09-12

- Gate Review 7/7 PASS；CG-01 满足。
- Product Owner 批准 `P2.0｜PASS`。

## T-006 V001｜P2_1_PRODUCTION_PARAMETER_SET_V001｜ENGINEERING HOLD

- Think Level: HIGH。
- Formal Parameter Set：85/85；Dependency Matrix：85/85。
- Machine validation PASS；11/11 tests PASS。
- Production preflight HOLD：`Z-006` 为 `BLOCKS_P2_2_GEOMETRY`；geometry-critical unresolved blocker = 1。
- `DG-114` = BOUNDED_NON_BLOCKING；`HIS-002` = METADATA_ONLY_BLOCK。
- 无静默补值、无 Blender 正式几何。
- Canonical commit：`1ccf08aeed6f5bb6ae3ed0e0ccd25cd8346055f0`。

## T-006 V002｜P2_1_PRODUCTION_PARAMETER_SET_V002｜ENGINEERING PASS / COMPLETE

- Product Owner 通过 D-023 批准独立 `Z-006-RC-01 = 11 × MOD-006 = 3534.3mm`。
- Z-006 仍 `UNKNOWN / null / DO_NOT_LOCK`；RC-01 独立、可替换、可追溯。
- V001 regression 11/11 PASS；总测试 21/21 PASS；production preflight PASS。
- geometry-critical unresolved blocker = 0。
- Canonical commit：`fc124922d5c0c1674548f9b99968f9848ffbb332`。

## P2.1 Gate Review｜APPROVED / PASS / CLOSED｜2026-09-12

- DoD 9/9 PASS；Product Owner 批准 `P2.1｜PASS`。
- P2.1 CLOSED；P2.2 解锁。

## T-007 V001｜P2_2_STRUCTURAL_SKELETON_V001｜ENGINEERING PASS / COMPLETE

- Think Level: HIGH。
- Blender 3.6.23；Blender Python 3.10.13；host test Python 3.10.2。
- 正式输入 hash、approved override、dependency matrix 与 schema 进入 build manifest。
- Structural scope：**6/6**。
- 稳定命名 mesh objects：**217** = GRID 8 / COLUMN 12 / FRAME 62 / BRACKET 88 / ROOF 43 / GABLE 4。
- 217 为 Blender 机器结构/控制对象数，不等于217个历史构件。
- `Z-006` 仍 UNKNOWN；RC-01 独立、可替换并驱动柱高 3534.3mm。
- Machine geometry validation：PASS / 0 errors；tolerance 0.01mm。
- Naked historical constant scan：PASS。
- Deterministic rebuild：PASS；结构/语义结果一致，`.blend` 字节级 hash 不要求相同。
- Independent reopen：PASS / PASS。
- Replaceability synthetic rebuild tests：PASS。
- Automated tests：32/32 PASS。
- PLAN / ELEVATION / AXON 三张 review PNG 已生成并归档。
- Local-only `.blend` SHA256：`3b61ccbaca17836bd63d9369ebc3a4c6e25fb27f0d274ea67e64f732ad3000e4`。
- Canonical engineering commit：`a5a4181499c0494d16fbaf59d29337fa7d688e9d`。

## P2.2 Gate Review｜APPROVED / PASS / CLOSED｜2026-09-12

- Engineering review：PASS。
- Product Owner 直接审核 PLAN / ELEVATION / AXON：PASS。
- DoD-01～DoD-09：**9/9 PASS**。
- Product Owner 明确批准：`P2.2｜PASS`。
- P2.2 CLOSED；P2.3 解锁。
- Carry-forward：Z-006、DG-114、HIS-002 与45°转角/榫卯/隐角梁等证据边界继续生效；217对象数不作为历史构件数量声明。
- Gate Review：`docs/production/zhenguo_wanfo/P2_2_GATE_REVIEW_2026-09-12.md`。

## Current Execution State｜2026-09-12

- T-001：PASS
- T-002：PASS
- T-003：PASS / Class B
- T-004：PASS
- T-005 V002：ENGINEERING PASS / COMPLETE / canonical evidence archived
- T-006 V002：ENGINEERING PASS / COMPLETE / canonical evidence archived
- T-007 V001：ENGINEERING PASS / COMPLETE / canonical evidence archived
- P0：CLOSED / APPROVED
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO
- P2：ACTIVE / 3 of 4 Gates PASS
- P2.0：PASS / APPROVED
- P2.1：PASS / APPROVED / CLOSED
- P2.2：**PASS / APPROVED / CLOSED**
- P2.3：**UNLOCKED / CURRENT / DOD DEFINITION REQUIRED**
- Formal Case：平遥镇国寺万佛殿
- Formal Blender geometry：P2.2 medium-LOD structural baseline APPROVED / local-only blend
- Current blocker：NONE
- Current task：NONE
- Next action：明确并锁定 P2.3 Definition of Done；在此之前不创建下一项正式工程 T-###。