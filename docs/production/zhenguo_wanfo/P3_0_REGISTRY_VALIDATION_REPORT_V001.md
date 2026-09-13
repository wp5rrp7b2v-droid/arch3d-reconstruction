# P3.0 Registry Validation Report V001

Status: **T-009 MACHINE VALIDATION PASS / P3.0 GATE REVIEW PENDING**

| 检查 | 结果 |
|---|---|
| Family / Variant / Instance coverage | 11/11 / 40/40 / 365/365 |
| Orphan family / variant / instance | 0 / 0 / 0 |
| Ontology | PASS |
| Registry schema | PASS |
| Evidence boundary | PASS |
| Determinism | PASS: sorted inputs and canonical JSON; --check byte comparison |

## 机器检查

- `schema`: PASS
- `unique_component_ids`: PASS
- `unique_variant_ids`: PASS
- `unique_instance_ids`: PASS
- `legal_ontology`: PASS
- `family_coverage`: PASS
- `variant_coverage`: PASS
- `instance_coverage`: PASS
- `audit_variant_coverage`: PASS
- `audit_instance_coverage`: PASS
- `zero_orphans`: PASS
- `component_backlinks`: PASS
- `component_semantics`: PASS
- `audit_relations`: PASS
- `variant_provenance`: PASS
- `instance_provenance`: PASS
- `parameter_evidence_preservation`: PASS
- `control_envelope_exclusion`: PASS
- `machine_instances_not_historical_count`: PASS
- `Z-006_boundary`: PASS
- `RC_boundary`: PASS
- `DG_HIS_boundary`: PASS
- `semantic_layers`: PASS
- `assembly_vocabulary`: PASS

P2 manifest SHA256: `5b10f3d83c4d72cc312c5f896e7cff5838365986612a885a310e2799e2a844a7`。Schema 使用 JSON Schema Draft 2020-12。执行 `python3 production/zhenguo_wanfo/scripts/build_p3_0_component_registry_v001.py --check` 进行只读字节复验。

本报告不批准 P3.0 Gate PASS；Product Owner / ChatGPT 后续按 D-030 做最终 Gate Review。
