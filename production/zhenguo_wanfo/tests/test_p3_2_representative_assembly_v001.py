"""T-016 required negative fixtures; each assertion checks a stable rejection code."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import p3_2_representative_common_v001 as t

class RepresentativeNegativeTests(unittest.TestCase):
    def setUp(self):
        self.data=t.read(t.GRAPH)
        self.result=t.derive(self.data)

    def rejected(self,code,**kwargs):
        errors=t.validate(self.data,self.result,**kwargs)
        self.assertIn(code,{e['code'] for e in errors},errors)

    def test_a_missing_top_support_interface(self):
        g=self.data['unit_graphs']['A'];g['interfaces']=[i for i in g['interfaces'] if i['interface_id']!='CMP-COLUMN-001__TOP-SUPPORT-PLANE']
        self.rejected('NONEXISTENT_INTERFACE')

    def test_a_world_only_manual_ludou(self):
        g=self.data['unit_graphs']['A'];g['relationships']=[r for r in g['relationships'] if r['relationship_id']!='A-R02'];g['placements']=[{'node_id':'CMP-LUDOU-COLUMN-001','interface_id':'CMP-LUDOU-COLUMN-001__AXIS','method':'MANUAL_WORLD_PLACEMENT','rule_id':'','coordinate_space':'WORLD','parameter_refs':[],'world_result_mm':[0,0,3534.3]}]
        self.rejected('BAKED_MANUAL_ASSEMBLY')

    def test_a_rc_to_confirmed(self):
        self.data['column_height_evidence_override']='CONFIRMED'
        self.rejected('EVIDENCE_STATUS_UPGRADE')

    def test_a_joinery_upgrade(self):
        self.data['unit_graphs']['A']['relationships'][0]['joinery_detail_status']='CONFIRMED'
        self.rejected('EVIDENCE_STATUS_UPGRADE')

    def test_b_reference_length_leak(self):
        self.data['b_geometry_request']={'create_actual_full_length_geometry':True,'actual_length_mm':1000,'actual_length_source':'canonical_reference_length_mm'}
        self.rejected('REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY')

    def test_b_proxy_historicized(self):
        n=next(n for n in self.data['unit_graphs']['B']['nodes'] if n['node_id']=='PRX-FRAME-CONNECTOR-001');n['historical_claim']=True;n['qualification_status']='FORMAL_APPROVED_MASTER'
        self.rejected('SILENT_HISTORICIZATION')

    def test_b_control_historicized(self):
        n=next(n for n in self.data['unit_graphs']['B']['nodes'] if n['node_id']=='CTL-FRAME-001');n['historical_claim']=True;n['qualification_status']='FORMAL_APPROVED_MASTER'
        self.rejected('SILENT_HISTORICIZATION')

    def test_b_direct_historical_connect(self):
        r=copy.deepcopy(self.data['unit_graphs']['B']['relationships'][2]);r.update(relationship_id='B-ILLEGAL',source_node=t.FRAME_IDS[0],target_node=t.FRAME_IDS[1],target_interface=t.FRAME_IDS[1]+'__LOWER-PLANE',evidence_status='CONFIRMED')
        self.data['unit_graphs']['B']['relationships'].append(r)
        self.rejected('DIRECT_HISTORICAL_CONNECTION_UNSUPPORTED')

    def test_b_block_bypass(self):
        self.data['b_actual_full_length_geometry_created']=True
        self.rejected('BLOCK_BYPASS')

    def test_c_naked_spacing_without_ref(self):
        r=self.data['unit_graphs']['C']['relationships'][0];r['parameter_refs']=['RULE-C-COUNT'];r['repeat_rule']['spacing_ref']='3505.7'
        self.rejected('INVALID_REPEAT_RULE')

    def test_c_instance_new_component_identity(self):
        self.result['C']['instances'][1]['component_id']='CMP-COLUMN-002'
        self.rejected('DUPLICATE_COMPONENT_IDENTITY')

    def test_c_pm005_mutation(self):
        self.rejected('PM005_MUTATION_FORBIDDEN',pm_override=3506.0)

    def test_c_world_only_placement(self):
        g=self.data['unit_graphs']['C'];g['relationships']=[r for r in g['relationships'] if r['relationship_id']!='C-R01'];g['placements']=[{'node_id':'CMP-COLUMN-001','interface_id':'CMP-COLUMN-001__ORIGIN','method':'MANUAL_WORLD_PLACEMENT','rule_id':'','coordinate_space':'WORLD','parameter_refs':[],'world_result_mm':[3505.7,0,0]}]
        self.rejected('BAKED_MANUAL_ASSEMBLY')

    def test_belong_cycle(self):
        g=self.data['unit_graphs']['A'];u=copy.deepcopy(g['nodes'][-1]);u['node_id']='AU-TEST-CYCLE';u['noncomponent_ref']='AU-TEST-CYCLE';g['nodes'].append(u)
        a=copy.deepcopy(g['relationships'][2]);a.update(relationship_id='A-CYCLE-1',source_node='AU-COLUMN-LUDOU-001',target_node='AU-TEST-CYCLE')
        b=copy.deepcopy(a);b.update(relationship_id='A-CYCLE-2',source_node='AU-TEST-CYCLE',target_node='AU-COLUMN-LUDOU-001')
        g['relationships'].extend([a,b]);self.rejected('BELONG_HIERARCHY_CYCLE')

    def test_illegal_interface_endpoint(self):
        self.data['unit_graphs']['A']['relationships'][0]['source_interface']='CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE'
        self.rejected('NONEXISTENT_INTERFACE')

if __name__=='__main__':unittest.main()
