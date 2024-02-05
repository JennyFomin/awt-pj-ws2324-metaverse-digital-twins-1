import paho.mqtt.client as mqtt
import sqlite3
import json
import time

# MQTT-Einstellungen
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "#"  # Hier könntest du das spezifische MQTT-Thema für deine IoT-Daten anpassen


def execute_sql_script(script_path, parameters):
    with open(script_path, 'r') as script_file:
        sql_script = script_file.read()

    # SQLite-Datenbankverbindung herstellen
    db_connection = sqlite3.connect("energy_data.db")
    cursor = db_connection.cursor()

    try:
        # SQL-Skript mit Parametern ausführen
        cursor.execute(sql_script, parameters)

        # Änderungen in der Datenbank bestätigen
        db_connection.commit()

        print("Daten in die Datenbank geschrieben")

    except Exception as e:
        print(f"Fehler beim Ausführen des SQL-Skripts: {e}")

    finally:
        # Verbindung schließen
        db_connection.close()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit dem MQTT-Broker mit Resultat-Code: " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        timestamp = int(time.time())
        topic = msg.topic

        # Hier könntest du weitere Datenverarbeitung und Anpassungen vornehmen,
        # abhängig von der Struktur deiner IoT-Daten

        # SQL-Skript ausführen
        execute_sql_script('insert_data.sql', (timestamp, topic, payload))

        print(f"Daten empfangen und in die Datenbank geschrieben: {data}")

    except Exception as e:
        print(f"Fehler beim Verarbeiten der MQTT-Nachricht: {e}")

# MQTT-Client initialisieren
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Mit dem MQTT-Broker verbinden
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# MQTT-Client in einer Schleife laufen lassen
mqtt_client.loop_forever()
