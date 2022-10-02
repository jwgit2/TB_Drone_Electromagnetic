#!/bin/sh

sudo apt update
sudo apt install python3-venv
sudo mkdir -p ../../Measurements/.venvs
sudo python3 -m venv ../../Measurements/.venvs/flask
cd ../../Measurements/
source ./.venvs/flask/bin/activate
