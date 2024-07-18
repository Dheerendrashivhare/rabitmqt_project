import paho.mqtt.client as mqtt
import pika
import json
import time
import random

# RabbitMQ connection setup
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbitmq_connection.channel()
channel.queue_declare(queue='mqtt_queue')

# MQTT client setup
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

mqtt_client.on_connect = on_connect
mqtt_client.connect("localhost", 1883, 60)

def publish_status():
    while True:
        status = random.randint(0, 6)
        # Always use ISO format for timestamps
        message = {"status": status, "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S')}
        channel.basic_publish(exchange='', routing_key='mqtt_queue', body=json.dumps(message))
        print(f"Published: {message}")
        time.sleep(1)

if __name__ == "__main__":
    mqtt_client.loop_start()
    try:
        publish_status()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.loop_stop()
        rabbitmq_connection.close()
