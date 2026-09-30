# T-020｜FR-007 Direction / Consumption Correction V001

**Date:** 2026-09-30  
**Status:** PRODUCT OWNER APPROVED / STRUCTURAL REGRESSION 18/18 PASS / PR #51 MERGED INTO PR #50 WORKING BRANCH / MAIN NOT YET UPDATED  
**Scope:** T-020 reconstructed-design roof Y control only  
**Historical claim:** NONE

## 1. Correction

The source parameter remains unchanged:

- `FR-007 = [120,115,210] fen`
- `MOD-002 = 15.3 mm/fen`

The measured-report diagram and frame-depth analysis establish the FR-007 source sequence as **RIDGE_TO_EAVE**. T-020's canonical control chain is named **EAVE_TO_RIDGE** (`N00→N01→N02→N03`), so consumption must reverse the source sequence:

- source / ridge→eave: `[120,115,210] fen`
- consumed / eave→ridge: `[210,115,120] fen`
- consumed lengths: `[3213.0,1759.5,1836.0] mm`

Corrected Y controls:

- N00 = -6808.5
- N01 = -3595.5
- N02 = -1836.0
- N03 = 0.0
- S02 = +1836.0
- S01 = +3595.5
- S00 = +6808.5

## 2. Invariants

The correction MUST NOT change:

- FR-007 source values
- MOD-002
- cumulative half-run = 6808.5 mm
- RIDGE_Y = 0
- N03 as the single shared ridge identity
- prohibition of S03
- PM-008—PM-012
- FR-004 / FR-005 / FR-006
- ROOF-007 / ROOF-008 / ROOF-009 Z-chain
- Component Registry / approved Masters / P3.2 relationship vocabulary
- historical evidence classifications

## 3. Downstream impact

Expected derived impact is limited to consumers of the corrected roof Y controls, including future/rebuilt PURLIN controls, RAFTER proxies, ROOF_ENVELOPE, GABLE_CONTROL, and roof-dependent FRAME_CONTROL / FRAME_SUPPORT endpoints.

Historical T-018 V002 audit artifacts that contain the old N01/N02/S01/S02 coordinates are retained as historical audit evidence and are **SUPERSEDED FOR ROOF-Y PLACEMENT VALUES ONLY**. They are not rewritten as if the old run had produced the corrected values.

T-018 remains HOLD. AF-01 must consume the corrected T-020 authority only after this patch passes regression and is merged into the active canonical line.

## 4. Evidence boundary

This is a project-engineering correction of parameter-direction interpretation. It does not introduce a new historical dimension and does not upgrade any reconstructed-design candidate to confirmed historical fact.

## 5. Regression result

Connector-executed structural regression: **18/18 PASS**.

Verified unchanged byte identities against PR #50 base:
- formal production parameter set
- building parameter bindings
- building assembly graph
- current Component Instance Registry
- Stage1 Master Catalog
- P3.2 relationship vocabulary

Verified corrected rule invariants:
- FR-007 source value remains [120,115,210]
- source direction = RIDGE_TO_EAVE
- eave→ridge consumption = [210,115,120]
- segment lengths = [3213.0,1759.5,1836.0] mm
- cumulative half-run = 6808.5 mm
- RIDGE_Y = 0
- N03 remains the single shared ridge
- north/south placement remains mirrored
- Z-chain inputs and plan dimensions remain unchanged

Machine-readable evidence:
`docs/evidence/zhenguo_wanfo/P3_3_T020_FR007_DIRECTION_CORRECTION_VALIDATION_V001.json`

The repository Python validator was not represented as having run in GitHub Actions; this evidence is explicitly a connector-executed structural regression.

## 6. Integration

Product Owner approved PR #51 Ready→Merge. PR #51 merged into the PR #50 working branch at `36def19143ddddccbbc424f59a529ce7d78d99fc`.

- correction integration: PASS
- PR #50: DRAFT / UNMERGED
- main: UNCHANGED
- AF-01: planning unblocked on working branch
- engineering generation: NOT AUTHORIZED
- T-018: HOLD
