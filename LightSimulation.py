import time
import random
import paho.mqtt.client as mqtt
import threading

# MQTT broker settings
broker_address = "your_broker_address"
broker_port = 1883
sensor_topic = "light_sensor_data"
control_topic = "light_control"

# Initial state of the artificial light
artificial_light_on = False

# Lock for synchronizing access to shared variables
lock = threading.Lock()


def simulate_light_sensor():
    while True:
        # Simulate different light sources and conditions
        time_of_day = time.localtime().tm_hour

        # Adjust light intensity based on time of day
        if 6 <= time_of_day < 18:  # Daytime
            base_intensity = random.randint(50, 100)  # Simulate sunlight
        else:  # Nighttime
            base_intensity = random.randint(0, 30)  # Simulate darkness

        # Toggle the artificial light based on control commands
        with lock:
            if artificial_light_on:
                artificial_light_intensity = random.randint(50, 100)
            else:
                artificial_light_intensity = 0

        # Calculate the total light intensity
        total_intensity = base_intensity + artificial_light_intensity

        # Publish the simulated data to the sensor topic

        # Print the simulated data every 10 seconds
        print(f"Time of Day: {time_of_day}, Total Light Intensity: {total_intensity}")
        time.sleep(10)


def sunlight_change():
    while True:
        # Change sunlight mode every two minutes
        with lock:
            print("Changing sunlight mode...")
        time.sleep(120)


# Callback function for handling control messages
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


# Set the callback function for incoming message
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
    for _ in range(144):  # Simulate a full 24-hour day (144 intervals of 10 seconds each)
        # Simulate different light sources and conditions
        time_of_day = _ // 6  # 6 intervals per hour, so time_of_day ranges from 0 to 23

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

        # Print the simulated data every 10 seconds
        print(f"Time of Day: {time_of_day}, Total Light Intensity: {total_intensity}")
        time.sleep(10)


# Create and start threads for simulating light sensor and changing sunlight
light_sensor_thread = threading.Thread(target=simulate_light_sensor)
sunlight_change_thread = threading.Thread(target=sunlight_change)
scenario_thread = threading.Thread(target=scenario1)

user_input_thread = threading.Thread(target=user_input)

user_input_thread.start()
scenario_thread.start()

# Wait for the threads to finish
user_input_thread.join()
scenario_thread.join()

