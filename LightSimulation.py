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

energyConsumption = 0

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

def publish_data(time_of_day, total_light_intensity, energy_consumption):
    # create message as JSON-String
    message = f'{{"time_of_day": {time_of_day}, "total_light_intensity": {total_light_intensity}, "total_energy_consumption": {energy_consumption}}}'
    # publish message to defined topic
    mqtt_client.publish(mqtt_topic, message)
    print(f"Veröffentlichte Daten: {message}")

def simulate_light_sensor():
    while True:
        # Simulate different light sources and conditions
        time_of_day = time.localtime().tm_hour

        # Adjust light intensity based on time of day
        if 6 <= time_of_day < 18:  # Daytime
            base_intensity = random.randint(50, 100)  # Simuliere Sonnenlicht
        else:  # Nighttime
            base_intensity = random.randint(0, 30)  # Simuliere Dunkelheit

        # Toggle the artificial light based on control commands
        with lock:
            if artificial_light_on:
                artificial_light_intensity = random.randint(50, 100)
            else:
                artificial_light_intensity = 0

        # Calculate the total light intensity
        total_intensity = base_intensity + artificial_light_intensity

        # Publish the simulated data to the sensor topic
        publish_data(time_of_day, total_intensity, energyConsumption)

        # Print the simulated data every 10 seconds
        print(f"Time of Day: {time_of_day}, Total Light Intensity: {total_intensity}")
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
    global energyConsumption

    for _ in range(144):  # Simulate a full 24-hour day (144 intervals of 10 seconds each)
        # Simulate different light sources and conditions
        time_of_day = _ // 6  # 6 intervals per hour, so time_of_day ranges from 0 to 23

        if artificial_light_on:
            energyConsumption += (60 * 10 * 60) # for a 60 watt LED in 10 minutes

        # Adjust light intensity based on time of day
        if 6 <= time_of_day < 18:  # Daytime
            base_intensity = random.randint(50, 100)  # Simulate sunlight
        else:  # Nighttime
            base_intensity = random.randint(0, 30)  # Simulate darkness

        # Automatically toggle the artificial light based on sunrise and sunset simulation
        with lock:
            if 18 <= time_of_day < 19:  # Sunset (turn on artificial light)
                artificial_light_on = True
            elif 5 <= time_of_day < 6:  # Sunrise (turn off artificial light)
                artificial_light_on = False

            # Simulate the artificial light intensity
            if artificial_light_on:
                artificial_light_intensity = 50
            else:
                artificial_light_intensity = 0

        # Calculate the total light intensity
        total_intensity = base_intensity + artificial_light_intensity

        # Publish the simulated data to the sensor topic
        publish_data(time_of_day, total_intensity, energyConsumption)


        # Print the simulated data every 10 seconds
        print(f"Time of Day: {time_of_day}, Total Light Intensity: {total_intensity}, Total Energy Consumption: {energyConsumption}")
        time.sleep(10)

# Create and start threads for simulating light sensor and changing sunlight
light_sensor_thread = threading.Thread(target=simulate_light_sensor)
user_input_thread = threading.Thread(target=user_input)
sunlight_change_thread = threading.Thread(target=sunlight_change)
scenario_thread = threading.Thread(target=scenario1)

user_input_thread.start()
scenario_thread.start()

# Wait for the threads to finish
user_input_thread.join()
scenario_thread.join()