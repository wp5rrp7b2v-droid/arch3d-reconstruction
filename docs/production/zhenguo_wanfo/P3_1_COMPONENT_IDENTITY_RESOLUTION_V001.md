# P3.1 Component Identity Resolution V001｜T-010

Status: **EVIDENCE REVIEW COMPLETE / PRODUCT OWNER REVIEW REQUIRED**

The JSON companion carries every attribute and source reference. `CONFIRMED` observed measurements are not automatically 963 design facts; report ideal and reconstructed candidate remain separate.

## PRX-BRACKET-JUMP-001｜未定铺作出跳代理

- Identity: `unresolved_bracket_jump_proxy`; real historical type: `None`; status: `PROXY_ONLY`.
- Context: 外檐铺作出跳. P2 relationship: 保留代理；后续按实证拆分栱、昂及铺作组合，不把四跳均分网格当成构件。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: P2 equal jump subdivisions are aggregate graphic topology; DG-110–113 do not identify individual 栱 or 昂.
- Known input: P2 engineering parameter IDs: DG-001, DG-002, DG-110, DG-111, DG-112, DG-113, MOD-002, MOD-003, MOD-004, Z-006-RC-01; not direct member geometry
- Unresolved: DG-110～113 只控制总体出跳；45°构件、栱昂分件、榫卯未定。; HIS-002: component originality unknown; Individual member drawings, section, endpoints and 45° node evidence.
- Source pages: PDF p119–120 / printed p104–105 recommended conclusions.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: DG-001=七铺作、双杪双下昂 [CONFIRMED, observed_current_topology, DIRECT_PLUS_SUPPORT]; DG-002=五铺作、双杪偷心 [CONFIRMED, observed_current_topology, DIRECT_PLUS_SUPPORT]; DG-110=48 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; DG-111=47 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; DG-112=47 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; DG-113=21 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-003=14 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-004=10 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## PRX-BRACKET-CONTACT-001｜铺作端点接触代理

- Identity: `bracket_endpoint_contact_proxy`; real historical type: `False`; status: `PROXY_ONLY`.
- Context: 铺作出跳端点. P2 relationship: 保留端点代理；不得重命名为小斗。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: Diagrammatic contact block is not 小斗; DG-114 unified-small-dou rule remains UNKNOWN.
- Known input: P2 engineering parameter IDs: DG-001, DG-002, DG-110, DG-111, MOD-002, MOD-003, MOD-004, MOD-005, Z-006-RC-01; not direct member geometry
- Unresolved: DG-114 为 UNKNOWN / DO_NOT_LOCK；不能据此给散斗、齐心斗或交互斗统一规格。; HIS-002: component originality unknown; A component-specific斗 identity and shape source, without using P2 contact-block dimensions.
- Source pages: PDF p65–66 / printed p50–51 tables 2-28 / 2-29.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: DG-001=七铺作、双杪双下昂 [CONFIRMED, observed_current_topology, DIRECT_PLUS_SUPPORT]; DG-002=五铺作、双杪偷心 [CONFIRMED, observed_current_topology, DIRECT_PLUS_SUPPORT]; DG-110=48 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; DG-111=47 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-003=14 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-004=10 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-005=21 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## CMP-COLUMN-001｜柱

- Identity: `column`; real historical type: `True`; status: `MASTER_REQUIRED`.
- Context: 外围檐柱柱网. P2 relationship: 归入柱构件概念；位置和候选尺寸只作为建筑专属变体。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: Column type and observed diameter are verified; a reusable parametric column body is feasible while Z-006 remains unknown.
- Known input: Observed diameter approximately 460 mm (Z-001); report design candidate 459 mm (Z-002); height is an explicit free parameter, not a historical constant.
- Unresolved: Z-006 963柱高 UNKNOWN；Z-006-RC-01 仅是 D-023 可替换生产候选；角柱生起为报告猜测。; HIS-002: component originality unknown; 963 column height and individual originality remain unknown; no fixed historical height is licensed.; Z-006-RC-01 is a separate replaceable candidate under D-023, not Z-006 history.
- Source pages: PDF p49–50 / printed p34–35 2.1.2 / table 2-6.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: PM-013=12 [CONFIRMED, observed_current_topology, DIRECT_PRIMARY]; PM-014=0 [CONFIRMED, observed_current_topology, DIRECT_PRIMARY]; Z-002=459 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; Z-005=61.2 [REASONABLE_COMPLETION, reconstructed_963_candidate, REPORT_INFERRED_GUESS]; Z-001=460 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; Z-006=None [UNKNOWN, reconstructed_963_candidate, UNKNOWN].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `CMP-COLUMN-001`; asset-contract readiness: `READY_WITH_BOUNDED_LOD`.

## CTL-FRAME-001｜梁架层位控制对象

- Identity: `frame_tier_control`; real historical type: `False`; status: `CONTROL_ONLY`.
- Context: 梁架控制坐标. P2 relationship: 保留工程控制命名空间，不迁入历史构件目录。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: Frame-tier locator has no physical historical member identity.
- Known input: P2 engineering parameter IDs: FR-004, FR-005, FR-006, FR-007, MOD-002, MOD-003, MOD-004, PM-012, ROOF-004, ROOF-005, ROOF-006, ROOF-007, ROOF-008, ROOF-009, Z-006-RC-01; not direct member geometry
- Unresolved: 控制长度和位置不能解释为实体梁、枋或节点。; HIS-002: component originality unknown; Not applicable to a control object.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: FR-004=1759.5 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; FR-005=1759.5 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; FR-006=1836 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; FR-007=[120, 115, 210] [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-003=14 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-004=10 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; PM-012=10710 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; ROOF-004=25 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-005=40 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-006=82 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-007=88 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-008=61 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-009=82 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## PRX-FRAME-CONNECTOR-001｜梁架层位连接代理

- Identity: `frame_tier_connector_proxy`; real historical type: `False`; status: `PROXY_ONLY`.
- Context: 梁架层位连接处. P2 relationship: 保留代理；未来按确证梁架成员替换。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: P2 connector endpoints do not identify 托脚, 蜀柱 or joints.
- Known input: P2 engineering parameter IDs: FR-004, FR-005, FR-006, FR-007, MOD-002, MOD-003, MOD-004, PM-012, ROOF-004, ROOF-005, ROOF-006, ROOF-007, ROOF-008, ROOF-009, Z-006-RC-01; not direct member geometry
- Unresolved: 端点与截面为中等 LOD；不能命名为托脚、蜀柱等具体历史构件。; HIS-002: component originality unknown; Member-specific section, length, topology and contact/joint evidence.
- Source pages: PDF p81 / printed p66 table 2-38.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: FR-004=1759.5 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; FR-005=1759.5 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; FR-006=1836 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; FR-007=[120, 115, 210] [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-003=14 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-004=10 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; PM-012=10710 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; ROOF-004=25 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-005=40 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-006=82 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-007=88 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-008=61 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-009=82 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## CTL-GABLE-001｜山面轮廓控制对象

- Identity: `gable_guide_control`; real historical type: `False`; status: `CONTROL_ONLY`.
- Context: 山面轮廓. P2 relationship: 保留诊断控制命名空间。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: Gable diagnostic line is not 博风板, 角梁 or another physical member.
- Known input: P2 engineering parameter IDs: FR-007, MOD-002, OUT-003, ROOF-010, ROOF-011, Z-006-RC-01; not direct member geometry
- Unresolved: 山面控制线不能解释为博风板、角梁或其他实体构件。; HIS-002: component originality unknown; Not applicable to a control object.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: FR-007=[120, 115, 210] [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; OUT-003=92 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-010=231 [REASONABLE_COMPLETION, reconstructed_963_candidate, REPORT_INFERRED_HIGH_CAUTION]; ROOF-011=3534.3 [REASONABLE_COMPLETION, reconstructed_963_candidate, REPORT_INFERRED_HIGH_CAUTION].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## CTL-GRID-001｜柱网定位控制对象

- Identity: `bay_grid_control`; real historical type: `False`; status: `CONTROL_ONLY`.
- Context: 平面柱网. P2 relationship: 保留定位控制命名空间。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: Grid locator is not a column or historical member.
- Known input: P2 engineering parameter IDs: MOD-001, PM-001, PM-002, PM-008, PM-009, PM-010, Z-007; not direct member geometry
- Unresolved: 线段数不是柱数或历史构件数。; HIS-002: component originality unknown; Not applicable to a control object.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: MOD-001=306 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; PM-001=3 [CONFIRMED, observed_current_topology, DIRECT_PRIMARY]; PM-002=3 [CONFIRMED, observed_current_topology, DIRECT_PRIMARY]; PM-008=14.5 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; PM-009=12 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; PM-010=11.5 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; Z-007=Z = 0; abstract column-foot design plane [REASONABLE_COMPLETION, project_model_datum, PROJECT_RULE].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## UNR-PRIMARY-FRAME-001｜未分解主体梁架代理

- Identity: `unresolved_primary_frame_proxy`; real historical type: `None`; status: `PROXY_ONLY`.
- Context: 主体梁架. P2 relationship: 保留集合代理；后续按证据拆分六椽栿、梁、枋等，不能把整个 family 命名为单件。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: Aggregate P2 frame meshes cannot be assigned to individual 六椽栿, 梁 or 枋.
- Known input: P2 engineering parameter IDs: DG-113, MOD-002, MOD-003, MOD-004, MOD-005, PM-011, PM-012, RF-001, Z-006-RC-01; not direct member geometry
- Unresolved: 六椽栿、阑额等术语有证据，但 P2 两种网格不能逐一等同具体历史成员。; HIS-002: component originality unknown; Member-by-member mapping; independently verified identities are separate derived candidates.
- Source pages: PDF p81 / printed p66 table 2-38.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: DG-113=21 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-003=14 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-004=10 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-005=21 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; PM-011=11475 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; PM-012=10710 [HIGH_CONFIDENCE_INFERENCE, reconstructed_963_candidate, REPORT_INFERRED]; RF-001=复合式六椽栿通檐用两柱、彻上露明 [CONFIRMED, observed_current_topology, DIRECT_PRIMARY].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## CMP-PURLIN-001｜槫类构件

- Identity: `purlin_type`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: 屋架各槫位. P2 relationship: 以报告使用的槫为类名；具体撩风/下平/上平/脊槫分型暂不由 P2 单一 variant 锁定。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: 槫 is a verified type term, but P2 one section/variant is an engineering envelope, not a measured component profile.
- Known input: Measured purlin-to-purlin rises A/B/C and inferred position rises constrain placement, not an individual 槫 cross-section.
- Unresolved: 当前 P2 截面、数量和排布为 roof-control 候选，不是逐根原构清单。; HIS-002: component originality unknown; Position-specific sections, member lengths, end conditions and evidence for whether positions are variants or separate types.
- Source pages: PDF p103–107 / printed p88–92 tables 2-51 / 2-52.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: FR-007=[120, 115, 210] [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; OUT-003=92 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-007=88 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-008=61 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-009=82 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-010=231 [REASONABLE_COMPLETION, reconstructed_963_candidate, REPORT_INFERRED_HIGH_CAUTION]; ROOF-011=3534.3 [REASONABLE_COMPLETION, reconstructed_963_candidate, REPORT_INFERRED_HIGH_CAUTION].
- Evidence gap / next source: Position-specific sections, member lengths, end conditions and evidence for whether positions are variants or separate types. / Obtain attributable report drawings/tables or an approved formal bridge resolving: Position-specific sections, member lengths, end conditions and evidence for whether positions are variants or separate types..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## CMP-RAFTER-001｜椽类构件

- Identity: `rafter_type`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: 屋面各坡段. P2 relationship: 保留椽构件概念，P2 三种坡段仅作图示代理。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: 椽 type is real, but P2 slope segments and spacing are diagrammatic.
- Known input: Roof slope and eave references constrain envelope/placement, not individual 椽 shape or count.
- Unresolved: P2 36 个图示段的间距、数量、翼角做法不能作为历史精确椽布置。; HIS-002: component originality unknown; Measured sections, lengths, eave/flying-rafter distinctions, spacing and wing-corner form.
- Source pages: PDF p104–109 / printed p89–94 2.3.3 / 2.4.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: FR-007=[120, 115, 210] [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; OUT-003=92 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-007=88 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-008=61 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-009=82 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED].
- Evidence gap / next source: Measured sections, lengths, eave/flying-rafter distinctions, spacing and wing-corner form. / Obtain attributable report drawings/tables or an approved formal bridge resolving: Measured sections, lengths, eave/flying-rafter distinctions, spacing and wing-corner form..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## ENV-ROOF-001｜屋面连续形态包络

- Identity: `roof_surface_envelope`; real historical type: `False`; status: `ENVELOPE_ONLY`.
- Context: 屋面外表. P2 relationship: 保留零厚度包络层，不登记为瓦、望板或实体屋面构件。
- Derivation: P3.0 record retained unchanged; no automatic historical upgrade.
- Decision: Zero-thickness surface strips are not tiles, boarding or solid roof members.
- Known input: P2 engineering parameter IDs: FR-007, MOD-002, OUT-003, ROOF-007, ROOF-008, ROOF-009, ROOF-010, ROOF-011, Z-006-RC-01; not direct member geometry
- Unresolved: 六片平面条带无厚度、铺瓦及真实曲面构造主张。; HIS-002: component originality unknown; Not applicable to an envelope surface.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md, docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md, docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md, production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json, production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json, production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json, production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json.
- Attribute evidence: FR-007=[120, 115, 210] [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; MOD-002=15.3 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; OUT-003=92 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-007=88 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-008=61 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-009=82 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; ROOF-010=231 [REASONABLE_COMPLETION, reconstructed_963_candidate, REPORT_INFERRED_HIGH_CAUTION]; ROOF-011=3534.3 [REASONABLE_COMPLETION, reconstructed_963_candidate, REPORT_INFERRED_HIGH_CAUTION].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## CMP-LUDOU-COLUMN-001｜柱头栌斗

- Identity: `column_head_ludou`; real historical type: `True`; status: `MASTER_REQUIRED`.
- Context: 外檐柱头铺作下层. P2 relationship: P1-derived identity; P2 BRACKET_CONTACT remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-CONTACT-001 (BRACKET_CONTACT) record is retained, not renamed or superseded.
- Decision: Distinct named column-head斗 with measured width/depth/height supports a bounded reusable type; P2 contact block supplies no geometry.
- Known input: Top/bottom width and depth plus total, flat and sloped heights from tables 2-26/2-27.
- Unresolved: Exact 3D ear/cavity/profile and mortise geometry are not directly quantified; limit later Master to evidence-bounded medium LOD.; Observed means include compression/wear and are not 963 design dimensions; DG-114 remains UNKNOWN.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p62–63 / printed p47–48 tables 2-26 / 2-27.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: DG-101=475.1 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; DG-102=327.1 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; DG-103=446.3 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; DG-104=305.5 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_total_height=293.8 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_flat_height=58.75 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_sloped_height=116.2 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `CMP-LUDOU-COLUMN-001`; asset-contract readiness: `READY_WITH_BOUNDED_LOD`.

## CMP-DOU-BOTTOM-LONGKAI-001｜底斗

- Identity: `bottom_long_kai_dou`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: 外檐铺作长开斗组. P2 relationship: P1-derived identity; P2 BRACKET_CONTACT remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-CONTACT-001 (BRACKET_CONTACT) record is retained, not renamed or superseded.
- Decision: Named and measured distinct斗 type, but missing depth prevents a qualified canonical 3D Master; DG-114 cannot fill it.
- Known input: Top/bottom widths and total height, table 2-28/2-29.
- Unresolved: Exact 3D ear/cavity/profile and mortise geometry are not directly quantified; limit later Master to evidence-bounded medium LOD.; Observed means include compression/wear and are not 963 design dimensions; DG-114 remains UNKNOWN.; Depth is not recorded in the approved direct-review summary.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p65–66 / printed p50–51 tables 2-28 / 2-29.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: DG-105=255.56 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; DG-106=178.56 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_total_height=161.78 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY].
- Evidence gap / next source: Exact 3D ear/cavity/profile and mortise geometry are not directly quantified; limit later Master to evidence-bounded medium LOD.; Observed means include compression/wear and are not 963 design dimensions; DG-114 remains UNKNOWN.; Depth is not recorded in the approved direct-review summary. / Obtain direct original-page member-specific geometry and identity comparison resolving: Exact 3D ear/cavity/profile and mortise geometry are not directly quantified; limit later Master to evidence-bounded medium LOD.; Observed means include compression/wear and are not 963 design dimensions; DG-114 remains UNKNOWN.; Depth is not recorded in the approved direct-review summary..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗

- Identity: `single_direction_long_kai_dou`; real historical type: `True`; status: `MASTER_REQUIRED`.
- Context: 外檐铺作单向长开位置. P2 relationship: P1-derived identity; P2 BRACKET_CONTACT remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-CONTACT-001 (BRACKET_CONTACT) record is retained, not renamed or superseded.
- Decision: Named orientation-specific斗 with distinct measured profile; future placement rotation alone does not create another type.
- Known input: Top/bottom width and depth plus height, table 2-28/2-29.
- Unresolved: Exact 3D ear/cavity/profile and mortise geometry are not directly quantified; limit later Master to evidence-bounded medium LOD.; Observed means include compression/wear and are not 963 design dimensions; DG-114 remains UNKNOWN.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p65–66 / printed p50–51 tables 2-28 / 2-29.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: DG-107=236.2 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_bottom_width=162.7 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_top_depth=256.2 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_bottom_depth=177.2 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_total_height=158.6 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `CMP-DOU-SINGLE-LONGKAI-001`; asset-contract readiness: `READY_WITH_BOUNDED_LOD`.

## CMP-DOU-INTERACTIVE-001｜交互斗

- Identity: `interactive_dou`; real historical type: `True`; status: `MASTER_REQUIRED`.
- Context: 外檐铺作交互承托位置. P2 relationship: P1-derived identity; P2 BRACKET_CONTACT remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-CONTACT-001 (BRACKET_CONTACT) record is retained, not renamed or superseded.
- Decision: Explicit measured斗 identity and profile distinguish it from a generic contact block; no unified small-dou design claim.
- Known input: Top/bottom width and depth plus height, table 2-28/2-29.
- Unresolved: Exact 3D ear/cavity/profile and mortise geometry are not directly quantified; limit later Master to evidence-bounded medium LOD.; Observed means include compression/wear and are not 963 design dimensions; DG-114 remains UNKNOWN.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p65–66 / printed p50–51 tables 2-28 / 2-29.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: DG-108=255.2 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; DG-109=240.0 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_bottom_width=176.2 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_bottom_depth=165.1 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; measured_total_height=148.5 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `CMP-DOU-INTERACTIVE-001`; asset-contract readiness: `READY_WITH_BOUNDED_LOD`.

## CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿

- Identity: `lower_six_chuanfu`; real historical type: `True`; status: `MASTER_REQUIRED`.
- Context: 主体梁架下层通檐构架. P2 relationship: P1-derived identity; P2 PRIMARY_FRAME remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 UNR-PRIMARY-FRAME-001 (PRIMARY_FRAME) record is retained, not renamed or superseded.
- Decision: Independent lower six-rafter beam identity and observed section support a bounded parametric member type; P2 frame mesh is not inherited.
- Known input: Measured width 493.5 mm, tenon-area thickness 375 mm and maximum thickness 444 mm; verified frame-system topology.
- Unresolved: Member full length, camber, end profile and exact joinery are not verified as individual geometry.; Observed sections must not become fixed 963 design dimensions; length needs an explicit parameter.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p81 / printed p66 table 2-38.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: RF-001=复合式六椽栿通檐用两柱、彻上露明 [CONFIRMED, observed_current_topology, DIRECT_PRIMARY]; RF-002=493.5 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; RF-003=375 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; RF-004=444 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `CMP-FRAME-LOWER-SIX-CHUANFU-001`; asset-contract readiness: `READY_WITH_BOUNDED_LOD`.

## CMP-FRAME-UPPER-SIX-CHUANFU-001｜上六椽栿

- Identity: `upper_six_chuanfu`; real historical type: `True`; status: `MASTER_REQUIRED`.
- Context: 主体梁架上层通檐构架. P2 relationship: P1-derived identity; P2 PRIMARY_FRAME remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 UNR-PRIMARY-FRAME-001 (PRIMARY_FRAME) record is retained, not renamed or superseded.
- Decision: Independent upper six-rafter beam identity and distinct observed section support a bounded parametric member type; P2 frame mesh is not inherited.
- Known input: Measured width 334 mm, tenon-area thickness 209 mm and maximum thickness 240.5 mm; verified frame-system topology.
- Unresolved: Member full length, camber, end profile and exact joinery are not verified as individual geometry.; Observed sections must not become fixed 963 design dimensions; length needs an explicit parameter.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p81 / printed p66 table 2-38.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: RF-001=复合式六椽栿通檐用两柱、彻上露明 [CONFIRMED, observed_current_topology, DIRECT_PRIMARY]; RF-005=334 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; RF-006=209 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY]; RF-007=240.5 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY].
- Evidence gap / next source: None blocking current qualification / Later Master contract must preserve listed unknowns.
- Originality: `unknown`; future component ID: `CMP-FRAME-UPPER-SIX-CHUANFU-001`; asset-contract readiness: `READY_WITH_BOUNDED_LOD`.

## P1-REVIEW-COLUMN-HEAD-NIDAO-GONG｜柱头泥道栱

- Identity: `column_head_nidao_gong`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 BRACKET_ARM remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-JUMP-001 (BRACKET_ARM) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: Bridge paper cites measured length; original component profile, section and exact member mapping not directly verified.; HIS-002: individual 963 originality unknown.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=柱头泥道栱 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: Bridge paper cites measured length; original component profile, section and exact member mapping not directly verified. / Obtain direct original-page member-specific geometry and identity comparison resolving: Bridge paper cites measured length; original component profile, section and exact member mapping not directly verified..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-LARGE-MAN-GONG｜大型慢栱

- Identity: `large_man_gong`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 BRACKET_ARM remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-JUMP-001 (BRACKET_ARM) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: Bridge length and derived centre length are mixed; section and 3D profile not directly verified.; HIS-002: individual 963 originality unknown.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=大型慢栱 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: Bridge length and derived centre length are mixed; section and 3D profile not directly verified. / Obtain direct original-page member-specific geometry and identity comparison resolving: Bridge length and derived centre length are mixed; section and 3D profile not directly verified..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-HUA-GONG｜华栱

- Identity: `hua_gong`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 BRACKET_ARM remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-JUMP-001 (BRACKET_ARM) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: P1 bridge separates column-head/intercolumn jumps, but individual length, section and placement mapping remain mixed or inferred.; HIS-002: individual 963 originality unknown.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=华栱 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: P1 bridge separates column-head/intercolumn jumps, but individual length, section and placement mapping remain mixed or inferred. / Obtain direct original-page member-specific geometry and identity comparison resolving: P1 bridge separates column-head/intercolumn jumps, but individual length, section and placement mapping remain mixed or inferred..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-INTERCOLUMN-NIDAO-GUAZI-GONG｜补间泥道瓜子栱

- Identity: `intercolumn_nidao_guazi_gong`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 BRACKET_ARM remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-JUMP-001 (BRACKET_ARM) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: Bridge paper gives one length, but direct original-page profile, section and joint evidence are not established.; HIS-002: individual 963 originality unknown.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=补间泥道瓜子栱 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: Bridge paper gives one length, but direct original-page profile, section and joint evidence are not established. / Obtain direct original-page member-specific geometry and identity comparison resolving: Bridge paper gives one length, but direct original-page profile, section and joint evidence are not established..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-LOWER-ANG｜下昂

- Identity: `lower_ang`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 BRACKET_ARM remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-JUMP-001 (BRACKET_ARM) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: DG-112/113 describe a report-inferred triangle, not a full individual昂 geometry or 45° node.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p119–120 / printed p104–105 recommended conclusions.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: DG-112=47 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED]; DG-113=21 [HIGH_CONFIDENCE_INFERENCE, reconstructed_design_candidate, REPORT_INFERRED].
- Evidence gap / next source: DG-112/113 describe a report-inferred triangle, not a full individual昂 geometry or 45° node. / Obtain direct original-page member-specific geometry and identity comparison resolving: DG-112/113 describe a report-inferred triangle, not a full individual昂 geometry or 45° node..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-FOUR-CHUANFU｜四椽栿

- Identity: `four_chuanfu`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 PRIMARY_FRAME remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 UNR-PRIMARY-FRAME-001 (PRIMARY_FRAME) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: D-015 mentions deformation but approved direct review lacks a member-specific section and length.; HIS-002: individual 963 originality unknown.
- Source pages: PDF p131 / printed p116 deformation analysis; 四椽栿 mention only.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=四椽栿 [CONFIRMED, observed_as_measured, DIRECT_PRIMARY].
- Evidence gap / next source: D-015 mentions deformation but approved direct review lacks a member-specific section and length. / Obtain direct original-page member-specific geometry and identity comparison resolving: D-015 mentions deformation but approved direct review lacks a member-specific section and length..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-PING-LIANG｜平梁

- Identity: `ping_liang`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 PRIMARY_FRAME remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 UNR-PRIMARY-FRAME-001 (PRIMARY_FRAME) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: Structural position is described in secondary topology; member-specific section, length and joinery not directly verified.; HIS-002: individual 963 originality unknown.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_03.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=平梁 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: Structural position is described in secondary topology; member-specific section, length and joinery not directly verified. / Obtain direct original-page member-specific geometry and identity comparison resolving: Structural position is described in secondary topology; member-specific section, length and joinery not directly verified..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-TUO-JIAO｜托脚

- Identity: `tuo_jiao`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 FRAME_SUPPORT remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-FRAME-CONNECTOR-001 (FRAME_SUPPORT) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: Secondary/bridge discussion distinguishes bearing relationship, but the specific section, endpoints and angle are not verified.; HIS-002: individual 963 originality unknown.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_04.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=托脚 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: Secondary/bridge discussion distinguishes bearing relationship, but the specific section, endpoints and angle are not verified. / Obtain direct original-page member-specific geometry and identity comparison resolving: Secondary/bridge discussion distinguishes bearing relationship, but the specific section, endpoints and angle are not verified..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-LAN-E｜阑额

- Identity: `lan_e`; real historical type: `True`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 PRIMARY_FRAME remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 UNR-PRIMARY-FRAME-001 (PRIMARY_FRAME) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: Term and column-between role are present in secondary evidence, but independent geometry and mapping are absent.; HIS-002: individual 963 originality unknown.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_03.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=阑额 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: Term and column-between role are present in secondary evidence, but independent geometry and mapping are absent. / Obtain direct original-page member-specific geometry and identity comparison resolving: Term and column-between role are present in secondary evidence, but independent geometry and mapping are absent..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## P1-REVIEW-INTERCOLUMN-SEATED-DOU｜补间坐斗

- Identity: `intercolumn_seated_dou`; real historical type: `None`; status: `DEFERRED_INSUFFICIENT_EVIDENCE`.
- Context: P1 package named member; precise position requires source drawing. P2 relationship: P1-derived identity; P2 BRACKET_CONTACT remains an unchanged aggregate/proxy.
- Derivation: DERIVED_FROM_P1_EVIDENCE; related P3.0 PRX-BRACKET-CONTACT-001 (BRACKET_CONTACT) record is retained, not renamed or superseded.
- Decision: Historical component term merits review, but source grade or member geometry does not meet Master threshold.
- Known input: A type/position mention only; no P2 mesh is adopted as member geometry.
- Unresolved: Bridge measurement is mentioned, but equivalence to directly verified 底斗 or another named斗 is unproved; independent profile and location need direct verification.; HIS-002: individual 963 originality unknown.; E-022 shares the reported top/bottom widths of 底斗; identity equivalence or distinction is unproved.
- Source pages: No direct member page established.
- Source references: docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md, docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md, docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md.
- Attribute evidence: identity_mention=补间坐斗 [HIGH_CONFIDENCE_INFERENCE, source_mention_only, A_BRIDGE_OR_SECONDARY].
- Evidence gap / next source: Bridge measurement is mentioned, but equivalence to directly verified 底斗 or another named斗 is unproved; independent profile and location need direct verification. / Obtain direct original-page member-specific geometry and identity comparison resolving: Bridge measurement is mentioned, but equivalence to directly verified 底斗 or another named斗 is unproved; independent profile and location need direct verification. Compare E-022 and D-008 original labels/positions before a separate type ID..
- Originality: `unknown`; future component ID: `None`; asset-contract readiness: `NOT_READY`.

## Explicit future evidence requests

For every deferred record, the `evidence_gap` in JSON is the specific blocker. Obtain directly attributable member drawings/tables or a formally reviewed bridge before changing its status. Do not upgrade evidence classification by naming alone.
45° corner placement, exact mortise, hidden angle-beam identification, DG-114 and HIS-002 remain unresolved. No P3.0 Registry record is overwritten.
