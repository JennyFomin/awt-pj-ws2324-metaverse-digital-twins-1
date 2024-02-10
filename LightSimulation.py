import time
import random
import threading
import paho.mqtt.client as mqtt

# MQTT broker settings
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "smart_home/simulation"
control_topic = "light_control"

# Initial state of the artificial light
artificial_light_on = False


# Lock for synchronizing access to shared variables
lock = threading.Lock()

# initialize MQTT Client 
mqtt_client = mqtt.Client()

# Callback Funktion für erfolgreiche Verbindung
def on_connect(client, userdata, flags, rc):
    print(f"Verbunden mit MQTT Broker mit Resultat-Code: {rc}")

# Callback Funktion für eingehende Nachrichten
def on_message(client, userdata, msg):
    global artificial_light_on
    payload = msg.payload.decode("utf-8")

    if msg.topic == control_topic:
        with lock:
            if payload.lower() == "on":
                artificial_light_on = True
                print("Artificial Light is ON")
            elif payload.lower() == "off":
                artificial_light_on = False
                print("Artificial Light is OFF")


# set Callback function
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT Broker 
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Starte den Netzwerk-Schleifen-Thread im Hintergrund
mqtt_client.loop_start()

def publish_data(time_of_day, total_light_intensity):
    # create message as JSON-String
    message = f'{{"time_of_day": {time_of_day}, "total_light_intensity": {total_light_intensity}}}'
    # publish message to defined topic
    mqtt_client.publish(mqtt_topic, message)
    print(f"Veröffentlichte Daten: {message}")

def simulate_light_sensor():
    while True:
        # Simulate different light sources and conditions
        time_of_day = time.localtime().tm_hour

        # Adjust light intensity based on time of day
        if 6 <= time_of_day < 18:  # Daytime
            intensity = random.randint(650, 1023)  # Simuliere Sonnenlicht
        else:  # Nighttime
            intensity = random.randint(0, 150)  # Simuliere Dunkelheit

        scaledIntensity = float(intensity) / float(1023)

        # Publish the simulated data to the sensor topic
        publish_data(time_of_day, scaledIntensity)

        # Print the simulated data every 10 seconds
        print(f"Time of Day: {time_of_day}, Total Light Intensity: {scaledIntensity}")
        time.sleep(10)

def sunlight_change():
    while True:
        # Change sunlight mode every two minutes
        with lock:
            print("Changing sunlight mode...")
        time.sleep(120)

def user_input():
    global artificial_light_on
    while True:
        # Read user input to control the artificial light
        command = input("Enter 'on' to turn on the artificial light, 'off' to turn it off: ").lower()
        with lock:
            if command == "on":
                artificial_light_on = True
                print("Artificial Light is ON")
            elif command == "off":
                artificial_light_on = False
                print("Artificial Light is OFF")
            else:
                print("Invalid command. Enter 'on' or 'off'.")

def scenario1():
    global artificial_light_on

    while(True):
        for _ in range(144):  # Simulate a full 24-hour day (144 intervals of 10 seconds each)
            # Simulate different light sources and conditions
            time_of_day = _ / 6  # 6 intervals per hour, so time_of_day ranges from 0 to 23

            # Adjust light intensity based on time of day
            if 6 <= time_of_day < 18:  # Daytime
                intensity = random.randint(650, 1023)  # Simulate sunlight
            else:  # Nighttime
                intensity = random.randint(0, 200)  # Simulate darkness

            scaledIntensity = float(intensity) / float(1023)

            # Publish the simulated data to the sensor topic
            publish_data(time_of_day, scaledIntensity)

            # Print the simulated data every 10 seconds
            print(f"Time of Day: {time_of_day}, Total Light Intensity: {scaledIntensity}")

            time.sleep(10)

# Create and start threads for simulating light sensor and changing sunlight


user_input_thread = threading.Thread(target=user_input)
sunlight_change_thread = threading.Thread(target=sunlight_change)
scenario_thread = threading.Thread(target=scenario1)

user_input_thread.start()
scenario_thread.start()

# Wait for the threads to finish
user_input_thread.join()
scenario_thread.join()