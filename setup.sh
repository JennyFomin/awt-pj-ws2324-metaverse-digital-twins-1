#!/bin/bash

# -----------------
#
# This script installs the required packages for the project:
#   - Mosquitto MQTT
#   - MongoDB
#   - MongoDB Compass
#   - tmux
#   - Required Python packages
# 
# -----------------


# Spinner function to show progress
spinner() {
    local pid=$!
    local delay=0.75
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}


# Ask for the password upfront
echo "Please enter your password for installation process:"
sudo -v

# Keep-alive: update existing `sudo` timestamp until script has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

echo -n "Installing Mosquitto MQTT..."
(sudo apt-get update > /dev/null && sudo apt-get install -y mosquitto > /dev/null) & spinner
echo "done."

echo -n "Installing MongoDB..."
(sudo wget https://downloads.mongodb.com/compass/mongodb-mongosh_2.2.0_amd64.deb > /dev/null) & spinner
(sudo dpkg -i mongodb-mongosh_2.2.0_amd64.deb > /dev/null) & spinner
(sudo apt-get install -f > /dev/null) & spinner
echo "done."

echo -n "Installing tmux..."
(sudo apt-get install -y tmux > /dev/null) & spinner
echo "done."

echo -n "Installing required Python packages..."
(pip3 install -r requirements.txt > /dev/null) & spinner
echo "done."



https://downloads.mongodb.com/compass/mongodb-mongosh_2.2.0_amd64.deb