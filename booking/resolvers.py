import requests
from database import bookings_collection

MOVIE_URL = "http://movie:3001"
SCHEDULE_URL = "http://schedule:3002"


# RESOLVER 1 : Liste de toutes les réservations
# query { get_bookings { userid dates { date movies { id title rating director } } } }
def get_bookings(_, info):
    return list(bookings_collection.find({}, {"_id": 0}))


# RESOLVER 2 : Réservation d'un utilisateur
# query { get_booking_by_id(userid: "chris_rivers") { userid dates { date movies { id title rating director } } } }
def get_booking_by_id(_, info, userid):
    return bookings_collection.find_one({"userid": userid}, {"_id": 0})


# RESOLVER 3 : Ajouter une réservation pour un utilisateur
# mutation { add_booking(userid: "john_doe", dates: [{date: "20151201", movies: ["267eedb8-0f5d-42d5-8f43-72426b9fb3e6"]}]) { userid dates { date movies { id title rating director } } } }
def add_booking(_, info, userid, dates):
    # Vérifier si l'utilisateur possède déjà des réservations
    existing = bookings_collection.find_one({"userid": userid})
    if existing:
        return None

    # Vérifier que chaque film est programmé à la date demandée
    for entry in dates:
        date = entry["date"]

        response = requests.get(
            f"{SCHEDULE_URL}/schedule/{date}",
            timeout=5
        )
        if response.status_code != 200:
            return None

        schedules = response.json()

        for movieid in entry["movies"]:
            if not any(movieid in s["movies"] for s in schedules):
                return None

    # Ajouter la réservation
    booking = {
        "userid": userid,
        "dates": dates
    }
    bookings_collection.insert_one(booking.copy())
    return booking


# RESOLVER 4 : Supprimer les réservations d'un utilisateur
# mutation { delete_booking(userid: "john_doe") { userid } }
def delete_booking(_, info, userid):
    return bookings_collection.find_one_and_delete(
        {"userid": userid},
        projection={"_id": 0}
    )

# RESOLVER 5 : Supprimer un film d'une réservation à une date donnée
# mutation { delete_movie_from_booking(userid: "chris_rivers", date: "20151201", movieid: "267eedb8-0f5d-42d5-8f43-72426b9fb3e6") { userid dates { date movies { id title } } } }
def delete_movie_from_booking(_, info, userid, date, movieid):
    # Chercher la réservation de l'utilisateur
    booking = bookings_collection.find_one({"userid": userid}, {"_id": 0})

    if booking:
        for d in booking["dates"]:
            if str(d["date"]) == str(date):
                if movieid not in d["movies"]:
                    return None
                # Supprimer le film
                d["movies"].remove(movieid)
                # Mettre à jour dans MongoDB
                bookings_collection.update_one(
                    {"userid": userid},
                    {"$set": {"dates": booking["dates"]}}
                )
                return booking
    return None


# RESOLVER IMBRIQUÉ : Informations des films
# Utilisé automatiquement lorsqu'une requête demande le champ movies de BookingDate
def resolve_movies(booking_date, info):
    result = []

    for movieid in booking_date["movies"]:
        query = """
        query ($id: String!) {
            movie_with_id(_id: $id) {
                id
                title
                director
                rating
            }
        }
        """

        response = requests.post(
            f"{MOVIE_URL}/graphql",
            json={
                "query": query,
                "variables": {"id": movieid}
            },
            timeout=5
        )
        response.raise_for_status()
        movie = response.json()["data"]["movie_with_id"]

        if movie:
            result.append(movie)

    return result