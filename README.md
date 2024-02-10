# INSTALLATIONS

## memory monitoring
pip install psutil
pip install pymongo
pip install paho-mqtt

## Mosquitto installation
sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa

sudo apt install mosquitto mosquitto-clients

## MongoDB installation
https://www.mongodb.com/docs/manual/administration/install-community/

# MongoDB Compass installation
https://www.mongodb.com/try/download/compass

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

## run database bridge script
python3 mongoDB-bridge.py

## connect mongoDB compass to database
URI: mongodb://localhost:27017

## start device simulation
python3 LightSimulation.py


# STOP SIMULATION

## stop Mosquitto
sudo systemctl stop mosquitto

## stop MongoDB
sudo systemctl stop mongod
