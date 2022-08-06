#!/usr/bin/env bash
set -eu

# MIT License
# (c) 2017 Pimoroni Ltd.
# (c) 2019 Tiryoh

# function define

confirm() {
    if [ "$FORCE" == '-y' ]; then
        true
    else
        read -r -p "$1 [y/N] " response < /dev/tty
        if [[ $response =~ ^(yes|y|Y)$ ]]; then
            true
        else
            false
        fi
    fi
}

prompt() {
        read -r -p "$1 [y/N] " response < /dev/tty
        if [[ $response =~ ^(yes|y|Y)$ ]]; then
            true
        else
            false
        fi
}

success() {
    echo -e "$(tput setaf 2)$1$(tput sgr0)"
}

inform() {
    echo -e "$(tput setaf 6)$1$(tput sgr0)"
}

warning() {
    echo -e "$(tput setaf 1)$1$(tput sgr0)"
}

newline() {
    echo ""
}

progress() {
    count=0
    until [ $count -eq 7 ]; do
        echo -n "..." && sleep 1
        ((count++))
    done;
    if ps -C $1 > /dev/null; then
        echo -en "\r\e[K" && progress $1
    fi
}


# main script


if ls /dev/spi* &> /dev/null; then
	inform "SPI already enabled"
else
	if command -v raspi-config > /dev/null && sudo raspi-config nonint get_spi | grep -q "1"; then
		sudo raspi-config nonint do_spi 0
		inform "SPI is now enabled"
	else
		warning "Error enabling SPI"
	fi
fi

if ls /dev/i2c* &> /dev/null; then
	inform "I2C already enabled"
else
	if command -v raspi-config > /dev/null && sudo raspi-config nonint get_i2c | grep -q "1"; then
		sudo raspi-config nonint do_i2c 0
		inform "I2C is now enabled"
	else
		warning "Error enabling I2C"
	fi
fi