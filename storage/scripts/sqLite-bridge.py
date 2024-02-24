import paho.mqtt.client as mqtt
import sqlite3
import json

# MQTT-Einstellungen
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "smart_home/simulation"  # Topic anpassen an das, was in LightSimulation.py verwendet wird

# SQLite-Datenbankverbindung herstellen
db_connection = sqlite3.connect("smart_home_data.db")
cursor = db_connection.cursor()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    
    # Extrahieren der Daten
    time_of_day = data['time_of_day']
    total_light_intensity = data['total_light_intensity']
    total_energy_consumption = data['total_energy_consumption']

    # Daten in SQLite einfügen
    execute_sql_script('insert_data.sql', (time_of_day, total_light_intensity, total_energy_consumption))
    print(f"Data inserted: {data}")

def execute_sql_script(script_path, parameters):
    with open(script_path, 'r') as script_file:
        sql_script = script_file.read()

    # SQLite-Datenbankverbindung herstellen
    db_connection = sqlite3.connect("smart_home_data.db")
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

# MQTT-Client initialisieren
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Mit dem MQTT-Broker verbinden
client.connect(mqtt_broker, mqtt_port, 60)

# MQTT-Client in Endlosschleife laufen lassen
client.loop_forever()
