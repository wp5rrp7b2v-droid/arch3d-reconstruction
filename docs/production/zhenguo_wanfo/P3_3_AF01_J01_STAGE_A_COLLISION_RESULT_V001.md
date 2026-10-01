# AF01-J01｜Stage A Unmodified Collision Audit Result V001

- Date: 2026-10-01
- Status: **MACHINE PASS / DIAGNOSTIC COMPLETE / PRODUCT OWNER REVIEW REQUIRED**
- Scope: 北立面东中柱柱头节点
- A0 Product Owner approval: **YES**
- Workflow Run: **36821565714**
- Workflow conclusion: **SUCCESS**
- Artifact: `AF01_J01_STAGE_A_UNMODIFIED_COLLISION_AUDIT_V001`
- Artifact ID: **11143832506**
- Artifact digest: `sha256:d742c3073bc05826cc252731a2383edbe82457d5fd97fd071b41aeb7c90475e1`
- Head commit: `219f3eeb84b708f9189d5f24d5f104bd4c3cceaf`

## 1. Participants

Seven real approved component bodies / instance realizations were used:

1. 柱-03
2. 柱头栌斗-北侧东中柱
3. 华栱-北-05-一跳
4. 华栱-北-05-二跳
5. 头昂-北-05
6. 二昂-北-05
7. 下六椽栿-东缝

No proxy support body was inserted.

The Lower-Six instance consumes AF01-B02 realization length 10710 mm while preserving the approved Master section dimensions. This is an assembly-instance realization, not a Master mutation.

## 2. Machine audit summary

- pair count: **21**
- volume-intersection pair count: **3**
- Lower-Six volume-intersection pair count: **2**
- Master mutation: **FALSE**
- proxy support count: **0**
- new joinery cuts: **0**

### Collision C1｜JUMP_2_HUAGONG × TOU_ANG

- pair: `HG_J2 ↔ TOU_ANG`
- volume: **745,309.489 mm³**
- collision bbox dimensions:
  - X = **154.000 mm**
  - Y = **195.111 mm**
  - Z = **32.507 mm**
- bbox world:
  - min = `[2141.5, 5447.660, 4327.993]`
  - max = `[2295.5, 5642.771, 4360.5]`

Meaning:

The current approved outer envelopes of second-jump Huagong and Tou-Ang interpenetrate under the A0 project datum.

This does **not** prove which historical member was cut, notched, seated, or relieved.

### Collision C2｜TOU_ANG × LOWER_SIX

- volume: **13,760,889.399 mm³**
- collision bbox dimensions:
  - X = **154.000 mm**
  - Y = **445.156 mm**
  - Z = **419.686 mm**
- bbox world:
  - min = `[2141.5, 4909.844, 4401.901]`
  - max = `[2295.5, 5355.0, 4821.587]`

This is the dominant Lower-Six collision.

The collision X extent is 154 mm, numerically below the observed Lower-Six tenon-area thickness of 375 mm.

However:

> **This does not prove that the collision lies inside the historical 375 mm tenon envelope.**

The tenon-zone offset, exact longitudinal position and cut distribution remain UNKNOWN. No symmetric 444→375 reduction is assumed.

### Collision C3｜ER_ANG × LOWER_SIX

- volume: **534,989.023 mm³**
- collision bbox dimensions:
  - X = **154.000 mm**
  - Y = **124.700 mm**
  - Z = **55.717 mm**
- bbox world:
  - min = `[2141.5, 5230.300, 4798.283]`
  - max = `[2295.5, 5355.000, 4854.0]`

Again, 154 mm is numerically compatible with the 375 mm thickness constraint only. Exact historical tenon-envelope membership is unresolved.

## 3. Important non-collision result

### JUMP_2_HUAGONG × LOWER_SIX

- volume intersection = **0**
- AABB Z overlap = **0**
- state = **contact-plane / zero-volume intersection under current envelopes**

This is consistent with the locked support relation:

`JUMP_2_HUAGONG upper level = LOWER_SIX support plane = Z 4360.5 mm`

It is not a historical contact-surface proof.

## 4. Visible gaps are not historical gap claims

This diagnostic intentionally instantiates only the seven listed objects.

It does not instantiate the complete column-head puzuo stack, including all intermediate dou / transverse gong / supporting pieces.

Therefore visible open space between:
- Ludou and J1 Huagong;
- J1 and J2;
- other non-adjacent levels

must not be interpreted as actual historical air gaps.

Stage A tests envelope conflicts at the targeted Lower-Six / Huagong / Ang node only.

## 5. Stage A interpretation

The original recovery hypothesis is supported:

> The assembly problem is not solved by XYZ placement alone. Real approved outer-envelope components generate specific physical interpenetrations at the exact node where historical local processing / joinery must exist.

The largest actionable conflict is:

`LOWER_SIX ↔ TOU_ANG`

followed by:

`LOWER_SIX ↔ ER_ANG`

There is also an independent:

`JUMP_2_HUAGONG ↔ TOU_ANG`

conflict.

These are three separate collision facts. They must not be collapsed into one guessed rectangular slot.

## 6. Gate

Stage A diagnostic execution: **COMPLETE / MACHINE PASS**

Not authorized:
- no Stage B cut;
- no Master boolean;
- no permanent joinery feature;
- no proxy insertion;
- no whole-frame generation.

Next decision must be Product Owner review of the collision map.

If approved, the next bounded engineering step should select **one collision only** for a Joinery Candidate study. The recommended first collision is the dominant `LOWER_SIX ↔ TOU_ANG` conflict, because it directly addresses the original Lower-Six column-head assembly question.
