# INSTALLATIONS

## memory monitoring
pip install psutil

## Mosquitto installation
sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa

sudo apt install mosquitto mosquitto-clients

## VSCode extensions
- SQLite Viewer 
- Python
- Pylance

# START SIMULATION

## start mosquitto
mosquitto -c mosquitto.conf 

## start subscriber in console
mosquitto_sub -h localhost -t "#" -v

## Test publisher (message should to all subscriber -> console and DB)
mosquitto_pub -h localhost -t "test_topic" -m 'Hello, Mosquitto!'

## create database table
python3 sqLite.py

## start bridge between mqtt broker and sqlite db
python3 sqLite-bridge.py 

## start device simulation
python3 LightSimulation.py

# STOP SIMULATION

## stop Mosquitto
sudo systemctl stop mosquitto