import open3d as o3d
import os


def getPath(data):
    return os.path.join('./OpenXD-OmniObject3D-New/raw/decimated',data,'Scan')

mesh = o3d.io.read_triangle_mesh(os.path.join(getPath('anise/anise_001'),'Scan.obj'))
vis = o3d.visulization.Visualizer()
vis.create_window()
vis.add_geometry(mesh)
vis.run()
vis.destroy_window()