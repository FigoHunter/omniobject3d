import bpy
import os
from blender_figo import file
from blender_figo import environ
import math
import threading
import psutil
import time
import sys
import platform
import subprocess

DECIMATE_ITERATE_RATION=0.8

def kill():
    if platform.system().lower() == 'windows':
        subprocess.run(f"taskkill /f /pid {str(os.getpid())}", shell=True)
    elif platform.system().lower() == 'linux':
        subprocess.run(f"kill -9 {str(os.getpid())}", shell=True)

def checkParentProcess(pid):
    print(f"ChildProcess[{os.getpid()}] monitor ParentProcess[{pid}] status")        
    while True:
        try:
            if not pid or psutil.Process(pid) is None:
                kill()
        except Exception as e:
            kill()
        time.sleep(2)

def process(input, output):
    print(input)
    print(output)
    file.importFile(input)
    modifierName='DecimateMod'
    objectList=bpy.data.objects

    face_count=0
    for obj in objectList:
        if(obj.type=="MESH"):
            face_count=face_count+len(obj.data.polygons)

    decimateRatio=min(1,3000/face_count)
    numberOfIteration=math.ceil(math.log(decimateRatio,DECIMATE_ITERATE_RATION))

    for i in range(0,numberOfIteration):
        for obj in objectList:
            if(obj.type=="MESH"):
                # bf_modifier.cleanAllDecimateModifiers(obj)
                modifier=obj.modifiers.new(modifierName,'DECIMATE')
                modifier.ratio=DECIMATE_ITERATE_RATION
                modifier.use_collapse_triangulate=True

    file.exportFile(output)

if __name__=='__main__':
    ppid=environ.getEnvVar("PARENT_PID")
    if ppid:
        ppid=int(ppid)
        t=threading.Thread(None,checkParentProcess,"CheckParentProcess",(ppid,),daemon=True)
        t.start()
    objs = environ.getEnvVarAsList("ROSITA_OBJS")
    import bpy
    for f in objs:
        print(f)
        name = os.path.basename(f)
        f=os.path.abspath(f)
        target = f.replace("raw_scans","decimated")
        def postaction():
            process(f,target)
        file.newFile(postaction)
        