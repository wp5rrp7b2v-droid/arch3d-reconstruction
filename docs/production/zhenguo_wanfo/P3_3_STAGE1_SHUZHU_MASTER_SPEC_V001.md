# P3.3 Stage1 蜀柱 Master Spec V001

Status: **LOCKED / PRODUCT OWNER DELEGATED END-TO-END AUTHORIZATION / D-115**

## 1. Master identity

- component_id: `CMP-FRAME-SHUZHU-001`
- master_id: `CMP-FRAME-SHUZHU-001_MASTER`
- master_version: `V001`
- physical instances: 4
- INTERIOR_FRAME: 2
- GABLE_FRAME: 2
- Geometry Variant count: 0

## 2. Canonical body

Stage1 canonical specimen:
- reference length: 1000 mm
- width: 218.75 mm
- thickness: 157.5 mm
- body: straight constant rectangular bounding-envelope timber
- profile state: exact historical profile UNKNOWN
- end state: simplified planar structural ends

The 1000 mm length is `RECONSTRUCTION_REFERENCE_LENGTH` only and is not a historical or building-instance height.

## 3. Evidence basis

A1:
- PDF p90-91 / printed p75-76 / §2.3.1.9 / Table 2-46
- published/recomputed mean = 218.75 × 157.5 mm
- both gable thickness records (东山 / 西山) = 未及
- no source-internal numeric conflict detected

A2:
- official same-building statement places 蜀柱 above 平梁 with 驼峰 and 叉手

V008:
- 4 instances locked derived by measured-position + drawing closure

## 4. Placement / endpoint rule

Actual building instance:
- `P_lower` = Pingliang upper support/connection region
- `P_upper` = ridge-support lower connection region
- `V = P_upper - P_lower`
- `L = ||V||`
- `P_center = (P_upper + P_lower)/2`
- local longitudinal axis aligns to `V`

Stage1 does not lock final four building XYZ coordinates.

Expected role:
- vertical support
- exact historical height metadata may remain UNKNOWN
- production height may be RECONSTRUCTED_DESIGN derived from later locked assembly endpoints

## 5. Variant policy

One shared Master is used for all four instances.

Do **not** create a Geometry Variant for:
- 东缝 vs 西缝
- 东山 vs 西山
- INTERIOR_FRAME vs GABLE_FRAME
- different endpoint-derived height
- the two gable `未及` thickness records

A future Variant requires a stable repeated body-geometry difference supported by evidence.

## 6. Joinery / end treatment

Stage1:
- `STRUCTURAL_SIMPLIFIED_FLAT_END`
- mortise/tenon/notch/groove = not modeled unless directly supported later
- historical-original end treatment remains metadata UNKNOWN

## 7. Review Board

Required panels:
1. AXON
2. LONG_SIDE
3. END_SECTION
4. DIMENSION_AND_PARAMETRIC_LENGTH
5. PLACEMENT_AND_ENDPOINT_LOGIC
6. SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY

The placement panel must show two vertical endpoint fixtures with different lengths using the same Master and section.

## 8. Acceptance

Must machine-verify:
- 4 Registry instances
- 2+2 role split
- section 218.75 × 157.5 mm
- source numeric conflict FALSE
- reference length non-historical
- endpoint-derived length/center/direction
- same-direction vertical fixtures allowed by generic Definition-driven endpoint policy
- no reference-length leakage
- no false Geometry Variant
- no unsupported joinery claim
- shared Master V2 regressions remain PASS

The Product Owner's instruction to complete 蜀柱 end-to-end delegates conditional execution, first-article acceptance, formalization and merge to ChatGPT **only when all locked evidence, visual, machine and regression gates PASS**. A failed hard gate is not pre-approved.
