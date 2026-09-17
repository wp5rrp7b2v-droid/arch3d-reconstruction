# Daily Close｜2026-09-17｜ARCH3D-001

## 1. Session status

- Project: 中国古建筑3D复原
- Case: 平遥镇国寺万佛殿
- Phase: P3｜古建筑构件系统化与组合建模
- Gate: P3.3｜构件驱动整殿重建
- Gate progress: 3/4
- Cloud Mode: RC-014 ACTIVE（2026-09-16～20）
- Start canonical main SHA: `574a00831ac827d67dd58667f80fb57d1dd0c77e`
- Latest material decision remains: `D-055`
- New Product Owner decision ID today: NONE

## 2. T-018 work completed today

T-018 continued on the existing branch / PR only:

- Branch: `codex/t-018`
- PR: `#3`
- PR status at close: `OPEN / NOT MERGED`
- GitHub-visible head at close: `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- PR merge authorization: FALSE

### 2.1 Correction Round 2

Round 2 corrected the earlier false whole-building realization state.

Machine result after correction:

- 365 / 365 runtime records = `RULE_DERIVED`
- `NOT_REALIZED_NO_APPROVED_PLACEMENT_RULE = 0`
- Formal = 12
- Proxy = 178
- Control = 66
- Envelope = 6
- UNKNOWN_BLOCKED = 96
- DEFERRED = 7
- 7 / 7 PURLIN remain DEFERRED
- unexplained omission = 0
- anonymous formal mesh = 0
- broken identity = 0
- PM-005 mutation and restore chain passed

Formal visual review did not pass Round 2 because most non-formal records were rendered as generic point/octahedron technical markers. The machine spatial state was substantially improved, but the four review views did not yet express a readable whole-building engineering system.

### 2.2 Correction Round 3

Round 3 was therefore restricted to engineering representation geometry and view-aware review evidence, while attempting to preserve Round 2 placement / identity / evidence boundaries.

Representation changes included differentiated technical geometry for:

- GRID_CONTROL
- BRACKET_CONTACT
- BRACKET_ARM
- FRAME_CONTROL
- FRAME_SUPPORT
- PRIMARY_FRAME
- GABLE_CONTROL
- PURLIN
- RAFTER
- ROOF_ENVELOPE

Generic octahedron representation for all non-formal families was removed. Review-display constants were isolated from historical / structural dimensions.

The Codex internal correction SHA was `dbd7fc30836a128914bad0daaeae869d3b9cca04`; internal SHA is not canonical. The correction was ultimately published to the existing PR #3, with the final GitHub-visible evidence head `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`.

### 2.3 Final GitHub Actions evidence run

Formal headless run:

- Workflow: `T-018 P3.3 Deterministic Whole Building`
- Run ID: `35226626839`
- Run number: `29`
- Head SHA: `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- Conclusion: `SUCCESS`
- Blender: 4.5.13 linux-x64
- Run A canonical build: PASS
- Run B independent reopen / validation: PASS
- Review rendering: PASS
- Run C PM-005 mutation: PASS
- Run D canonical restore: PASS
- Persistent hash / evidence step: PASS
- Artifact upload: PASS

Artifact:

- ID: `10499236860`
- Name: `P3_3_T018_HEADLESS_EVIDENCE_V001`
- Digest: `sha256:1acb510ed409e490319d62dad2232d082f163413ab81a209484f00b8b67329fa`
- Expiry: 2026-10-17

Four generated review views were directly inspected by ChatGPT:

- PLAN
- FRONT_ELEVATION
- SIDE_ELEVATION
- AXON

## 3. Formal visual review result

Final result today:

`T-018 = HOLD / MACHINE PASS / FORMAL VISUAL REVIEW FAIL`

The Round 3 views were materially better than Round 2 and exposed a roof-control topology defect rather than merely a display problem.

Observed defect:

- Runtime used an unapproved `COLUMN_GRID_Y_MIRROR_RULE` to synthesize a missing south terminal control.
- Current north terminal `ROOF_PURLIN_N_03` and synthetic south terminal did not converge to one shared ridge datum.
- The resulting roof envelope crossed / overlapped around the ridge in AXON.

The issue is therefore not accepted as a rendering-only defect.

## 4. Read-only roof-control origin audit

A read-only audit was performed after the visual failure. No project file was modified by the audit.

Audit conclusion:

`B — STOP / approved roof-origin + shared-ridge datum rule is missing upstream.`

### 4.1 Seven-PURLIN semantic topology

Canonical identities:

- `ROOF_PURLIN_N_00` = north eave control
- `ROOF_PURLIN_N_01` = north first inward control
- `ROOF_PURLIN_N_02` = north second inward control
- `ROOF_PURLIN_N_03` = shared ridge terminal control
- `ROOF_PURLIN_S_00` = south eave control
- `ROOF_PURLIN_S_01` = south first inward control
- `ROOF_PURLIN_S_02` = south second inward control
- no `ROOF_PURLIN_S_03` by design; ridge terminal is shared

This is control-topology semantics only. It does not upgrade the DEFERRED PURLIN family into confirmed historical members.

### 4.2 Authorized relative chain

`FR-007` is a reconstructed-design eave-to-ridge horizontal sequence:

- `[120, 115, 210] fen`
- `MOD-002 = 15.3 mm/fen`
- intervals = 1836.0 / 1759.5 / 3213.0 mm
- total eave-to-ridge half-run `D = 6808.5 mm`

ROOF-007 / 008 / 009 provide the corresponding eave→lower, lower→upper, upper→ridge rise sequence.

Existing inputs are sufficient to authorize the ridge-relative topology:

- north: `R-D → R`
- south: `R+D → R`
- shared terminal: `N03 = R`
- south final segment terminates at the same `N03`

They are not sufficient to authorize the absolute building-space value of `R`.

### 4.3 Current formula defect

Round 2 / Round 3 incorrectly mixed:

- observed/as-measured column-grid coordinate frame
with
- reconstructed-963 candidate roof-control sequence.

The implementation effectively assumed the reconstructed roof eave origins were tied directly to observed north/south grid boundaries. That alignment rule is not present in the protected authoritative inputs.

Round 3 then added `COLUMN_GRID_Y_MIRROR_RULE`, which is not an approved canonical rule and is therefore a synthetic relation.

### 4.4 Root-cause classification

This is classified as:

`UPSTREAM ENGINEERING RULE MODELING OMISSION + T-018 FAILURE TO STOP`

It is not a newly discovered historical-evidence gap.

The missing upstream semantic rule must define:

- the shared ridge datum for the reconstructed roof system;
- the relationship between that datum and the whole-building reconstructed-design coordinate system;
- the coordinate-layer policy separating observed reference geometry from reconstructed-design geometry;
- both roof slopes terminating at the same ridge control;
- no synthetic second ridge identity;
- the eave-origin relationship required by FR-007.

## 5. Consequence for earlier Round 2 freeze

The previous assumption that all Round 2 roof placements were frozen-correct is withdrawn.

At minimum, the following must be re-derived after an approved upstream datum rule exists:

- 7 PURLIN control placements
- 36 RAFTER proxy placements
- 6 ROOF_ENVELOPE placements
- 4 GABLE_CONTROL placements
- any FRAME_CONTROL / FRAME_SUPPORT endpoints that depend on the roof-control chain

The 365/365 machine PASS demonstrated deterministic self-consistency of the implemented formulas, but did not prove that the roof-origin formula was authorized by upstream rules.

## 6. Proposed next task — NOT YET AUTHORIZED

Proposed task:

`T-020｜P3.3_ROOF_SHARED_RIDGE_DATUM_RULE_V001｜屋顶共享脊基准与设计坐标层对齐规则`

Status at daily close:

`PROPOSED / NOT AUTHORIZED / NO BRANCH / NO PR`

Intended scope:

- establish a project-level engineering datum rule, not a new historical measurement;
- lock one shared ridge control;
- define reconstructed-design center-plane / roof-system LOCATE semantics;
- explicitly prohibit observed-grid values from silently becoming reconstructed-roof placement inputs;
- preserve PURLIN 7/7 DEFERRED and all historical evidence boundaries;
- prohibit any T-018-local invented `*_RULE` from filling the gap.

No T-020 engineering work has started and no Product Owner approval has been recorded.

## 7. Final cross-check snapshot before Project Control close

Verified facts:

- canonical main before this Project Control close: `574a00831ac827d67dd58667f80fb57d1dd0c77e`
- P3 remains ACTIVE / 3 of 4
- P3.0 PASS / CLOSED
- P3.1 PASS / CLOSED / D-040
- P3.2 PASS / CLOSED / D-046
- P3.3 ACTIVE / NOT PASS
- T-017 CLOSED / D-050, corrected by T-019
- T-019 CLOSED / D-055 / PR #4 MERGED
- T-018 PR #3 OPEN / NOT MERGED
- T-018 current head `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- latest T-018 Actions run `35226626839` SUCCESS
- artifact `10499236860` exists and is not expired
- T-018 formal acceptance = HOLD
- PR #3 merge authorization = FALSE
- latest formal decision remains D-055
- no T-020 task contract / branch / PR exists at close
- RC-014 remains ACTIVE through 2026-09-20
- local Mac sync remains pending for 2026-09-21
- no P3 phase archive closure is applicable because P3 remains ACTIVE

## 8. Next-session handoff

On next start:

1. Read GitHub `main` Project Control first.
2. Confirm PR #3 remains OPEN / NOT MERGED and record its current head before any work.
3. Do not continue T-018 placement correction while the shared-ridge datum gap is unresolved.
4. First design the minimal T-020 contract / DoD for the upstream roof shared-ridge datum and reconstructed-design coordinate alignment rule.
5. Obtain Product Owner approval before creating / executing T-020.
6. After T-020 is approved, executed, reviewed and merged to `main`, sync PR #3 to the new upstream main and only then resume T-018 correction.
7. If work continues during 2026-09-18～20, update the Cloud Mode Sync Ledger at daily close.
