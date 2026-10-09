import json,numpy as np,manifold3d as mf
from pathlib import Path
R=Path(__file__).resolve().parent;j=json.loads((R/'PILOT_GEOMETRY.json').read_text());objs={o['id']:o for o in j['objects']}
def levels(o):
 v=np.array(o['vertices']);f=np.array(o['faces']);groups={}
 for tri in v[f]:
  if np.ptp(tri[:,2])>1e-7:continue
  z=round(float(tri[0,2]),6);sign=np.cross(tri[1]-tri[0],tri[2]-tri[0])[2]
  if abs(sign)<1e-9:continue
  groups.setdefault((z,1 if sign>0 else -1),[]).append(tri[:,:2].copy())
 return {k:mf.CrossSection(polys,mf.FillRule.NonZero) for k,polys in groups.items()}
r=json.loads((R/'PILOT_VALIDATION.json').read_text())
for c in r['contact_checks']:
 a=levels(objs[c['a']]);b=levels(objs[c['b']]);matches=[]
 for (z,sign),pol in a.items():
  q=b.get((z,-sign))
  if q is not None:
   area=float((pol^q).area())
   if area>1e-5:matches.append({'plane_z_mm':z,'area_mm2':area})
 c['horizontal_contact_patches']=matches;c['total_horizontal_contact_area_mm2']=sum(x['area_mm2'] for x in matches)
 assert c['total_horizontal_contact_area_mm2']>100,c
 c['note']='positive face-to-face contact area verified; not bearing-strength certification'
(R/'PILOT_VALIDATION.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print([(c['description'],c['total_horizontal_contact_area_mm2']) for c in r['contact_checks']])
