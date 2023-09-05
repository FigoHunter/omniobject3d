import os
import tarfile
import threading
from queue import Queue

THREADCOUNT=16
data_path='./OpenXD-OmniObject3D-New/'

q = Queue(maxsize=100)
threads=[]

def worker(queue,index):
    while True:
        file = queue.get()
        target = file.replace('.tar.gz','')
        try:
            print(f'[THREAD-{index}] extracting: '+file)
            tar = tarfile.open(file,':gz')
            for extracted_file in tar.getnames():
                if not os.path.exists(os.path.join(target, extracted_file)):
                    tar.extract(extracted_file,target)
                    print(f'[THREAD-{index}] '+ extracted_file)
                else:
                    print(f'[THREAD-{index}] skip: ' + extracted_file)
            tar.close()
            os.remove(file)
        except Exception as e:
            print(f'[THREAD-{index}] '+str(e))
            print(f'[THREAD-{index}] Fail with: ' + str(file))
        q.task_done()


for i in range(THREADCOUNT):
    t=threading.Thread(None,target=worker,args=(q,i,),daemon=True)
    threads.append(t)
    t.start()

for root, dirs, files in os.walk(data_path):
    for file in files:
        file = os.path.join(root, file)
        if file.endswith('.tar.gz'):
            q.put(file)

q.join()