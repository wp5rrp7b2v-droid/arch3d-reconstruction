# P3.3 Stage1｜瓜子栱族 Master Spec V001

Status: **LOCKED / PRODUCT OWNER APPROVED / D-181**
Date: 2026-09-27
Stage: P3.3 V002 Stage 1

## 1. Scope

One shared Master family covers:
- 大型瓜子栱: 16
- 小型瓜子栱: 28
- total Registry records: 44

Architecture:
- one reusable Master family
- two geometry variants: LARGE_GUAZI_GONG / SMALL_GUAZI_GONG
- no per-location Master duplication

## 2. Primary source

SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》
Canonical PDF SHA-256:
94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472

Direct measurement bindings:
- PDF p54 / Table 2-12: 瓜子栱广 mean 214.7 mm, n=44
- PDF p56 / Table 2-16: 瓜子栱厚 mean 156.5 mm, n=16
- PDF p58 / Table 2-20: 大型瓜子栱 length mean 1007 mm, n=16
- PDF p58 / Table 2-20: 小型瓜子栱 length mean 895 mm, n=28
- PDF p59 / Table 2-21: design-value analysis is retained as report analysis and is not substituted for the measured means above
- PDF p73-76 / Fig. 2-27..2-31: same-building bracket-set visual/form evidence

## 3. Locked dimensions

LARGE_GUAZI_GONG:
- length = 1007.0 mm / OBSERVED_MEAN / n=16
- width = 214.7 mm / FAMILY_OBSERVED_MEAN / n=44
- thickness = 156.5 mm / OBSERVED_SAMPLE_MEAN / n=16 / subgroup attribution = UNRESOLVED

SMALL_GUAZI_GONG:
- length = 895.0 mm / OBSERVED_MEAN / n=28
- width = 214.7 mm / FAMILY_OBSERVED_MEAN / n=44
- thickness = 156.5 mm / OBSERVED_SAMPLE_MEAN / n=16 / subgroup attribution = UNRESOLVED

The width mean is a family-level observed mean (n=44). The thickness value is an observed sample mean (n=16), but the report excerpt does not resolve whether those 16 samples belong to LARGE, SMALL, or a mixed subset; therefore subgroup attribution is explicitly UNRESOLVED. Applying 156.5 mm to both geometry variants is a Stage1 production-family application, not a claim that each variant was separately measured at 156.5 mm. None of these means are 44 per-instance exact measurements or proven 963 original-design dimensions.

## 4. Profile authority

PROFILE_AUTHORITY = SOURCE_DERIVED_PROFILE

The Stage1 profile is recovered from same-building bracket-set drawings after D-076 Product Owner visual/form review.

Locked semantic boundary:
- exact historical curve/control-point dimensions = UNRESOLVED
- normalized profile points are deterministic Stage1 reconstruction controls
- normalized points are NOT direct measurements
- current 13-point control set is locked numerically in the Definition and is therefore reproducible from the Definition
- source-image re-extraction is NOT claimed to reproduce the same numeric points; no metric pixel-to-mm calibration was performed or claimed
- source role = same-building qualitative form/envelope authority (PDF p73 Fig 2-27; p76 Fig 2-31)
- construction rule = bilateral symmetric normalized envelope; X normalized by each variant length, Z normalized by representative thickness, then extruded across representative width
- normalized profile is REPLACEABLE if stronger direct or metrically calibrated evidence appears
- no generic Song-template profile may silently replace the same-building evidence basis

## 5. Variant rule

Allowed sharing:
- topology
- profile derivation rule
- coordinate system
- builder/validator logic
- evidence schema

Forbidden:
- SMALL = uniform_scale(LARGE, 895/1007)
- width or thickness scaling with length
- location-driven geometry variants

## 6. Unsupported / deferred detail

Deferred:
- exact mortise-tenon geometry
- hidden slots/cavities
- exact roll-cut or local curvature controls
- wear, damage, warp and per-instance deformation
- unmeasured micro-chamfers

These remain UNRESOLVED / DEFERRED and must not be invented in Stage1.

## 7. Gate lineage

D-180: Source Readiness + D-076 PASS
D-181: Master Spec V001 LOCKED
D-182: T-037 Task Contract LOCKED
D-183: T-037 Engineering Execution AUTHORIZED
D-185: T-037 First Article PRODUCT OWNER APPROVED
D-186: Traceability Review Patch AUTHORIZED + COMPLETED

T-018 remains HOLD. Stage2 remains NOT AUTHORIZED.
