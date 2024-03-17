#!/bin/bash

# -----------------
#
# This script stops the required services for the project: 
#   - IoT Device Simulation
#   - Mosquitto MQTT
#   - MongoDB
# 
# -----------------

# Keep-alive: update existing `sudo` timestamp until script has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

echo -n "Stopping IoT Device Simulation..."
sudo pkill -f LightSimulation.py
echo "done."

echo -n "Stopping Mosquitto..."
sudo systemctl stop mosquitto
echo "done."

echo -n "Stopping MongoDB..."
sudo sudo systemctl stop mongod
echo "done."