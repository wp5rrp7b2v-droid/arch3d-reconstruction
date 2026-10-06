# MP-01B Gate H｜Evidence Recheck V001

Status: **EVIDENCE REVIEW FAIL / ENGINEERING REVISION REQUIRED / NO BLENDER**
Date: 2026-10-06

## 1. Trigger

Product Owner questioned why the left/right support connections in the Gate H Review Board appeared different and requested a source recheck without changing the model merely to make it look better.

The recheck compares:
- SRC-ZG-WF-001 detailed survey report;
- Drawing 11 East-Seam section / point-cloud comparison;
- Table 2-49 interior column-dou measurements;
- Table 2-52 vertical decomposition;
- SRC-ZG-WF-002 / S15 as a secondary cross-check;
- A2 official same-building description.

## 2. Primary-source finding A — Gate H's 306 mm decomposition is wrong

SRC-ZG-WF-001, PDF p107 / printed p92, immediately below Table 2-52 states:

- 下平槫与上平槫之高差 = 61分；
- 其中 **四椽栿、驼峰、襻间柱斗平欹共垫高40分**.

This directly invalidates the Gate F/G/H interpretation:

`306 mm = Tuofeng height + Interior Linggong total height`

The 20-fen remainder after the Four-Chuanfu is not identified by the source as “Tuofeng + Linggong height”. The report explicitly includes the **襻间柱斗平欹** in that vertical decomposition.

Therefore these Gate H derived values are not evidence-supported:
- Tuofeng residual height = 91 mm;
- Linggong base/top = Z 91 / 306;
- direct additive chain `Tuofeng 91 + Linggong 215 = 306`;
- direct contact planes `Tuofeng→Linggong Z=91` and `Linggong→Pingliang Z=306`.

## 3. Primary-source finding B — an interior column-dou family is directly measured

SRC-ZG-WF-001, PDF p99 / printed p84, Table 2-49:

`万佛殿襻间/隔架用柱斗实测与分析表`

directly measures the interior `柱斗` used in purlin/spacer bracket contexts.

Reported means include:
- 总宽 = 332.1 mm;
- 下宽 = 230.0 mm;
- 总高 = 225.1 mm;
- 平高 = 45.0 mm;
- 欹高 = 88.1 mm;
- a depth-direction mean = 353.6 mm (field must be re-read against the table heading before engineering use).

This does **not** yet prove that the exact East-Seam Four-Chuanfu→Pingliang node uses this mean unchanged.

It does prove that the prior Gate H six-object stack cannot claim the directly documented interior support system contains only:
`Four-Chuanfu + Tuofeng + Linggong + Pingliang`.

The column-dou role must be resolved before the next build.

## 4. Primary-source finding C — do not rotate the Linggong just because Gate H looked odd

Drawing 11 (PDF p292 / printed p277) shows the East-Seam frame section with a bracketed support assembly at each Pingliang end.

The section visibly contains:
- a hump/support form on the lower beam;
- block/dou-like rectangular elements;
- a gong-like curved horizontal profile under the Pingliang end.

This is consistent with a bracket assembly rather than the Gate H direct three-body stack.

Importantly, the drawing does **not** support the previous chat suspicion that the support group should simply be shifted inward or that the Linggong should automatically be rotated 90°.

Current decision:
- support stations at the Pingliang ends: **retain as candidate / no change yet**;
- Linggong long-axis orientation: **retain as candidate / do not rotate merely for appearance**;
- exact axis and target-instance geometry remain subject to source-labelled node resolution.

## 5. S15 cross-check

SRC-ZG-WF-002 / S15 distinguishes:
- `横栱方向`;
- `华栱方向`;

and Table 4 treats `令栱` with the small horizontal-gong family in its scale discussion.

S15 therefore confirms that gong directionality is a real construction variable and must be handled explicitly.

However S15 is a same-building scholarly interpretation and primarily analyzes bracket-set scale logic. It does not by itself identify the exact interior Four-Chuanfu→Pingliang node.

Classification:
`SECONDARY_SCHOLARLY_SAME_BUILDING / CROSS-CHECK ONLY`.

## 6. A2 official description

A2 states:

`四椽栿上用驼峰、令栱承平梁。`

This is retained as direct role evidence for Tuofeng and Linggong.

It is an abbreviated structural description. It must **not** be read as evidence that no Dou exists between those named members when SRC-ZG-WF-001 directly documents interior column dou and the East-Seam section visibly contains block/dou elements.

## 7. Gate H verdict

### Machine result

Retained:

`MACHINE PASS / 51 of 51`

The software correctly executed the Gate G contract.

### Evidence result

Changed to:

`EVIDENCE REVIEW FAIL`

Reason:
the Gate G contract itself encoded an unsupported vertical decomposition and omitted a directly relevant physical component family.

Therefore:

> **Gate H is not approved as MP-01B Minimum Proof.**

This is not a Blender failure.

It is an evidence-contract failure discovered by Product Owner visual review and primary-source recheck.

## 8. What is NOT being changed

No evidence currently justifies changing:
- ±1836 support-station candidate;
- Pingliang realization length solely because of this finding;
- Four-Chuanfu realization length solely because of this finding;
- South/North symmetry;
- Linggong axis merely because the simplified render looked strange.

No Blender rebuild is authorized in this recheck.

## 9. What must be resolved before a corrected build

Exactly four questions:

1. What is the target-node `柱斗` identity: the Table 2-49 purlin/spacer column-dou family or another specific dou family?
2. What part of the 20-fen remainder belongs to Tuofeng versus the relevant Dou geometry?
3. How does the Linggong seat in/over the Dou, i.e. what vertical overlap replaces the false additive `91 + 215` stack?
4. Does Drawing 11 plus the target photographs establish the Linggong long axis and center placement strongly enough to lock them, or must they remain reconstructed/replaceable?

Until these are answered:
- Gate F numeric support-stack interpretation is superseded for build use;
- Gate G build-preparation contact planes are superseded for build use;
- Gate H remains an archived machine-proof artifact only;
- MP-01A is unaffected;
- PR #56 remains open / merge not authorized.
