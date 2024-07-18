import pika
import json
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import threading
from dateutil.parser import isoparse

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client.mqtt_database
collection = db.mqtt_messages

# RabbitMQ connection setup
rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = rabbitmq_connection.channel()
channel.queue_declare(queue='mqtt_queue')

app = FastAPI()

def callback(ch, method, properties, body):
    message = json.loads(body)
    # Convert timestamp to datetime object
    try:
        message['timestamp'] = datetime.strptime(message['timestamp'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
    except ValueError:
        print(f"Skipping invalid timestamp format: {message['timestamp']}")
        return
    collection.insert_one(message)
    print(f"Stored in MongoDB: {message}")

channel.basic_consume(queue='mqtt_queue', on_message_callback=callback, auto_ack=True)

@app.on_event("startup")
def startup_event():
    def rabbitmq_consume():
        print("Starting RabbitMQ consumer...")
        channel.start_consuming()

    threading.Thread(target=rabbitmq_consume).start()

@app.get("/status_counts/")
async def get_status_counts(start_time: str, end_time: str):
    try:
        start_datetime = isoparse(start_time)
        end_datetime = isoparse(end_time)

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_datetime, "$lte": end_datetime}}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]

        result = list(collection.aggregate(pipeline))
        return {item["_id"]: item["count"] for item in result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
