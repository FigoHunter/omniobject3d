import importlib
import os

HOME_PATH=os.getenv("WORKSPACE_HOME")
STARTUP_PATH=os.path.join(HOME_PATH,"startup")

dir=STARTUP_PATH

for f in os.listdir(dir):
    path = os.path.join(dir, f)
    if os.path.isdir(path):
        importlib.import_module(f)
