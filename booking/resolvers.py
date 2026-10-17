# Imports
import json 
import os
import requests
from pymongo import MongoClient

# Connexion à MongoDB
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["TP-MIXTE"]


# RESOLVER 1 : Liste des réservations d'un utilisateur
# query { get_bookings_by_userid(userid: "chris_rivers") { userid dates { date movies { title rating director } } } }
def get_bookings_by_userid (_,info,userid):
    booking = db.bookings.find_one({"userid": userid}, {"_id": 0})
    if booking:
        return [booking]
    return []


# RESOLVER 2 : Ajouter un film à une date pour un utilisateur
# mutation { add_booking(userid: "chris_rivers", date: "20151201", movieid: "267eedb8-0f5d-42d5-8f43-72426b9fb3e6") { userid dates { date movies { id title rating } } } }
def add_booking(_, info, userid, date, movieid):
    # Appel service REST
    schedule_url = os.environ.get("SCHEDULE_URL", "http://localhost:3002")
    response = requests.get(schedule_url + "/schedule/" + date)
    if response.status_code != 200 or movieid not in response.json()["movies"]:
        return None

    # Chercher l'utilisateur et la date
    booking = db.bookings.find_one({"userid": userid}, {"_id": 0})
    if booking:
        for d in booking["dates"]:
            if str(d["date"]) == str(date):
                d["movies"].append(movieid)
                # Mettre à jour dans Mongo
                db.bookings.update_one(
                    {"userid": userid},
                    {"$set": {"dates": booking["dates"]}}
                )
                return booking
    return None


# RESOLVER 3 : Supprimer un film d'une date pour un utilisateur
# mutation { delete_booking(userid: "chris_rivers", date: "20151201", movieid: "267eedb8-0f5d-42d5-8f43-72426b9fb3e6") { userid } }
def delete_booking(_, info, userid, date, movieid):
    # Chercher l'utilisateur et la date
    booking = db.bookings.find_one({"userid": userid}, {"_id": 0})
    if booking:
        # Chercher la date
        for d in booking["dates"]:
            if str(d["date"]) == str(date):
                # Supprimer le film
                d["movies"].remove(movieid)
                # Mettre à jour dans MongoDB
                db.bookings.update_one(
                    {"userid": userid},
                    {"$set": {"dates": booking["dates"]}}
                )
                return booking
    return None


# RESOLVER 4 : Resolver imbriqué (informations des movies de Booking)
# booking_date : { "date": "...", "movies": ["movieid1", "movieid2"] }
def resolve_movies(booking_date, info):
    # Url du service Movie
    movie_url = os.environ.get("MOVIE_URL", "http://localhost:3001")
    
    # Boucle sur chaque film de Booking
    result = []
    for movieid in booking_date["movies"]:
        # Communication avec Movie (HTTP POST GraphQL)
        query = f'query {{ movie_with_id(_id: "{movieid}") {{ id title director rating }} }}'
        response = requests.post(movie_url + "/graphql", json={"query": query})
        movie = response.json()["data"]["movie_with_id"]
        
        # Ajout film aux résulats si trouvé 
        if movie:
            result.append(movie)
    return result
