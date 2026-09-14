"""Run only through Blender 3.6.23 --background --python. Uses approved Master meshes."""
import hashlib
import json
import sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'production/zhenguo_wanfo'
LIB=json.loads((BASE/'registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json').read_text())
MASTERS={m['component_id']:m for m in LIB['masters']}
argv=sys.argv[sys.argv.index('--')+1:]
mode=argv[0]
unit=argv[1]
output=Path(argv[2])
result=json.loads(Path(argv[3]).read_text()) if mode=='build' else None
signature_path=Path(argv[4]) if mode=='build' and len(argv)>4 else (Path(argv[3]) if mode=='check' and len(argv)>3 else None)

def load_mesh(cid,instance_id,location):
    master=MASTERS[cid]
    path=ROOT/master['local_binary_path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==master['canonical_asset_sha256'],cid
    with bpy.data.libraries.load(str(path),link=False) as (src,dst):
        dst.objects=[name for name in src.objects if name.startswith('MASTER__')]
    meshes=[obj for obj in dst.objects if obj and obj.type=='MESH']
    assert len(meshes)==1,(cid,len(meshes))
    obj=meshes[0]
    bpy.context.scene.collection.objects.link(obj)
    obj.name=instance_id
    obj.location=location
    obj['source_component_id']=cid
    obj['instance_id']=instance_id
    obj['placement_rule']='INTERFACE_PARAMETER_RULE'
    return obj

def signature():
    out=[]
    for obj in sorted((o for o in bpy.context.scene.objects if o.type=='MESH'),key=lambda o:o.name):
        out.append({'instance_id':obj.get('instance_id'), 'source_component_id':obj.get('source_component_id'), 'location_mm':[round(float(v),3) for v in obj.location], 'bounds_mm':[round(float(v),3) for v in obj.dimensions], 'placement_rule':obj.get('placement_rule'), 'vertices':len(obj.data.vertices), 'faces':len(obj.data.polygons)})
    return {'unit':bpy.context.scene.get('assembly_unit_id'), 'objects':out}

if mode=='build':
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.context.scene.unit_settings.system='METRIC'
    bpy.context.scene.unit_settings.scale_length=.001
    bpy.context.scene['assembly_unit_id']='AU-COLUMN-LUDOU-001' if unit=='A' else 'AU-COLUMN-GRID-001'
    bpy.context.scene['generation']='T-016:REGISTRY_RELATION_INTERFACE_PARAMETER'
    if unit=='A':
        for cid,loc in result['A']['placements_mm'].items():load_mesh(cid,'ASM-A-'+cid,loc)
    elif unit=='C':
        for item in result['C']['instances']:load_mesh(item['source_component_id'],item['instance_id'],item['derived_transform']['location_mm'])
    else:raise ValueError('only A/C geometry permitted')
    output.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    sig=signature()
    if signature_path:signature_path.write_text(json.dumps(sig,sort_keys=True,indent=2)+'\n')
    print('T016_SIGNATURE='+json.dumps(sig,sort_keys=True))
elif mode=='check':
    assert bpy.context.scene.get('generation')=='T-016:REGISTRY_RELATION_INTERFACE_PARAMETER'
    expected='AU-COLUMN-LUDOU-001' if unit=='A' else 'AU-COLUMN-GRID-001'
    assert bpy.context.scene.get('assembly_unit_id')==expected
    sig=signature()
    if signature_path:signature_path.write_text(json.dumps(sig,sort_keys=True,indent=2)+'\n')
    print('T016_SIGNATURE='+json.dumps(sig,sort_keys=True))
else:raise ValueError(mode)
