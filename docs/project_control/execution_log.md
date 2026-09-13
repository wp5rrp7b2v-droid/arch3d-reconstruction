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

## T-008 V001｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001｜ENGINEERING HOLD

- Think Level: HIGH。
- 本地 Blender 3.6.23；Blender Python 3.10.13；host Python 3.10.2。
- Component Library：**11 families / 40 variants**。
- Integrated candidate：**365 stable mesh instances**；柱12、主要梁架8、示意框架连接件54、斗栱臂88、示意接触块88、檩7、椽36、屋面6，其余66为分层诊断控制对象。
- Machine QC：**34/34 PASS / 0 errors**。
- Automated tests：**33/33 PASS**。
- Replacement / mutation：PASS；deterministic rebuild：PASS；independent reopen：PASS / PASS。
- Naked historical constant / manual drift audit：PASS。
- `Z-006` 继续 UNKNOWN / null / DO_NOT_LOCK；`Z-006-RC-01` 继续独立可替换；DG-114 / HIS-002 / 45°转角等边界未升级。
- 六张正式审核图已生成：PLAN / ELEVATION / AXON / EXTERIOR_3Q / STRUCTURE_DETAIL / EVIDENCE_DIAGNOSTIC。
- Local-only final candidate SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。
- Canonical engineering commit：`5bd6ca1f8300a170b74c3a9058352768800b56a6`。
- **HOLD blocker：DoD-07 Cloud roundtrip 未执行。**

## T-008 V002｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V002｜ENGINEERING HOLD

- V001 frozen baseline 回归：33/33 automated tests PASS；34/34 local machine QC PASS；semantic snapshot compare PASS。
- Candidate 保持 11 families / 40 variants / 365 stable mesh instances；历史证据边界不变。
- Git blob SHA：`23797dbd360ba67b8195d988f2161ff9eaf37d48`；临时 transport tag push PASS。
- 两次独立临时仓库 fetch 均 FAIL：`Empty reply from server`。
- Cloud Blender 4.5.13 workflow 未运行；按合同 HOLD。
- Canonical engineering commit：`d88fa5e1ebed56bb3ec2d79f903697baf1155091`。

## T-008 V003｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V003｜ENGINEERING PASS / COMPLETE

- V001 candidate 与全部本地 PASS 证据冻结。
- GitHub Actions 使用 runner `github.token` + Git Blobs API 按已知 blob SHA 读取 binary，不读取本机凭据或 PAT。
- Workflow commit `d595a587c72dc4e76afac249d8a4e667ac772fd0`；Actions run `34695870243` SUCCESS。
- Cloud Blender 4.5.13 input / independent reopen semantic QC PASS。
- Artifact `P2_3_CLOUD_ROUNDTRIP_V001` 下载与 SHA256 核验 PASS。
- Local Blender 3.6.23 return semantic QC PASS；full machine QC 34/34 PASS；core semantic diff NONE。
- V001 regression：33/33 automated tests PASS、34/34 machine QC PASS；11/40/365 与历史边界不变。
- temporary transport / trigger tags 全部清理。
- Canonical final evidence commit：`c18945c52da6666ac9dbe6842fb3d51422fd440a`。
- DoD-07 blocker 清零。

## T-008 V004｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V004｜ENGINEERING PASS / COMPLETE

- Think Level: MEDIUM。
- 首轮六图审核中五张结构图 PASS；原 Evidence Diagnostic 因四级证据边界不可区分而 HOLD。
- V004 只新增只读 diagnostic renderer / sidecar / review evidence，不修改 canonical 建筑几何。
- canonical `.blend` SHA256 before/after：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512` / same。
- 11 families / 40 variants / 365 stable mesh instances unchanged；geometry changed = NO。
- automated tests 33/33 PASS；independent reopen machine QC 34/34 PASS。
- 新 diagnostic SHA256：`998739c5c93e5d835c563bfdcaea4552749427d3511dfd9258d22bb67f719d9c`。
- 四类 priority：UNKNOWN / PLACEHOLDER > RC / approved override > HCI > CONFIRMED。
- category counts：CONFIRMED 0 / HCI 0 / RC 35 / UNKNOWN-placeholder 330；四类 legend 均保留。
- Canonical V004 commit：`93aef4803d2c0d3f7e3e3d29e9ab235c2f92d8f3`。
- ChatGPT 独立工程复核 PASS；Product Owner 直接视觉审核 V002 PASS。

## P2.3 Gate Review｜APPROVED / PASS / CLOSED｜2026-09-12

- PLAN / ELEVATION / AXON / EXTERIOR_3Q / STRUCTURE_DETAIL / corrected EVIDENCE_DIAGNOSTIC_V002：**6/6 PASS**。
- DoD-01～DoD-09：**9/9 PASS**。
- Product Owner 明确批准：`P2.3｜PASS`。
- `CONFIRMED=0 / HCI=0` 仅为 Conservative Risk Map 的实例级最高不确定性聚合结果，不代表参数证据中不存在 CONFIRMED / HCI。
- Evidence Visualization 双层 carry-forward 已批准并归档。

## P2 Phase Closure｜APPROVED / CLOSED｜2026-09-12

- P2.0 / P2.1 / P2.2 / P2.3：**4 / 4 PASS**。
- Decision：D-028。
- Closure archive：`docs/project_control/phase_archive/P2_closure.md`。

## T-009｜P3_0_COMPONENT_ONTOLOGY_REGISTRY_MIGRATION_V001｜ENGINEERING PASS / COMPLETE

- Think Level: HIGH。
- Component Ontology、Naming/ID、Registry Schema、P2 semantic audit、migration、validation 完成。
- Family coverage：**11/11**；Variant coverage：**40/40**；Instance coverage：**365/365**。
- Orphan family / variant / instance：**0 / 0 / 0**。
- Ontology / Registry Schema / Evidence Boundary / Determinism：PASS。
- P2 11 engineering families 已明确区分 historical component concepts、geometric proxies、control objects 与 roof envelope。
- `COLUMN / PURLIN / RAFTER` 仅建立历史构件类型概念；P2 placement 不作为原构数量。
- `BRACKET_ARM / PRIMARY_FRAME` 保持 unresolved/proxy；`BRACKET_CONTACT` 未被解释为小斗。
- `Z-006`、`Z-006-RC-01`、`DG-114`、`HIS-002`、45°转角、榫卯、隐角梁等边界全部保持。
- 未修改 Blender 几何或 P2 canonical `.blend`。
- Canonical engineering commit：`3db50b94cd72e79cef419054aeaa7d2b75523ba5`。

## P3.0 Gate Review｜APPROVED / PASS / CLOSED｜2026-09-13

- DoD-01～DoD-09：**9/9 PASS**。
- 11/11 families、40/40 variants、365/365 instances；orphan 0/0/0。
- Product Owner 明确批准：`P3.0｜PASS / CLOSED`。
- Decision：D-031。
- Gate Review：`docs/production/zhenguo_wanfo/P3_0_GATE_REVIEW_2026-09-13.md`。
- P3.1 `Component Master & Variant Library` 解锁并进入；其 DoD 批准前不得创建 T-010 或启动新增构件几何。

## T-010｜P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001｜ENGINEERING PASS / COMPLETE / APPROVED

- Think Level: HIGH。
- Engineering commit：`774a1469416d49268997d20970c71bb9357849aa`。
- P3.0 Registry coverage：**11/11**；P1 minimum scope：**9/9**；total review records：**27**。
- Eligibility：MASTER_REQUIRED 6 / PROXY_ONLY 4 / CONTROL_ONLY 3 / ENVELOPE_ONLY 1 / DEFERRED_INSUFFICIENT_EVIDENCE 13 / unexplained pending 0。
- Evidence provenance / historical boundary / determinism：PASS；5/5 negative mutation probes REJECTED；P2 frozen baseline hashes unchanged。
- Product Owner 批准 T-010 Scope Matrix & Identity Resolution；Decision：D-033。
- 当前锁定 6 个 MASTER_REQUIRED：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿。
- 13 个证据不足对象继续 Deferred；P3.0 proxy/control/envelope 边界保持，不发生静默历史化。
- T-010 未创建 Blender Master / Variant geometry；批准不等于 P3.1 PASS。
- Technical Review：`docs/production/zhenguo_wanfo/P3_1_T010_SCOPE_IDENTITY_REVIEW_2026-09-13.md`。

## Current Execution State｜2026-09-13

- P0：CLOSED / APPROVED。
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO。
- P2：CLOSED / 4/4 PASS / PRODUCT OWNER APPROVED。
- P3：ACTIVE / **1/4 PASS**。
- P3.0：**CLOSED / 9/9 PASS / PRODUCT OWNER APPROVED**。
- P3.1：**ACTIVE / DOD LOCKED / T-010 APPROVED / SIX-MASTER SCOPE LOCKED**。
- Current engineering blocker：NONE。
- Current task：NONE。
- Next action：先为 6 个 approved MASTER_REQUIRED 建立 Canonical Master Asset Contract；在 Contract 锁定前不启动批量 Blender Master 几何。