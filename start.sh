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

echo -n "Starting Mosquitto..."
sudo systemctl start mosquitto
while [[ $(systemctl is-active mosquitto) == "activating" ]]; do
  sleep 1
done
echo "done."

echo -n "Starting MongoDB Server..."
sudo systemctl start mongod
echo "done."

echo -n "Starting IoT Device Simulation..."
tmux new-session -d -s light_simulation 'python3 simulation/LightSimulation.py'
echo "done."

tmux attach-session -t light_simulation