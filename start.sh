#!/bin/bash

# -----------------
#
# This script starts the required services for the project:
#   - Mosquitto MQTT
#   - MongoDB
#   - IoT Device Simulation
# 
# -----------------

# Keep-alive: update existing `sudo` timestamp until script has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

if command -v systemctl &> /dev/null
then
    echo "Running on native Linux"
    echo -n "Starting Mosquitto..."
    sudo mosquitto -c messaging/mosquitto.conf &
    echo "done."

    echo -n "Starting MongoDB Server..."
    sudo systemctl start mongod &
    echo "done."
else
    echo "Running on Windows Subsystem for Linux"
    echo -n "Starting Mosquitto..."
    sudo mosquitto -c messaging/mosquitto.conf &
    echo "done."

    echo -n "Starting MongoDB Server..."
    mongod_path=$(which mongod)
    sudo $mongod_path 
    echo "done."
fi

echo -n "Starting IoT Device Simulation..."
tmux new-session -d -s light_simulation 'python3 simulation/LightSimulation.py'
echo "done."

tmux attach-session -t light_simulation