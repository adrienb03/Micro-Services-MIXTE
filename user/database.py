import os
import json
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB"]]

users_collection = db["users"]

def init_database():
    if users_collection.count_documents({}) == 0:
        with open("data/users.json", "r") as f:
            data = json.load(f)
        users_collection.insert_many(data["users"])