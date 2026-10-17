"""Meaningful delivery checks: registry coverage, local navigation and image decode."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[2];site=root/'docs/component_atlas_v001'
data=json.loads((site/'atlas_data.json').read_text());reg=json.loads((root/'docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json').read_text())
expected={x['component'] for x in reg['items']}|set(reg['pending_source_binding'])
assert {c['name'] for c in data}==expected
masters={p.name for p in (root/'production/zhenguo_wanfo/component_library/masters').iterdir() if p.is_dir()}
assert {c['cid'] for c in data if c['cid']}==masters
assert len(data)==len({c['id'] for c in data})
for c in data:
    assert (site/'pages'/(c['id']+'.html')).exists()
    assert c['sources'] and c['note'] and c['status']
    if c['cid']:assert c['models']
source=json.loads((site/'assets/sources/SOURCE_IMAGE_PROVENANCE.json').read_text())
for im in source:assert hashlib.sha256((site/'assets/sources'/im['file']).read_bytes()).hexdigest()==im['sha256']
renders=json.loads((site/'assets/models/RENDER_PROVENANCE.json').read_text())
assert all(x['status']=='PASS_READONLY' and x['binary_unchanged'] and x['mesh_transform_unchanged'] for x in renders)
assert {'LOCAL_C02','LOCAL_UPPER6_C01','ASSEMBLY_WORK_V003'}<={x['id'] for x in renders}
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append((tag,k,a[k]))
links=0;images=set();errors=[]
for f in site.rglob('*.html'):
    p=Links();p.feed(f.read_text())
    for tag,k,ref in p.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(f.parent/unquote(u.path)).resolve() if u.path else f
        if not target.exists():errors.append((str(f),ref))
        elif tag=='img':images.add(target)
        if u.fragment:
            q=Links();q.feed(target.read_text())
            if u.fragment not in q.ids:errors.append((str(f),'fragment '+ref))
        links+=1
assert not errors,errors
for p in images:
    im=Image.open(p);im.load();assert im.width>0 and im.height>0
report=dict(status='PASS_STATIC_DELIVERY_CHECKS',detail_pages=len(data),covered_scope_entries=len(expected),linked_master_families=len(masters),registry_records=len(reg['items']),registry_records_are_physical_count=False,source_images=len(source),model_binary_jobs=len(renders),model_render_views=sum(len(x['images']) for x in renders),checked_local_references=links,decoded_referenced_images=len(images),missing_links=0,missing_target_families=0,all_master_pages_have_existing_model_views=True,all_binary_and_mesh_checks_pass=True,source_hash_checks_pass=True,browser_visual_qa='NOT_RUN_NO_SUPPORTED_BROWSER_PLUGIN',formal_models_modified=False,main_merged=False)
(site/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
