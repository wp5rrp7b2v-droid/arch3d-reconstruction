# MP-01B Gate E｜Interior Linggong First Article Engineering Result V001

Status: **PRODUCT OWNER APPROVED / FORMALIZED / CATALOG+V008 BOUND**
Date: 2026-10-06

## 1. Accepted engineering run

- Task: `T-043`
- GitHub Actions Run: `37424767731`
- Run conclusion: **SUCCESS**
- Head SHA: `0ee069d22e3de86b058c237489e7b68b56f0694b`
- Artifact ID: `11394896083`
- Artifact name: `P3_3_T043_INTERIOR_LINGGONG_MASTER_FIRST_ARTICLE_V001`
- Artifact digest: `sha256:397adf6552f3f1d9d4791cc8dbaf3ea5197ee556c673aee11ade113c3491610d`

## 2. Machine result

**28 / 28 PASS**

Validated:
- one Master family;
- one role variant `LOWER_PINGLIANG_SUPPORT`;
- canonical Fixture A;
- independent reopen;
- mutation Fixture B;
- identity/role invariance through mutation;
- deterministic restore;
- seat footprint within body footprint;
- engineering-test classification;
- no historical metric claim;
- no building-dimension claim;
- outer-eaves 897 / 217.4 / 155.6 values absent from geometry inputs;
- outer-eaves 14-point profile not used;
- historical dimensions/profile remain UNKNOWN;
- hidden joinery remains UNKNOWN / DEFERRED;
- zero joinery cuts;
- Source Binding exists;
- approved Candidate Geometry exists;
- Review Board generated.

## 3. Exact signatures

- Canonical geometry signature:
  `7ef466c39b08f7485da1c7e91af8882446da7f6d9546668ac28132445d19232f`
- Mutation geometry signature:
  `e983cda6c0b9c612621108a5141279aa36e777ba0862492ff97a7706bbf94847`
- Canonical .blend SHA-256:
  `82a16ddf3c3d727ddd4cb03408ade7b4ff9a25afd8a42cb7215edc2178a22301`
- Semantic JSON SHA-256:
  `eb222833544bc28ef2f88d897249742b912202e049a7f45fc320256a29aae772`
- Review Board SHA-256:
  `d71324582fe3193a8ba3a6c3fca15206d65e16a0eaf2202fdbf43e0f38a2a5fb`
- Validation JSON SHA-256:
  `f35f72c462903d653efaf943adc25b0438bd635539f543af726bf7ae0dfcbca5`
- Definition SHA-256 embedded in semantic:
  `4249aec56a83c387ee471bee7c1d1bfa8ec937ffa891bba220ceaf0cbbea2afa`
- Blender: `4.5.13 LTS`

## 4. First Article geometry

Fixture A remains:

`ENGINEERING_TEST_ONLY / NOT_BUILDING_DIMENSIONS`

- BODY_ZONE: 1000 × 500 × 180
- UPPER_BEARING_ZONE: 550 × 500 × 120
- combined test height: 300

These dimensions are **not Wanfo Hall building dimensions**.

## 5. Scope proven

Gate E proves only:

> `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER` can be generated, mutated, reopened and deterministically restored as a provenance-bounded neutral two-zone digital support component.

It does not prove:
- the historical Linggong profile;
- historical dimensions;
- equality to the outer-eaves Linggong;
- historical joinery;
- actual MP-01B building placement;
- whole-frame or whole-hall correctness.

## 6. Next decision

Product Owner reviews the First Article Review Board.

If approved:
- First Article may enter **Formalization + Catalog/V008 binding**;
- after formalization, MP-01B may proceed to resolve the actual assembly envelope for `四椽栿 → 驼峰 / 令栱 → 平梁`.

PR #56 merge remains not authorized.


## 7. Product Owner approval / formalization

- First Article: **APPROVED**
- Formalization: **COMPLETE**
- Catalog binding: **COMPLETE**
- V008/CURRENT binding: **COMPLETE**
- Master-scope: **30/30 = 100%**
- Approved Master families: **27**

Next: resolve the actual MP-01B assembly-owned metric envelope and placement for `四椽栿 → 驼峰 / 令栱 → 平梁`.
