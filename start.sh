#!/bin/bash

echo "Starting backend server, Logging to nohup.out"

cd /workspace/backend-server

source backend-venv/bin/activate

nohup python run.py > nohup.out &

deactivate

echo "Backend server started"