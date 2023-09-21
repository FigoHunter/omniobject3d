import trimesh
import json
from scipy.spatial.transform import Rotation
import numpy as np

def getAffineMat(matrix:np.ndarray) -> np.ndarray:
    affine_mat = matrix.copy()
    affine_mat = np.insert(affine_mat,3,values=[0,0,0],axis=1)
    affine_mat = np.insert(affine_mat,3,values=[0,0,0,1],axis=0)
    return affine_mat

mesh = trimesh.load(r'Y:\hddisk5\users\yifei\omniobject3d\OpenXD-OmniObject3D-New\raw\decimated\anise\anise_002\Scan\Scan.obj')
with open(r'Y:\hddisk5\users\yifei\omniobject3d\OpenXD-OmniObject3D-New\raw\decimated\anise\anise_002\Scan\Scan.json','r') as f:
    j = json.load(f)

coord=np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
mesh.show()

pos = j['data'][0]['pos']
rot = j['data'][0]['rot']
mat = getAffineMat(Rotation.from_quat(rot).as_matrix())
mat[0][3]=pos[0]
mat[1][3]=pos[1]
mat[2][3]=pos[2]
print(mat)
mat = coord@mat@np.linalg.inv(coord)
print(mat)

mesh.apply_transform(mat)
mesh.show()
