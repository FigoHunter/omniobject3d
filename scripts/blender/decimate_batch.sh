#!/bin/bash
export WORKSPACE_HOME=$(dirname $(readlink -f "$0"))/../..
export PYTHONPATH=${PYTHONPATH}:${WORKSPACE_HOME}/packages:${WORKSPACE_HOME}/startup
python ${WORKSPACE_HOME}/scripts/blender/decimate_batch.py ${WORKSPACE_HOME}/OpenXD-OmniObject3D-New