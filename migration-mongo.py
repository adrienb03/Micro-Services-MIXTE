# IMPORTS
import json
import os
from pymongo import MongoClient

# Connection Mongo
client = MongoClient("mongodb://root:example@localhost:27017/")
db = client.get_default_database()

# Fichiers Json à importer
fichiers = [
    ("movie/data/movies.json", "movies"),
    ("movie/data/actors.json", "actors"),
    ("schedule/data/times.json", "schedule"),
    ("user/data/users.json", "users"),
    ("booking/data/bookings.json", "bookings"),
]

# Travail
for chemin, collection_name in fichiers:
    with open(chemin, "r") as f:
        data = json.load(f)
        liste = data[collection_name]
        db[collection_name].insert_many(liste)