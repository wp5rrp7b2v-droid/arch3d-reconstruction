# Phase 1A Evidence Baseline Finalization Patch V1.0

> Archive class: Superseded Working Record
> Date: 2026-10-02
> Purpose: finalization attempt after Evidence Baseline v1.0
> Current-use warning: superseded by the V1.1 finalization specification.

## 1. Finalization objectives

The V1.0 finalization pass attempted to make the Phase 1A evidence baseline auditable and ready for a final freeze decision by preserving the fixed P01–P24 candidate range and eight Deep Dive clusters, separating evidence levels, applying five validation classes, improving claim-to-source traceability, isolating unresolved evidence, and preventing premature route selection.

## 2. Evidence-conflict policy

The earlier idea that a correction patch could not change Phase 1A conclusions was rejected as an evidence rule.

Correct policy:
- do not proactively expand the research question or candidate pool during a minor correction;
- if new primary evidence directly conflicts with an earlier conclusion, revise or retract the earlier conclusion and record why.

## 3. Five validation classes

1. Geometric validation
2. Connection / topology-expression validation
3. Physical assembly validation
4. Historical / literature validation
5. Structural / engineering validation

These classes must remain orthogonal.

## 4. Important case corrections

### P05 — Chi Lin Nunnery
Physical simulated assembly / collision evidence justified treating P05 as a genuine assembly-validation precedent.

### P16 — Bai traditional timber dwellings
Construction logic, spatial topology, and algorithmic generation supported topology / relationship expression. They did not by themselves prove physical assembly validation.

### P18 — Chuzu'an Hall
Geometric validation was strong. The 45-stage TimeLiner virtual-construction sequence was not physical assembly validation.

### P19 — Zhenwu Pavilion
Engineering validation was strong through the HBIM → IFC → SAP2000 chain. Modeling according to construction logic did not automatically establish physical assembly validation.

### P21 — HBIM–IFC
Machine-readable component relationships and construction logic supported topology / connection-expression validation. They did not prove physical mortise-tenon assembly feasibility.

### P09 / P11 / P15
Regularized or procedural generation was not to be counted as assembly validation unless a separate physical/digital assembly test was actually demonstrated.

## 5. Eight Deep Dive Claim-to-Source requirement

Dedicated claim-level audit tables were required for:

1. Chi Lin Nunnery — P05/P06
2. Yingxian Wooden Pagoda — P07/P08
3. Jinci Shengmu Hall — P14
4. Chuzu'an Hall — P18
5. Foguang Temple East Hall — P03/P04
6. Dong drum-tower procedural modeling — P15
7. Regularized grid / rebuild — P09/P11
8. Rule-driven HBIM–IFC — P21

Required fields:
Claim ID; Case / method cluster; Claim text; Source; Page / Section locator; Evidence scope; Evidence level; Single-source?; Needs Phase 1B verification?; Notes.

## 6. Source-link rule

Use an official or reliable source only when actually verified. If no such source can be verified after allowed targeted checking, record UNKNOWN / NOT VERIFIED. Never insert a low-quality or speculative link merely to avoid a blank field.

## 7. Session-reference rule

A frozen evidence baseline must not depend on conversation-internal references such as turn-file, turn-search, or turn-view IDs. The final evidence chain must be independently auditable using real bibliography, DOI, publisher/official URL, and page/section locators.

## 8. Bounded negative findings

Negative search conclusions must be bounded to the P01–P24 candidate pool and the evidence verified in this Phase 1A review.

## 9. Governance correction

- Phase 1A Evidence Baseline: NOT FROZEN until final QA and PO freeze decision.
- Phase 1B Evidence Readiness: READY only if finalization conditions are met.
- Phase 1B Product Owner Approval: AWAITING PRODUCT OWNER APPROVAL.
- Route Selection: NOT READY.

## 10. Why V1.0 was superseded

The subsequent V1.1 instruction corrected residual formalization issues:
- the Claim-to-Source table was made a true ten-field structure by explicitly adding Case / Method Cluster;
- the final Gate became binary: FROZEN / NOT FROZEN;
- SOURCE LINKS requirements were prevented from encouraging filler;
- the final baseline was required to remove all dependency on chat-internal reference IDs.

This V1.0 document is retained for audit provenance only.
