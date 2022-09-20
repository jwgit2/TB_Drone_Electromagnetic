#!/bin/bash

sudo apt update
sudo python3 -m venv ../../Website/.venvs/flask
sudo touch ../../Website/.venvs/.gitignore
sudo echo "flask/" >> ../../Website/.venvs/.gitignore
source ../../Website/.venvs/flask/bin/activate
sudo pip3 install Flask
sudo pip3 install flask-sqlalchemy
cd ../../Website/
pip3 freeze> requirements.txt