import json
import os 
from pymongo import MongoClient

# Connexion à MongoDB
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["TP-MIXTE"]

def get_movies(_, info):
    movies = list(db.movies.find({}, {"_id": 0}))
    return movies

def movie_with_id(_,info,_id):
    movie = db.movies.find_one({"id": _id}, {"_id": 0})
    return movie

def add_movie(_,info,movie):
    db.movies.insert_one(movie)
    return movie

def update_movie_rate(_,info,_id,_rate):
    updated_movie = db.movies.find_one_and_update(
        {"id": _id},
        {"$set": {"rating": _rate}},
        return_document=True,
        projection={"_id": 0}
    )
    return updated_movie

def delete_movie(_,info,_id):
    deleted_movie = db.movies.find_one_and_delete({"id": _id}, projection={"_id": 0})
    return deleted_movie

def resolve_actors_in_movie(movie, info):
    actors = list(db.actors.find({"films": movie["id"]}, {"_id": 0}))
    return actors
