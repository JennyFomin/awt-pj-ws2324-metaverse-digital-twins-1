# -----------------
#
# This Python script integrates MQTT with MongoDB to store energy data 
# from smart home devices or the ditigal twin. 
# It uses paho-mqtt for MQTT communication and pymongo for MongoDB operations. 
# The script is configured to subscribe to four MQTT topics. 
# The collection in which the data is stored depends on the topic of the received message.
# 
# -----------------

import paho.mqtt.client as mqtt
import pymongo
import json
from datetime import datetime

mongo_host = 'localhost'
mongo_port = 27017
mongo_db_name = 'SmartHomeDB'

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic_energy_data = "smart_home/energy_data"  # Erstes Topic
mqtt_topic_simulation_data = "smart_home/simulation_data"  # Neues Topic
mqtt_topic_energy_data_DT = "smart_home/energy_data_DT"  # Erstes Topic
mqtt_topic_simulation_data_DT = "smart_home/simulation_data_DT"  # Neues Topic

def connect_to_mongodb():
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_db_name]
    return db

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # subscribe to all topics
    client.subscribe([(mqtt_topic_energy_data, 0), (mqtt_topic_simulation_data, 0), (mqtt_topic_simulation_data_DT, 0), (mqtt_topic_energy_data_DT, 0)])

def on_message(client, userdata, msg):
    db = connect_to_mongodb()
    # receve and decode message
    message = json.loads(msg.payload)
    print(f"Received message: {message} on topic {msg.topic}")

    message['timestamp'] = datetime.now()

    # choose collection according to the topic the message received from
    if msg.topic == mqtt_topic_energy_data:
        collection = db['EnergyData']
    elif msg.topic == mqtt_topic_simulation_data:
        collection = db['SimulationData']
    elif msg.topic == mqtt_topic_simulation_data_DT:
        collection = db['SimulationDataDT']
    elif msg.topic == mqtt_topic_energy_data_DT:
        collection = db['EnergyDataDT']

    # store data in chosen db collection
    result = collection.insert_one(message)
    print(f"Successfully saved data in {collection.name}, document-id: {result.inserted_id}")

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    # Blocking call - wait for messages
    client.loop_forever()

if __name__ == '__main__':
    start_mqtt_client()
