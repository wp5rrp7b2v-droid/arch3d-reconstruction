# P3.3 Stage2-C｜Attachment-Specific Interface / Connection Layer Materialization Plan V0.1

- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Authority: D-272 Stage2 design-only entry + D-273 Stage2-A lock + D-275 Stage2-B lock
- Engineering execution: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Goal

Convert the Stage2-B family-level interface/variant rules into explicit, machine-readable attachment records in bounded batches.

Stage2-C is still design/governance materialization. It does not create Blender geometry or whole-building topology.

## Batch strategy

### Batch 01｜Upper Six-Chuanfu → San-Dou → Four-Chuanfu
Use the already proven T-032 chain as the lowest-risk first production materialization target.

Scope:
- upper-six-chuanfu upper support reference;
- four-chuanfu lower support reference;
- SAN_DOU_SUPPORT connector role;
- family-level SUPPORT semantics;
- explicit PHYSICAL_CONNECTOR Connection Layer record;
- preserve exact connector geometry / lateral anchor / joinery as unresolved or replaceable.

### Later batches｜NOT AUTHORIZED BY THIS PLAN
Provisional sequencing only:
- Batch 02: primary frame stack / short-post / purlin attachment classes;
- Batch 03: column–lintel/eaves support classes;
- Batch 04: bracket-set internal attachment classes;
- Batch 05: corner-member attachment classes.

The later sequence may be revised after each batch review and is not itself approval to materialize those records.

## Materialization rules

1. Every attachment class must identify its participating approved Master family/families.
2. Interface records are engineering references unless direct evidence establishes a historical contact/joinery feature.
3. A connector role may be materialized without claiming a counted physical Registry instance.
4. UNKNOWN family count or exact geometry must remain UNKNOWN.
5. World coordinates are prohibited.
6. T-020 / RZ / FV cannot supply Stage2 placement authority.
7. A family-level attachment class does not imply every possible whole-building instance.
8. No attachment class may silently create historical joinery.
9. Every Connection Layer record must use one of:
   - PHYSICAL_CONNECTOR
   - JOINERY_FEATURE
   - CONTACT_INTERFACE
10. Body contact alone is not attachment closure.

## Batch 01 acceptance gate

Batch 01 may be locked only if:
- both participating Master interfaces are explicit;
- evidence binding preserves the direct source statement;
- 散斗 remains a connector role / reference-bound family, not a newly invented Master or counted instance;
- vertical support chain is explicit;
- exact lateral anchor is not fabricated;
- exact historical connector dimensions are not claimed;
- no world coordinates are introduced;
- no Stage3 or engineering authorization is implied.
