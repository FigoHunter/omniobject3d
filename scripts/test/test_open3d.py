import open3d as o3d
import os
import json
from scipy.spatial.transform import Rotation
import numpy as np

def getPath(data):
    return os.path.join(r'Y:\hddisk5\users\yifei\omniobject3d\OpenXD-OmniObject3D-New\raw\decimated',data,'Scan')

data_path = 'anise/anise_002'

mesh = o3d.io.read_triangle_mesh(os.path.join(getPath(data_path),'Scan.obj'))
with open(os.path.join(getPath(data_path),'Scan.json'),'r') as f:
    data = json.load(f)

points_index=[0,1,7,2,3,6,4,5,3]

def drawbox(corner_box):
    lines = [[0, 1],[1,7],[7,2],[2,0],
             [3,6],[6,4],[4,5],[5,3],
             [0,3],[1,6],[7,4],[2,5]]

    def diff(a, b, len=1):
        if abs(a - b)<len/2:
            return abs(a-b)
        return len-abs(a-b)

    # Use the same color for all lines

    colors = [[max(0,1-diff(i/len(lines),0)*3), max(0,1-diff(i/len(lines),1/3)*3), max(0,1-diff(i/len(lines),2/3)*3)] for i in range(len(lines))]
    print(colors)

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(corner_box)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set


mat = np.array(data['data'][0]['matrix'])
# coord=np.array([[-1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]])

# mat = coord@mat@np.linalg.inv(coord)
ls=[]
mesh.transform(mat)
ls.append(mesh)
bbox = mesh.get_minimal_oriented_bounding_box()

points = bbox.get_box_points()
print(points)
np_points = np.asarray(points)

print(np_points)

coord_mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
coord_mesh.scale(3,[0,0,0])
coord_mesh.translate((-10,-10,0))

lineset = drawbox(np_points)

ls.append(lineset)


o3d.visualization.draw_geometries(ls)

