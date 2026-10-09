import numpy as np
import trimesh
import manifold3d
from functools import reduce
def boolean64(meshes,operation,check_volume=True,**kwargs):
 if check_volume and not all(m.is_volume for m in meshes):raise ValueError('Input is not a positive closed solid')
 manifolds=[manifold3d.Manifold(manifold3d.Mesh64(vert_properties=np.array(m.vertices,dtype=np.float64),tri_verts=np.array(m.faces,dtype=np.uint64))) for m in meshes]
 if any(m.status()!=manifold3d.Error.NoError for m in manifolds):raise ValueError('Manifold input status error')
 if operation=='intersection':q=reduce(lambda a,b:a^b,manifolds)
 elif operation=='union':q=reduce(lambda a,b:a+b,manifolds)
 elif operation=='difference':q=manifolds[0]-reduce(lambda a,b:a+b,manifolds[1:])
 else:raise ValueError(operation)
 if q.status()!=manifold3d.Error.NoError:raise ValueError('Manifold output status error')
 result=q.to_mesh64();return trimesh.Trimesh(result.vert_properties,result.tri_verts,process=False)
trimesh.boolean._engines['manifold']=boolean64
