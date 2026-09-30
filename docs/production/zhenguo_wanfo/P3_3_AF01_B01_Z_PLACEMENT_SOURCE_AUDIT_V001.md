# AF-01 / B01｜East-Seam Main-Frame Z Placement Source Audit V001

- Date: **2026-09-30**
- Task: **AF-01-B01**
- Status: **SOURCE AUDIT COMPLETE / NUMERIC Z CLOSURE NOT YET LOCKED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: 下六椽栿 / 上六椽栿 / 四椽栿 / 平梁 only

## 1. Direct source findings

The measured report directly supports the following structural facts:

1. Wanfo Hall uses a six-rafter main-frame system; the east and west seams each carry the main transverse frame.
2. East/west seams each have **two six-chuanfu members stacked vertically**.
3. **Lower six-chuanfu** enters the column-head bracket set and is placed **above the second-jump huagong**.
4. **Upper six-chuanfu** bears on / presses the **second lower ang** of the column-head bracket set at the column-center position.
5. **Four-chuanfu** is above the upper six-chuanfu; between them is one intermediate bracket-gong set; no ludou is used below the four-chuanfu; a san-dou provides support.
6. **Pingliang** belongs above the four-chuanfu in the main-frame sequence and participates in the ridge-support system together with shuzhu/chashou.
7. The report directly measures member sections, but does **not** publish one common absolute-Z table for the four beam bodies.

## 2. What the roof-elevation chapter does and does not authorize

The report's purlin-elevation analysis provides:

- eave-purlin → lower-purlin rise = 88 fen;
- lower-purlin → upper-purlin rise = 61 fen;
- upper-purlin → ridge-purlin rise = 82 fen;
- total roof rise = 231 fen.

These are **purlin-control elevation differences**. They do not directly assign beam-body Z values to lower six-chuanfu, upper six-chuanfu, four-chuanfu or pingliang.

Therefore B01 MUST NOT set beam Z by silently equating a beam tier with N00/N01/N02/N03 purlin Z.

## 3. Deformation drawings boundary

Figures 2-99 onward overlay the measured point cloud / current frame against the inferred ideal model and annotate settlement / inward-outward deformation.

Those annotation values are deformation quantities, not absolute building-Z placement authority.

They may be used later as a validation cross-check, not as canonical beam elevation inputs.

## 4. Existing project-rule audit

The prior T-018 FV-B exact numeric frame-tier formula is not admissible for AF-01 B01.

P3.2 review already established that frame-tier semantics were valid while exact historical/production elevations were not proven; the later semantic-validity check explicitly rejected promoting ROOF-004/005/006 into an exact Frame-tier Z authority.

No legacy P2 / FV numeric tier may be revived by renaming it.

## 5. Minimum deterministic resolver implied by source

B01 should be closed by **support/contact-driven placement**, not by inventing four independent absolute heights.

Required resolver chain:

- LOWER_SIX_CHUANFU Z ← actual support plane of the column-head second-jump huagong assembly role.
- UPPER_SIX_CHUANFU Z ← actual receiving/support plane associated with the column-head second lower-ang role at column center.
- FOUR_CHUANFU Z ← actual san-dou / intermediate-support top plane above upper six-chuanfu.
- PINGLIANG Z ← actual upper support/contact stack above four-chuanfu as resolved from the east-seam measured frame.

The support/contact planes may be reconstructed-design engineering datums, but each must remain explicitly replaceable and must not be labelled as a directly measured 963 absolute elevation unless the report supplies such evidence.

## 6. Result

### Resolved
- structural vertical order;
- support-role identity for lower six / upper six / four-chuanfu;
- prohibition against using purlin Z as beam Z;
- prohibition against using deformation labels as absolute Z;
- prohibition against reusing T-018 FV-B exact tier values.

### Still blocking
- exact engineering contact-plane Z for the two column-head support roles;
- exact engineering intermediate-support height from upper six to four-chuanfu;
- exact engineering support-stack height from four-chuanfu to pingliang.

## 7. Next bounded action

**B01-1｜Lower + Upper Six-Chuanfu Support-Plane Closure**

Only resolve the two column-head support planes required by:
- lower six-chuanfu;
- upper six-chuanfu.

Do not solve four-chuanfu/pingliang in the same step.
Do not generate Blender.
