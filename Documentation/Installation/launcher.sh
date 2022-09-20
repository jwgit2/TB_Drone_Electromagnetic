#!/bin/bash

## Website
cd ~/TB_Drone_Electromagnetic/Website/
source .venvs/flask/bin/activate
pip3 install -I -r requirements.txt 
sudo python3 app.py 
