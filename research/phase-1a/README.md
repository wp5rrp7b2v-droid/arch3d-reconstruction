# Phase 1A Research Archive

Project: 中国建筑3D复原 — 平遥镇国寺万佛殿3D复原  
Research thread: 《平遥镇国寺万佛殿3D复原｜技术路线先例与实施方法深度研究》  
Archive status date: 2026-10-02

## 1. Purpose

This directory archives the Phase 1A evidence-baseline work for the independent technical-route research thread.

Phase 1A is **not** an implementation plan and does not authorize changes to the Wanfo Hall modeling route. Its purpose is to establish a traceable precedent/evidence base before Phase 1B deep dives and before any later route comparison.

## 2. Current gate status

- **Phase 1A Evidence Baseline:** NOT FROZEN
- **Phase 1A Evidence Baseline Finalization Patch V1.1:** IN PROGRESS / FORMAL CANDIDATE PENDING
- **Phase 1B Evidence Readiness:** expected to be evaluated after Final v1.1 QA
- **Phase 1B Product Owner Approval:** AWAITING PRODUCT OWNER APPROVAL
- **Route Selection:** NOT READY

The in-progress V1.1 work must not be treated as a completed or frozen baseline. Existing Phase 1A outputs remain working/superseded records until Final v1.1 is produced and passes final audit.

## 3. Research boundary

Phase 1A covers technical-route research, precedent investigation, evidence analysis, route-comparison preparation, and validation-design preparation.

It does **not**:
- modify the existing Wanfo Hall 3D implementation;
- select a final technical route;
- create engineering tasks, Masters, Registers, Matrices, Gates, or Project Control changes;
- assume that the existing project route is correct;
- treat a plausible explanation or a local modeling demo as proof of whole-building success.

## 4. Core research question

The research asks how mature or semi-mature practices have handled the reconstruction of Chinese historic timber buildings from measured survey reports, drawings, photographs, historical materials, point clouds, and incomplete evidence, with attention to:

1. geometric correctness;
2. timber connection/topology representation;
3. whole-building scalability;
4. traceability of conclusions;
5. separation of measured / inferred / reconstructed-design / unknown information;
6. deterministic regeneration;
7. reduction of ad hoc manual placement and untraceable patching.

## 5. Required evidence labels

- **FACT-FULLTEXT** — original full text checked; claim stays within the source's support.
- **FACT-ABSTRACT** — original publisher/author abstract directly supports the claim.
- **FACT-METADATA** — only bibliographic/existence metadata is verified.
- **INFERENCE** — synthesis from confirmed facts; not a direct source conclusion.
- **WORKING HYPOTHESIS** — worth testing; not proven.
- **UNKNOWN** — insufficient evidence.

New primary evidence is allowed to modify or retract an earlier conclusion. If that occurs, the archive must record what changed, why it changed, and which evidence caused the change.

## 6. Five validation classes

Every precedent must distinguish the following validation types:

1. **Geometry validation** — dimensions, point-cloud fit, drawing overlay, sections, dimensional audit.
2. **Connection / topology expression validation** — machine-readable or explicit representation of relationships, support, contact, insertion, interfaces, or topology.
3. **Assembly validation** — evidence that parts can actually be assembled under physical/geometric constraints; virtual construction sequence alone is not sufficient.
4. **Historical / documentary validation** — comparison against survey reports, repair records, historical documents, typological evidence, or expert historical interpretation.
5. **Structural / engineering validation** — structural analysis, mechanical behavior, engineering simulation, or equivalent engineering checks.

Important distinctions:
- connection/topology expression ≠ physical assembly validation;
- construction sequence/virtual construction ≠ mortise-tenon assembly-constraint validation;
- rule-based generation ≠ proven collision-free assembly;
- complete building model ≠ building-level deterministic regeneration.

## 7. Phase 1A source pool

The bounded Phase 1A pool is **P01–P24**. No P25+ source is part of the current Phase 1A baseline.

See: `evidence-register-p01-p24.md`.

Priority deep-dive clusters retained from Phase 1A:
1. Chi Lin Nunnery — P05/P06
2. Yingxian Wooden Pagoda — P07/P08
3. Jinci Shengmu Hall — P14
4. Chuzu'an Hall — P18
5. Foguang Temple East Hall — P03/P04
6. Dong drum tower procedural modeling — P15
7. regularized grid / rebuild HBIM — P09/P11
8. rule-driven HBIM–IFC — P21

## 8. Current Phase 1A conclusions that remain bounded

The current evidence supports retaining the following as research conclusions, not Wanfo Hall implementation rules:

- Chinese timber digital-reconstruction precedents exist.
- Several precedents place global datum/grid/structural organization before or above detailed component modeling, but this does not yet prove the correct Wanfo Hall route.
- Point-cloud or surface geometry alone does not establish hidden timber connection logic.
- “Whole building model” is used with different meanings across the literature.
- A complete HBIM does not by itself prove deterministic regeneration.
- Component-level parametric modeling does not by itself prove whole-hall scaling.
- No case in the bounded P01–P24 review has yet been established as proving all Wanfo Hall goals simultaneously.

Any “no case found” statement is bounded to the P01–P24 pool and the source access actually verified; it is not a universal claim about all literature.

## 9. Open evidence risks before freeze

Known open items include:
- P04: original/full-text auditability remains incomplete in the current baseline.
- P12: public original thesis/full text not recovered; metadata-level record only.
- P13: bibliographic identity remains unresolved; status UNKNOWN.
- P14: technical claims must remain bounded to metadata/abstract-level support unless original full text is recovered and checked.
- Final v1.1 must audit all P01–P24 validation labels and document every partial/uncertain label.
- Final v1.1 must provide an independently auditable Claim-to-Source table for the eight deep-dive clusters.

## 10. Final v1.1 acceptance requirements

The final Phase 1A baseline can be marked **FROZEN** only if the executed V1.1 output passes final audit, including:

- no P25+ expansion and no Phase 1B research;
- evidence-conflict policy retained;
- P01–P24 five-validation matrix completed;
- strict assembly-vs-topology distinction applied consistently;
- P05/P16/P18/P19/P21 labels corrected and all partial labels explained;
- eight deep-dive Claim-to-Source tables use ten fields:
  `Claim ID | 案例/方法簇 | Claim text | Source | Page/Section locator | Evidence scope | Evidence level | Single-source? | Needs Phase1B verification? | Notes`;
- FACT-FULLTEXT claims have usable locators;
- FACT-ABSTRACT / FACT-METADATA claims do not overreach;
- source links use official/reliable destinations when verified; otherwise `UNKNOWN / NOT VERIFIED` is recorded rather than guessed;
- no dependency on transient chat reference IDs for final auditability;
- Phase 1B is not described as approved;
- negative findings are explicitly bounded;
- Change Log and QA are present;
- final gate is binary: **FROZEN / NOT FROZEN**.

## 11. Archive policy while V1.1 is still running

Finalization Patch V1.1 and its expected outputs are recorded as a **FORMAL CANDIDATE — pending generation and final audit**.

This does not block the present archival work. It also does not authorize Phase 1B or route selection.

When the executed Final v1.1 is available, update this archive only after final audit. If it passes, the allowed gate wording is:

- Phase 1A Evidence Baseline: FROZEN
- Phase 1B Evidence Readiness: READY
- Phase 1B Product Owner Approval: AWAITING PRODUCT OWNER APPROVAL
- Route Selection: NOT READY

Explicit Product Owner approval is still required before entering Phase 1B.
