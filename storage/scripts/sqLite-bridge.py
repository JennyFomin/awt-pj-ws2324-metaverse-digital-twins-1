# -----------------
# NOT USED 
#
# This Python script integrates MQTT with SQLite to store data from smart home simulations. 
# Using the paho-mqtt library, it connects to an MQTT broker and subscribes to a topic. 
# When a message is received, the script decodes the payload from JSON format, 
# extracts relevant data and inserts this data into an SQLite database.
# 
# -----------------

import paho.mqtt.client as mqtt
import sqlite3
import json

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "smart_home/simulation"

# connect to sqLite database
db_connection = sqlite3.connect("smart_home_data.db")
cursor = db_connection.cursor()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    # receive MQTT message and load json 
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    
    time_of_day = data['time_of_day']
    total_light_intensity = data['total_light_intensity']
    total_energy_consumption = data['total_energy_consumption']

    # insert data into sqLite database
    execute_sql_script('insert_data_to_sqLite.sql', (time_of_day, total_light_intensity, total_energy_consumption))
    print(f"Data inserted: {data}")

def execute_sql_script(script_path, parameters):
    with open(script_path, 'r') as script_file:
        sql_script = script_file.read()

    db_connection = sqlite3.connect("smart_home_data.db")
    cursor = db_connection.cursor()

    try:
        # execute sql script with received data from mqtt
        cursor.execute(sql_script, parameters)

        # confirm changes in the database
        db_connection.commit()

        print("Stored data in database")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        db_connection.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)


# Blocking call - wait for messages
client.loop_forever()
