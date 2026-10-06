# MP-01B Gate H-R4｜Corrected Lower Assembly Engineering Result V001

Status: **MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED / NOT YET ACCEPTED**
Date: 2026-10-06

## 1. Final engineering run

- Task: `T-045`
- GitHub Actions Run: `37453623798`
- Conclusion: **SUCCESS**
- Head SHA: `52bcf586367238df635d2bf2fad848fce5f12076`
- Artifact: `MP01B_GATE_H_R4_CORRECTED_LOWER_ASSEMBLY_V001`
- Artifact ID: `11407787011`
- Artifact size: `5,124,642 bytes`
- Artifact digest: `sha256:c5126228683f9c396f5cf3580022b97a4ef979be23e8af44ee2e802d308019ee`

## 2. Validation

**56 / 56 PASS**

Passed:
- 10 rendered physical geometries;
- 2 deferred Panjian Fang records with no fabricated mesh;
- Four-Chuanfu / Pingliang envelopes;
- target Linggong direct dimensions and assembly-X / 顺身 direction;
- no Gate-F 893.3 mm Linggong analog leakage;
- Huagong assembly-Y / 进深 direction;
- Huagong 900 mm remains project completion, not direct measurement;
- Huagong endpoint controls;
- no outer-eaves Huagong geometry authority;
- FRONT/REAR Tuofeng heights 172.9 / 196 mm;
- target Panjian Ludou envelopes;
- reconstructed bottom-depth handling;
- no column-head Ludou geometry authority;
- common gong-seat reference Z=306;
- target Ludou physical tops 398 / 415;
- Linggong/Pingliang ±2 mm reconciliation;
- orthogonal Huagong/Linggong interlock;
- hidden cuts/joinery UNKNOWN;
- 6 SUPPORT / 8 LOCATE / 2 BELONG / 0 CONNECT;
- independent reopen;
- deterministic rebuild;
- Huagong 900→950 dependency mutation;
- Blender 4.5.13 LTS;
- all five engineering renders + Review Board non-empty.

## 3. Exact signatures

- Canonical assembly signature:
  `a3dfdf40d98fb376df05d84f75f79bfdd675e2eb96c57ef994a07865e194c9b9`
- Mutation assembly signature:
  `8b37647d927a3d0183c966327a5facbbe39b179dd47bc17d0a7428a40fb63499`
- Canonical .blend SHA-256:
  `49095581eccbbe5020cf79945812511485535373d2b053b2e02c5ffe17391fb4`
- Semantic JSON SHA-256:
  `255d9b7ecf01f6cce69951151ee0e3697e5c66c615395d90f635387097b91996`
- Review Board SHA-256:
  `2d71f6f8ead9d6ab862d728de04d7a20a76e9e5f2460eca1f76a5eaf1a4c6d6b`

## 4. Canonical corrected node

Rendered geometry:
1. 四椽栿-东缝
2. 平梁-东缝
3. FRONT Tuofeng
4. REAR Tuofeng
5. FRONT Panjian Ludou
6. REAR Panjian Ludou
7. FRONT Interior Huagong
8. REAR Interior Huagong
9. FRONT target Linggong
10. REAR target Linggong

Deferred:
- FRONT Panjian Fang
- REAR Panjian Fang

Corrected axis logic:
- Linggong = 顺身 / assembly X
- Huagong = 进深 / assembly Y

## 5. Dependency mutation

Controlled:
`Huagong 900 → 950 mm`

Held fixed:
- outer Tuojiao-control endpoints.

Observed:
- FRONT inner gong-head endpoint: 1186 → 1136;
- REAR inner gong-head endpoint: -1186 → -1136;
- midpoint shifts inward 25 mm;
- all non-Huagong geometry invariant;
- evidence classifications invariant.

Result: **PASS**

## 6. First-run validation patch

Initial Run `37453391634` reached:
- canonical build PASS;
- reopen PASS;
- mutation PASS;
- deterministic rebuild PASS;
- Review Board PASS;

but failed validator check 36 because the semantic field used the wording
`HUAGONG_LINGGONG_ORTHOGONAL_OVERLAP`
instead of the R3 contract label
`BRACKET_INTERLOCK_ZONE`.

Patch:
- builder semantic field was bound directly to the approved R3 contract value;
- geometry and numeric controls were unchanged.

Final Run `37453623798` then passed **56/56**.

## 7. Visual-review boundary

The Review Board now shows:
- the Linggong as an out-of-section / along-building member;
- the Huagong as the in-section / depth-direction member;
- the two gongs intersecting orthogonally at each Panjian Ludou node.

The Huagong/Linggong bodies are currently bounded-envelope representations. Their visible intersection does **not** model the hidden historical cuts.

The Panjian Fang remains visible only in semantic/deferred records, not as invented geometry.

## 8. Scope

Gate H-R4 MACHINE PASS proves only that the corrected R3 contract can be generated, reopened, deterministically rebuilt and dependency-mutated.

It does not prove:
- exact historical joint geometry;
- exact original 963 profile;
- exact Panjian Fang geometry;
- whole-frame completion;
- whole-hall scalability.

## 9. Next decision

Product Owner reviews the corrected R4 Review Board and chooses:
- APPROVE MP-01B corrected Minimum Proof;
- or request targeted rework.

MP-01A + MP-01B combination and PR #56 merge remain NOT AUTHORIZED.
