# MP-01A Gate B｜Ridge Support Target Datum Resolution V001

Status: **PASS / TARGET OWNER RESOLVED / NUMERIC PLACEMENT NOT YET LOCKED**
Date: 2026-10-06

## 1. Question

For the East-Seam upper-ridge Minimum Proof, what owns the upper target used by:

- `蜀柱-东缝` upper endpoint;
- `叉手-东缝-南侧` upper endpoint;
- `叉手-东缝-北侧` upper endpoint?

## 2. Decision

Create one assembly datum:

`DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM`

Canonical meaning:

> **东缝梁架平面 × 正身脊槫线 的脊部支撑节点**

English semantic:

`EAST_SEAM_FRAME_PLANE × MAIN_BODY_RIDGE_PURLIN_LINE SUPPORT NODE`

This datum is **not a historical timber component** and is **not a new V008 physical instance**.

It is an assembly-owned datum anchored to the **RIDGE_PURLIN role**.

## 3. Evidence basis

### A1 primary report

Relevant locations:

- PDF p106 / printed p91 / Fig. 2-71｜万佛殿上平槫与脊槫之高差示意图
- PDF p107 / printed p92 / Table 2-52｜万佛殿各槫高差中间距 A、B、C 归纳与推算
- PDF p109 / printed p94 / Fig. 2-73｜万佛殿梁架举折方法示意图

Fig. 2-71 directly establishes:
- a single central ridge-purlin line above the central ridge-support group;
- the Shuzhu is vertically aligned below that ridge region;
- the two diagonal Chashou converge into the same central ridge-support zone;
- the vertical relationship is expressed against the ridge-purlin / upper-purlin level system.

Table 2-52 records:
- `东缝前 C = 1245 mm`;
- `东缝后 C = 未及`;
- published measured-C mean = `1249.5 mm`;
- report rounded analysis = `82分`.

Boundary:
- C is a purlin-level height difference, not a direct Shuzhu length;
- it does not prove exact contact-face geometry;
- it does not prove the small intermediate support/block geometry below the ridge purlin.

### A2 official same-building structural statement

The official Wanfo Hall digital presentation states:

- “平梁之上设驼峰、蜀柱、叉手。”

This confirms membership in the same ridge-support system but does not independently give the upper endpoint XYZ or exact contact topology.

### Existing Master / Registry basis

`CMP-FRAME-PURLIN-001_MASTER` already recognizes the role:
- `RIDGE_PURLIN`

and explicitly keeps:
- segment length = assembly-owned;
- placement = assembly-owned;
- exact section profile = UNKNOWN;
- end/joinery geometry = UNKNOWN.

Therefore the purlin **role line** can own the datum without pretending that the current rectangular purlin envelope is the exact historical contact profile.

## 4. Why the owner is a role/node, not one purlin segment body

V008 registers the main-body ridge purlin as three physical segment records:
- `槫-正身-脊槫-西段`
- `槫-正身-脊槫-中段`
- `槫-正身-脊槫-东段`

At this Gate, the exact East-Seam segment-end ownership has not yet been independently bound.

Therefore Gate B does **not** silently choose:
- 中段 only;
- 东段 only;
- a specific historical scarf/joint between the two.

Instead:

`DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM`
is bound to the **RIDGE_PURLIN assembly role line at the East-Seam frame plane**.

Later whole-building segment placement may bind this node to one or two actual purlin segment end interfaces without changing the MP-01A component identities.

## 5. Datum semantics

```text
datum_id = DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM
coordinate_space = MP01A_ASSEMBLY_LOCAL
physical_component = false
historical_component_claim = false

frame_plane = EAST_SEAM
ridge_role = RIDGE_PURLIN

X = EAST_SEAM_FRAME_PLANE
Y = RIDGE_PURLIN_CENTERLINE
Z = RIDGE_PURLIN_LEVEL

exact XYZ = NOT YET LOCKED
exact contact face = UNKNOWN
historical joint = UNKNOWN
```

The labels X/Y/Z above are semantic coordinates; they do not yet assert a global millimetre transform.

## 6. Endpoint ownership

### Shuzhu

`蜀柱-东缝`

- lower endpoint owner: Pingliang upper ridge-support chain;
- upper endpoint owner: `DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM`;
- exact historical height: not copied from Stage1 reference fixture;
- realized length: endpoint-derived.

### Chashou South / North

`叉手-东缝-南侧`
`叉手-东缝-北侧`

- lower endpoints: Pingliang upper connection region;
- upper target: shared `DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM`;
- exact historical angle: UNKNOWN;
- realized angle / length: endpoint-derived.

This does **not** claim that all three members terminate on one exact physical contact point.
The datum represents a bounded ridge-support target region for Minimum Proof placement.

## 7. Evidence classification

| Claim | Classification |
|---|---|
| central ridge purlin exists above the ridge-support group | FACT / A1 |
| Shuzhu aligns vertically into the central ridge-support zone | FACT / A1 visual |
| Chashou pair converges into the same central ridge-support zone | FACT / A1 visual |
| Pingliang above has Shuzhu / Chashou system | FACT / A2 |
| exact timber-to-timber contact face | UNKNOWN |
| exact small intermediate support/block geometry | UNKNOWN |
| exact East-Seam ridge-purlin segment-end ownership | UNKNOWN |
| use of one assembly target datum | RECONSTRUCTED_DESIGN / PROJECT ASSEMBLY RULE |
| exact global XYZ | NOT YET LOCKED |

## 8. Gate B result

**PASS**

The upper endpoint target now has a legitimate owner:

> `RIDGE_PURLIN ROLE × EAST_SEAM FRAME PLANE`

No historical joint or exact contact surface has been invented.

## 9. Next complete step

**MP-01A Gate C｜Assembly-Local Numeric Placement Resolver**

Gate C will resolve only the minimum numbers needed to generate the first actual 3D assembly:

1. Pingliang local placement baseline;
2. Ridge target elevation/offset;
3. Tuofeng `UPPER_RIDGE_SUPPORT` assembly envelope;
4. Shuzhu endpoint-derived height;
5. South/North Chashou endpoint-derived lengths and angles.

Rules:
- prefer East-Seam direct values where available;
- any value calibrated or completed from Fig. 2-71 must be labeled `RECONSTRUCTED_DESIGN / SOURCE_IMAGE_CALIBRATED`;
- `东缝后 C = 未及` must remain UNKNOWN;
- do not substitute the 1249.5 mm family mean as an “East-Seam exact” measurement;
- no Blender build until Gate C inputs and classifications are explicit.
