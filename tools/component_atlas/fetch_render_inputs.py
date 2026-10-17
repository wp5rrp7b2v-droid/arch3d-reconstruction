"""Recover existing artifact BLENDs by registered byte hash. No generators run."""
import os,json,pathlib,hashlib,urllib.request,zipfile,io
root=pathlib.Path.cwd();tmp=pathlib.Path('/tmp/wanfo-atlas-inputs');tmp.mkdir(exist_ok=True)
library=json.loads((root/'production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json').read_text())
token=os.environ['GH_TOKEN'];jobs=[];fetch_log=[]
def bodies(v):
    if isinstance(v,dict):
        if 'geometry_vertices_mm' in v and 'name' in v:yield v['name']
        for x in v.values():yield from bodies(x)
    elif isinstance(v,list):
        for x in v:yield from bodies(x)
for m in library['new_masters']:
    cid=m['component_id'];a=m.get('source_artifact')
    if not a:continue
    a=a.get('accepted_first_article',a);aid=a.get('artifact_id')
    if not aid:continue
    expected=m['canonical_asset_sha256']
    try:
        req=urllib.request.Request(f'https://api.github.com/repos/wp5rrp7b2v-droid/arch3d-reconstruction/actions/artifacts/{aid}/zip',headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json'})
        blob=urllib.request.urlopen(req,timeout=120).read()
        archive_sha=hashlib.sha256(blob).hexdigest()
        if a.get('artifact_zip_sha256') and archive_sha!=a['artifact_zip_sha256']:raise RuntimeError('archive hash mismatch')
        z=zipfile.ZipFile(io.BytesIO(blob));found=False
        for name in z.namelist():
            if not name.endswith('.blend'):continue
            binary=z.read(name)
            if hashlib.sha256(binary).hexdigest()!=expected:continue
            p=tmp/(cid+'.blend');p.write_bytes(binary);found=True
            semantics=[json.loads(p.read_text()) for p in (root/'production/zhenguo_wanfo/component_library/masters'/cid).glob('*SEMANTIC*.json')]
            names=list(dict.fromkeys(n for s in semantics for n in bodies(s)))
            jobs.append(dict(id=cid,path=str(p),sha256=expected,artifact_id=aid,archive_sha256=archive_sha,body_names=names,individual=True))
            fetch_log.append(dict(id=cid,status='RECOVERED_EXACT',artifact_id=aid,sha256=expected))
            break
        if not found:raise RuntimeError('registered binary hash not found in artifact')
    except Exception as e:fetch_log.append(dict(id=cid,status='UNAVAILABLE',reason=str(e),artifact_id=aid))
# Existing main work BLEND: inspect each mesh without changing approved/pending scope.
p=root/'production/zhenguo_wanfo/assembly/working_snapshots/2026-10-12/repaired_joint_v003/WANFO_TWO_FRAMES_THREE_PURLINS_REPAIRED_WORK_V003.blend'
jobs.append(dict(id='ASSEMBLY_WORK_V003',path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),body_names=[],individual=True))
(root/'docs/component_atlas_v001/render_inputs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2))
(root/'docs/component_atlas_v001/BINARY_RECOVERY.json').write_text(json.dumps(fetch_log,ensure_ascii=False,indent=2))
print('Recovered',len(jobs)-1,'registered Master binaries; one existing assembly work BLEND')
