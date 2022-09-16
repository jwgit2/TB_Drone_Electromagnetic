#!/bin/bash

sudo apt update
sudo python3 -m venv ../../Website/.venvs/flask
sudo touch ../../Website/.venvs/.gitignore
sudo echo "flask/" >> ../../Website/.venvs/.gitignore
sudo git add ../../Website/.venvs/* ../../Website/.venvs/.gitignore
source ../../Website/.venvs/flask/bin/activate
cd ../../Website/
pip3 install Flask gunicorn
pip3 freeze> requirements.txt
