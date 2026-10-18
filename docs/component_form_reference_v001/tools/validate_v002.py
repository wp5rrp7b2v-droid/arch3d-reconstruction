"""Check scope, preservation, derivations and truthful candidate labels."""
from pathlib import Path
import json,subprocess,hashlib
OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[1]
BASE='83cee5522b6f468677b2b42ced9f1f821500b9db'
IDS={'F003','F004','F005','F007','F008','F009','F030'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def original(p):return subprocess.check_output(['git','show',BASE+':'+str(p.relative_to(ROOT))],cwd=ROOT)
def main():
 old=json.loads(original(OUT/'data.json'));new=json.loads((OUT/'data.json').read_text())
 assert len(new)==16
 keys=['c','c_original','master_id','model_identity','model_provenance','model_origin_url','local_models','registry_items','geometry','count','count_kind','position']
 for a,b in zip(old,new):
  assert a['id']==b['id']
  for k in keys:assert a[k]==b[k],(b['id'],'MODEL_OR_COUNT_CHANGED',k)
  if b['id'] not in IDS:
   assert a==b,('NINE_PAGE_DATA_CHANGED',b['id'])
   p=OUT/'pages'/(b['id']+'.html');assert p.read_bytes()==original(p),('NINE_PAGE_CHANGED',b['id'])
  else:
   p=OUT/'pages'/(b['id']+'.html');s=p.read_text()
   assert s.count('<figure class="recommended">')==1
   assert '时代形制参考示意' in s and '未知' in s and '未作尺寸或坐标配准' in s
   assert b['b'].endswith('.svg') and (OUT/b['b']).exists()
   assert b['b']!=a['b']
 for d in json.loads((OUT/'assets/v002/DERIVATION.json').read_text()):
  assert sha(OUT/d['file'])==d['sha256'] and d['not_approved']
  for p,digest in d['source_sha256'].items():assert sha(OUT/p)==digest
 # Check both committed and uncommitted modifications, including file additions.
 names=set(subprocess.check_output(['git','diff','--name-only','-z',BASE],cwd=ROOT).decode().strip('\0').split('\0'))
 names.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode().strip('\0').split('\0'))
 allowed={'.github/workflows/wanfo_component_form_sources.yml','.github/workflows/wanfo_component_form_qa.yml'}
 bad=[p for p in names if p and not p.startswith('docs/component_form_reference_v001/') and p not in allowed]
 assert not bad,bad
 result=dict(status='PASS',baseline=BASE,changed_detail_pages=sorted(IDS),nine_other_pages='BYTE_IDENTICAL',nine_data_rows='IDENTICAL',all_16_model_and_quantity_records='IDENTICAL',candidate_derivations='7_HASH_AND_SOURCE_CHAINS_PASS',protected_paths='NO_CHANGES',limitations='Preservation and traceability tests; not an independent historical-form judgment.')
 (OUT/'qa/V002_STATIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
