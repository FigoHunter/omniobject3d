set WORKSPACE_HOME=%~dp0\..\..
set PYTHONPATH=%PYTHONPATH%;%WORKSPACE_HOME%\packages;%WORKSPACE_HOME%\startup
python %~dp0\batch_alignment.py Y:\hddisk5\users\yifei\omniobject3d\OpenXD-OmniObject3D-New\raw\decimated

pause