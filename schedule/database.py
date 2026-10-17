import os
import json
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB"]]

schedule_collection = db["schedule"]

def init_database():
    if schedule_collection.count_documents({}) == 0:
        with open("data/times.json", "r") as f:
            data = json.load(f)
        schedule_collection.insert_many(data["schedule"])