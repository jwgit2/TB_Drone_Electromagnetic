#!/bin/bash

sudo apt update
sudo python3 -m venv ../../Website/.venvs/flask
cd ../../Website/
source ./.venvs/flask/bin/activate
