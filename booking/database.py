# CONFIGURATION BDD
# BDD MongoDB pour le service Booking

# Imports
import os
import json
from pymongo import MongoClient

# Connexion BDD
client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB"]]
bookings_collection = db["bookings"]

# Initialisation BDD avec données Json
def init_database():
    if bookings_collection.count_documents({}) == 0:
        with open("data/bookings.json", "r") as f:
            data = json.load(f)
        bookings_collection.insert_many(data["bookings"])
