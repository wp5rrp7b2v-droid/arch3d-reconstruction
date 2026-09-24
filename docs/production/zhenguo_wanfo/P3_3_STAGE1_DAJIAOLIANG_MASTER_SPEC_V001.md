# P3.3 V002 Stage 1｜大角梁 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-124**  
**日期：2026-09-24**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**资料主权：D-099 / RC-019**  
**复原方法：D-108 / RC-020｜Evidence-Constrained Reconstruction**  
**视觉门：D-076 PASS WITH GEOMETRY BOUNDARY**  
**任务性质：正式锁定规格；不等于 T-030 工程执行授权**

## 1. Component Identity

- 中文名：大角梁
- component id：`CMP-FRAME-DAJIAOLIANG-001`
- master id：`CMP-FRAME-DAJIAOLIANG-001_MASTER`
- master version：`V001`
- physical instances：**4**
- locations：东北角 / 东南角 / 西南角 / 西北角
- family：角梁
- geometry variant count：**0**

锁定一个 shared parametric Master。

四个角部的直接实测截面差异由 instance parameters 表达，不复制为四个独立 Master，也不建立四个 Geometry Variant。

## 2. Authoritative Inputs

### A1
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct locator：
- PDF p88–89
- printed p73–74
- §2.3.1.7｜角梁
- Fig. 2-50
- Table 2-44

Formal evidence record：
`docs/evidence/zhenguo_wanfo/P3_3_DAJIAOLIANG_DIRECT_SOURCE_BINDING_V001.md`

### A2
山西文物数字博物馆·万佛殿专题及已登记同建筑结构语义。

允许使用：
- 转角铺作与角梁的层位 / 承托拓扑
- 同建筑视觉与结构交叉验证

不作为：
- 精确长度
- 精确45°坐标
- 精确坡度
- 榫卯尺寸 authority

### Canonical Registry
`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`

V008/CURRENT locks four 大角梁 physical instances.

## 3. Measurement Contract

A1 direct measured instance sections：

| Registry location | A1 label | width / 广 | thickness / 厚 |
|---|---|---:|---:|
| 东南角 | 东南大角梁 | 240 | 210 |
| 东北角 | 东北大角梁 | 216 | 187 |
| 西南角 | 西南大角梁 | 218 | 206 |
| 西北角 | 西北大角梁 | 226 | 199 |

Report-published mean：
- width = **225 mm**
- thickness = **200.5 mm**

Independent recompute：
- width = **225 mm**
- thickness = **200.5 mm**

Locked:
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = false`
- `sample_to_instance_mapping = DIRECT_LOCKED`

The four directly measured instance sections are production evidence and must not be collapsed to the family mean.

## 4. Family Reference Specimen

Stage1 canonical family reference body：

**1000 × 225 × 200.5 mm**

Axes:
- +X = longitudinal
- +Y = 广 / width
- +Z = 厚 / thickness

Origin:
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform:
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

The 1000 mm length is:
- `RECONSTRUCTION_REFERENCE_LENGTH`
- non-historical
- replaceable
- Master specimen only

The 225 × 200.5 section is:
- `DIRECT_MEASURED_REPORT_FAMILY_MEAN`
- family-reference specimen only
- not a claim that all four building instances share the same section

## 5. Instance Section Contract

One shared Master must support four locked instance sections:

- 东南角 = 240 × 210 mm
- 东北角 = 216 × 187 mm
- 西南角 = 218 × 206 mm
- 西北角 = 226 × 199 mm

Policy:
- section parameters are instance-owned measured inputs
- changing width/thickness does not create a new Master identity
- changing width/thickness does not create a Geometry Variant
- the four mappings are direct measured facts and are not replaceable by the family mean without a new source/decision

## 6. Endpoint-driven Assembly Geometry

Actual building instance length and orientation are assembly-owned.

For an instance:
- `V = P_end - P_start`
- `L = ||V||`
- `P_center = (P_start + P_end) / 2`
- local +X aligns to `V`

Therefore:
- actual length = endpoint-derived
- actual orientation = endpoint-derived
- actual installation angle = endpoint-derived
- Master stores no fixed historical full length
- Master stores no fixed 45° installation angle

Stage1 does not lock the final four building endpoint coordinates.

## 7. End / Joinery Boundary

Stage1 V001:
- body = straight rectangular bounding envelope
- reference end profile = `STRUCTURAL_SIMPLIFIED_FLAT_END`
- historical end profile = `UNRESOLVED_METADATA`
- mortise/tenon = `NOT_MODELED_AT_STAGE1`
- notch/groove = `NOT_MODELED_AT_STAGE1`

Later reconstructed end treatment may be added only if required for collision/visual closure or supported by new evidence, and must remain explicitly non-historical unless direct evidence supports it.

## 8. Related-component Isolation

This Master includes only 大角梁.

Explicitly excluded:
- 子角梁
- 隐角梁
- 隐衬角栿 / 递角栿 family members
- wing-corner rafters

Current Registry treatment remains unchanged:
- 子角梁 = separate Master scope
- 隐角梁 = PARAMETRIC_COMPLETION / not Master-tracked

No related component may be silently absorbed into `CMP-FRAME-DAJIAOLIANG-001_MASTER`.

## 9. Variant Policy

V001:
- canonical Master count = 1
- Geometry Variant count = 0

Do not create Variant for:
- NE / SE / SW / NW placement
- different direct-measured section parameters
- different endpoint-derived length
- different endpoint-derived orientation
- mirror / rotation

A future Variant requires a stable repeated body-form difference that cannot be represented by the locked parametric Master contract.

## 10. Review Board

Required six panels:
1. AXON
2. LONG_SIDE
3. END_SECTION
4. DIMENSION_AND_PARAMETRIC_LENGTH
5. PLACEMENT_AND_ENDPOINT_LOGIC
6. SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY

END_SECTION must display:
- family mean specimen 225 × 200.5
- all four direct instance sections with location labels
- clear statement that family mean does not overwrite instance measurements

PLACEMENT_AND_ENDPOINT_LOGIC must prove:
- same Master identity
- at least two endpoint fixtures with different orientation/length
- no fixed 45° Master angle
- no 1000 mm building-length leakage

## 11. Geometry Prohibitions

V001 must not:
- replace four measured instance sections with 225 × 200.5
- create four duplicate Master assets
- create four Geometry Variants solely from measured section parameters
- hard-code 1000 mm as building length
- hard-code 45° as historical installation angle
- invent exact corner-node coordinates
- invent end cuts / mortise / tenon / grooves
- absorb 子角梁 / 隐角梁 / 隐衬角栿
- claim exact 963 originality

## 12. Acceptance Boundary

The Master Spec is locked by D-124.

Next allowed step:
- establish `T-030｜P3_3_DAJIAOLIANG_MASTER_V2_V001` Task Contract

Not authorized by this Spec:
- production branch
- PR
- GitHub Actions / Blender
- first-article acceptance
- Catalog/V008 approved binding
- Stage1 PASS
- Stage2
- T-018 resume
