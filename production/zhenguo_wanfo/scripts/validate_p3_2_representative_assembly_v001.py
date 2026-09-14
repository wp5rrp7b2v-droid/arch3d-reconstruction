"""T-016 canonical validator and review report. Blender signatures come from independent CLI reopens."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import p3_2_representative_common_v001 as t
import validate_p3_2_relationship_foundation_v001 as foundation

ROOT=t.ROOT
BASE=t.BASE
REPORT=BASE/'validation/P3_2_REPRESENTATIVE_ASSEMBLY_VALIDATION_V001.json'
SIG_PATHS={'A_reopen':'/tmp/t016_a_reopen_sig.json','A_regen':'/tmp/t016_a_regen_sig.json','C_reopen':'/tmp/t016_c_reopen_sig.json','C_restore':'/tmp/t016_c_restore_sig.json','C_mutation_reopen':'/tmp/t016_c_mutation_reopen_sig.json'}
REVIEW=BASE/'review/P3_2/representative_assembly_v001'
BLENDS={'A':BASE/'assembly/local/AU-COLUMN-LUDOU-001_V001.blend','C':BASE/'assembly/local/AU-COLUMN-GRID-001_V001.blend'}
HARD={'REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY','SILENT_HISTORICIZATION','BAKED_MANUAL_ASSEMBLY','EVIDENCE_STATUS_UPGRADE','DUPLICATE_COMPONENT_IDENTITY','BLOCK_BYPASS','PROTECTED_BASELINE_MUTATION','P3_3_SCOPE_LEAK'}

def main():
    graph,units,nodes,interfaces,types,schema=t.inputs()
    result=t.derive(graph)
    errors=t.validate(graph,result)
    checks={}
    def check(name,value,code='VALIDATION_FAILED'):
        checks[name]={'status':'PASS' if value else 'FAIL','error_code':None if value else code}
    foundation_checks,_=foundation.canonical_checks()
    check('t015_foundation_31_of_31',len(foundation_checks)==31 and all(v['status']=='PASS' for v in foundation_checks.values()),'FOUNDATION_INVALID')
    for letter in 'ABC':
        check(f'{letter}_schema_topology_valid',not foundation.validate_graph(graph['unit_graphs'][letter],nodes,interfaces,types,schema),'ASSEMBLY_GRAPH_INVALID')
    check('representative_validator_zero_error',not errors,str(errors))
    ids=[u['assembly_unit_id'] for u in units['units']]
    check('three_unique_units',len(ids)==len(set(ids))==3)
    check('assembly_units_organizational',all(u['evidence_status']=='PROJECT_RULE' and not u['historical_claim'] for u in units['units']),'SILENT_HISTORICIZATION')
    check('approved_component_mapping_6_of_6',len(nodes['nodes'])==6 and {n['node_id'] for n in nodes['nodes']}=={m['component_id'] for m in t.read(t.LIBRARY)['masters']},'DUPLICATE_COMPONENT_IDENTITY')
    check('five_relationship_types_covered',{r['relation_type'] for g in graph['unit_graphs'].values() for r in g['relationships']}=={'SUPPORT','CONNECT','LOCATE','REPEAT','BELONG'})
    check('no_historical_relation_claims',all(r['historical_claim'] is False and r['evidence_status']=='PROJECT_RULE' for g in graph['unit_graphs'].values() for r in g['relationships']),'SILENT_HISTORICIZATION')
    a=graph['unit_graphs']['A']; b=graph['unit_graphs']['B']; c=graph['unit_graphs']['C']
    ai={x['interface_id']:x for x in a['interfaces']}
    ar={x['relationship_id']:x for x in a['relationships']}
    check('a_members_complete',{n['node_id'] for n in a['nodes']}=={'CMP-COLUMN-001','CMP-LUDOU-COLUMN-001','AU-COLUMN-LUDOU-001'})
    check('a_top_support_interface',ai['CMP-COLUMN-001__TOP-SUPPORT-PLANE']['local_datum'].get('z_parameter_ref')=='CMP-COLUMN-001:height_mm')
    check('a_lower_support_interface',ai['CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE']['local_datum']['origin_mm']==[0,0,0])
    check('a_support_relation',ar['A-R01']['relation_type']=='SUPPORT' and ar['A-R01']['source_interface']=='CMP-COLUMN-001__TOP-SUPPORT-PLANE')
    check('a_locate_relation',ar['A-R02']['relation_type']=='LOCATE' and ar['A-R02']['source_interface']=='CMP-COLUMN-001__AXIS')
    check('a_belong_2_of_2',sum(r['relation_type']=='BELONG' for r in a['relationships'])==2)
    check('a_support_plane_alignment',result['A']['support_plane_world_z_mm']==result['A']['lower_plane_world_z_mm'])
    check('a_axis_alignment',result['A']['axis_aligned'] and result['A']['placements_mm']['CMP-LUDOU-COLUMN-001'][:2]==[0,0])
    column={x['key']:x for x in t.read(t.COLUMN_PARAMS)['parameters']}
    check('a_z006_unknown',column['historical_height_Z006_mm']['value'] is None and column['historical_height_Z006_mm']['classification']=='UNKNOWN' and column['historical_height_Z006_mm']['production_use']=='DO_NOT_LOCK','EVIDENCE_STATUS_UPGRADE')
    check('a_rc_replaceable',column['height_mm']['value']==3534.3 and column['height_mm']['classification']=='REASONABLE_COMPLETION' and column['height_mm']['replaceable'],'EVIDENCE_STATUS_UPGRADE')
    check('a_joinery_unknown',ar['A-R01']['joinery_detail_status']=='UNKNOWN')
    check('a_derived_not_manual',not a['placements'] and result['A']['placements_mm']['CMP-LUDOU-COLUMN-001'][2]==column['height_mm']['value'],'BAKED_MANUAL_ASSEMBLY')
    bn={n['node_id']:n for n in b['nodes']}
    br={r['relationship_id']:r for r in b['relationships']}
    check('b_members_complete',len(bn)==5)
    check('b_control_only',bn['CTL-FRAME-001']['qualification_status']=='CONTROL_ONLY' and bn['CTL-FRAME-001']['historical_claim'] is False,'SILENT_HISTORICIZATION')
    check('b_proxy_only',bn['PRX-FRAME-CONNECTOR-001']['qualification_status']=='PROXY_ONLY' and bn['PRX-FRAME-CONNECTOR-001']['historical_claim'] is False,'SILENT_HISTORICIZATION')
    check('b_locate_2_of_2',all(br[f'B-R0{i}']['relation_type']=='LOCATE' for i in (1,2)))
    check('b_connect_2_of_2',all(br[f'B-R0{i}']['relation_type']=='CONNECT' for i in (3,4)))
    check('b_belong_4_of_4',sum(r['relation_type']=='BELONG' for r in b['relationships'])==4)
    check('b_no_direct_frame_connect',all(not (r['relation_type']=='CONNECT' and {r['source_node'],r['target_node']}==set(t.FRAME_IDS)) for r in b['relationships']))
    check('b_connector_identity_unknown',all(br[f'B-R0{i}']['historical_connector_identity']=='UNKNOWN' for i in (3,4)))
    check('b_joinery_unknown',all(br[f'B-R0{i}']['joinery_detail_status']=='UNKNOWN' for i in (3,4)))
    check('b_semantic_valid',result['B']['semantic_status']=='SEMANTIC_ASSEMBLY_VALID')
    check('b_geometry_block_expected',result['B']['geometry_status']=='FULL_LENGTH_GEOMETRY_BLOCKED' and not result['B']['actual_full_length_geometry_created'],'BLOCK_BYPASS')
    check('b_no_approved_building_full_length',not any(p['parameter_id'].startswith('FRAME') for p in b['building_parameters']))
    check('b_reference_leak_fixture',t.geometry_gate({'create_actual_full_length_geometry':True,'actual_length_mm':1000,'actual_length_source':'canonical_reference_length_mm'})=='REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY','REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY')
    check('b_block_reason_stable',t.derive(graph)['B']==result['B'])
    pm=t.read(t.PARAMS)['parameters']['PM-005'];cp={p['parameter_id']:p for p in c['building_parameters']};cr=next(r for r in c['relationships'] if r['relation_type']=='REPEAT')
    check('c_pm005_resolved',pm['value']==cp['PM-005']['value']==result['C']['resolved_spacing_mm']==3505.7)
    check('c_pm005_evidence',pm['classification']=='CONFIRMED' and pm['time_layer']=='observed_as_measured' and pm['source_layer']=='DIRECT_PRIMARY')
    check('c_repeat_project_rule',cr['evidence_status']=='PROJECT_RULE' and cr['historical_claim'] is False)
    check('c_repeat_rule_parameterized',cr['repeat_rule']['spacing_ref']=='PM-005' and 'PM-005' in cr['parameter_refs'])
    check('c_canonical_count_2',cp['RULE-C-COUNT']['value']==result['C']['count']==2)
    check('c_runtime_instance_count_2',len(result['C']['instances'])==2)
    check('c_runtime_ids',[i['instance_id'] for i in result['C']['instances']]==['INST-COLUMN-SIDEBAY-001','INST-COLUMN-SIDEBAY-002'])
    check('c_single_component_identity',all(i['source_component_id']=='CMP-COLUMN-001' and 'component_id' not in i for i in result['C']['instances']),'DUPLICATE_COMPONENT_IDENTITY')
    check('c_spacing_derived',result['C']['instances'][1]['derived_transform']['location_mm'][0]-result['C']['instances'][0]['derived_transform']['location_mm'][0]==pm['value'])
    check('c_belong_2_of_2',sum(r['relation_type']=='BELONG' for r in c['relationships'])==2)
    check('c_manifest_matches',t.read(t.MANIFEST)['instances']==result['C']['instances'])
    mutation=json.loads(Path('/tmp/t016_mutation_result.json').read_text())
    check('c_mutation_count_3',mutation['C']['count']==len(mutation['C']['instances'])==3)
    check('c_mutation_same_component',all(i['source_component_id']=='CMP-COLUMN-001' for i in mutation['C']['instances']))
    check('c_restore_deterministic',t.derive(graph)==result)
    git_pm=subprocess.check_output(['git','show',f'HEAD:{t.PARAMS}'],cwd=ROOT)
    check('c_pm005_file_unchanged',(ROOT/t.PARAMS).read_bytes()==git_pm,'PM005_MUTATION_FORBIDDEN')
    signatures={name:json.loads(Path(path).read_text()) for name,path in SIG_PATHS.items()}
    check('a_independent_reopen',signatures['A_reopen']['unit']=='AU-COLUMN-LUDOU-001' and len(signatures['A_reopen']['objects'])==2)
    check('a_deterministic_regen',signatures['A_reopen']==signatures['A_regen'])
    check('c_independent_reopen',signatures['C_reopen']['unit']=='AU-COLUMN-GRID-001' and len(signatures['C_reopen']['objects'])==2)
    check('c_mutation_blender_reopen_3',len(signatures['C_mutation_reopen']['objects'])==3)
    check('c_blender_restore_deterministic',signatures['C_reopen']==signatures['C_restore'])
    check('b_no_blender_actual_geometry',not (ROOT/BASE/'assembly/local/AU-FRAME-TIER-001_V001.blend').exists(),'BLOCK_BYPASS')
    review_names=['A_COLUMN_LUDOU_SUPPORT.png','B_FRAME_TIER_SEMANTIC_BLOCKED.png','C_COLUMN_GRID_REPEAT.png','P3_2_REPRESENTATIVE_ASSEMBLY_OVERVIEW_V001.png']
    check('four_review_assets',all((ROOT/REVIEW/name).is_file() for name in review_names))
    check('b_review_explicit_block',b'FULL-LENGTH GEOMETRY BLOCKED' in (ROOT/BASE/'scripts/render_p3_2_representative_review_v001.py').read_bytes())
    check('p2_frozen_baseline',foundation_checks['p2_frozen_19_asset_hashes']['status']=='PASS' and foundation_checks['p2_frozen_baseline']['status']=='PASS','PROTECTED_BASELINE_MUTATION')
    check('p31_master_binaries',all(foundation_checks['master_binary_hash_'+m['component_id']]['status']=='PASS' for m in t.read(t.LIBRARY)['masters']),'PROTECTED_BASELINE_MUTATION')
    check('p31_tracked_assets',foundation_checks['p3_1_tracked_assets_unchanged']['status']=='PASS','PROTECTED_BASELINE_MUTATION')
    changed=subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=ROOT,text=True)
    check('p33_scope_zero',not any('P3_3' in line or 'P3.3' in line for line in changed.splitlines()),'P3_3_SCOPE_LEAK')
    check('unrelated_untracked_not_staged',not any(line.startswith(('A ','M ')) and ('poc/' in line or 'output/' in line or '.pdf' in line) for line in changed.splitlines()))
    suite=unittest.defaultTestLoader.discover(str(ROOT/BASE/'tests'),pattern='test_p3_2_representative_assembly_v001.py')
    tests=unittest.TextTestRunner(stream=sys.stdout,verbosity=1).run(suite)
    negative={'passed':tests.testsRun-len(tests.failures)-len(tests.errors),'total':tests.testsRun,'status':'PASS' if tests.wasSuccessful() else 'FAIL'}
    check('required_negative_15_of_15',negative['passed']==negative['total']==15,'NEGATIVE_TEST_FAILED')
    hard=sorted({e['code'] for e in errors if e['code'] in HARD}|{v['error_code'] for v in checks.values() if v['status']=='FAIL' and v['error_code'] in HARD})
    blends={letter:{'path':str(path),'sha256':t.digest(path)} for letter,path in BLENDS.items()}
    paths=[t.GRAPH,t.UNITS,t.EXTENSION,t.SCHEMA_EXTENSION,t.PARAMS,t.LIBRARY]
    report={'task':'T-016','engineering_id':'P3_2_REPRESENTATIVE_ASSEMBLY_VALIDATION_V001','status':'ENGINEERING_COMPLETE_REVIEW_REQUIRED' if all(x['status']=='PASS' for x in checks.values()) and negative['status']=='PASS' else 'FAIL','checks':checks,'check_pass_count':sum(x['status']=='PASS' for x in checks.values()),'check_total':len(checks),'negative_tests':negative,'canonical_errors':errors,'hard_fails_canonical':hard,'derived_result':result,'blender_signatures':signatures,'local_only_blends':blends,'review_assets':[str(REVIEW/name) for name in review_names],'input_sha256':{str(p):t.digest(p) for p in paths},'p3_3_files_created':0,'gate_status':'P3_2_ACTIVE_P3_3_LOCKED_PRODUCT_OWNER_REVIEW_REQUIRED'}
    t.write(REPORT,report)
    print(json.dumps({'status':report['status'],'machine_validation':f"{report['check_pass_count']}/{report['check_total']}",'negative_tests':negative,'hard_fails_canonical':hard},ensure_ascii=False))
    return 0 if report['status']=='ENGINEERING_COMPLETE_REVIEW_REQUIRED' else 1

if __name__=='__main__':raise SystemExit(main())
