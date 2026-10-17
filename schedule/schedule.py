# IMPLÉMENTATION EN REST

# Imports
from flask import Flask, request, jsonify, make_response
import json
import requests
import os
from pymongo import MongoClient

# Création de l'application Flask
app = Flask(__name__)

# Serveur
PORT = 3002
HOST = '0.0.0.0'

# Connexion à MongoDB
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["TP-MIXTE"]

# Récupération des films
def fetch_movies():
    movies_response = requests.post("http://movie:3001/graphql",
                                    json={"query": "{ get_movies { id title director rating } }"},
                                    timeout=5)
    movies = movies_response.json()
    return movies['data']['get_movies']

# Route 1 : Acceuil 
# http://localhost:3002/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the Schedule service!</h1>", 200)


# Route 2 : Liste des séances
# http://localhost:3002/schedule
@app.route("/schedule", methods=['GET'])
def get_schedule ():
   schedule = list(db.schedule.find({}, {"_id": 0}))
   res = make_response(jsonify(schedule), 200)
   return res


# Route 3 : Films à une date spécifique
# http://localhost:3002/schedule/20151130
@app.route("/schedule/<date>", methods=['GET'])
def get_schedule_by_date (date):
   s = list(db.schedule.find({"date": date}, {"_id": 0}))
   if s:
      return make_response(jsonify(s), 200)
   return make_response(jsonify({"error": "no schedule found for this date"}), 404)


# Route 4 : Ajouter une séance
# POST http://localhost:3002/schedule/20260101
# {"date": "20260101", "movies": ["720d006c-3a57-4b6a-b18f-9b713b073f3c"]}
# git restore schedule/data/times.json
@app.route("/schedule/<date>", methods=['POST'])
def add_schedule(date):
    # Vérification existance date
    existing_schedule = db.schedule.find_one({"date": date})
    if existing_schedule:
        return make_response(jsonify({"error": "schedule already exists for this date"}), 409)      
    # Vérification corps requête
    req = request.get_json()
    if not req or "movies" not in req:
        return make_response(jsonify({"error": "invalid request body"}), 400)
    # Vérification existence films
    movies = fetch_movies()
    for movie_id in req["movies"]:
        if not any(movie["id"] == movie_id for movie in movies):
            return make_response(
                jsonify({"error": f"Movie {movie_id} not found"}),
                400
            )
    # Nouvelle séance
    new_schedule = {
        "date": date,
        "movies": req["movies"]
    }
    db.schedule.insert_one(new_schedule)
    return make_response(jsonify(new_schedule), 201)      


# Route 5 : Supprimer une séance
# DELETE http://localhost:3002/schedule/20151130
# git restore schedule/data/times.json
@app.route("/schedule/<date>", methods=['DELETE'])
def delete_schedule(date):
    deleted = db.schedule.find_one_and_delete({"date": date}, projection={"_id": 0})
    if deleted:
        return make_response(jsonify(deleted), 200)
    return make_response(jsonify({"error": "no schedule found for this date"}), 404)


# Additional endpoint number 3/3
# Get schedules for a date with the movies details insted of their ids
# http://localhost:3002/schedule/20151130/details
@app.route("/schedule/<date>/details", methods=["GET"])
def get_schedule_details(date):
    s = db.schedule.find_one({"date": date}, {"_id": 0})
    if s:
        result = {
            "date": s["date"],
            "movies": []
        }
        movies = fetch_movies()
        for movie_id in s["movies"]:
            for movie in movies:
                if movie["id"] == movie_id:
                    result["movies"].append(movie)
                    break
        return make_response(jsonify(result), 200)
    return make_response(jsonify({"error": "Schedule not found"}), 404)


# Point d'entrée
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
