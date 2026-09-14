# P3.2｜构件组合关系模型｜Gate Review

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Gate：P3.2｜构件组合关系模型
- Review date：2026-09-14
- DoD baseline：`P3_2_DEFINITION_OF_DONE_V001.md` / D-041
- Review status：**CHATGPT GATE REVIEW PASS / 9 OF 9 DOD PASS / CANONICAL HARD FAIL = 0 / PRODUCT OWNER APPROVAL REQUIRED**
- P3.3：**LOCKED UNTIL PRODUCT OWNER GATE APPROVAL**

## 1. Review Scope

本 Gate Review 独立核对 P3.2 DoD V001 的 9 项要求、三项 Gate Hard Fail、T-015 关系基础工程以及 T-016 代表性构件组合验证。T-015 已由 D-042 批准关闭；T-016 已由 D-045 批准关闭。

P3.2 的判定目标不是完成整座万佛殿，而是确认：正式构件身份、组合关系、接口、建筑层级参数、证据边界、自动验证与确定性重建已经构成可供 P3.3 直接使用的基础体系。

## 2. Definition of Done Review｜9/9 PASS

| DoD | Gate Review | 主要依据 | 结论 |
|---|---|---|---|
| DoD-01｜组合范围与构件资格 | P3.1 六个 approved Master 以原 component identity 进入关系体系；Proxy / Control / Envelope / Deferred / UNKNOWN 保持原资格与证据边界。T-016 的 Control、Proxy、Assembly Unit 均明确为非历史工程对象。 | T-015 6/6 mapping；T-016 assembly registry | **PASS** |
| DoD-02｜构件关系分类体系 | 正式关系固定为 SUPPORT / CONNECT / LOCATE / REPEAT / BELONG 五类；机器可读定义已建立，T-016 实际代表性覆盖 5/5。 | T-015 relationship types；T-016 5/5 coverage | **PASS** |
| DoD-03｜构件接口与定位规则 | T-015 建立 6 Master / 18 个基础局部接口；T-016 进一步建立柱上承托面、栌斗下承托面、中心轴、梁架层位 datum、重复起点/方向等真实组合所需接口。A/C Blender 位置由接口与参数派生，不以人工 world-space 摆放作为正式输入。 | T-015 interface foundation；T-016 A/C | **PASS** |
| DoD-04｜代表性组合单元与关系覆盖 | A=`AU-COLUMN-LUDOU-001` 覆盖竖向承托；B=`AU-FRAME-TIER-001` 覆盖梁架层位/连接语义；C=`AU-COLUMN-GRID-001` 覆盖重复。三单元均引用 Registry identity，runtime instance 不生成新 component_id。 | T-016 assembly registry / relationship graph | **PASS** |
| DoD-05｜尺寸与参数传递 | C 由建筑层级 `PM-005=3505.7mm` 驱动 spacing；B 在缺少 approved building-specific 六椽栿全长时主动阻断实际几何；1000mm reference specimen 注入 actual/building length 会稳定触发 Hard Fail。 | T-015 parameter isolation；T-016 B/C | **PASS** |
| DoD-06｜史料依据与不确定性边界 | A 保持 Z-006 UNKNOWN、Z-006-RC-01 replaceable RC、joinery UNKNOWN；B 保持 connector identity / joinery / historical full length UNKNOWN，Control/Proxy 不历史化；C 将 PM-005 的 CONFIRMED 测量证据与 REPEAT 的 PROJECT_RULE 分离。 | T-016 A/B/C evidence boundaries | **PASS** |
| DoD-07｜机器验证与组合关系完整性 | T-015 31/31 checks + 21/21 negative fixtures；T-016 65/65 checks + 15/15 negative fixtures；canonical errors=0。三项 Gate Hard Fail 均有可触发测试并在 canonical 数据中为 0。 | 两份 validation reports | **PASS** |
| DoD-08｜确定性重建与参数变更验证 | A 完成 interface-driven Blender build、independent reopen、deterministic regeneration；C 完成 PM-005-driven runtime instances、2→3→2 mutation / rebuild / reopen / restore，恢复后 canonical signature 一致。 | T-016 Blender signatures / validation | **PASS** |
| DoD-09｜P3.3 整殿重建就绪性验证 | Schema、node/interface/relationship structures、assembly-unit registry、runtime-instance pattern、building-parameter isolation、validator、review assets 均已建立。P3.3 可以在现有五类关系和接口/参数机制上扩展更多 building-level relationship instances，无需重新发明基础组合体系。 | T-015 foundation + T-016 representative implementation | **PASS** |

**DoD Final：9 / 9 PASS。**

## 3. Gate Hard Fail Review

| Hard Fail | Canonical Status | Gate Review |
|---|---|---|
| `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` | 0；1000mm 六椽栿 reference specimen 未进入实际建筑长度，非法注入可稳定触发拒绝。 | **PASS / NOT TRIGGERED** |
| `SILENT_HISTORICIZATION` | 0；Proxy / Control / Assembly Unit / UNKNOWN 均保持非历史或未知状态。 | **PASS / NOT TRIGGERED** |
| `BAKED_MANUAL_ASSEMBLY` | 0；A/C 可从 Registry + relation/interface + parameters 重建并独立重开。 | **PASS / NOT TRIGGERED** |

**Canonical Hard Fail = 0。**

## 4. P3.3 Readiness Judgment

### 4.1 已经具备的基础机制

P3.3 可直接继承：

1. approved component identity / Registry；
2. SUPPORT / CONNECT / LOCATE / REPEAT / BELONG 五类关系；
3. point / axis / plane 与关系语义接口；
4. Assembly Unit 与 runtime instance 组织方式；
5. building-level parameter → relationship / placement → derived transform 的参数传递方式；
6. evidence status / provenance / replaceability / historical claim 分层；
7. reference-length isolation 与 non-historicization Hard Fail；
8. deterministic rebuild / independent reopen / mutation-restore validation 方法。

因此，P3.3 新增整殿关系实例、更多局部接口或具体建筑参数属于**在既有体系中扩展数据与实例**，不属于重新设计基础关系体系。

### 4.2 Carry-forward constraints｜不是 P3.2 blocker

以下内容继续带入 P3.3，但不要求在 P3.2 内消除：

- 六椽栿 historical full length 继续 `UNKNOWN / null`；在取得独立 approved building-specific full length 前，相关实际全长几何必须继续 BLOCKED；
- Z-006 继续 `UNKNOWN / null / DO_NOT_LOCK`，Z-006-RC-01 保持 replaceable `REASONABLE_COMPLETION`；
- 具体榫卯、隐藏连接、45°转角、隐角梁等继续按现有 evidence boundary 处理；
- Deferred 构件不因整殿重建需求自动升级为 historical Master；需要时仍须走独立证据/资格流程；
- P3.3 可以新增具体 building-level interfaces / relationship instances，但不得新增第六类基础关系或绕开 P3.2 Schema / Validator。

B 单元的 `FULL_LENGTH_GEOMETRY_BLOCKED` 是**正确的就绪行为**，不是失败：它证明系统能在缺乏合法建筑参数时阻止错误几何，同时等待未来参数进入同一既有机制。

## 5. Visual / Human Review

T-016 四张正式 review PNG 已按 RC-015 从 GitHub 直接调阅并实际逐张打开目视审核，4/4 PASS：A 能组合、B 能正确阻断、C 能重复，Overview 对三种系统行为的表达与 evidence boundary 一致。

## 6. Final Gate Review Conclusion

- DoD：**9 / 9 PASS**
- Canonical Hard Fail：**0**
- T-015：**PASS / APPROVED / CLOSED / D-042**
- T-016：**PASS / APPROVED / CLOSED / D-045**
- P3.3 foundational readiness：**PASS**
- Additional engineering task required before Gate decision：**NO**
- ChatGPT Gate Review：**PASS**
- Product Owner Gate Approval：**REQUIRED / PENDING**

### Recommended Product Owner Decision

建议批准：

> **P3.2｜构件组合关系模型 = PASS / APPROVED / CLOSED**

批准后：

- P3 Gate Progress：2/4 → 3/4；
- P3.3｜构件驱动整殿重建正式 UNLOCKED / ENTERED；
- P3.3 开始前应先定义并批准其 Definition of Done，不直接创建整殿工程任务。

在 Product Owner 明确批准前，P3.2 仍保持 `ACTIVE / GATE REVIEW PASS / PO APPROVAL REQUIRED`，P3.3 继续 LOCKED。