# -----------------
# NOT USED 
#
# This Python script connects to an MQTT broker to receive energy consumption messages 
# and stores them in a Redis database. 
# It uses paho-mqtt to subscribe to the "smart_home/simulation" topic and redis to handle data storage.
# 
# -----------------

import paho.mqtt.client as mqtt
import redis
import json
from datetime import datetime

redis_host = 'localhost'
redis_port = 6379
redis_db = 0

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "smart_home/simulation"  

def connect_to_redis():
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    # receive MQTT message and load json 
    message = json.loads(msg.payload)
    print(f"Received message: {message} on topic {msg.topic}")

    r = connect_to_redis()

    message['timestamp'] = str(datetime.now())

    # generate unique key for redis dataset 
    key = f"total_energy_consumption:{message['time_of_day']}:{message['total_light_intensity']}:{message['timestamp']}"

    # save message as hash in redis
    r.hmset(key, message)

    print(f"Successfully saved data in redis with the following key: {key}")

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    # Blocking call - wait for messages
    client.loop_forever()

if __name__ == '__main__':
    start_mqtt_client()
