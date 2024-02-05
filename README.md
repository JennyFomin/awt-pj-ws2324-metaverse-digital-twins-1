# INSTALLATIONS

## Mosquitto installation
sudo add-apt-repository ppa:mosquitto-dev/mosquitto-ppa

sudo apt install mosquitto mosquitto-clients

## Docker installation
sudo apt install ca-certificates curl apt-transport-https

sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose

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
mosquitto_pub -h localhost -t "test_topic" -m '{"device_id": 1, "value": 25}'

## start bridge between mqtt broker and sqlite db
python3 sqLite-bridge.py 

## start device simulation
python3 iot-device.py