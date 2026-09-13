# Execution Log｜ARCH3D-001

本文件记录实际工程执行结果，只保留足以追溯结论的关键事实、证据、失败原因和最终结果；完整脚本、Workflow、Commit 与历史版本由 GitHub 保存。Checkpoint 可压缩重复或过细记录，但不得丢失正式结论与关键证据。

## T-001～T-004｜P0 技术链验证｜PASS

- T-001：项目工作区建立完成；LOW。
- T-002：Local Blender 3.6.23 灰模生成、保存、独立重开、Geometry Integrity、PNG review PASS；MEDIUM。
- T-003：Local 3.6 → GitHub Actions Blender 4.5.13 → Local 3.6 roundtrip PASS / Class B；commit `e26d5d600ed693a8e86a914e24dfbe652d718ed3`。
- T-004：JSON 参数驱动同一 Blender Python 脚本；Baseline / Variant 参数响应、独立重开、Determinism PASS；commit `63a0c506f98d843376361421cf88e1e74c807dc7`。
- P0：4/4 PASS / APPROVED / CLOSED。

## P1｜选题取证｜PASS / CLOSED

- 正式案例：山西平遥镇国寺万佛殿。
- `SRC-ZG-WF-001` 完整精细测绘报告直接核读完成。
- 85/85 关键参数完成分级；Product Owner 批准 `CONDITIONAL GO`；P1 4/4 PASS / CLOSED。

## T-005｜P2.0 Schema Validation｜PASS

- UNKNOWN/DO_NOT_LOCK、RC 可替换、observed / report-ideal / reconstructed 三层语义验证 PASS。
- Canonical evidence commit：`a938d9fe96c579c21fb3a16734f9b74efcd7d8bc`。

## T-006｜P2.1 Production Parameter Set｜PASS

- 85/85 formal parameter + dependency matrix 完成。
- D-023 批准独立可替换 `Z-006-RC-01 = 11 × MOD-006 = 3534.3mm`；Z-006 本体保持 UNKNOWN / null / DO_NOT_LOCK。
- 21/21 tests PASS；production preflight PASS；canonical commit `fc124922d5c0c1674548f9b99968f9848ffbb332`。

## T-007｜P2.2 Structural Skeleton｜PASS / APPROVED

- Think Level: HIGH；Blender 3.6.23。
- Structural scope 6/6；217 stable machine objects（不等于历史构件数）。
- Machine geometry validation / 32 tests / naked historical constant scan / deterministic rebuild / independent reopen PASS。
- Local-only `.blend` SHA256：`3b61ccbaca17836bd63d9369ebc3a4c6e25fb27f0d274ea67e64f732ad3000e4`。
- Engineering commit：`a5a4181499c0494d16fbaf59d29337fa7d688e9d`。

## T-008｜P2.3 Integrated Reconstruction Candidate｜PASS / APPROVED

- 11 families / 40 variants / 365 stable mesh instances。
- 33/33 tests、34/34 machine QC、Local3.6→Cloud4.5→Local3.6 roundtrip PASS；core semantic diff NONE。
- Final local-only candidate SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。
- Final engineering commit：`93aef4803d2c0d3f7e3e3d29e9ab235c2f92d8f3`；P2 CLOSED / D-028。

## T-009｜P3.0 Component Ontology & Registry Migration｜PASS / APPROVED / CLOSED

- Component Ontology、Naming/ID、Registry Schema、P2 semantic audit / migration 完成。
- Coverage：11/11 families / 40/40 variants / 365/365 instances；orphan 0/0/0。
- Engineering commit：`3db50b94cd72e79cef419054aeaa7d2b75523ba5`；D-031。

## T-010｜P3.1 Component Master Scope & Identity｜PASS / APPROVED

- Engineering commit：`774a1469416d49268997d20970c71bb9357849aa`。
- 27 records；MASTER_REQUIRED 6 / Deferred 13 / Proxy 4 / Control 3 / Envelope 1；pending 0。
- 六类 Master scope：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿；D-033。

## T-011｜P3.1 Column Master Pilot｜PASS / APPROVED / CLOSED

- Blender 3.6.23 CLI/background；22/22 machine checks PASS。
- deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild / Registry registration PASS。
- Review 6/6 visual PASS；Product Owner APPROVED / D-035。
- Canonical `.blend` SHA256：`98211701fcc358f6174829257ef13310baa4d1a2d5e762637c25c812a4362487`。
- Engineering commit：`4eb79f37d31202ab2088724008b5412cba4d38b0`。

## T-012｜P3.1 Dou Master Lean Batch V002｜PASS / APPROVED / CLOSED

- Execution Mode：`LEAN_PRODUCTION_MODE_V001`。
- First Article `CMP-LUDOU-COLUMN-001` PASS；shared pipeline PASS；3/3 engineering PASS。
- deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild：3/3 PASS。
- Review：18/18 individual + 1/1 overview = 19/19 visual PASS；Product Owner APPROVED / D-037。
- Engineering commit：`d1ae53ee368729a395623a8d9a4342f7455e2e9b`。
- Canonical SHA256：Ludou `bc46dbcd...bf57`；Single-longkai `dc1cc930...be32`；Interactive `d7a78d63...73d0c`。
- RC-009 Lean Production Mode 首次闭环验证成功。

## T-013｜P3.1 Six-Chuanfu Master Batch V002｜PASS / APPROVED / CLOSED

- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL + LEAN_PRODUCTION_MODE_V001`；Codex default Think = MEDIUM。
- Authorization：D-038；final approval/closure：D-039。
- First Article `CMP-FRAME-LOWER-SIX-CHUANFU-001` 先 PASS；`CMP-FRAME-UPPER-SIX-CHUANFU-001` 后续 PASS。
- Shared long-member pipeline：PASS。
- 两件各 26/26 machine checks PASS；52 项逐资产检查 PASS；无 unexplained validation errors。
- deterministic semantic regeneration / independent reopen / length mutation / tenon metadata mutation / canonical rebuild：2/2 PASS。
- historical full length = `UNKNOWN / null`；`canonical_reference_length_mm=1000` 仅为 NON-HISTORICAL / REPLACEABLE PROJECT_RULE reference specimen。
- `max_thickness` 保持 observed upper bound；`tenon_area_thickness` 保持 metadata-only / geometry use = 0。
- Unsupported geometry = 0；P2 PRIMARY_FRAME proxy non-use PASS；`REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` carry-forward active。
- P2 frozen baseline、Contract V002、四件既有 approved Master 保护性检查 PASS；`.blend/.blend1` 未进入 Git。
- Canonical `.blend` SHA256：
  - Lower `71b6c0aecc179ff79b95c48fad38645108854e2b14d572d4f11f454e0856a1fd`
  - Upper `c4b83d0c0dc179c3946b2744b9c3887301fb81c3d835bd0f24a96336616a07e7`
- Engineering commit：`f607245444927b9853e0976b891673e387a14750`，发布 SUCCESS。
- 初次视觉审核：12/13 PASS；Batch Overview 因两构件视觉叠合造成潜在局部削形误读，判定为 presentation-only defect。
- 仅重渲染 Overview；其余 12 review assets 与 canonical Masters unchanged。
- Overview correction commit：`cbc0a5417e56b6851778c254a8c4b5a87fc413d3`，发布 SUCCESS。
- Corrected overview SHA256：`fd03116ba035dd98a66363d7bb4699634ebb62484c58c04c3befae32c33d9f32`。
- 最终 Review：**13/13 visual PASS**；Product Owner `APPROVED / CLOSED / D-039`。
- 两个 frame Master Registry 状态提升为 `PRODUCT_OWNER_APPROVED_D039`。
- P3.1 Master coverage：**6/6 approved**。

## Current Execution State｜R069｜2026-09-13

- P0：CLOSED / APPROVED。
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO。
- P2：CLOSED / 4/4 PASS / PRODUCT OWNER APPROVED。
- P3：ACTIVE / 1/4 PASS。
- P3.0：CLOSED / APPROVED。
- P3.1：ACTIVE / DoD LOCKED / Contract V002 LOCKED / **6 OF 6 MASTERS APPROVED**。
- Current engineering blocker：NONE。
- Current task：NONE。
- T-013：APPROVED / CLOSED / D-039。
- Next action：执行独立 `P3.1 Gate Review`，逐项核对 DoD 9/9；Product Owner 明确批准 P3.1 PASS / CLOSED 前，P3.2 继续 LOCKED。
