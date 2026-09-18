# T-018 V002｜Impact / Non-Impact Contract V001

## Status
DESIGN COMPLETE / NOT AUTHORITY / IMPLEMENTATION FROZEN

本文件规定：未来为补齐 Control Placement Authority 而做的任何 correction，必须先声明它允许改变什么，并由机器证明没有越界。

## 1. Permanently protected / must not change

以下内容在任何 bounded completion 中都必须保持不变：

- P3.0 component identity / ontology
- P3.1 approved Master identities and geometry contracts
- P3.2 five relationship types:
  - SUPPORT
  - CONNECT
  - LOCATE
  - REPEAT
  - BELONG
- T-017 365/365 accounting and 11-family coverage
- family counts / component IDs / runtime IDs
- evidence classification / historical-claim boundaries
- PM-003..PM-007 = validation-only
- P2 world transforms = prohibited as generative input
- 7/7 PURLIN disposition = DEFERRED
- T-020 X=0 / Y=0 reconstructed-design datum
- T-020 roof Y positions
- N03 sole shared ridge
- no ROOF_PURLIN_S_03
- no new historical dimension
- no sixth P3.2 relationship type

Any change to the above is an immediate STOP and requires separate Product Owner decision outside this bounded package.

## 2. Correction module FV｜Frame Vertical Completion

Allowed to affect:
- 6 FRAME_TIER control Z values
- 48 FRAME_POST LOW/UP endpoints
- paired 54 FRAME_SUPPORT proxy endpoints
- optional 8 PRIMARY_FRAME semantic anchor elevations only if explicitly declared as engineering anchors

Must not affect:
- GRID_CONTROL coordinates
- COLUMN origins/heights
- any roof-control Y
- any roof-control Z unless the correction contract explicitly says the Frame endpoint consumes Roof, never the reverse
- RAFTER / ROOF_ENVELOPE / GABLE topology
- BRACKET internal geometry
- any identity/count/disposition

Machine checks:
- affected runtime IDs exactly match declared set
- all unaffected normalized placement hashes unchanged
- no Frame→Roof back-propagation
- no DG-113 or ROOF-004/005/006 cross-system use unless separately approved in the completion authority

## 3. Correction module RZ｜Roof Z Closure

Allowed to affect:
- Z coordinates of 7 PURLIN technical controls
- endpoints of 36 RAFTER proxies
- vertices of 6 ROOF_ENVELOPE surfaces
- vertices of 4 GABLE_CONTROL polylines
- upper endpoints of the 24 FRAME_POST_*_UP controls and their paired support proxies, because they terminate on the roof profile

Must not affect:
- roof-control Y positions
- roof X stations / gable projection
- GRID_CONTROL
- COLUMN origins/heights
- FRAME_TIER Z values
- FRAME_POST_*_LOW base/tier endpoints
- PURLIN identity/disposition
- N03/shared-ridge identity
- any Bracket parameter/placement

Machine checks:
- N03 remains single shared ridge
- north/south ridge endpoint coordinates coincide exactly
- non-Z roof coordinates unchanged
- all unrelated object hashes unchanged

## 4. Correction module RT｜Control Topology Formalization

Allowed to affect:
- machine-readable adjacency/endpoint/surface mapping records for:
  - PURLIN controls
  - RAFTER
  - ROOF_ENVELOPE
  - GABLE_CONTROL
  - FRAME_CONTROL↔FRAME_SUPPORT pairing

Must not affect:
- canonical parameter values
- any coordinate value already fixed by an authority rule
- identities/counts/dispositions
- evidence classifications

Machine checks:
- topology map is deterministic and stable-serialized
- all 36 rafters map to exactly one adjacent control pair
- all 6 roof surfaces map to exactly one adjacent control interval
- all 4 gable controls terminate at N03 and contain the expected control sequence
- no orphan / duplicate topology edges

## 5. Correction module BA｜Technical Anchor Closure

Allowed to affect:
- technical representation anchors for:
  - 88 BRACKET_ARM UNKNOWN markers
  - 88 BRACKET_CONTACT proxies
  - 8 PRIMARY_FRAME UNKNOWN semantic markers, if not covered by FV

Must not affect:
- Frame placement authority
- Roof placement authority
- Column geometry
- historical claim status
- Master qualification
- any accounting or identity

Machine checks:
- anchor derivation uses only approved grid/column technical datums
- bracket-internal parameters remain local to bracket representation
- no anchor becomes a source for Frame/Roof placement

## 6. Global non-impact invariants

Every future completion implementation must prove before/after:

1. 365/365 identities unchanged.
2. 11 family counts unchanged.
3. 7/7 PURLIN remain DEFERRED.
4. P3.2 relationship vocabulary unchanged.
5. PM-003..PM-007 generative-use count remains zero.
6. P2 numeric-transform generative-use count remains zero.
7. protected upstream hashes unchanged unless a separately approved additive project-rule artifact is explicitly introduced.
8. no historical_claim upgrade.
9. no undeclared object coordinate change.
10. no new Blender-local geometry derivation.

## 7. Escalation boundary

The bounded completion must be abandoned and Outcome C declared if any required fix would:
- modify component identity;
- modify P3.2 relationship definitions/vocabulary;
- require a new historical dimension;
- require P2 world transforms;
- create a circular dependency;
- require broad changes outside FV/RZ/RT/BA affected sets;
- require changing T-019 PURLIN disposition or T-020 shared-ridge topology.

This contract is preventive only; it authorizes no correction by itself.
