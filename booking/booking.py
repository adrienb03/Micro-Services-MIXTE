# FICHIER DE BASE

# Imports
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response
from database import init_database
import resolvers as r

# Configuration
PORT = 3003
HOST = '0.0.0.0'
app = Flask(__name__)

# Objets de type
type_defs = load_schema_from_path("booking.graphql")
query = QueryType()
mutation = MutationType()
booking_date = ObjectType('BookingDate')

# Bindings
query.set_field('get_bookings', r.get_bookings)
query.set_field('get_booking_by_id', r.get_booking_by_id)

mutation.set_field('add_booking', r.add_booking)
mutation.set_field('delete_booking', r.delete_booking)
mutation.set_field('delete_movie_from_booking', r.delete_movie_from_booking)

booking_date.set_field('movies', r.resolve_movies)

# Schéma
schema = make_executable_schema(type_defs, query, mutation, booking_date)


# ROUTE 0 - Accueil
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Booking service!</h1>", 200)


# ROUTE 1 - Envoi de requêtes GraphQL au serveur
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


# Démarrage serveur
if __name__ == "__main__":
    # Initialisation de la base de données
    init_database()
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)