import paho.mqtt.client as mqtt
import pymongo
import json
from datetime import datetime

# MongoDB-Verbindungseinstellungen
mongo_host = 'localhost'
mongo_port = 27017
mongo_db_name = 'smart_home_db'

# MQTT-Einstellungen
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic_energy_data = "smart_home/energy_data"  # Erstes Topic
mqtt_topic_simulation_data = "smart_home/simulation_data"  # Neues Topic
mqtt_topic_energy_data_DT = "smart_home/energy_data_DT"  # Erstes Topic
mqtt_topic_simulation_data_DT = "smart_home/simulation_data_DT"  # Neues Topic

def connect_to_mongodb():
    # Verbindung zu MongoDB herstellen
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_db_name]
    return db

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Abonnieren beider Topics
    client.subscribe([(mqtt_topic_energy_data, 0), (mqtt_topic_simulation_data, 0), (mqtt_topic_simulation_data_DT, 0), (mqtt_topic_energy_data_DT, 0)])

def on_message(client, userdata, msg):
    # Verbindung zur MongoDB-Datenbank herstellen
    db = connect_to_mongodb()

    message = json.loads(msg.payload)
    print(f"Received message: {message} on topic {msg.topic}")

    # Zeitstempel zum Nachrichtenobjekt hinzufügen
    message['timestamp'] = datetime.now()

    # Unterscheidung, von welchem Topic die Nachricht stammt
    if msg.topic == mqtt_topic_energy_data:
        # Speichern in der 'energy_data' Kollektion
        collection = db['energy_data']
    elif msg.topic == mqtt_topic_simulation_data:
        # Speichern in der 'simulation_data' Kollektion
        collection = db['simulation_data']
    elif msg.topic == mqtt_topic_simulation_data_DT:
        # Speichern in der 'simulation_data' Kollektion
        collection = db['simulation_data_DT']
    elif msg.topic == mqtt_topic_energy_data_DT:
        # Speichern in der 'simulation_data' Kollektion
        collection = db['energy_data_DT']

    # Nachricht in der entsprechenden MongoDB-Kollektion speichern
    result = collection.insert_one(message)
    print(f"Daten erfolgreich in {collection.name} gespeichert, Dokument-ID: {result.inserted_id}")

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    # Blocking call - auf Nachrichten warten
    client.loop_forever()

if __name__ == '__main__':
    start_mqtt_client()
