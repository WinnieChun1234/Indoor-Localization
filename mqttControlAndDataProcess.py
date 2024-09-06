import tkinter as tk
from tkinter import simpledialog
import paho.mqtt.client as mqtt
import os

# MQTT Settings
MQTT_BROKER = "172.20.10.3"
MQTT_PORT = 1883
MQTT_TOPIC_COMMANDS = "COMMANDS"
MQTT_TOPIC_SENSOR = "SENSOR_DATA"

# Function to connect to MQTT Broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_SENSOR)  # Subscribe to sensor data topic

# Function to handle incoming MQTT messages
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received '{message}' from '{msg.topic}'")
    if msg.topic == MQTT_TOPIC_SENSOR:
        sensor_label.config(text=f"Sensor Data: {message}")  # Update the GUI with sensor data
        with open('output.txt', 'a') as file:
            try:
                # if "SSID: HKU " in message:
                file.write(message)
                file.write("\n")
                print("Data written to 'output.txt'")
            except Exception as e:
                print("Error: The file 'output.txt' does not exist.")

# Function to handle publishing messages
def send_command(command):
    mqttClient.publish(MQTT_TOPIC_COMMANDS, command)
    print(f"Sent '{command}' to topic '{MQTT_TOPIC_COMMANDS}'")

# Setup MQTT Client
mqttClient = mqtt.Client("GUI_Client")
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect(MQTT_BROKER, MQTT_PORT)
mqttClient.loop_start()


# Create the main window
root = tk.Tk()
root.title("ESP32 Control Panel")

# Add a label to display sensor data
sensor_label = tk.Label(root, text="Sensor Data: Waiting for data...", width=80, height=4, anchor='w')
sensor_label.pack(pady=20)

# Function to handle "Start" button press
def start_command():
    send_command("start")

# Function to handle "Stop" button press
def stop_command():
    send_command("stop")

# Adding buttons to the GUI
start_button = tk.Button(root, text="Start", command=start_command, height=2, width=10)
start_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop", command=stop_command, height=2, width=10)
stop_button.pack(pady=20)

# Start the GUI
root.mainloop()

# Clean up
mqttClient.loop_stop()
mqttClient.disconnect()