import os
import sys
import glob
from blender_figo import file
import subprocess
import time
import threading
from queue import Queue

BATCH_SIZE=10

fileQ=[]


# Yield successive n-sized
# chunks from l.
def divide_chunks(list, n):
    # looping till length l
    for i in range(0, len(list), n):
        yield list[i:i + n]


if __name__=='__main__':
    dir = os.path.abspath(sys.argv[1])
    globpath = os.path.join(dir,"**","*.obj")
    fileList = glob.glob(globpath,recursive=True)
    print(globpath)
    print(fileList)
    import platform
    index=0
    pid=os.getpid()


    for f in divide_chunks(fileList, BATCH_SIZE):
        workspace_home=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
        script_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'decimate.py'))
        if platform.system().lower() == 'windows':
            cmd = f"set ROSITA_OBJS={';'.join(f)}\n" + \
                "@echo off\n"+\
                f"set PARENT_PID={str(pid)}\n"+\
                f"set WORKSPACE_HOME={workspace_home}\n"+\
                r"set PYTHONPATH=%PYTHONPATH%;%WORKSPACE_HOME%\packages;%WORKSPACE_HOME%\startup"+"\n"+\
                r"set BLENDER_SYSTEM_SCRIPTS=%WORKSPACE_HOME%\startup;%BLENDER_SYSTEM_SCRIPTS%"+"\n"+\
                rf"Unity.exe -projectPath %WORKSPACE_HOME%\Unity-Physical-Alignment -executeMethod SetupObject.Execute_Main -batchmode -quit -logfile -"
        else:
            raise Exception('系统未支持: '+ platform.system().lower())
        t=time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        tempFile=os.path.join(workspace_home,"temp",f"{t}---{index}.bat")
        file.createTmpFile(tempFile, content=cmd)
        fileQ.append(tempFile)
        # process = subprocess.Popen(f"chmod +x {tempFile}&&{tempFile}", shell=True)
        # process_list.append(process)
        index=index+1

    for path in fileQ:
        with open(os.path.splitext(path)[0]+".log","w") as f:
            if platform.system().lower() == 'windows':
                process = subprocess.Popen(f"{path}", shell=True, stdout=f, stderr=f)
            else:
                raise Exception('系统未支持: '+ platform.system().lower())
            process.wait()