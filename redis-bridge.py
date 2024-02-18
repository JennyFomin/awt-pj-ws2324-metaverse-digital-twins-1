import paho.mqtt.client as mqtt
import redis
import json
from datetime import datetime

# Redis-Verbindungseinstellungen
redis_host = 'localhost'
redis_port = 6379
redis_db = 0

# MQTT-Einstellungen
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "smart_home/simulation"  # Topic für Energieverbrauchsdaten

def connect_to_redis():
    # Verbindung zu Redis herstellen
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    # Nachricht von MQTT empfangen und JSON-Format annehmen
    message = json.loads(msg.payload)
    print(f"Received message: {message} on topic {msg.topic}")

    # Redis-Verbindung herstellen
    r = connect_to_redis()

    # Zeitstempel zum Nachrichtenobjekt hinzufügen
    message['timestamp'] = str(datetime.now())

    # Eindeutigen Schlüssel für Redis-Datensatz generieren
    key = f"total_energy_consumption:{message['time_of_day']}:{message['total_light_intensity']}:{message['timestamp']}"

    # Nachricht in Redis als Hash speichern
    r.hmset(key, message)

    print(f"Daten erfolgreich in Redis gespeichert unter dem Schlüssel: {key}")

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    # Blocking call - auf Nachrichten warten
    client.loop_forever()

if __name__ == '__main__':
    start_mqtt_client()
