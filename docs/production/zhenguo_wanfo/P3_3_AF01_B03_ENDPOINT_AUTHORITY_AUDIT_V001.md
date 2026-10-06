# AF-01 / B03｜Shuzhu / Chashou / Tuojiao Endpoint Authority Audit V001

- Date: **2026-09-30**
- Task: **AF01-B03**
- Status: **STARTED / AUTHORITY AUDIT COMPLETE / ENDPOINTS NOT YET LOCKED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: 蜀柱×1 / 叉手×2 / 托脚×4 for the east-seam first article only

## 1. Purpose

B03 resolves the seven endpoint-driven members remaining after B01+B02.

This audit answers only:

1. what endpoint authority already exists;
2. what numeric anchor planes/nodes are already usable;
3. where a real ambiguity remains.

It does not generate Blender and does not mutate Masters or Registry.

## 2. Existing locked component contracts

### Shuzhu

Master contract:

- member type = `VERTICAL_RIDGE_SUPPORT_POST`
- `P_lower = PINGLIANG_UPPER_SUPPORT_REGION`
- `P_upper = RIDGE_SUPPORT_LOWER_CONNECTION_REGION`
- length = `norm(P_upper-P_lower)`
- local +X aligns with endpoint vector.

### Chashou

Master contract:

- member type = `DIAGONAL_RIDGE_SUPPORT_MEMBER`
- `P_lower = PINGLIANG_UPPER_CONNECTION_REGION`
- `P_upper = RIDGE_SUPPORT_CONNECTION_REGION`
- length and angle are endpoint-derived;
- fixed historical angle is prohibited.

### Tuojiao

Master / Stage2-C contract:

- member type = `DIAGONAL_FRAME_SUPPORT`
- same-building structural semantic = `SUPPORTS_ENDS_OF_FOUR_CHUANFU`
- four AF-01 instances are role-bound to:
  - north lower purlin
  - north upper purlin
  - south lower purlin
  - south upper purlin
- exact contact XYZ and angle remain unresolved.

## 3. Existing AF-01 numeric anchors

Inherited from B01/B02 and locked G2/G3 intermediate outputs:

- slice X = **+2218.5 mm**
- Upper-Six top = **5337.1 mm**
- Four-Chuanfu bottom/support plane = **5658.4 mm**
- Four-Chuanfu top = **6084.9 mm**
- Pingliang bottom/support plane = **6406.2 mm**
- Pingliang EW production section guang = **395.5 mm**
- therefore Pingliang execution-body top = **6801.7 mm**

The Pingliang 395.5 mm value is the approved EW family production mean; raw 390/401 samples remain unmapped east↔west.

B03 may use `6801.7 mm` only as an AF-01 execution-body surface, not as a direct measured East-seam historical elevation.

## 4. Source support for ridge-system topology

The report / locked source bindings establish:

- Pingliang lies below the ridge-support system;
- Pingliang above carries hump / Shuzhu / Chashou;
- Shuzhu is vertical;
- Chashou is a north/south paired diagonal system;
- Fig. 2-73 depicts the idealized symmetric ridge triangle in the east/west main-frame logic.

Therefore the plan anchors are already deterministic for AF-01:

- Shuzhu lower plan anchor: `Y=0`
- Chashou north lower plan anchor: `Y=-1836.0`
- Chashou south lower plan anchor: `Y=+1836.0`
- shared ridge-support plan anchor: `Y=0`

All remain at slice `X=+2218.5`.

What is still required is one AF-01-local **ridge-support connection Z**. It must be derived from same-building roof/frame evidence; the legacy T-018 RZ purlin Z values remain planning/cross-check only in the current AF-01 spec and are not silently promoted here.

## 5. Source support for Tuojiao topology

Direct source / same-building authority establishes:

- main-frame upper/lower purlin roles use Tuojiao;
- Four-Chuanfu ends are supported by Tuojiao;
- the east seam has four instances:
  - `托脚-东缝-北下平槫`
  - `托脚-东缝-北上平槫`
  - `托脚-东缝-南下平槫`
  - `托脚-东缝-南上平槫`
- Fig. 2-73 visually shows diagonal support members stepping between the beam/purlin tiers.

However the current locked records do **not** uniquely state, for each of the four instances:

- which physical end is the Four-Chuanfu contact;
- which exact surface/point on the named purlin support node is the opposite endpoint;
- whether the lower/upper-purlin pair shares a common Four-Chuanfu endpoint or uses two vertically separated end-region anchors.

This is a real instance-mapping gap, not a missing component-family problem.

## 6. Prohibited shortcut

B03 must not do any of the following:

- assign Tuojiao endpoints merely from the instance name;
- force a lower-purlin Tuojiao between two nodes with identical Y and call the result a diagonal member;
- reuse T-018 FRAME_SUPPORT proxy endpoints;
- read a fixed angle by eye and bake it into the Master;
- treat the 1000 mm Master reference length as building length;
- turn Fig. 2-73 idealized geometry into DIRECT_MEASURED historical endpoint coordinates.

## 7. Audit result

B03 is now reduced to **two bounded resolvers**:

### B03-R｜Ridge-support endpoint resolver
Outputs:
- Shuzhu P_lower / P_upper
- north Chashou P_lower / P_upper
- south Chashou P_lower / P_upper

Known already:
- all X;
- all lower Y;
- shared upper Y=0;
- Pingliang execution top surface Z=6801.7.

Only one shared ridge-support connection Z remains to resolve.

### B03-T｜Tuojiao endpoint mapping resolver
Outputs:
- four P_lower / P_upper pairs.

Known already:
- four instance identities;
- north/south role;
- upper/lower-purlin role;
- Four-Chuanfu support semantic;
- all AF-01 beam tier coordinates.

Only the exact per-instance endpoint-to-node mapping remains to resolve from Fig. 2-73 / same-building source geometry.

## 8. Fastest next action

Next controlled step:

**AF01-B03-R｜resolve the single shared ridge-support Z and close Shuzhu + both Chashou endpoints.**

Do not resolve Tuojiao in the same step.

After B03-R is locked, execute B03-T as the final AF-01 blocker.

No Blender.
