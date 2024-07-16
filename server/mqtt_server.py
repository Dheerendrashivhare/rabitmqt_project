import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from datetime import datetime

# MQTT broker settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "status_topic"

# MongoDB connection
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mqtt_data"
MONGO_COLLECTION = "status_messages"

mqtt_client = mqtt.Client()

# Create MongoDB client
mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def on_connect(client, rc):
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
    status = message["status"]
    message["timestamp"] = datetime.now()
    collection.insert_one(message)
    # collection.insert_one({"status": status, "timestamp": timestamp})


if __name__ == "__main__":
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()