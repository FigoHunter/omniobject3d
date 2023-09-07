import os
import sys
import glob
from blender_figo import file
import subprocess
import time
import shutil
import threading
from queue import Queue

PROCESS_COUNT=4
BATCH_SIZE=10

fileQ=Queue()


# Yield successive n-sized
# chunks from l.
def divide_chunks(list, n):
    # looping till length l
    for i in range(0, len(list), n):
        yield list[i:i + n]

def startProcessThread(q,index):
    while True:
        path = q.get()
        if path == "end":
            print(f"[THREAD-{index}] Exit On End")
            break
        if not os.path.exists(path):
            print(f"THREAD-{index}] Command File Not Found: {path}")
            continue
        print(f"[THREAD-{index}] Working On: {path}")
        with open(os.path.splitext(path)[0]+".log","w") as f:
            if platform.system().lower() == 'windows':
                process = subprocess.Popen(f"{path}", shell=True, stdout=f, stderr=f)
            elif platform.system().lower() == 'linux':
                process = subprocess.Popen(f"chmod +x {path}&&{path}", shell=True, stdout=f, stderr=f)
            else:
                raise Exception('系统未支持: '+ platform.system().lower())
            process.wait()
        print(f"[THREAD-{index}] Done")


if __name__=='__main__':
    dir = os.path.abspath(sys.argv[1])
    fileList = glob.glob(os.path.join(dir,"**","*.obj"),recursive=True)
    rmls=[]
    for f in fileList:
        if "decimated" in f:
            print(f"remove: {f}")
            rmls.append(f)
    for f in rmls:
        fileList.remove(f)
    import platform
    index=0
    pid=os.getpid()

    for i in range(PROCESS_COUNT):
        thread = threading.Thread(None,startProcessThread,args=(fileQ,i,),daemon=True)
        thread.start()


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
                f"blender.exe --background --log-level -1 --python {script_path}"
        elif platform.system().lower() == 'linux':
            cmd = f"export ROSITA_OBJS={':'.join(f)}\n" + \
                "#!/bin/bash\n"+\
                f"export PARENT_PID={str(pid)}\n"+\
                "export  WORKSPACE_HOME={workspace_home}\n"+\
                "export PYTHONPATH=${PYTHONPATH}:${WORKSPACE_HOME}/packages:${WORKSPACE_HOME}/startup\n"+\
                "export BLENDER_SYSTEM_SCRIPTS=${WORKSPACE_HOME}/startup:${BLENDER_SYSTEM_SCRIPTS}\n"+\
                f"blender --background --log-level -1 --python {script_path}"
        else:
            raise Exception('系统未支持: '+ platform.system().lower())
        t=time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        tempFile=os.path.join(workspace_home,"temp",f"{t}---{index}.bat")
        file.createTmpFile(tempFile, content=cmd)
        fileQ.put(tempFile)
        # process = subprocess.Popen(f"chmod +x {tempFile}&&{tempFile}", shell=True)
        # process_list.append(process)
        index=index+1

    for i in range(PROCESS_COUNT):
        fileQ.put("end")
        