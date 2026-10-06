# MP-01A Gate D｜First Assembly Engineering Build V001

Status: **PRODUCT OWNER AUTHORIZED / ENGINEERING EXECUTION ACTIVE**
Date: 2026-10-06
Branch: `assembly/mp01-east-seam-core-frame-v001`
PR: #56

## 1. Authorization

Product Owner instruction:

> 完成Gate-D

This authorizes:
- Blender execution for the MP-01A first assembly;
- deterministic rebuild/reopen checks;
- Review Board generation;
- machine validation;
- Actions Artifact generation.

It does not authorize:
- claiming historical joinery;
- changing Gate C evidence classes;
- merging PR #56;
- extending PASS beyond MP-01A;
- treating MP-01B / Linggong as resolved.

## 2. Locked input

Authoritative numeric contract:

`production/zhenguo_wanfo/assembly/MP01A_GATE_C_ASSEMBLY_LOCAL_NUMERIC_PLACEMENT_V001.json`

Assembly objects:

1. `平梁-东缝`
2. `ASM-MP01A-TUOFENG-UPPER-01`
3. `蜀柱-东缝`
4. `叉手-东缝-南侧`
5. `叉手-东缝-北侧`

Control-only:
- `DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM`
- ridge-purlin reference level Z=1245 mm

## 3. Geometry implementation

### Pingliang
- rectangular bounded outer envelope only;
- dimensions from Gate C;
- long axis aligned to assembly Y;
- top plane Z=0;
- historical full length remains UNKNOWN.

### Tuofeng Upper
- preserve approved `UPPER_RIDGE_SUPPORT` normalized stepped-hump topology;
- scale to Gate C assembly-owned envelope;
- no historical metric claim.

### Shuzhu
- rectangular bounded section envelope;
- longitudinal axis = endpoint vector;
- Gate C endpoints drive length;
- no Stage1 reference length leakage.

### Chashou pair
- rectangular bounded section envelopes;
- longitudinal axes = endpoint vectors;
- mirrored endpoint solution;
- no fixed historical angle claim.

## 4. Relationship boundary

Allowed:
- LOCATE
- SUPPORT
- CONTACT_REGION
- ENDPOINT_TARGET

Not allowed:
- exact historical mortise/tenon topology;
- exact contact-face geometry;
- inferred hidden cuts.

## 5. Review outputs

Required:
1. front elevation;
2. axonometric assembly;
3. object/instance provenance;
4. relation/evidence table;
5. numeric placement summary;
6. UNKNOWN / reconstruction boundary.

## 6. Machine PASS

Gate D PASS requires:

1. exactly five physical/reconstructed assembly bodies;
2. four V008 physical instance identities preserved;
3. Tuofeng remains reconstructed assembly instance with no whole-hall count claim;
4. Pingliang dimensions match Gate C;
5. Tuofeng envelope matches Gate C;
6. Shuzhu endpoints and length match Gate C;
7. Chashou endpoints, mirror symmetry, lengths and angles match Gate C;
8. no historical metric claim on reconstructed values;
9. hidden joinery remains UNKNOWN / no joinery geometry;
10. independent reopen reproduces geometry signatures;
11. clean deterministic rebuild reproduces semantic geometry signatures;
12. a +50 mm ridge-target perturbation changes Shuzhu/Chashou derived values but leaves Pingliang/Tuofeng inputs unchanged;
13. Review Board produced and non-empty.

## 7. PASS scope

A PASS proves only:

> the MP-01A upper ridge-support subset can be deterministically generated as a provenance-rich assembly from explicit Master identities + evidence-classified assembly inputs.

It does not prove:
- historical exactness;
- whole-frame completeness;
- MP-01B;
- whole-hall scalability;
- structural safety.
