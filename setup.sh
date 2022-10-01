#!/bin/bash
inform "Installation of needed packages"
sudo ./Documentation/Installation/install_pi.sh
inform "Enabling interfaces"
sudo ./Documentation/Installation/enable_interfaces.sh -y
inform "Installation of Qwiic Hat"
sudo ./Documentation/Installation/install_QwiicPiHat.sh
inform "Installation of BME280"
sudo ./Documentation/Installation/install_bme280.sh
inform "Installation of INA219"
sudo ./Documentation/Installation/install_ina219.sh
inform "Installation of Flask website"
sudo ./Documentation/Installation/install_website.sh
inform "Installation done, rebooting now."
sudo reboot now