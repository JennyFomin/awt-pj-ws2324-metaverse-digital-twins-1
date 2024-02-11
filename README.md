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

# start performance measurements scripts
.\total-gpu.ps1
python3 memory-usage.py

## start mosquitto
mosquitto -c mosquitto.conf 

## (start subscriber in console)
mosquitto_sub -h localhost -t "#" -v

## (Test publisher (message should to all subscriber -> console and DB))
mosquitto_pub -h localhost -t "test_topic" -m 'Hello, Mosquitto!'

## start mongodb
sudo systemctl start mongod

## run database bridge script
python3 mongoDB-bridge.py

## connect mongoDB compass to database
URI: mongodb://localhost:27017

## start unity application

## start device simulation
python3 LightSimulation.py

# AFTER SIMULATION

## export database as csv file
export data -> export query results -> "all fields" + next -> "csv" + export 

## run visualisation scripts
python3 visualize-energy-data.py
python3 visualize-memory-usage.py
python3 visualize-gpu-usage.py

# STOP SIMULATION

## stop Mosquitto
sudo systemctl stop mosquitto

## stop MongoDB
sudo systemctl stop mongod

## stop unity application