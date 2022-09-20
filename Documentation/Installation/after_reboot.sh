#!/bin/bash
sudo ./enable_interfaces.sh
sudo ./install_QwiicPiHat.sh
sudo ./install_bme280.sh
sudo ./install_ina219.sh
sudo ./install_website.sh

sudo reboot now