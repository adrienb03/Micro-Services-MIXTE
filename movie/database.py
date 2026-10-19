# CONFIGURATION BDD
# BDD MongoDB pour le service Movie

# Imports
import os
import json
from pymongo import MongoClient

# Connexion BDD
client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB"]]
movies_collection = db["movies"]
actors_collection = db["actors"]

# Initialisation BDD avec données Json
def init_database():
    if movies_collection.count_documents({}) == 0:
        with open("data/movies.json", "r") as f:
            data = json.load(f)
        movies_collection.insert_many(data["movies"])

    if actors_collection.count_documents({}) == 0:
        with open("data/actors.json", "r") as f:
            data = json.load(f)
        actors_collection.insert_many(data["actors"])