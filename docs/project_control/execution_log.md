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
- Engineering commit：`a5a4181499c0494d16fbaf59d29337fa7d688e9d`。

## T-008｜P2.3 Integrated Reconstruction Candidate｜PASS / APPROVED

- 11 families / 40 variants / 365 stable mesh instances。
- 33/33 tests、34/34 machine QC、Local3.6→Cloud4.5→Local3.6 roundtrip PASS；core semantic diff NONE。
- Engineering commit：`93aef4803d2c0d3f7e3e3d29e9ab235c2f92d8f3`；P2 CLOSED / D-028。

## T-009｜P3.0 Component Ontology & Registry Migration｜PASS / APPROVED / CLOSED

- Component Ontology、Naming/ID、Registry Schema、P2 semantic audit / migration 完成。
- Coverage：11/11 families / 40/40 variants / 365/365 instances；orphan 0/0/0。
- Engineering commit：`3db50b94cd72e79cef419054aeaa7d2b75523ba5`；D-031。

## T-010｜P3.1 Component Master Scope & Identity｜PASS / APPROVED

- Engineering commit：`774a1469416d49268997d20970c71bb9357849aa`。
- 27 records；MASTER_REQUIRED 6 / Deferred 13 / Proxy 4 / Control 3 / Envelope 1；pending 0。
- 六类 Master scope：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿；D-033。

## T-011｜P3.1 Column Master Pilot｜PASS / APPROVED / CLOSED

- 22/22 machine checks PASS。
- deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild / Registry registration PASS。
- Review 6/6 visual PASS；Product Owner APPROVED / D-035。
- Engineering commit：`4eb79f37d31202ab2088724008b5412cba4d38b0`。

## T-012｜P3.1 Dou Master Lean Batch V002｜PASS / APPROVED / CLOSED

- First Article `CMP-LUDOU-COLUMN-001` PASS；3/3 engineering PASS。
- deterministic regeneration / reopen / mutation / rebuild：3/3 PASS。
- Review：19/19 visual PASS；Product Owner APPROVED / D-037。
- Engineering commit：`d1ae53ee368729a395623a8d9a4342f7455e2e9b`。

## T-013｜P3.1 Six-Chuanfu Master Batch V002｜PASS / APPROVED / CLOSED

- `CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL + LEAN_PRODUCTION_MODE_V001`；Codex MEDIUM。
- 两件各 26/26 machine checks PASS；52 项逐资产检查 PASS。
- deterministic regeneration / independent reopen / mutation / canonical rebuild：2/2 PASS。
- historical full length = `UNKNOWN / null`；`canonical_reference_length_mm=1000` 仅为 NON-HISTORICAL / REPLACEABLE PROJECT_RULE reference specimen。
- 最终 Review：13/13 visual PASS；Product Owner APPROVED / D-039。
- Engineering commit：`f607245444927b9853e0976b891673e387a14750`；Overview correction `cbc0a5417e56b6851778c254a8c4b5a87fc413d3`。
- P3.1 Master coverage：6/6 approved。

## T-014｜P3.1 Master Library Overview V001｜PASS / CLOSED

- whole-library Overview 覆盖 6/6 approved Masters；formal variants = 0。
- canonical Masters / individual review assets / batch overviews / P2 frozen baseline / Contract V002：UNCHANGED。
- Final Overview SHA256：`4719a31c18de13b0453a64d29847381d8e45af0f145bcb37bf7fee0abf9671a7`。
- Publication merge commit：`c15064bcd7d5cf2f3e58cdbffccc256043836413`。
- ChatGPT final visual review：PASS。

## P3.1 Gate Review｜9/9 PASS / APPROVED / CLOSED / D-040

- MASTER_REQUIRED coverage：6/6 / 100%。
- Proxy 4 / Control 3 / Envelope 1 / Deferred 13 保持非历史化。
- Registry / evidence traceability / replaceability / deterministic regeneration / independent reopen / P2 frozen baseline：PASS。
- P3.2｜构件组合关系模型解锁并进入。

## T-015｜P3.2 构件组合关系基础工程实现｜PASS / APPROVED / CLOSED / D-042

- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE`；Think Level：MEDIUM。
- Design baseline：`P3_2_RELATIONSHIP_FOUNDATION_DESIGN_V001`（T-015A / Chat design）。
- Engineering commit：`49b0415479d811a26d4f44588d15cd863467edf4`；`origin/main` 同 SHA。
- 正式节点：6/6 approved Masters 唯一映射；未创建重复 component identity。
- 基础关系：5/5（承托、连接、定位、重复、从属）。
- Interface foundation：PASS；6 个 Master 共 18 个最小局部接口。
- Machine validation：31/31 PASS。
- Negative tests：21/21 expected rejection PASS。
- Gate Hard Fail 触发测试：`REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`、`SILENT_HISTORICIZATION`、`BAKED_MANUAL_ASSEMBLY` 均可触发；canonical state = 0 Hard Fail。
- P2 frozen baseline：UNCHANGED；P3.1 canonical Masters：UNCHANGED；unrelated untracked files：UNTOUCHED。
- 独立 Git diff 核对：`2685a80 → 49b0415` 仅新增 8 个 T-015 文件，P2/P3.1 既有 tracked files 无修改。
- ChatGPT structural review：PASS。
- Product Owner：APPROVED / CLOSED / D-042。
- 非阻断 carry-forward：后续真实代表性组合不得机械使用统一“局部下参考面”替代全部承托/连接界面；应按关系显式建立/验证上承托、下承托及中心/轴线定位基准，并区分工程接口与历史接触关系。
- **T-015 CLOSED 不等于 P3.2 PASS。**

## Current Execution State｜R073｜2026-09-14

- P0：CLOSED / APPROVED。
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO。
- P2：CLOSED / 4/4 PASS / PRODUCT OWNER APPROVED。
- P3：ACTIVE / **2/4 PASS**。
- P3.0：PASS / APPROVED / CLOSED。
- P3.1：PASS / APPROVED / CLOSED / D-040。
- P3.2：**ACTIVE / DOD LOCKED / T-015 APPROVED CLOSED / NEXT TASK PLANNING READY**。
- P3.3：LOCKED / WAITING_FOR_P3.2_PASS。
- Current engineering blocker：NONE。
- Current task：NONE。
- Next action：设计 P3.2 下一项“代表性构件组合关系验证”任务，覆盖竖向承托链、横向梁架链与重复关系，并显式验证真实接口和证据边界。
