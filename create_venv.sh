#!/bin/sh
python3 -m venv db_interface_venv
source ./db_interface_venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
