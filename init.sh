#!/bin/bash

python3 -m venv backend-venv

source backend-venv/bin/activate

pip install -r requirements.txt

python init_db.py

deactivate