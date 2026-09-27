# P3.3 Stage1｜T-040 华栱 Profile Control Set V0.1

Status: **LOCKED / PRODUCT OWNER APPROVED / D-233**
Date: 2026-09-27
Task: `T-040｜P3_3_HUAGONG_MASTER_V2_V001`
Task Contract: **LOCKED / D-229**
Gate A Length/Assembly Control: **LOCKED / D-231**
Control-set candidate id: `HUAGONG_PROFILE_CONTROL_SET_V001_C01`

## 1. Purpose

This Gate B Candidate supplies a deterministic Stage1 profile-control method for the two 华栱 reference variants after Gate A fixed their reference lengths, section and assembly-control semantics.

It does **not** claim recovery of the exact historical 华栱 side profile.

Classification:

`SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`

## 2. Source role and evidence boundary

Same-building source authority:

- `SRC-ZG-WF-001`
- PDF p73 / printed p58 / Fig.2-27 as the primary same-building visual/form context;
- adjacent p74–76 bracket-set relation / measured-drawing context carried forward by D-225.

Source role:

`QUALITATIVE_FORM_AND_ENVELOPE_AUTHORITY`

The source supports:
- 华栱 identity as a longitudinal/out-jump bracket arm;
- first/second jump assembly positions;
- broad horizontal upper-bearing character;
- broad non-ornamental bracket-member silhouette;
- relation to adjacent dougong layers.

The source does **not** establish:
- metric pixel-to-mm profile tracing;
- exact historical curve;
- exact inflection coordinates;
- exact historical end drop;
- exact shoulder/notch geometry;
- exact hidden overlap;
- mortise-tenon / slot / groove / cavity geometry.

Metric source-image calibration:

`NOT PERFORMED / NOT CLAIMED`

Historical control-point claim:

`false`

## 3. Independent Candidate identity

Candidate id:

`HUAGONG_PROFILE_CONTROL_SET_V001_C01`

Point count:

**16**

Control-set SHA-256:

`f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e`

Signature method:
- UTF-8 compact JSON serialization of the normalized-point array;
- separators = comma/colon;
- no whitespace significance.

This Candidate is independently constructed for T-040.

It does **not** copy, scale, average or morph:
- T-037 瓜子栱 profile controls;
- T-038 慢栱 profile controls;
- T-039 令栱 profile controls.

Prior control hashes retained for audit only:
- T-037 瓜子栱 = `35041b73a096c3cc46f4145ac24477523cf8e74d6324d8b6523a654fa1991920`
- T-038 慢栱 = `07d5d9172f25758f057c4bc0200fc35aa892a9a72ef15b40735fcc5c620e80c4`
- T-039 令栱 = `0a3081110d36fea812739a942eca1522a510810f5ea52ee3b4c9ebaa51c1c1a7`

Candidate hash differs from all three.

## 4. Normalized coordinate meaning

Profile plane:

- normalized x = fraction of the variant reference-specimen full length, centered at x=0;
- normalized z = fraction of the fixed Gate A reference thickness, centered at z=0;
- top bearing envelope = z=+0.50;
- deepest simplified underside = z=-0.50.

Extrusion:
- +Y;
- width fixed by Gate A = **214.2 mm**.

Symmetry:
- bilateral symmetry = **Stage1 simplification only**;
- it is not a claim that every historical 华栱 was geometrically symmetric;
- wear / deformation / repair asymmetry remain excluded.

## 5. Candidate 01 normalized polygon

```json
[
  [
    -0.5,
    0.5
  ],
  [
    0.5,
    0.5
  ],
  [
    0.5,
    0.26
  ],
  [
    0.465,
    0.16
  ],
  [
    0.405,
    0
  ],
  [
    0.325,
    -0.18
  ],
  [
    0.235,
    -0.34
  ],
  [
    0.145,
    -0.44
  ],
  [
    0.09,
    -0.5
  ],
  [
    -0.09,
    -0.5
  ],
  [
    -0.145,
    -0.44
  ],
  [
    -0.235,
    -0.34
  ],
  [
    -0.325,
    -0.18
  ],
  [
    -0.405,
    0
  ],
  [
    -0.465,
    0.16
  ],
  [
    -0.5,
    0.26
  ]
]
```

Total points:

**16**

## 6. Shape rationale

Candidate 01 intentionally uses a coarse, non-decorative envelope:

- one continuous horizontal upper bearing line;
- short terminal drops;
- a clear but broad terminal-to-body transition;
- two gradual underside descent zones;
- a broad central low zone rather than a needle point;
- no micro-serration, roll-cut, carved notch or ornamental generic-template detail.

The numerical inflection positions are Stage1 reconstruction controls only.

They are **not** described as measured from Fig.2-27.

The 16-point topology is intentionally distinct from:
- T-037 13-point set;
- T-038 18-point set;
- T-039 14-point set.

Point-count difference by itself is not treated as proof of independence; the audit also preserves distinct normalized coordinates and the distinct Candidate SHA-256.

## 7. JUMP_1 / JUMP_2 application rule

Both variants use the **same normalized 16-point control set**.

### JUMP_1_HUAGONG

Gate A reference specimen:
- L = **898.8 mm**
- W = **214.2 mm**
- T = **153.0 mm**

Application:
- actual x = normalized_x × 898.8
- actual z = normalized_z × 153.0
- extrusion width = 214.2

### JUMP_2_HUAGONG

Gate A reference specimen:
- L = **1630.0 mm**
- W = **214.2 mm**
- T = **153.0 mm**

Application:
- actual x = normalized_x × 1630.0
- actual z = normalized_z × 153.0
- extrusion width = 214.2

### Critical variant boundary

This is not:
- uniform 3D scaling of a finished JUMP_1 mesh into JUMP_2;
- uniform 3D scaling of a finished JUMP_2 mesh into JUMP_1;
- evidence that the historical profiles were metrically identical;
- evidence that the 898.8 / 1630.0 reference lengths apply to all Registry instances.

Required engineering method after future authorization:
- evaluate the normalized control set independently for each variant;
- build each canonical body independently;
- keep W/T fixed rather than scaling them by the L ratio;
- produce separate geometry signatures.

Different reference lengths do not create distinct profile-control point sets.

## 8. Gate A dependency

This Candidate is subordinate to the locked D-231 Gate A.

Required locked inputs:

- `HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001_C01`
- Gate A SHA-256:
  `ffacd94f5d6c2102a3a2378b3a1529a052a1c9b60d0ebc982d8c3b9c5dac201b`

The profile Candidate must not overwrite or reinterpret:
- 898.8 mm reference-only semantics;
- 1630.0 mm secondary-calculated/reference-only semantics;
- 214.2 × 153.0 mm report-ideal-model section semantics;
- 732.4 mm assembly-level direct observed mean;
- 56-instance standalone-length UNRESOLVED status.

## 9. Visual-review artifact

Candidate silhouette visualization:

`docs/production/zhenguo_wanfo/P3_3_STAGE1_HUAGONG_PROFILE_CONTROL_SET_V001.svg`

The SVG is a deterministic rendering of the 16 normalized points only.

It is **not**:
- a traced source image;
- a metric overlay;
- source-image calibration evidence;
- proof of historical curve accuracy.

Product Owner visual review should check:

1. top edge reads as a stable horizontal bearing surface;
2. terminal drops are short and non-decorative;
3. underside deepening is broad rather than ornate;
4. central low zone is visibly broad;
5. silhouette does not appear to be a copied瓜子栱/慢栱/令栱 polygon;
6. no unsupported notch, socket, groove, mortise or tenon is implied;
7. same normalized method can plausibly serve both reference variants without creating a second historical-form claim;
8. no part of the silhouette depends on the 732.4 mm assembly projection.

## 10. Independence audit

Required locked audit facts if later approved:

- `T037_GUAZI_CONTROL_REUSED = false`
- `T038_MANGONG_CONTROL_REUSED = false`
- `T039_LINGGONG_CONTROL_REUSED = false`
- `PRIOR_GONG_CONTROL_AVERAGED = false`
- `PRIOR_GONG_CONTROL_MORPHED = false`
- `GENERIC_TEMPLATE_SUBSTITUTION = false`
- `COMPARATIVE_BUILDING_PROFILE_AUTHORITY = false`

The prior hashes are stored only as anti-reuse references.

They do not contribute mathematically to the 16 Candidate coordinates.

## 11. Unsupported / deferred geometry

Remain explicitly unresolved/deferred:

- exact historical 华栱 side curve;
- exact historical profile control dimensions;
- exact end shoulder / notch;
- exact hidden overlap;
- physical bearing/contact datum;
- mortise-tenon;
- grooves;
- slots;
- cavities;
- hidden connection cuts;
- unmeasured chamfers;
- wear / damage / warp;
- per-instance deformation;
- per-instance repair/originality differences.

No such feature may be added to make the body look more realistic.

## 12. Future machine validation requirements

After future Product Owner lock and separate Engineering Execution Authorization, validation must verify:

- Candidate id/version/signature exactly match the locked Gate B;
- point count = 16;
- normalized-point SHA-256 = `f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e`;
- bilateral symmetry = true;
- classification remains `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
- metric source-image calibration remains `NOT_PERFORMED / NOT_CLAIMED`;
- JUMP_1 application = 898.8 × 214.2 × 153.0 envelope;
- JUMP_2 application = 1630.0 × 214.2 × 153.0 envelope;
- W/T do not scale by length ratio;
- finished-mesh uniform scale is not used to derive either variant;
- separate JUMP_1/JUMP_2 geometry signatures exist;
- Gate A SHA matches the D-231 locked control;
- prior-gong control hashes are not substituted;
- unsupported end/joinery geometry absent.

## 13. Future hard fails

- `HUAGONG_PROFILE_POINT_COUNT_NOT_16`
- `HUAGONG_PROFILE_SIGNATURE_MISMATCH`
- `PROFILE_CONTROL_SET_NOT_PO_APPROVED`
- `PROFILE_MARKED_DIRECT_MEASUREMENT`
- `METRIC_SOURCE_CALIBRATION_FALSE_CLAIM`
- `GUAZI_PROFILE_CONTROL_REUSE`
- `MANGONG_PROFILE_CONTROL_REUSE`
- `LINGGONG_PROFILE_CONTROL_REUSE`
- `PRIOR_GONG_PROFILE_AVERAGED`
- `PRIOR_GONG_PROFILE_MORPHED`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `COMPARATIVE_BUILDING_PROFILE_USED_AS_AUTHORITY`
- `JUMP_VARIANT_CREATED_BY_UNIFORM_MESH_SCALE`
- `WIDTH_SCALED_BY_LENGTH_RATIO`
- `THICKNESS_SCALED_BY_LENGTH_RATIO`
- `DISTINCT_JUMP_PROFILE_INVENTED_WITHOUT_EVIDENCE`
- `GATE_A_CONTROL_SHA_MISMATCH`
- `PROFILE_USES_732_4_AS_MEMBER_LENGTH`
- `UNSUPPORTED_END_SHAPE`
- `UNSUPPORTED_JOINERY_OR_LOCAL_CUTS`
- `SILENT_HISTORICIZATION`

## 14. Candidate 01 decision boundary｜D-232

D-232 prepares this Profile Control Set Candidate for Product Owner review only.

Current status:

**LOCKED / PRODUCT OWNER APPROVED / D-233**

D-232 does **not** authorize:
- Profile Control Set lock;
- Engineering Execution Authorization;
- production branch / PR;
- builder implementation;
- GitHub Actions / Blender;
- First Article;
- formalization;
- Catalog/V008/CURRENT binding;
- Stage2;
- T-018 resume.

If Product Owner approves this Candidate, the next complete step is:

**formally lock `HUAGONG_PROFILE_CONTROL_SET_V0.1`; Engineering Execution remains a separate authorization gate.**


## 15. Product Owner Approval / Lock｜D-233

Product Owner approved D-232 Candidate 01 without changing any normalized point, evidence classification, Gate A dependency or deferred boundary.

D-233 formally locks:

- candidate id: `HUAGONG_PROFILE_CONTROL_SET_V001_C01`;
- point count: **16**;
- normalized control-set SHA-256: `f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e`;
- classification: `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
- source role: `QUALITATIVE_FORM_AND_ENVELOPE_AUTHORITY`;
- metric source-image calibration: `NOT PERFORMED / NOT CLAIMED`;
- JUMP_1 Gate A envelope: **898.8 × 214.2 × 153.0 mm**;
- JUMP_2 Gate A envelope: **1630.0 × 214.2 × 153.0 mm**;
- same normalized profile method for both variants;
- independent body generation requirement;
- no finished-mesh uniform scaling;
- no prior-gong control reuse / averaging / morphing.

The locked profile controls remain reconstruction controls and do not establish:
- exact historical 华栱 curve;
- exact historical profile-point dimensions;
- exact end shoulder/notch;
- hidden overlap/contact datum;
- mortise-tenon / grooves / slots / cavities / hidden cuts;
- per-instance deformation/originality.

D-233 closes Gate B but does **not** authorize:
- production branch / PR;
- builder implementation;
- GitHub Actions / Blender;
- First Article;
- formalization;
- Catalog/V008/CURRENT binding;
- Stage2;
- T-018 resume.

Next complete gate:

**Engineering Execution Authorization for T-040 — NOT YET AUTHORIZED.**
