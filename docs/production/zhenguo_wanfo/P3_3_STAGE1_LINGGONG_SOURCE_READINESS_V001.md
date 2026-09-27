# P3.3 Stage1｜令栱 Source Readiness + Visual/Form Evidence Review V001

Status: **REVIEW COMPLETE / PASS WITH EXPLICIT EVIDENCE BOUNDARIES / MASTER SPEC NEXT / ENGINEERING NOT AUTHORIZED**

Date: 2026-09-27
Target: 令栱 / 28 Registry records
Coverage Matrix priority: 17
Primary source authority: SRC-ZG-WF-001｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》
Secondary same-building authority: 山西文物数字博物馆｜镇国寺·万佛殿专题

## 1. Registry / coverage boundary

V008 currently contains **28** physical 令栱 records:
- 7 south-facing
- 7 north-facing
- 7 east-facing
- 7 west-facing

All 28 records are:
- count_status = `LOCKED_DERIVED`
- stage1_disposition = `需新建Master`
- master_coverage_status = `MASTER_REQUIRED_PENDING`

Coverage Matrix:
- component = 令栱
- records = 28
- family = 栱
- priority = 17
- action = 28件；尺寸已锁

The 28-record physical count is a Registry/topology result. It must **not** be justified merely by the report sample count, even though the report also contains n=28 measurement series.

## 2. Direct width evidence

SRC-ZG-WF-001 PDF p55 / printed p40 / §2.2.1.5 栱广:
- 令栱广 observed mean = **217.4 mm**
- minimum = **208 mm**
- maximum = **228 mm**
- sample count = **n=28**
- source table = **Table 2-14**

Classification:
- **DIRECT_PRIMARY / OBSERVED_MEAN**
- family-level observed statistic
- not per-instance exact width
- not proven 963 original design dimension

## 3. Direct thickness evidence

SRC-ZG-WF-001 PDF p57 / printed p42 / §2.2.1.6 栱厚:
- 令栱厚 observed mean = **155.6 mm**
- minimum = **150 mm**
- maximum = **165 mm**
- sample count = **n=28**
- source table = **Table 2-17**

Classification:
- **DIRECT_PRIMARY / OBSERVED_MEAN**
- family-level observed statistic
- not per-instance exact thickness
- not proven 963 original design dimension

## 4. Direct length evidence

SRC-ZG-WF-001 PDF p60–61 / printed p45–46 / §2.2.2.3 令栱:
- 令栱长 observed mean = **897 mm**
- minimum = **860 mm**
- maximum = **925.6 mm**
- sample count = **n=28**
- distribution = Fig. 2-16
- source table = **Table 2-24**

Classification:
- **DIRECT_PRIMARY / OBSERVED_MEAN**
- family-level observed statistic
- not per-instance exact length
- not proven 963 original design dimension

Any report-side design conversion / modular analysis after the observed statistics must remain **REPORT_INFERRED** and must not overwrite these direct observed statistics.

## 5. Visual / form evidence

The primary report directly places 令栱 within the outer-eaves dougong system and supplies same-building bracket-set measurement context. The official 山西文物数字博物馆 万佛殿专题 independently confirms the same building's:
- 柱头铺作 / 补间铺作 / 转角铺作 system context;
- 柱头七铺作双杪双下昂;
- 补间五铺作双杪偷心造;
- same-building photographic / structural context.

This is sufficient at D-076 level to support:
- component identity = 令栱;
- horizontal gong-member family context;
- outer-eaves bracket-set placement context;
- broad relationship to adjacent dougong members.

It is **not** sufficient to establish:
- exact standalone historical profile curve;
- numeric profile control points;
- exact end shaping;
- grooves / slots / cavities;
- mortise-tenon or hidden connection cuts;
- per-location geometric differences.

## 6. Family / variant boundary for next Master Spec

Evidence currently supports:
- one 令栱 component family candidate;
- 28 Registry records;
- one shared observed family envelope candidate: **897 × 217.4 × 155.6 mm** using observed means;
- no evidence at this gate requiring per-location Master duplication;
- no evidence at this gate requiring multiple length variants.

These are **Source Readiness findings only**. Master family ID, exact geometry architecture, profile-control method and final variant count remain for Master Spec V0.1.

The next Master Spec must not:
- reuse T-037 瓜子栱 profile control points by inheritance;
- reuse T-038 慢栱 profile control points by inheritance;
- substitute a generic Song/Yingzao Fashi template as if it were direct Wanfo evidence;
- invent joinery or local cuts to make modeling easier.

## 7. Unresolved / deferred

- exact historical standalone 令栱 profile = **UNRESOLVED**
- numeric profile controls = **UNRESOLVED**
- per-instance dimensional mapping = **UNKNOWN**
- end geometry / local shaping = **UNRESOLVED**
- mortise-tenon / grooves / slots / cavities / hidden cuts = **DEFERRED**
- 963 original-design attribution of observed means = **NOT ESTABLISHED**

Any reconstruction control introduced later must be explicitly classified, versioned and replaceable.

## 8. Review result

**SOURCE READINESS = PASS WITH BOUNDARIES**

**D-076 VISUAL/FORM GATE = PASS WITH BOUNDARIES**

The evidence is sufficient to proceed to:

**令栱 Master Spec V0.1 design**

This result does **not** authorize:
- Master Spec approval / lock;
- engineering T-task creation;
- branch / PR creation;
- Blender execution;
- first article;
- formalization;
- Catalog/V008 binding;
- Stage2;
- T-018 resume.
