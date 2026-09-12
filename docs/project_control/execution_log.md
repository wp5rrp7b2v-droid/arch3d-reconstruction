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
- 六张正式审核图已生成：PLAN / ELEVATION / AXON / EXTERIOR_3Q / STRUCTURE_DETAIL / EVIDENCE_DIAGNOSTIC；Product Owner 尚未完成正式 P2.3 视觉审核。
- Local-only final candidate SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。
- Canonical engineering commit：`5bd6ca1f8300a170b74c3a9058352768800b56a6`。
- **HOLD blocker：DoD-07 Cloud roundtrip 未执行。** Workflow 与语义快照已准备，但尚无 Blender 4.5.13 cloud run、artifact return 或 Local Blender 3.6 返回验证。
- 不使用被拒绝的 credential extraction / custom API upload 路线。

## T-008 V002｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V002｜ENGINEERING HOLD

- V001 frozen baseline 回归：33/33 automated tests PASS；34/34 local machine QC PASS；semantic snapshot compare PASS。
- Candidate 保持 11 families / 40 variants / 365 stable mesh instances；历史证据边界不变。
- Local canonical `.blend` SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。
- Git blob SHA：`23797dbd360ba67b8195d988f2161ff9eaf37d48`。
- 临时 transport tag：`p2-3-transport-v001`；push PASS；remote advertisement 返回精确 blob SHA。
- 两次独立临时仓库 fetch 均 FAIL：`Empty reply from server`。
- 按 V002 Task Contract 立即 HOLD；Cloud Blender 4.5.13 workflow 未运行，artifact 未生成，Local 3.6 return QC 未运行。
- transport tag 按合同暂不清理，等待 roundtrip 真正完成后统一删除。
- Canonical engineering commit：`d88fa5e1ebed56bb3ec2d79f903697baf1155091`。
- V002 失败发生在本机 Git HTTP binary fetch 路径，不代表 V001 模型或本地 QC 退化。

## T-008 V003｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V003｜READY FOR LOCAL EXECUTION

- 同一 T-008 目标继续，不创建 T-009。
- V001 candidate 与全部本地 PASS 证据继续冻结。
- 不再依赖本机/runner 通过 Git fetch 读取 transport tag binary。
- GitHub Actions 使用其自动提供的 `github.token`，通过 GitHub REST Git Blobs API 按已知 blob SHA 读取 binary；runner 解码后必须重新验证 canonical SHA256 才可启动 Blender。
- 使用普通 Git `p2-3-roundtrip-run-*` tag（指向正常 main commit）触发 workflow，不需要本机 GitHub API credential 或 `gh`。
- Cloud 4.5 QC PASS 后取回 artifact，并由 Local Blender 3.6.23 做最终返回验证；必要时允许 Product Owner 从 Actions 页面手工下载 artifact，安全规则优先于全自动化。
- 完成后更新 manifest / validation evidence，并清理 transport tag + workflow trigger tag。
- Task Contract：`docs/tasks/T-008_P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V003.md`。

## Current Execution State｜2026-09-12

- T-001：PASS
- T-002：PASS
- T-003：PASS / Class B
- T-004：PASS
- T-005 V002：ENGINEERING PASS / COMPLETE / canonical evidence archived
- T-006 V002：ENGINEERING PASS / COMPLETE / canonical evidence archived
- T-007 V001：ENGINEERING PASS / COMPLETE / canonical evidence archived
- T-008 V001：**ENGINEERING HOLD / LOCAL ENGINEERING COMPLETE / CLOUD ROUNDTRIP PENDING**
- T-008 V002：**ENGINEERING HOLD / TRANSPORT BLOB PUSHED / CLOUD NOT RUN**
- T-008 V003：**READY FOR LOCAL EXECUTION**
- P0：CLOSED / APPROVED
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO
- P2：ACTIVE / 3 of 4 Gates PASS
- P2.0：PASS / APPROVED
- P2.1：PASS / APPROVED / CLOSED
- P2.2：PASS / APPROVED / CLOSED
- P2.3：**IN PROGRESS / DOD LOCKED / ENGINEERING HOLD**
- Formal Case：平遥镇国寺万佛殿
- Formal Blender geometry：P2.3 integrated candidate V001 generated locally / local-only canonical blend
- Current blocker：**P2.3 DoD-07 Cloud Blender 4.5.13 roundtrip + Local 3.6 return validation missing**
- Current task：**T-008 V003**
- Next action：执行 V003 authenticated blob retrieval roundtrip；完成后再进入 ChatGPT 独立复核与 Product Owner 六图审核。
