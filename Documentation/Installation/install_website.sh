#!/bin/bash

sudo apt update
sudo apt install python3.10-venv
sudo mkdir -p ../../Measurements/.venvs
sudo python3 -m venv ../../Measurements/.venvs/flask
cd ../../Measurements/
sudo source ./.venvs/flask/bin/activate
