# P3.3 Stage1｜华栱 Source Readiness + Visual/Form Evidence Review V001

Status: **REVIEW COMPLETE / PASS WITH EXPLICIT EVIDENCE BOUNDARIES / MASTER SPEC NEXT / NO ENGINEERING T-TASK**

Date: 2026-09-27
Target: 华栱 / V008 正身方向明确子集 56 Registry records
Coverage Matrix priority: 18
Primary source authority: SRC-ZG-WF-001｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》
Primary source SHA-256: `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`
Primary source bytes: 84,117,628

## 1. Registry / scope boundary

V008 contains **56** 华栱 records, all within the explicitly locked 正身方向子集:

- 南：一跳 7 + 二跳 7
- 北：一跳 7 + 二跳 7
- 东：一跳 7 + 二跳 7
- 西：一跳 7 + 二跳 7
- total：**28 一跳 + 28 二跳 = 56**

All 56 records are:
- `count_status = LOCKED_SUBSET`
- `stage1_disposition = 需新建Master`
- `master_coverage_status = MASTER_REQUIRED_PENDING`
- scope = `正身方向明确子集，不是全殿华栱总数`

Coverage Matrix:
- component = 华栱
- records = 56
- family = 华栱
- priority = 18
- action = `56件为正身方向明确子集；Master可建但不得称全殿总数闭合`

Hard boundary:
**56 is not the historical total count of all 华栱 in the hall.**
Any future Master/Catalog wording must preserve the subset qualification.

## 2. Direct primary evidence｜第一、二跳总出跳

SRC-ZG-WF-001 PDF p71 / printed p56 / §2.2.4.2 / Fig.2-25 / Table 2-33 directly records the combined first+second jump projection from the 3D laser-scan dougong dataset:

- observed mean = **732.4 mm**
- minimum = **704 mm**
- maximum = **755 mm**
- variance = **115.61**
- sample count = **n=46**

Classification:
- **DIRECT_PRIMARY / OBSERVED_MEAN**
- measurement object = **第一、二跳总出跳**
- assembly-level combined projection statistic
- **not** a standalone 一跳华栱 full length
- **not** a standalone 二跳华栱 full length
- **not** per-instance exact geometry
- **not** proven 963 original design
- report sample n=46 does **not** map one-to-one to the 56 Registry records
- `sample_to_instance_mapping = UNKNOWN`

This statistic may constrain later assembly geometry, but it cannot by itself define either individual 华栱 member length.

## 3. Report design synthesis｜48分 rule

SRC-ZG-WF-001 PDF p72 / printed p57 / §2.2.4.4 / Table 2-35 converts the measured/synthesized dougong dimensions into a modular design interpretation.

Relevant report values:
- material thickness observed/synthesized band = **154.0–156.9 mm**
- single-material width band = **214.1–218.9 mm**
- first+second total projection = **732.4 mm**
- report-adjusted first+second total projection = **48分**
- report adopts 营造尺 = **306 mm**
- in the report's synthesis, 1分 = 0.5寸 = **15.3 mm**

SRC-ZG-WF-001 PDF p120 / printed p105 repeats the recommended report conclusion:
- outer-eaves dougong uses material thickness as 10分 baseline;
- single-material width tends toward 14分;
- 第一、二跳总出跳 = **48分**;
- 第三、四跳总出跳 = 47分.

Classification for Stage1:
- **REPORT_INFERRED / REPORT_IDEAL_MODEL**
- useful as a replaceable reconstruction/design constraint
- must not be relabeled as direct measured standalone 华栱 dimensions
- must not be upgraded to 963-original fact

## 4. Individual 华栱 length evidence boundary

The primary report reviewed in this gate does **not** directly provide a standalone measured full length for:
- 一跳华栱;
- 二跳华栱.

Existing P1 bridge evidence records later/calculated values:
- 柱头二跳华栱 full length ≈ **1630 mm**
- 柱头二跳华栱 centre length ≈ **1464.8 mm**
- 补间二跳华栱 is similarly reconstructed/calculated;
- 补间一跳华栱 length is explicitly noted as not directly provided by the report and later values are hypothesis/completion.

Therefore:
- 1630 / 1464.8 must remain **SECONDARY_CALCULATED / REPORT-DERIVED-LATER**, not DIRECT_PRIMARY;
- no first-jump full length may be silently fabricated;
- no equality of 一跳 and 二跳 full lengths may be assumed;
- no one-to-one member length assignment may be inferred from the 732.4 mm combined projection.

A future Master Spec must explicitly decide how to represent this unresolved individual-length problem before engineering execution.

## 5. Visual / form evidence

Same-building primary evidence is adequate for D-076 form review:

- PDF p73 / printed p58 / Fig.2-27 contains a 万佛殿外檐铺作现场 photograph plus a same-building schematic of the bracket stack and out-jump relationships.
- The figure makes the layered horizontal/forward bracket members, outer-eaves dougong context and relationship to 下昂/正交构件 directly readable.
- PDF p72–73 discussion states that the report uses same-building 3D laser-scan point-cloud relationships to analyze outer-eaves bracket connections.

This supports:
- component identity = 华栱 / forward-projecting dougong arm member;
- first/second jump as distinct assembly positions;
- same-building outer-eaves bracket-set context;
- broad orientation and relation to adjacent dougong members;
- use of the combined first+second projection as an assembly constraint.

It does **not** establish:
- exact standalone historical side profile;
- exact one-jump / two-jump full lengths;
- exact numeric profile-control points;
- exact end shaping;
- exact hidden overlap lengths;
- grooves / slots / cavities;
- mortise-tenon or hidden connection cuts;
- per-location geometric differences among the 56 Registry records.

Comparative examples in the report from 佛光寺东大殿、独乐寺观音阁、应县木塔、高平崇明寺 are **comparative context only** and shall not be copied as Wanfo Hall geometry authority.

## 6. Family / variant questions for Master Spec V0.1

Source Readiness supports a 华栱 Master design study, but does **not** pre-decide the final Master/variant architecture.

Facts that must be preserved:
- Registry target = 56 explicit subset records;
- one-jump records = 28;
- two-jump records = 28;
- direction/location are assembly semantics, not automatically geometry variants;
- exact one-jump and two-jump standalone lengths are unresolved;
- combined first+second projection has direct observed constraint 732.4 mm mean;
- report ideal-model constraint = 48分 total;
- exact standalone profile remains unresolved.

Master Spec V0.1 must explicitly evaluate at least:
1. one shared parametric 华栱 family with jump-specific geometry parameters; versus
2. two explicit geometry variants (JUMP_1 / JUMP_2).

It must **not** lock either solution merely because V008 contains 一跳/二跳 labels.

## 7. Required pre-engineering gates implied by this evidence

Because individual member length and exact standalone profile are not directly closed, a future engineering contract shall require separate deterministic controls before Blender execution:

- **LENGTH / ASSEMBLY CONTROL SET**:
  - documents how individual member length is reconstructed from the same-building assembly evidence;
  - preserves the 732.4 mm combined observed constraint;
  - classifies every non-direct length as reconstructed / replaceable;
  - does not claim per-instance exactness.

- **PROFILE CONTROL SET**:
  - same-building source-guided;
  - deterministic/versioned/reproducible;
  - explicitly **NOT_DIRECT_MEASUREMENT**;
  - replaceable if stronger evidence appears.

Neither control set is authorized or designed by D-225.

## 8. Prohibited substitutions

The next stages must not:
- copy T-037 瓜子栱 profile controls as authority;
- copy T-038 慢栱 profile controls as authority;
- copy T-039 令栱 profile controls as authority;
- average/morph prior gong controls to create 华栱;
- substitute a generic Song / 《营造法式》 template as direct Wanfo evidence;
- copy 佛光寺 / 独乐寺 / 应县木塔 / 崇明寺 comparative geometry into Wanfo Hall;
- treat 48分 as a directly measured standalone member length;
- invent the first-jump member length;
- claim the 56-record subset is the whole-hall total;
- invent hidden joinery to make the model convenient.

## 9. Unresolved / deferred

- historical whole-hall 华栱 total count = **NOT CLOSED**
- one-jump standalone full length = **UNRESOLVED**
- two-jump standalone direct-measured full length = **UNRESOLVED**
- later/calculated two-jump 1630 mm value = **SECONDARY_CALCULATED / REPLACEABLE**
- one/two-jump sample-to-instance mapping = **UNKNOWN**
- exact standalone historical profile = **UNRESOLVED**
- exact numeric profile controls = **UNRESOLVED**
- exact end geometry / hidden overlap = **UNRESOLVED**
- mortise-tenon / grooves / slots / cavities / hidden cuts = **DEFERRED**
- per-instance 963 originality/repair state = **UNKNOWN**
- observed 732.4 mm mean as 963 original design = **NOT ESTABLISHED**

## 10. Review result

**SOURCE READINESS = PASS WITH BOUNDARIES**

**D-076 VISUAL/FORM GATE = PASS WITH BOUNDARIES**

Evidence is sufficient to proceed to:

**华栱 Master Spec V0.1 design**

The next Master Spec must preserve the unresolved individual-length problem and may not authorize Blender by itself.

D-225 does **not** authorize:
- Master Spec approval / lock;
- engineering T-task creation;
- branch / PR creation;
- Length/Assembly Control Set adoption;
- Profile Control Set adoption;
- Blender execution;
- first article;
- formalization;
- Catalog/V008 binding;
- Stage2;
- T-018 resume.
