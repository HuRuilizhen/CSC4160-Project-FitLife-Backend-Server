#!/bin/bash

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $(basename $0) [-h|--help]"
    echo "This script checks for and stops the process running on port 5004."
    exit 0
fi

PID=$(lsof -i :5004 -t)

if [ -z "$PID" ]; then
    echo "No process is running on port 5004."
else
    echo "Process ID $PID is running on port 5004. Attempting to stop it..."
    
    kill -15 $PID
    
    if kill -0 $PID > /dev/null 2>&1; then
        echo "Process $PID did not terminate gracefully, forcing shutdown."
        kill -9 $PID
    else
        echo "Process $PID has been stopped successfully."
    fi
fi