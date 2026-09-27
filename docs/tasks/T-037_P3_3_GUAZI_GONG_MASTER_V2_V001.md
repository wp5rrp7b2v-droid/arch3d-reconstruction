# 中国古建筑3D复原｜T-037｜P3_3_GUAZI_GONG_MASTER_V2_V001

Status: **POST-FORMALIZATION VERIFICATION PASS D-191 / PR #33 READY FOR PO PR-READY DECISION / PR STILL DRAFT / MERGE NOT AUTHORIZED**
Stage: P3.3 V002 Stage 1
Branch: codex/t037-p3-3-guazi-gong-master-v2-v001

## 1. Objective

Build and validate one reusable瓜子栱 Master family with two canonical geometry variants:
- LARGE_GUAZI_GONG: 16 physical records
- SMALL_GUAZI_GONG: 28 physical records

Total = 44 Registry records.

## 2. Identity

Family component id: CMP-GONG-GUAZI-001
Master id: CMP-GONG-GUAZI-001_MASTER
Master version: V001

Registry source component names remain:
- 大型瓜子栱
- 小型瓜子栱

The family identity is a Stage1 Master-family identity. It does not erase the two source component labels.

## 3. Dimension contract

LARGE:
- L = 1007.0 mm / OBSERVED_MEAN / n=16
- W = 214.7 mm / FAMILY OBSERVED_MEAN / n=44
- T = 156.5 mm / FAMILY OBSERVED_MEAN / n=16

SMALL:
- L = 895.0 mm / OBSERVED_MEAN / n=28
- W = 214.7 mm / FAMILY OBSERVED_MEAN / n=44
- T = 156.5 mm / FAMILY OBSERVED_MEAN / n=16

Means must not be rewritten as per-instance exact values or proven 963 original-design dimensions.

## 4. Profile contract

PROFILE_AUTHORITY = SOURCE_DERIVED_PROFILE.

The builder must use a deterministic normalized profile declared in the locked Definition. The points are reconstructed controls derived from same-building form evidence, not direct measured curve coordinates.

Hard boundary:
- exact historical curve = UNRESOLVED
- no generic Song-template substitution
- no aesthetic free-form adjustment
- no unsupported joinery/detail

## 5. Variant contract

One Master family, two geometry variants.

Forbidden:
- SMALL produced by uniform global scale from LARGE
- width/thickness scaled by 895/1007
- location-specific Master duplication

Required:
- same normalized profile rule
- variant-specific length
- shared canonical width and thickness representative means
- separate variant semantic signatures

## 6. First article

First article contains exactly two canonical variant bodies:
- LARGE
- SMALL

No 44-instance assembly is produced before Product Owner first-article approval.

## 7. Review evidence

Required Review Board domains:
1. LARGE axon
2. SMALL axon
3. LARGE front/profile
4. SMALL front/profile
5. LARGE vs SMALL overlay
6. dimension proof
7. source-derived profile provenance
8. evidence classification / unknown boundary

## 8. Validation domains

Validate:
- 44 = 16 large + 28 small
- V008 registry identity and dimensions
- one Master family / two variants
- LARGE length 1007
- SMALL length 895
- width 214.7
- thickness 156.5
- source-derived profile classification
- normalized profile symmetry and deterministic signature
- exact historical control dimensions remain unresolved
- no uniform-scale implementation
- manifold closed mesh
- no self-intersection by simple polygon contract
- Blender 4.5.13
- deterministic reopen
- canonical binary SHA
- no tracked .blend

## 9. Hard fails

- GUAZI_FAMILY_COUNT_NOT_44
- LARGE_COUNT_NOT_16
- SMALL_COUNT_NOT_28
- LARGE_LENGTH_NOT_1007
- SMALL_LENGTH_NOT_895
- WIDTH_MEAN_LOST
- THICKNESS_MEAN_LOST
- WIDTH_MEAN_MARKED_PER_INSTANCE_DIRECT
- THICKNESS_MEAN_MARKED_44_INSTANCE_DIRECT
- OBSERVED_MEAN_MARKED_ORIGINAL_DESIGN
- SMALL_CREATED_BY_UNIFORM_SCALE
- UNSUPPORTED_PROFILE_INVENTION
- PROFILE_SOURCE_NOT_RECORDED
- PROFILE_DERIVATION_NOT_REPRODUCIBLE
- UNSUPPORTED_JOINERY_MODELED
- LOCATION_CREATES_FALSE_VARIANT
- DUPLICATE_MASTER_PER_INSTANCE
- SILENT_HISTORICIZATION
- MODEL_BEFORE_EXECUTION_AUTHORIZATION

## 10. Scope protection

T-037 must not:
- reactivate T-018 / PR #3 / PR #6
- start Stage2
- modify T-020 datum authority
- rewrite A1/report direct evidence
- broaden into complete bracket-set assembly
- formalize Catalog/V008 binding before Product Owner first-article approval

## 11. Authorization

D-183 authorizes:
- production branch
- Draft PR
- locked execution Definition
- T-037 isolated builder/validator/workflow
- Blender 4.5.13 first article
- machine validation and Review Board generation

Not authorized:
- first-article acceptance
- formalization
- Catalog/V008 binding
- PR Ready/merge
- closure
- Stage2
- T-018 resume

## 12. First Article Approval

D-185 Product Owner approval recorded 2026-09-27.

Accepted:
- LARGE_GUAZI_GONG first article
- SMALL_GUAZI_GONG first article
- repaired Review Board / Run 36290968633

Evidence boundary retained:
- W 214.7mm = family observed mean / n=44
- T 156.5mm = observed sample mean / n=16 / subgroup attribution UNRESOLVED
- exact historical profile curve = UNRESOLVED
- normalized profile controls = SOURCE_DERIVED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT
- grooves / mortise-tenon / cavities / local connection cuts = DEFERRED

Traceability Review Patch D-186 completed:
- thickness 156.5mm = OBSERVED_SAMPLE_MEAN / n=16 / subgroup attribution UNRESOLVED;
- applying 156.5mm to LARGE and SMALL is Stage1 production-family application, not variant-specific direct observation;
- the current profile is reproducible from the locked 13-point Definition control set;
- no metric pixel-to-mm calibration or independently reproducible source-image re-extraction is claimed;
- PDF p73 Fig 2-27 and p76 Fig 2-31 remain qualitative same-building form/envelope authority;
- exact historical curve/control dimensions remain UNRESOLVED and the control set remains REPLACEABLE.

D-185/D-186 do not authorize formalization, Catalog/V008 binding, PR Ready/merge, closure, Stage2, or T-018 resume.

## 13. Post-Traceability Regression

D-187 records Run 36292530436 = SUCCESS / 43/43 PASS. LARGE and SMALL semantic geometry signatures exactly match the D-185 accepted first article, confirming D-186 changed traceability metadata only and did not change geometry. Formalization/Catalog-V008 binding/PR Ready/merge remain separately gated.

## 14. Formalization Authorization

D-188 authorizes formal materialization and Stage1 Catalog/V008 binding only. Derived Excel sync, PR Ready/merge, closure, Stage2 and T-018 resume remain outside this authorization.

## 15. Formalization Result

D-189 records successful formalization under D-188. Catalog branch count = 21/28; 44/44 guazi V008/CURRENT rows are bound to CMP-GONG-GUAZI-001_MASTER; CURRENT==V008. Approved canonical blend remains D-185 SHA 932571bcbff0c3f166dd5c449a35a96a618876ad8986d0dacbb668f9a510048a. Derived Excel sync, PR Ready/merge and closure remain separate gates.

## 16. Post-Formalization Verification Authorization

D-190 authorizes derived Excel synchronization, latest-head T-037 regression, and PR #33 readiness review. PR Ready transition, merge/closure, Stage2 and T-018 resume remain separately gated.

## 17. Post-Formalization Verification Result

D-191 records completion of D-190: derived Excel validation PASS, latest-head T-037 regression PASS 43/43 with exact LARGE/SMALL geometry-signature match to D-185, shared T-021/T-022/T-023/T-024 regressions PASS, and PR #33 readiness review PASS. PR #33 remains Draft; Ready transition, merge and closure require separate Product Owner authorization.
