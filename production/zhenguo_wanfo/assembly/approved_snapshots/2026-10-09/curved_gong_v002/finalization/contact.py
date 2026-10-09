import numpy as np
import trimesh
TOL=.001
def contact(seat,rod):
 # Require all triangle vertices plus centroid to lie on the rod boundary.
 pts=np.concatenate([seat.triangles.reshape(-1,3),seat.triangles_center])
 _,dist,ids=trimesh.proximity.closest_point_naive(rod,pts)
 assert np.isfinite(dist).all()
 n=len(seat.faces)
 good_vertices=(dist[:3*n].reshape(n,3)<=TOL).all(axis=1)
 opposite=np.einsum('ij,ij->i',seat.face_normals,rod.face_normals[ids[3*n:]])<-0.999
 good=good_vertices & (dist[3*n:]<=TOL) & opposite
 up=good & (seat.face_normals[:,2]>0.1)
 # Connectivity of contacting facets, independent of aggregate area.
 selected=set(np.flatnonzero(up).tolist()); parent={i:i for i in selected}
 def find(i):
  while parent[i]!=i:
   parent[i]=parent[parent[i]];i=parent[i]
  return i
 for a,b in seat.face_adjacency:
  if int(a) in selected and int(b) in selected:parent[find(int(a))]=find(int(b))
 patches=len({find(i) for i in selected})
 tris=seat.triangles[up]
 cuts=np.unique(np.round(tris[:,:,0].ravel(),6)) if len(tris) else []
 widths=[]
 for left,right in zip(cuts[:-1],cuts[1:]):
  if right-left<1e-5:continue
  x=(left+right)/2;intervals=[]
  for tri in tris:
   yy=[]
   for a,b in zip(tri,np.roll(tri,-1,axis=0)):
    if (a[0]-x)*(b[0]-x)<0:yy.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
   if len(yy)>=2:intervals.append((min(yy),max(yy)))
  intervals.sort();merged=[]
  for a,b in intervals:
   if merged and a<=merged[-1][1]+TOL:merged[-1][1]=max(b,merged[-1][1])
   else:merged.append([a,b])
  widths.append({'x_mm':float(x),'projected_contact_width_mm':float(sum(b-a for a,b in merged))})
 return {'area_mm2':float(seat.area_faces[good].sum()),'upward_area_mm2':float(seat.area_faces[up].sum()),
  'connected_upward_patch_count':patches,'projected_interval_checks':widths,
  'minimum_midinterval_projected_width_mm':min((x['projected_contact_width_mm'] for x in widths),default=0),
  'horizontal_projection_mm2':float((seat.area_faces[up]*seat.face_normals[up,2]).sum()),
  'triangles':int(good.sum()),'tolerance_mm':TOL,'max_boundary_distance_mm':float(dist[3*n:][good].max()) if good.any() else None,
  'upward_contact_bounds_mm':np.array([seat.triangles[up].reshape(-1,3).min(axis=0),seat.triangles[up].reshape(-1,3).max(axis=0)]).tolist() if up.any() else None}
