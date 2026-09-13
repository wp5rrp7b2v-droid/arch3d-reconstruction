# Execution Log｜ARCH3D-001

本文件记录实际工程执行结果，只保留足以追溯结论的关键事实、证据、失败原因和最终结果；完整脚本、Workflow、Commit 与历史版本由 GitHub 保存。Checkpoint 可压缩重复或过细记录，但不得丢失正式结论与关键证据。

## T-001～T-004｜P0 技术链验证｜PASS

- T-001：项目工作区建立完成；LOW。
- T-002：Local Blender 3.6.23 灰模生成、保存、独立重开、Geometry Integrity、PNG review PASS；MEDIUM。
- T-003：Local 3.6 → GitHub Actions Blender 4.5.13 → Local 3.6 roundtrip PASS / Class B；核心几何、Marker 与所需 Metadata 保留；commit `e26d5d600ed693a8e86a914e24dfbe652d718ed3`。
- T-004：JSON 参数驱动同一 Blender Python 脚本；Baseline 3×2 与 Variant 4×3 参数响应、独立重开、Determinism PASS；commit `63a0c506f98d843376361421cf88e1e74c807dc7`。
- P0：4/4 PASS / APPROVED / CLOSED。

## P1｜选题取证｜PASS / CLOSED

- 正式案例：山西平遥镇国寺万佛殿。
- `SRC-ZG-WF-001` 完整精细测绘报告直接核读完成。
- 85/85关键参数完成分级；46 CONFIRMED / 32 HCI / 4 RC / 3 UNKNOWN。
- Product Owner 批准 `CONDITIONAL GO`；P1 4/4 PASS / CLOSED。

## T-005｜P2.0 Schema Validation｜PASS

- V001 基础 UNKNOWN/DO_NOT_LOCK、RC 可替换约束 PASS。
- V002 增加 observed / report-ideal / reconstructed 三层语义并存验证；6 tests PASS。
- Canonical evidence commit：`a938d9fe96c579c21fb3a16734f9b74efcd7d8bc`。
- P2.0 APPROVED / PASS。

## T-006｜P2.1 Production Parameter Set｜PASS

- V001：85/85 parameter + dependency matrix 完成；因 Z-006 geometry-critical UNKNOWN HOLD。
- D-023 批准独立可替换 `Z-006-RC-01 = 11 × MOD-006 = 3534.3mm`；Z-006 本体保持 UNKNOWN / null / DO_NOT_LOCK。
- V002：21/21 tests PASS；production preflight PASS；geometry-critical unresolved blocker = 0。
- Canonical commit：`fc124922d5c0c1674548f9b99968f9848ffbb332`。
- P2.1 APPROVED / PASS / CLOSED。

## T-007｜P2.2 Structural Skeleton｜PASS

- Think Level: HIGH；Blender 3.6.23。
- Structural scope 6/6；217 stable machine objects（不等于历史构件数）。
- Machine geometry validation PASS；32/32 tests PASS；naked historical constant scan PASS；deterministic rebuild / independent reopen / replaceability tests PASS。
- Local-only `.blend` SHA256：`3b61ccbaca17836bd63d9369ebc3a4c6e25fb27f0d274ea67e64f732ad3000e4`。
- Engineering commit：`a5a4181499c0494d16fbaf59d29337fa7d688e9d`。
- PLAN / ELEVATION / AXON visual review PASS；P2.2 APPROVED / CLOSED。

## T-008｜P2.3 Integrated Reconstruction Candidate｜PASS

- V001：11 families / 40 variants / 365 stable mesh instances；33/33 tests、34/34 machine QC PASS；Cloud roundtrip initially HOLD。
- V003：GitHub Actions Blender 4.5.13 roundtrip successful；Local3.6 return semantic QC PASS；core semantic diff NONE；commit `c18945c52da6666ac9dbe6842fb3d51422fd440a`。
- V004：Evidence Diagnostic 修正；canonical geometry unchanged；33/33 tests、34/34 QC PASS；commit `93aef4803d2c0d3f7e3e3d29e9ab235c2f92d8f3`。
- Final local-only candidate SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。
- 六类视觉审核 PASS；P2.3 APPROVED / CLOSED；P2 4/4 PASS / CLOSED / D-028。

## T-009｜P3.0 Component Ontology & Registry Migration｜PASS / APPROVED

- Think Level: HIGH。
- Component Ontology、Naming/ID、Registry Schema、P2 semantic audit、migration、validation 完成。
- Coverage：11/11 families / 40/40 variants / 365/365 instances；orphan 0/0/0。
- Historical component / proxy / control / envelope 正式分离；Z-006、DG-114、HIS-002、45°转角/榫卯/隐角梁边界保持。
- Engineering commit：`3db50b94cd72e79cef419054aeaa7d2b75523ba5`。
- P3.0 DoD 9/9 PASS / Product Owner APPROVED / D-031。

## T-010｜P3.1 Component Master Scope & Identity｜PASS / APPROVED

- Think Level: HIGH。
- Engineering commit：`774a1469416d49268997d20970c71bb9357849aa`。
- P3.0 Registry 11/11；P1 minimum scope 9/9；27 records；pending 0。
- MASTER_REQUIRED 6 / Deferred 13 / Proxy 4 / Control 3 / Envelope 1。
- Evidence provenance / historical boundary / determinism PASS；5/5 negative mutation probes REJECTED；P2 frozen hashes unchanged。
- 六类 Master scope 锁定：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿。
- Product Owner APPROVED / D-033。

## T-011｜P3.1 Column Master Pilot｜PASS / APPROVED / CLOSED

- Think Level: HIGH；Blender 3.6.23 CLI/background / RC-008 compliant。
- `CMP-COLUMN-001`：diameter 460.0 mm；height 3534.3 mm via replaceable Z-006-RC-01；Z-006 remains UNKNOWN。
- 22/22 machine checks PASS；deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild / Registry registration PASS。
- Review package 6/6 ChatGPT visual PASS；Product Owner APPROVED / D-035。
- Canonical `.blend` SHA256：`98211701fcc358f6174829257ef13310baa4d1a2d5e762637c25c812a4362487`。
- Engineering commit：`4eb79f37d31202ab2088724008b5412cba4d38b0`。

## T-012｜P3.1 Dou Master Lean Batch V002｜PASS / APPROVED / CLOSED

- Execution Mode：`LEAN_PRODUCTION_MODE_V001`。
- Think Level：HIGH first article / MEDIUM proven batch repetition。
- First Article `CMP-LUDOU-COLUMN-001` PASS；shared pipeline PASS；3 components 3/3 engineering PASS。
- Contract：`P3_1_MASTER_ASSET_CONTRACT_V002 / D-036`；corrected ludou field mapping PASS。
- semantic snapshot / transform / evidence boundary / DG-114 non-use / unsupported detail / naked historical constant scan PASS。
- deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild：3/3 PASS。
- Registry registration PASS；P2 frozen baseline unchanged；Contract V002 unchanged；approved column preserved。
- Review package：18/18 individual + 1/1 batch overview；ChatGPT visual review **19/19 PASS**；Product Owner APPROVED / D-037。
- Engineering commit：`d1ae53ee368729a395623a8d9a4342f7455e2e9b`。
- Canonical `.blend` SHA256：
  - Ludou `bc46dbcdcbff738ddd0d88051e8ae362880a3edd8bc06a4144b5ff01788ebf57`
  - Single-longkai `dc1cc93016a19cd08ece0d84ce9bf584bf7780726ac8b6b3c975eae063cfbe32`
  - Interactive dou `d7a78d63a96cbaf215ed0b54692f1c48d0c1acf7410490580c993bbfb0b73d0c`
- Visual review record：`docs/production/zhenguo_wanfo/P3_1_T012_DOU_MASTER_VISUAL_REVIEW_2026-09-13.md`。
- RC-009 Lean Production Mode 首次正式闭环验证成功；未来仅对同质批次默认复用，实质变化仍须新 First Article / Pilot。

## Current Execution State｜R064｜2026-09-13

- P0：CLOSED / APPROVED。
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO。
- P2：CLOSED / 4/4 PASS / PRODUCT OWNER APPROVED。
- P3：ACTIVE / 1/4 PASS。
- P3.0：CLOSED / APPROVED。
- P3.1：ACTIVE / DoD LOCKED / Contract V002 LOCKED / **4 OF 6 MASTERS APPROVED**。
- Current engineering blocker：NONE。
- Current task：NONE。
- Remaining Masters：下六椽栿、上六椽栿。
- Next action：设计并审核梁架类正式 Task Contract；因几何方法不同，必须设置新的 First Article Gate；Product Owner 授权前不启动 Codex / Blender。
