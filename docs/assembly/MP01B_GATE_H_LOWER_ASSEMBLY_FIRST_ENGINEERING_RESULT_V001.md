# MP-01B Gate H｜Lower Assembly First Engineering Result V001

Status: **MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED / NOT YET ACCEPTED**
Date: 2026-10-06

## 1. Engineering run

- Task: `T-044`
- GitHub Actions Run: `37432149756`
- Run conclusion: **SUCCESS**
- Head SHA: `96d2a6ef8ace7aaeeceba2063ee83857f71bdeee`
- Artifact ID: `11397412125`
- Artifact name: `MP01B_GATE_H_LOWER_ASSEMBLY_V001`
- Artifact size: `3,925,214 bytes`
- Artifact digest: `sha256:0c06ac0b48d92783ea4b0a54d9eba355cae20094b2eb3e2866dd7fd332fc6606`

## 2. Machine result

**51 / 51 PASS**

Validated:
- exactly 6 logical assembly objects;
- Four-Chuanfu and Pingliang V008 identities preserved;
- 2 reconstructed LOWER_SUPPORT Tuofeng instances;
- 2 reconstructed Interior Linggong instances;
- no whole-hall count claim;
- Four-Chuanfu / Pingliang envelopes match Gate G;
- support stations = ±1836 mm;
- mirror symmetry;
- support-object axis mapping = Rz +90°;
- contact-plane closure at Z=0 / 91 / 306;
- no unintended Z penetration above tolerance;
- Interior Linggong analog envelope preserved;
- Tuofeng height = 91 mm;
- no outer-eaves Linggong geometry leakage;
- no First Article fixture leakage;
- reconstructed metrics remain non-historical;
- beam realization lengths remain non-historical;
- hidden joinery remains UNKNOWN / DEFERRED;
- joinery cut count = 0;
- 6 SUPPORT + 4 LOCATE relations;
- relation evidence remains explicit;
- independent reopen PASS;
- deterministic rebuild PASS;
- 306→310 dependency mutation PASS;
- canonical/mutation renders and Review Board PASS.

## 3. Exact signatures

- Canonical assembly signature:
  `d9e7880252746283dcf72534dd276a9ab6f0b2220f15b7d4b5169b26449c2d71`
- Mutation assembly signature:
  `74d6c243f4a2933f91ab65236a0cd62be67c50b88508e0d3a0bfd433b3a8f47d`
- Canonical .blend SHA-256:
  `6efc84d3468d31ecab7bf4cc3fd9887710288e9f38a07da2bcd9c19937c4cc35`
- Semantic JSON SHA-256:
  `7329397b0578837234c34800a1e81c25f023c1f6014e425270c899b5b4efb058`
- Review Board SHA-256:
  `b6297d6c87a4da0df06b7ac910fa07ab1c789d7c51d70cfc0065e02993c15f61`
- Validation JSON SHA-256:
  `df7e5fe0781f3c1b750ff020a955adaf741faf04a0005d57e291a22c69118e72`

## 4. Canonical vertical stack

- Four-Chuanfu top = Z 0
- Tuofeng top = Z 91
- Interior Linggong bottom/top = Z 91 / 306
- Pingliang underside/top = Z 306 / 586.5

## 5. Dependency mutation

Controlled mutation:

`support clearance 306 → 310 mm`

Observed:
- Tuofeng height: 91 → 95 mm;
- Linggong Z: 91/306 → 95/310 mm;
- Pingliang Z: 306/586.5 → 310/590.5 mm.

Invariant:
- Four-Chuanfu geometry/placement;
- beam realization lengths;
- support-station Y values;
- Interior Linggong local envelope;
- Tuofeng plan footprint;
- object identities;
- evidence classifications;
- hidden joinery UNKNOWN state.

Result: **PASS**

## 6. Product Owner visual-review note

The Review Board visibly shows the two support groups centered at Y=±1836 while the Pingliang realization also terminates at Y=±1836.

Therefore each support group extends to both sides of the Pingliang end station.

This is **not a machine-build error**: it is the direct result of the approved Gate G project-axis / support-station rule.

The orientation remains explicitly:

`PROJECT_ASSEMBLY_RULE / REPLACEABLE`

and is not a historical orientation fact.

Product Owner should therefore review the visible support orientation/overhang before accepting MP-01B.

## 7. Scope

Gate H machine PASS proves only:

> the Gate G lower-assembly contract can be generated, reopened, rebuilt and dependency-mutated deterministically with explicit evidence boundaries.

It does not prove:
- historical exactness;
- exact historical Linggong/Tuofeng orientation or profile;
- hidden joinery;
- whole-frame completeness;
- whole-hall scalability.

## 8. Next decision

Product Owner reviews the Gate H Review Board and chooses:
- APPROVE MP-01B Minimum Proof;
- or request local orientation/placement revision.

Combining MP-01A + MP-01B and PR #56 merge remain NOT AUTHORIZED.
