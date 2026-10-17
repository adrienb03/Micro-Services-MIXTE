# Imports
import json 
import os
import requests


# RESOLVER 1 : Liste des réservations d'un utilisateur
def get_bookings_by_userid (_,info,userid):
    with open ('{}/data/bookings.json'.format("."), "r") as file:
        bookings = json.load(file)
        for booking in bookings["bookings"]:
            if str(booking["userid"])==str(userid):
                return [booking]
    return []


# RESOLVER 2 : Ajouter un film à une date pour un utilisateur
def add_booking(_, info, userid, date, movieid):
    # Appel service REST
    schedule_url = os.environ.get("SCHEDULE_URL", "http://localhost:3002")
    response = requests.get(schedule_url + "/schedule/" + date)
    if response.status_code != 200 or movieid not in response.json()["movies"]:
        return None

    # Chargement du fichier
    with open('{}/data/bookings.json'.format("."), "r") as file:
        data = json.load(file)

    # Chercher l'utilisateur et la date
    for booking in data["bookings"]:
        if str(booking["userid"]) == str(userid):
            for d in booking["dates"]:
                if str(d["date"]) == str(date):
                    d["movies"].append(movieid)
                    with open('{}/data/bookings.json'.format("."), "w") as file:
                        json.dump(data, file)
                    return booking
    return None


# RESOLVER 3 : Supprimer un film d'une date pour un utilisateur
def delete_booking(_, info, userid, date, movieid):
    # Chargement du fichier
    with open('{}/data/bookings.json'.format("."), "r") as file:
        data = json.load(file)

    # Chercher l'utilisateur et la date
    for booking in data["bookings"]:
        if str(booking["userid"]) == str(userid):
            for d in booking["dates"]:
                if str(d["date"]) == str(date):
                    # Supprimer le film
                    d["movies"].remove(movieid)
                    with open('{}/data/bookings.json'.format("."), "w") as file:
                        json.dump(data, file)
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
