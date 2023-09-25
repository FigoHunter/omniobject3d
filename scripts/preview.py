import os
import glob
import open3d as o3d
import json
import numpy as np
from omniobject3d import align, utils

dir_path=r'./OpenXD-OmniObject3D-New/raw/decimated'

points_index=[0,1,7,2,3,6,4,5]

face=[[0,2,7,1],[0,3,5,2],[3,0,1,6],[4,5,3,6],[4,6,1,7],[4,7,2,5]]

def drawbox(points):
    lines = [[0,1],[1,2],[2,3],[3,0],
             [4,5],[5,6],[6,7],[7,4],
            #  [0,4],[1,5],[2,6],[3,7]
             ]

    def diff(a, b, len=1):
        if abs(a - b)<len/2:
            return abs(a-b)
        return len-abs(a-b)

    # Use the same color for all lines

    colors = [[max(0,1-diff(i/len(lines),0)*3), max(0,1-diff(i/len(lines),1/3)*3), max(0,1-diff(i/len(lines),2/3)*3)] for i in range(len(lines))]
    print(colors)

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set


def preview(path):
    data=np.load(os.path.join(path,'align.npy'),allow_pickle=True)
    print(f'==================')
    print(data)
    for piece in data:
        coord_mesh1 = o3d.geometry.TriangleMesh.create_coordinate_frame()
        coord_mesh1.translate(piece['extent']['min'])
        coord_mesh2 = o3d.geometry.TriangleMesh.create_coordinate_frame()
        coord_mesh2.translate(piece['extent']['max'])
        mesh = o3d.io.read_triangle_mesh(os.path.join(path,'Scan.obj'))
        mat = piece['matrix']
        mesh.transform(mat)
        bbox = mesh.get_axis_aligned_bounding_box()
        points = bbox.get_box_points()
        points = [points[x] for x in points_index]
        box_shape=drawbox(points)

        o3d.visualization.draw_geometries([box_shape,mesh,coord_mesh1,coord_mesh2])


paths = glob.glob(os.path.join(dir_path,'*','*','Scan'))
for p in paths:
    print(os.path.abspath(p))
    try:
        preview(p)
    except Exception as e:
        print(e)