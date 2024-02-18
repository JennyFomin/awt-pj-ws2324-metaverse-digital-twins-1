import time
import random
import paho.mqtt.client as mqtt

# MQTT-Einstellungen
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "energy_consumption/iot_device_1"

# Funktion zum Simulieren des Energieverbrauchs
def simulate_energy_consumption():
    # Hier könntest du eine einfachere oder komplexere Logik für die Energieverbrauchssimulation implementieren
    return random.uniform(1.0, 10.0)  # Simuliert einen zufälligen Energieverbrauch zwischen 1 und 10 Einheiten

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit dem MQTT-Broker mit Resultat-Code: " + str(rc))

def on_publish(client, userdata, mid):
    print("Nachricht veröffentlicht mit MID: " + str(mid))

# MQTT-Client initialisieren
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

# Mit dem MQTT-Broker verbinden
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Simuliere Energieverbrauch und sende Daten an Mosquitto
while True:
    energy_consumption = simulate_energy_consumption()
    message = f"{{\"energy_consumption\": {energy_consumption}}}"

    result = mqtt_client.publish(mqtt_topic, message)
    print(f"Simulierter Energieverbrauch: {energy_consumption}")

    time.sleep(5)  # Warte 5 Sekunden vor der nächsten Simulation
