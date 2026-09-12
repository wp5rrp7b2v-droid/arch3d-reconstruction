# T-008 P2.3 Integrated Candidate Engineering Validation V001

Date: 2026-09-12
Gate decision: **not made here**. Product Owner review remains separate.

The candidate is rebuilt by the approved P2.2 generator and a P2.3 component-library integration step. The approved P2.2 local `.blend`, script and manifest are hash checked before build. The resulting 365 stable mesh instances use 11 families and 40 variants. Repeated members share mesh prototypes within each variant; all instances have family, variant, parameter, override, evidence and originality metadata. P2.2 grid, gable and frame controls remain diagnostic. Separate bounded P2.3 frame connectors make the column–frame–roof control chain readable without claiming exact historical joints.

The roof uses six continuous envelope strips over approved control intervals, together with seven purlins and 36 rafters. Bracket presentation geometry includes 88 arm members and 88 diagrammatic contact blocks. These are evidence-bounded medium-LOD shapes, not exact 963 joinery or a `DG-114` small-dou specification. No walls, doors, windows, decoration or other unapproved detail were added to complete the image.

## Engineering checks

- Independent Blender 3.6 reopen machine QC: **PASS, 34 checks, 0 errors**. The validator compares saved instances to the integration manifest, verifies prototype sharing, collection separation, formal input hashes, P2.2 topology/dimensions, bracket contact continuity and roof strip seams.
- Two consecutive clean rebuilds: **PASS** for semantic summary, instance IDs, family/variant mapping, metadata and key dimensions. Two independently reopened test builds: **PASS**. Binary `.blend` hashes need not match.
- Test-only D-023 RC replacement: **PASS**. Changing the MOD-005 → MOD-006 source and matching sidecar cache changed all dependent candidate height/roof controls while `Z-006` stayed null. The formal files were unmodified.
- Test-only bracket contact variant change: **PASS**. Changing the graphic library fraction from 0.5 to 0.6 changed all 88 corresponding instance variant IDs; unrelated family mappings stayed stable.
- Numeric-literal/manual-drift audit: **PASS**. No formal historical dimension was embedded as a geometric constant in the P2.3 generator. The only formal numeric literal match is the topology count 12; other large literals are camera, image, hash buffer or clip settings. No edit-mode or hand-transform correction is used.
- Six review PNGs: `PLAN`, `ELEVATION`, `AXON`, `EXTERIOR_3Q`, `STRUCTURE_DETAIL`, `EVIDENCE_DIAGNOSTIC`. Exterior, structure-detail and evidence views were visually inspected for spatial continuity and evidence separation.

## Cloud roundtrip

**HOLD**. The workflow and version-aware semantic QC script are prepared. The local Blender 3.6 snapshot records per-instance geometry bounds, mesh and variant mapping, transforms, evidence metadata, collection mapping and camera assets. Two T-008 commits exist locally. Initial automatic approval review rejected the push; the Product Owner then explicitly authorized the exact private repository and temporary `.blend` transport. Three standard Git push attempts subsequently failed with `send-pack: unexpected disconnect while reading sideband packet`, and remote `main` remained at the pre-T-008 commit. Automatic approval review also rejected a custom API credential-extraction attempt, so that route was not used. The Cloud Blender 4.5 run and returned Blender 3.6 validation have not occurred. DoD-07 and canonical GitHub archive remain incomplete.

## Historical statement boundary

This is a controlled, evidence-traceable **963 reconstruction candidate**. A more complete model does not reduce the unresolved historical uncertainty. `Z-006` remains unknown; the D-023 production candidate is replaceable; `DG-114`, `HIS-002`, 45° corner joints, mortises and hidden-angle beam disputes are not promoted to exact historical conclusions.
