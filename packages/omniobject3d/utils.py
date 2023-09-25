import os

HOME_PATH=os.environ.get("WORKSPACE_HOME",'')
DATASET_PATH=os.path.join(HOME_PATH,"OpenXD-OmniObject3D-New")

def getAffineMat(matrix):
    import numpy as np
    affine_mat = matrix.copy()
    affine_mat = np.insert(affine_mat,3,values=[0,0,0],axis=1)
    affine_mat = np.insert(affine_mat,3,values=[0,0,0,1],axis=0)
    return affine_mat
