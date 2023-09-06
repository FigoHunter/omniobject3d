@echo off
set WORKSPACE_HOME=%~dp0\..\..
set PYTHONPATH=%PYTHONPATH%;%WORKSPACE_HOME%\packages;%WORKSPACE_HOME%\startup
python %~dp0\decimate_batch.py %WORKSPACE_HOME%\OpenXD-OmniObject3D-New

pause