from pathlib import Path
import hashlib,json,subprocess,re
T=Path(__file__).resolve().parent;R=T.parents[1];BASE='028517cbdada6cb266feae17f58ae0a7888c4a93'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=json.loads((T/'BLENDER_VALIDATION.json').read_text());assert b['gate']=='PASS' and len(b['models'])==4
v=json.loads((T/'TECHNICAL_VALIDATION.json').read_text());assert len(v['models'])==2
v['blender_gate']='PASS';v['PO_visual_gate']='PENDING';write(T/'TECHNICAL_VALIDATION.json',v)
# Existing source/approved files must match exact fixed input tree blobs.
status=subprocess.check_output(['git','diff',BASE,'--name-status'],cwd=R,text=True);assert all(row.split('\t')[0]=='A' and (row.split('\t')[1].startswith('review/ang_form_v002/') or row.split('\t')[1]=='.github/workflows/wanfo_ang_form_v002.yml') for row in status.splitlines()),status
# Track only new candidate files plus one isolated workflow. Existing tracked files unchanged.
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines()
assert all(p.startswith('review/ang_form_v002/') or p=='.github/workflows/wanfo_ang_form_v002.yml' for p in untracked),untracked
files=[p for p in T.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name not in ['DELIVERY_MANIFEST.json']]
for p in files:
 if p.suffix in ['.py','.md','.json','.yml']:
  s=p.read_text();assert not re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN .*PRIVATE KEY',s),p
write(T/'DELIVERY_MANIFEST.json',dict(status='PASS_LOCAL_CLOUD_DELIVERY_PENDING_REMOTE_BYTE_CHECK',base=BASE,existing_tracked_files_modified=0,approved_candidates_and_masters_unchanged=True,source_invariance_method='git diff fixed baseline: additions only in task files and isolated workflow',files=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)],count=len(files),PO_visual='PENDING'))
