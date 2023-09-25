from . import halfedge
from . import utils
import numpy as np

bbox_points=[0,1,7,2,3,6,4,5]
bbox_face=[[0,2,7,1],[0,3,5,2],[3,0,1,6],[4,5,3,6],[4,6,1,7],[4,7,2,5]]
bbox_halfEdge=halfedge.HalfEdgeObject(bbox_face)

def __normalize(vector):
    norm = np.linalg.norm(vector)
    return vector/norm

def getOrientationOfAlignedY(mesh):
    import open3d as o3d
    from scipy.spatial.transform.rotation import Rotation
    bbox = mesh.get_minimal_oriented_bounding_box()
    verts = np.asarray(bbox.get_box_points())
    edges = bbox_halfEdge.getEdgesOfVert(0)
    yAlignMin=1000
    minDir=None
    for e in edges:
        dir=verts[e[1]]-verts[e[0]]
        align=np.dot(dir,[0,1,0])
        if abs(align) < abs(yAlignMin):
            yAlignMin = align
            minDir = __normalize(dir)
    minDir[1]=0
    print(f'mindir:{minDir}')
    crossed=np.cross(minDir,np.array([1,0,0]))
    print(f'crossed:{crossed}')
    angle =  np.arcsin(np.linalg.norm(crossed))
    print(f'angle:{angle}')
    rot = Rotation.from_euler('y',angle,degrees=False)
    return rot.as_matrix()



def getBboxOfAlignedY(mesh):
    import open3d as o3d
    rot = getOrientationOfAlignedY(mesh)
    rot = utils.getAffineMat(rot)
    print(f'rot_matrix:{rot}')
    mesh.transform(rot)
    bbox = mesh.get_axis_aligned_bounding_box()
    # mesh.transform(np.linalg.inv(rot))
    # bbox.transform(np.linalg.inv(rot))
    return bbox
        
    



