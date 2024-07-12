import paho.mqtt.client as mqtt
import random
import time

# MQTT broker settings
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_BROKER_TOPIC = "status_topic"

client = mqtt.Client()

def lets_connect(client, userdata, flags, res):
    if res == 0:
        print("Connecting to MQTT Broker!...........")
    else:
        print("Failed to connecting to MQTT, return code %d\n", res)

def get_disconnect(client, userdata, rc):
    print("Disconnecting from MQTT Broker!........")

client.on_connect = lets_connect
client.on_disconnect = get_disconnect

client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

while True:
    status_value = random.randint(0, 6)
    message = {"status": status_value}
    client.publish(MQTT_BROKER_TOPIC, str(message))
    print(f"This Message has been published: {message}")
    time.sleep(1)

client.loop_forever()
