# IMPLÉMENTATION EN REST

from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3002
HOST = '0.0.0.0'

with open('{}/data/times.json'.format("."), 'r') as f:
   schedule = json.load(f)["schedule"]

def write(schedule):
    with open('{}/data/times.json'.format("."), 'w') as f:
        full = {}
        full['schedule'] = schedule
        json.dump(full, f)


# Route 1 : Acceuil 
# http://localhost:3002/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# Route 2 : Liste des séances
# http://localhost:3002/schedule
@app.route("/schedule", methods=['GET'])
def seances ():
   res = make_response(jsonify(schedule), 200)
   return res


# Route 3 : Films à une date spécifique
# http://localhost:3002/schedule/20151130
# http://localhost:3002/schedule/0
@app.route("/schedule/<date>", methods=['GET'])
def films_date (date):
   for s in schedule:
      if str(s["date"]) == str (date):
         return make_response(jsonify(s),200)
   return make_response (jsonify ({"error" : "aucun film à cette date"}), 404)


# Route 4 : Ajouter une séance
# http://localhost:3002/schedule/20260101
# {"date": "20151230", "movies": ["720d006c-3a57-4b6a-b18f-9b713b073f3c"]}
# git restore schedule/data/times.json
@app.route("/schedule/<date>", methods=['POST'])
def add_schedule(date):
    # Vérification existance date
    for s in schedule:
        if str(s["date"]) == str(date):
            return make_response(jsonify({"error": "schedule already exists"}), 409)      
    # Vérification corps requête
    req = request.get_json()
    if not req or "movies" not in req:
        return make_response(jsonify({"error": "corps invalide"}), 400)
    # Nouvelle séance
    new_schedule = {
        "date": date,
        "movies": req["movies"]
    }
    # Résultat
    schedule.append(new_schedule)
    write(schedule)
    return make_response(jsonify(new_schedule), 201)      


# Route 5 : Supprimer une séance
# http://localhost:3002/schedule/20151130
# git restore schedule/data/times.json
@app.route("/schedule/<date>", methods=['DELETE'])
def supprimer_seance(date):
    for s in schedule:
        if str(s["date"]) == str(date):
            schedule.remove(s)
            write(schedule)
            return make_response(jsonify(s), 200)
    return make_response(jsonify({"error": "séance non trouvée"}), 404)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
