"""T-016 locked representative assemblies. All coordinates are derived, never input."""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path('production/zhenguo_wanfo')
ASSEMBLY = BASE / 'assembly'
sys.path.insert(0, str(ROOT / BASE / 'scripts'))
import validate_p3_2_relationship_foundation_v001 as foundation

GRAPH = ASSEMBLY / 'P3_2_REPRESENTATIVE_RELATIONSHIP_GRAPH_V001.json'
UNITS = ASSEMBLY / 'P3_2_REPRESENTATIVE_ASSEMBLY_REGISTRY_V001.json'
EXTENSION = ASSEMBLY / 'P3_2_REPRESENTATIVE_INTERFACE_EXTENSION_V001.json'
SCHEMA_EXTENSION = ASSEMBLY / 'P3_2_REPRESENTATIVE_SCHEMA_EXTENSION_V001.json'
MANIFEST = ASSEMBLY / 'P3_2_RUNTIME_INSTANCE_MANIFEST_V001.json'
RESULT = ASSEMBLY / 'P3_2_REPRESENTATIVE_DERIVED_RESULT_V001.json'
PARAMS = BASE / 'params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json'
LIBRARY = BASE / 'registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json'
COLUMN_PARAMS = BASE / 'component_library/masters/CMP-COLUMN-001/CMP-COLUMN-001_MASTER_PARAMS_V001.json'
FRAME_IDS = ('CMP-FRAME-LOWER-SIX-CHUANFU-001', 'CMP-FRAME-UPPER-SIX-CHUANFU-001')


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def inputs():
    nodes, interfaces = read(foundation.NODES), read(foundation.INTERFACES)
    interfaces = copy.deepcopy(interfaces)
    interfaces['interfaces'].extend(read(EXTENSION)['interfaces'])
    schema = copy.deepcopy(read(foundation.SCHEMA))
    extension = read(SCHEMA_EXTENSION)
    schema['$defs']['interface']['properties']['local_datum']['properties'].update(extension['interface_local_datum_properties'])
    schema['$defs']['relationship']['properties'].update(extension['relationship_properties'])
    schema['$defs']['relationship']['properties']['repeat_rule']['properties'].update(extension['repeat_rule_properties'])
    return read(GRAPH), read(UNITS), nodes, interfaces, read(foundation.TYPES), schema


def error(code, detail):
    return {'code': code, 'detail': detail}


def geometry_gate(request, frame_params=None):
    """Require independent approved building-specific lengths for both beams."""
    if request.get('actual_length_source') in ('canonical_reference_length_mm', 'MASTER_REFERENCE') or request.get('actual_length_mm') == 1000 or any(p.get('derives_from') == 'canonical_reference_length_mm' for p in (frame_params or {}).values()):
        return 'REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY'
    if not request.get('create_actual_full_length_geometry', False):
        return 'FULL_LENGTH_GEOMETRY_BLOCKED'
    for cid in FRAME_IDS:
        param = (frame_params or {}).get(cid)
        if not param or param.get('approval_status') != 'PRODUCT_OWNER_APPROVED' or param.get('source_layer') != 'BUILDING_LEVEL_APPROVED' or not isinstance(param.get('actual_length_mm'), (int, float)) or param['actual_length_mm'] <= 0:
            return 'FULL_LENGTH_GEOMETRY_BLOCKED'
    return 'GEOMETRY_ELIGIBLE'


def derive(data=None, count=None):
    data = data or read(GRAPH)
    graphs = data['unit_graphs']
    a, b, c = (graphs[x] for x in 'ABC')
    column = {p['key']: p for p in read(COLUMN_PARAMS)['parameters']}
    height = column['height_mm']
    z006 = column['historical_height_Z006_mm']
    if height['classification'] != 'REASONABLE_COMPLETION' or not height['replaceable'] or z006['value'] is not None or z006['classification'] != 'UNKNOWN' or z006['production_use'] != 'DO_NOT_LOCK':
        raise ValueError('EVIDENCE_STATUS_UPGRADE')
    a_if = {i['interface_id']: i for i in a['interfaces']}
    top = a_if['CMP-COLUMN-001__TOP-SUPPORT-PLANE']
    lower = a_if['CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE']
    if top['local_datum'].get('z_parameter_ref') != 'CMP-COLUMN-001:height_mm':
        raise ValueError('TOP_SUPPORT_HEIGHT_RULE_MISSING')
    top_z = float(height['value'])
    lower_z = float(lower['local_datum']['origin_mm'][2])
    a_place = {'CMP-COLUMN-001': [0.0, 0.0, 0.0], 'CMP-LUDOU-COLUMN-001': [0.0, 0.0, round(top_z-lower_z, 4)]}
    pm = read(PARAMS)['parameters']['PM-005']
    if (pm['value'], pm['classification'], pm['time_layer'], pm['source_layer']) != (3505.7, 'CONFIRMED', 'observed_as_measured', 'DIRECT_PRIMARY'):
        raise ValueError('PM005_SOURCE_CHANGED')
    repeat = next(r for r in c['relationships'] if r['relation_type'] == 'REPEAT')
    rule = repeat['repeat_rule']
    if rule['spacing_ref'] != 'PM-005' or rule['count_ref'] != 'RULE-C-COUNT' or rule['start_interface'] != 'CTL-GRID-001__SIDEBAY-START' or rule['direction_interface'] != 'CTL-GRID-001__X-AXIS':
        raise ValueError('INVALID_REPEAT_RULE')
    c_count = next(p['value'] for p in c['building_parameters'] if p['parameter_id'] == 'RULE-C-COUNT') if count is None else count
    start = next(i['local_datum']['origin_mm'] for i in c['interfaces'] if i['interface_id'] == rule['start_interface'])
    direction = next(i['primary_direction'] for i in c['interfaces'] if i['interface_id'] == rule['direction_interface'])
    if rule['direction'] != direction or not isinstance(c_count, int) or not 1 <= c_count <= 3:
        raise ValueError('INVALID_REPEAT_RULE')
    instances = []
    for ordinal in range(1, c_count+1):
        location = [round(start[i] + (ordinal-1)*pm['value']*direction[i], 4) for i in range(3)]
        instances.append({'instance_id': f'INST-COLUMN-SIDEBAY-{ordinal:03}', 'source_component_id': 'CMP-COLUMN-001', 'assembly_unit_id': 'AU-COLUMN-GRID-001', 'generated_by_relation_id': 'C-R01', 'ordinal': ordinal, 'derived_transform': {'location_mm': location, 'rotation_euler_rad': [0,0,0], 'scale': [1,1,1]}, 'parameter_refs': ['PM-005', 'RULE-C-COUNT']})
    status = geometry_gate({'create_actual_full_length_geometry': True})
    return {'A': {'status': 'INTERFACE_ASSEMBLY_VALID', 'placements_mm': a_place, 'support_plane_world_z_mm': top_z, 'lower_plane_world_z_mm': a_place['CMP-LUDOU-COLUMN-001'][2] + lower_z, 'axis_aligned': True, 'height_source': 'Z-006-RC-01', 'height_evidence': 'REASONABLE_COMPLETION', 'joinery_detail_status': 'UNKNOWN'}, 'B': {'semantic_status': 'SEMANTIC_ASSEMBLY_VALID', 'geometry_status': status, 'blocked_reason': 'BUILDING_SPECIFIC_APPROVED_FULL_LENGTH_ABSENT', 'historical_full_length': None, 'historical_connector_identity': 'UNKNOWN', 'joinery_detail_status': 'UNKNOWN', 'actual_full_length_geometry_created': False}, 'C': {'count': c_count, 'spacing_ref': 'PM-005', 'resolved_spacing_mm': pm['value'], 'spacing_evidence': {'classification': pm['classification'], 'time_layer': pm['time_layer'], 'source_layer': pm['source_layer']}, 'repeat_evidence': 'PROJECT_RULE', 'instances': instances}}


def validate(data=None, result=None, count=2, pm_override=None):
    data = data or read(GRAPH)
    official_graph, units, nodes, interfaces, types, schema = inputs()
    errors = []
    graphs = data.get('unit_graphs', {})
    for letter in 'ABC':
        if letter not in graphs:
            errors.append(error('ASSEMBLY_UNIT_MISSING', letter))
            continue
        errors.extend(foundation.validate_graph(graphs[letter], nodes, interfaces, types, schema))
    if len(graphs) != 3 or len({u['assembly_unit_id'] for u in units['units']}) != 3:
        errors.append(error('ASSEMBLY_UNIT_IDENTITY_INVALID', 'A/B/C'))
    if errors:
        return errors
    a,b,c=(graphs[x] for x in 'ABC')
    all_rel = [r for g in graphs.values() for r in g['relationships']]
    if any(r.get('historical_claim') is not False for r in all_rel):
        errors.append(error('SILENT_HISTORICIZATION','relationship historical claim'))
    if {r['relation_type'] for r in all_rel} != {'SUPPORT','CONNECT','LOCATE','REPEAT','BELONG'}:
        errors.append(error('RELATION_COVERAGE_INVALID','five types'))
    aid={i['interface_id']:i for i in a['interfaces']}
    for id,owner,typ in [('CMP-COLUMN-001__TOP-SUPPORT-PLANE','CMP-COLUMN-001','PLANE'),('CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE','CMP-LUDOU-COLUMN-001','PLANE')]:
        if id not in aid or aid[id]['owner_node'] != owner or aid[id]['interface_type'] != typ:
            errors.append(error('SUPPORT_INTERFACE_INVALID',id))
    ar={r['relationship_id']:r for r in a['relationships']}
    if ar.get('A-R01',{}).get('joinery_detail_status') != 'UNKNOWN' or any(r.get('joinery_detail_status') not in (None,'UNKNOWN') for r in a['relationships']):
        errors.append(error('EVIDENCE_STATUS_UPGRADE','A joinery'))
    if ar.get('A-R02',{}).get('source_interface') != 'CMP-COLUMN-001__AXIS' or ar.get('A-R02',{}).get('target_interface') != 'CMP-LUDOU-COLUMN-001__AXIS':
        errors.append(error('BAKED_MANUAL_ASSEMBLY','A axis'))
    if any(p.get('coordinate_space')=='WORLD' or p.get('method')=='MANUAL_WORLD_PLACEMENT' for p in a['placements']+c['placements']) or not any(r['relation_type']=='LOCATE' for r in a['relationships']):
        errors.append(error('BAKED_MANUAL_ASSEMBLY','A/C placement'))
    col={p['key']:p for p in read(COLUMN_PARAMS)['parameters']}
    if col['height_mm']['classification']!='REASONABLE_COMPLETION' or col['historical_height_Z006_mm']['classification']!='UNKNOWN':
        errors.append(error('EVIDENCE_STATUS_UPGRADE','column'))
    if data.get('column_height_evidence_override') == 'CONFIRMED':
        errors.append(error('EVIDENCE_STATUS_UPGRADE','Z-006-RC-01'))
    bn={n['node_id']:n for n in b['nodes']}
    for id,qual in [('CTL-FRAME-001','CONTROL_ONLY'),('PRX-FRAME-CONNECTOR-001','PROXY_ONLY')]:
        if bn.get(id,{}).get('qualification_status')!=qual or bn.get(id,{}).get('historical_claim'):
            errors.append(error('SILENT_HISTORICIZATION',id))
    br={r['relationship_id']:r for r in b['relationships']}
    if any(r['relation_type']=='CONNECT' and {r['source_node'],r['target_node']}==set(FRAME_IDS) for r in b['relationships']):
        errors.append(error('DIRECT_HISTORICAL_CONNECTION_UNSUPPORTED','B'))
    if any(r.get('joinery_detail_status')!='UNKNOWN' or r.get('historical_connector_identity')!='UNKNOWN' for r in (br.get('B-R03',{}),br.get('B-R04',{}))) or data.get('historical_connector_identity')!='UNKNOWN':
        errors.append(error('EVIDENCE_STATUS_UPGRADE','B connector or joinery'))
    if data.get('b_actual_full_length_geometry_created'):
        errors.append(error('BLOCK_BYPASS','B'))
    request=data.get('b_geometry_request',{'create_actual_full_length_geometry':True})
    gate=geometry_gate(request,data.get('b_building_specific_lengths'))
    if gate=='REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY': errors.append(error(gate,'B reference specimen'))
    elif gate=='GEOMETRY_ELIGIBLE': errors.append(error('BLOCK_BYPASS','B scope locked; no approved parameter in canonical task'))
    cparams={p['parameter_id']:p for p in c['building_parameters']}
    repeat=next((r for r in c['relationships'] if r['relation_type']=='REPEAT'),{})
    if repeat.get('repeat_rule',{}).get('spacing_ref')!='PM-005' or 'PM-005' not in repeat.get('parameter_refs',[]):
        errors.append(error('INVALID_PARAMETER_REFERENCE','C spacing'))
    if repeat.get('repeat_rule',{}).get('direction_interface')!='CTL-GRID-001__X-AXIS':
        errors.append(error('INVALID_REPEAT_RULE','C direction interface'))
    pm=read(PARAMS)['parameters']['PM-005']
    if pm_override is not None or cparams.get('PM-005',{}).get('value')!=pm['value'] or cparams.get('PM-005',{}).get('evidence_status')!='CONFIRMED':
        errors.append(error('PM005_MUTATION_FORBIDDEN','PM-005'))
    if cparams.get('RULE-C-COUNT',{}).get('value')!=count:
        errors.append(error('REPEAT_COUNT_MISMATCH','C'))
    if result is not None:
        if result['B']['geometry_status']!='FULL_LENGTH_GEOMETRY_BLOCKED' or result['B']['actual_full_length_geometry_created']:
            errors.append(error('BLOCK_BYPASS','B result'))
        inst=result['C']['instances']
        if len(inst)!=count: errors.append(error('INSTANCE_COUNT_MISMATCH','C'))
        for x in inst:
            if x.get('source_component_id')!='CMP-COLUMN-001' or 'component_id' in x:
                errors.append(error('DUPLICATE_COMPONENT_IDENTITY',x.get('instance_id')))
        if result['A']['support_plane_world_z_mm']!=result['A']['lower_plane_world_z_mm'] or not result['A']['axis_aligned']:
            errors.append(error('SUPPORT_ALIGNMENT_INVALID','A'))
        if result['C']['resolved_spacing_mm']!=pm['value']:
            errors.append(error('INVALID_PARAMETER_REFERENCE','C result'))
    return errors


def canonical():
    data=read(GRAPH)
    result=derive(data)
    errors=validate(data,result)
    if errors: raise RuntimeError(errors)
    write(RESULT,result)
    write(MANIFEST,{'version':'V001','task':'T-016','assembly_unit_id':'AU-COLUMN-GRID-001','source_relation_id':'C-R01','instances':result['C']['instances']})
    return result
