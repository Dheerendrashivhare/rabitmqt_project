from fastapi import FastAPI, Query
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGO_DB = "mydb"
MONGODB_COLLECTION = "status_messages"

app = FastAPI()
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGO_DB]
collection = db[MONGODB_COLLECTION]

@app.get('/test/get_status_count')
async def fetch_status(startTime: datetime = Query(...), endTime: datetime = Query(...)):
    query = {
        "timestamp": {"$gte": startTime, "$lte": endTime}
    }

    response = collection.aggregate([
        {"$match": query},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ])

    get_status = {str(stat_val['_id']): stat_val['count'] for stat_val in response}

    return get_status