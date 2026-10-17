# FICHIER DE BASE

# Imports 
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response
import resolvers as r

# Configuration
PORT = 3003
HOST = '0.0.0.0'
app = Flask(__name__)

# Objets de type
type_defs=load_schema_from_path("booking.graphql")
query = QueryType()
mutation = MutationType()
booking = ObjectType('Booking')
booking_date=ObjectType('BookingDate')

# Bindings
query.set_field('get_bookings_by_userid', r.get_bookings_by_userid)
mutation.set_field('add_booking', r.add_booking)
mutation.set_field('delete_booking', r.delete_booking)
booking_date.set_field('movies', r.resolve_movies)

# Schéma
schema = make_executable_schema(type_defs, query, mutation, booking, booking_date) 


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Booking service!</h1>",200)


# graphql entry points
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


# Démmarre serveur 
if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)