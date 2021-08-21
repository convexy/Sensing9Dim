#!/usr/bin/bash
sudo apt -y update
sudo apt -y dist-upgrade
sudo apt -y autoremove

sudo apt -y install python3 python3-pip python3-venv sqlite3

python3 -m venv .
source bin/activate
python3 -m pip install -r requirements.txt

sqlite3 db/main.sqlite3 < db/ddl.sql
