# -----------------
#
# This Python script simulates a smart home light sensor environment using MQTT for communication. 
# It features a light sensor simulation that adjusts its readings based on the time of day, 
# simulating sunlight during the day and darkness at night. 
# The script uses paho-mqtt to connect to an MQTT broker, publish simulated light intensity data 
# to the mqtt topic, and listen for control commands on the control topic 
# to turn an artificial light on or off.
# 
# -----------------

import time
import random
import threading
import paho.mqtt.client as mqtt

# MQTT broker settings
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "smart_home/light_sensor"
control_topics = ["light_control_1", "light_control_2", "light_control_3",
                  "light_control_4", "light_control_5", "light_control_6"]

artificial_lights = [False,False,False,False,False,False]

# Lock for synchronizing access to shared variables
lock = threading.Lock()

# initialize MQTT Client 
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print(f"Connected with mqtt broker with the id: {rc}")
    for topic in control_topics:
        client.subscribe(topic)


def on_message(client, userdata, msg):

    payload = msg.payload.decode("utf-8")

    # control light based on feedback from digital twin
    for i in range(0, len(control_topics)):
        if msg.topic == control_topics[i]:
            with lock:
                if payload.lower() == "on":
                    artificial_lights[i] = True
                    print("Turn light " + str(i + 1) + " on")
                elif payload.lower() == "off":
                    artificial_lights[i] = False
                    print("Turn light" + str(i + 1) + " off")


# set Callback function
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT Broker 
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Starte den Netzwerk-Schleifen-Thread im Hintergrund
mqtt_client.loop_start()

# Publish the simulated data to the sensor topic


def publish_data(time_of_day, total_light_intensity):
    # create message as JSON-String
    message = f'{{"time_of_day": {time_of_day}, "total_light_intensity": {total_light_intensity}}}'

    mqtt_client.publish(mqtt_topic, message)
    print(f"Veröffentlichte Daten: {message}")


def simulate_light_sensor():
    while True:
        # Simulate different light sources and conditions
        time_of_day = time.localtime().tm_hour

        # Adjust light intensity based on time of day
        if 6 <= time_of_day < 18:  # Daytime
            intensity = random.randint(650, 1023)  
        else:  # Nighttime
            intensity = random.randint(0, 150)  

        scaled_intensity = float(intensity) / float(1023)

        publish_data(time_of_day, scaled_intensity)

        print(f"Time of Day: {time_of_day}, Total Light Intensity: {scaled_intensity}")
        time.sleep(10)

# Change sunlight mode every two minutes


def sunlight_change():
    while True:
        with lock:
            print("Changing sunlight mode...")
        time.sleep(120)

# Read user input to control the artificial light


def user_input():
    global artificial_light_on
    while True:
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

    while(True):
        for _ in range(144):  # Simulate a full 24-hour day (144 intervals of 10 seconds each)
            # Simulate different light sources and conditions
            time_of_day = _ / 6  # 6 intervals per hour, so time_of_day ranges from 0 to 23

            # Adjust light intensity based on time of day
            if 6 <= time_of_day < 18:  # Daytime
                intensity = random.randint(650, 1023) 
            else:  # Nighttime
                intensity = random.randint(0, 200) 

            scaled_intensity = float(intensity) / float(1023)

            publish_data(time_of_day, scaled_intensity)

            print(f"Time of Day: {time_of_day}, Total Light Intensity: {scaled_intensity}")

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