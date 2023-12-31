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
    with open(os.path.join(path,'Scan.json'),'r') as f:
        data = json.load(f)['data']
    for piece in data:
        coord_mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
        mesh = o3d.io.read_triangle_mesh(os.path.join(path,'Scan.obj'))
        mat = piece['matrix']
        mesh.transform(mat)
        bbox = align.getBboxOfAlignedY(mesh)
        points = bbox.get_box_points()
        points = [points[x] for x in points_index]
        box_shape=drawbox(points)

        coord_mesh.translate(points[0])
        o3d.visualization.draw_geometries([box_shape,mesh,coord_mesh])

def process(path):
    with open(os.path.join(path,'Scan.json'),'r') as f:
        data = json.load(f)['data']
    out_data=[]
    for piece in data:
        out_data_piece={}
        mesh = o3d.io.read_triangle_mesh(os.path.join(path,'Scan.obj'))
        mat = piece['matrix']
        mesh.transform(mat)
        rot = align.getOrientationOfAlignedY(mesh)
        rot = utils.getAffineMat(rot)
        mesh.transform(rot)
        mat = rot@mat
        bbox = mesh.get_axis_aligned_bounding_box()
        min = bbox.get_min_bound()
        max = bbox.get_max_bound()
        out_data_piece['matrix']=mat
        out_data_piece['extent']={'min':min,'max':max}
        out_data.append(out_data_piece)
    np.save(os.path.join(path,'align.npy'),out_data)


paths = glob.glob(os.path.join(dir_path,'*','*','Scan'))
for p in paths:
    print(os.path.abspath(p))
    try:
        process(p)
    except Exception as e:
        with open(os.path.join(p,'error_align.log'),'w') as f:
            f.write(str(e))