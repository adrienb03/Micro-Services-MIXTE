# CONFIGURATION BDD
# BDD MongoDB pour le service Schedule

# Imports
import os
import json
from pymongo import MongoClient

# Connexion BDD
client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB"]]
schedule_collection = db["schedule"]

# Initialisation BDD avec données Json
def init_database():
    if schedule_collection.count_documents({}) == 0:
        with open("data/times.json", "r") as f:
            data = json.load(f)
        schedule_collection.insert_many(data["schedule"])