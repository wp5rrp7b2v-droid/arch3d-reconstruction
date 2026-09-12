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

**DoD-07 roundtrip: PASS (T-008 V003).** The V001 local semantic snapshot records per-instance geometry bounds, mesh and variant mapping, transforms, evidence metadata, collection mapping and camera assets. GitHub Actions run [34695870243](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/actions/runs/34695870243) used its own `github.token` to retrieve the already registered Git blob, verified the decoded input SHA256 before starting Blender, and completed Blender 4.5.13 cloud input and independent reopen semantic QC. The returned artifact was downloaded and independently reopened in Local Blender 3.6.23. The local return semantic summary exactly matches the V001 snapshot; its 34/34 structural checks pass. No core geometry, family/variant/instance, metadata, collection or camera difference was found.

### V002 continuation — temporary Git blob tag

The V001 canonical `.blend` remains unchanged at SHA256 `ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`. Under the V002 Task Contract, it was written as Git blob `23797dbd360ba67b8195d988f2161ff9eaf37d48` and pushed through temporary lightweight tag `p2-3-transport-v001`. At the V002 checkpoint, remote `ls-remote` advertised that exact blob SHA. Two independent attempts to fetch the tag into a disposable repository failed with `Empty reply from server`; therefore the V002 section 4 transport condition was **HOLD**. The Blender 4.5 workflow had not been dispatched and no artifact or local-return QC existed. The tag was retained at that checkpoint because V002 section 7 allowed cleanup only after a successful workflow, artifact download and local return validation. The exact historical record is `validation/P2_3_V002_TRANSPORT_QC_V001.json`.

### V003 continuation — authenticated Actions blob retrieval

Workflow commit `d595a587c72dc4e76afac249d8a4e667ac772fd0` was pushed to private `main`, then normal commit tag `p2-3-roundtrip-run-v003-001` triggered the successful run. The runner Git Blobs API returned the expected blob SHA `23797dbd360ba67b8195d988f2161ff9eaf37d48`; decoded input SHA256 was the frozen `ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`. The cloud input and reopen semantic SHA256 both equal the V001 reference `1e6a1ab2c6f63d0d7772e69b189ab91447aaf8735285df6e9ab1ffb09d232750` (365 instances, 40 variants, 11 families). Artifact `P2_3_CLOUD_ROUNDTRIP_V001` was downloaded with ZIP SHA256 `09ebba82b33f6d5c2fcb62d4dd979289a73c8464f285cba823150d0ba9f66abb`; the returned `.blend` SHA256 is `d2c80c4e2e0ae278ad4b7055df6871e00bfb85ecf981fbc796ddd2f5e919efc0` and remains local only.

Local Blender 3.6.23 independently reopened the returned file twice: semantic compare **PASS**, and full machine QC **PASS 34/34**. The frozen V001 candidate separately passed **33/33** automated tests and **34/34** machine QC again. The first sandboxed regression attempts crashed during Metal GPU initialization before model validation; both checks passed when Blender had native graphics access. The known P0.2 UI-region-only warnings appeared on the 4.5→3.6 return, without any new core semantic loss. Detailed run, hashes, artifact and QC paths are archived in `validation/P2_3_V003_ROUNDTRIP_QC_V001.json`.

After canonical evidence commit `496ddb62fd095e63c49c719e906ea6244dd76f38` was pushed, both temporary transport and run-trigger tags were deleted remotely and locally; an independent remote tag listing returned no matching refs. The `.blend` remains local only and did not enter the `main` tree. This result supports a **T-008 V003 engineering PASS recommendation**; it does not decide the P2.3 Gate. Independent engineering review and Product Owner review of the six formal images and evidence diagnostic remain required.

## Historical statement boundary

This is a controlled, evidence-traceable **963 reconstruction candidate**. A more complete model does not reduce the unresolved historical uncertainty. `Z-006` remains unknown; the D-023 production candidate is replaceable; `DG-114`, `HIS-002`, 45° corner joints, mortises and hidden-angle beam disputes are not promoted to exact historical conclusions.
