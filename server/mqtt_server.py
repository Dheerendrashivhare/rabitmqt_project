import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient

# MQTT broker settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "status_topic"

# MongoDB connection
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mqtt_data"
MONGO_COLLECTION = "status_messages"

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Failed to connect, return code %d\n", rc)

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker!")

def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode())
    print(f"Received message: {message}")
    collection.insert_one(message)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()
