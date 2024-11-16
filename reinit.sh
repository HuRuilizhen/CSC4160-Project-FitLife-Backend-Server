#!/bin/bash

echo "Re-initializing backend server. Operation will delete current database. Type yes to continue:"

read input

if [ "$input" != "yes" ]; then
    echo "Operation cancelled"
    exit 0
fi

cd /workspace/backend-server

./stop.sh

rm instance/site.db

source backend-venv/bin/activate

python init_db.py

deactivate

cd -

echo "Backend server reinitialized."