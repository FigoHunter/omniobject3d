import os
import glob
import open3d as o3d
import json

dir_path=r'./OpenXD-OmniObject3D-New/raw/decimated'

points_index=[0,1,7,2,3,6,4,5,3]

def drawbox(points):
    lines = [[0,1],[1,2],[2,3],[3,0],
             [4,5],[5,6],[6,7],[7,4],
             [0,4],[1,5],[2,6],[3,7]]

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


def process(path):
    mesh = o3d.io.read_triangle_mesh(os.path.join(path,'Scan.obj'))
    with open(os.path.join(path,'Scan.json'),'r') as f:
        data = json.load(f)['data']
        for piece in data:
            mat = piece['matrix']
            mesh.transform(mat)
            bbox = mesh.get_minimal_oriented_bounding_box()
            points = bbox.get_box_points()
            points = [points[x] for x in points_index]
            box_shape=drawbox(points)
            o3d.visualization.draw_geometries(box_shape)
            


paths = glob.glob(os.path.join(dir_path,'*','*','Scan'))
for p in paths:
    print(os.path.abspath(p))
    process(p)
    pass