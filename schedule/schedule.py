# IMPLÉMENTATION EN REST

# Imports
from flask import Flask, request, jsonify, make_response
import json

# Création de l'application Flask
app = Flask(__name__)

# Serveur
PORT = 3002
HOST = '0.0.0.0'

# Chargement fichier json schedule
with open('{}/data/times.json'.format("."), 'r') as f:
   schedule = json.load(f)["schedule"]

# Écriture fichier json schedule
def write(schedule):
    with open('{}/data/times.json'.format("."), 'w') as f:
        full = {}
        full['schedule'] = schedule
        json.dump(full, f)


# Route 1 : Acceuil 
# http://localhost:3002/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the Schedule service!</h1>", 200)


# Route 2 : Liste des séances
# http://localhost:3002/schedule
@app.route("/schedule", methods=['GET'])
def get_schedule ():
   res = make_response(jsonify(schedule), 200)
   return res


# Route 3 : Films à une date spécifique
# http://localhost:3002/schedule/20151130
# http://localhost:3002/schedule/0
@app.route("/schedule/<date>", methods=['GET'])
def get_schedule_by_date (date):
   for s in schedule:
      if str(s["date"]) == str (date):
         return make_response(jsonify(s),200)
   return make_response (jsonify ({"error" : "no schedule found for this date"}), 404)


# Route 4 : Ajouter une séance
# http://localhost:3002/schedule/20260101
# {"date": "20260101", "movies": ["720d006c-3a57-4b6a-b18f-9b713b073f3c"]}
# git restore schedule/data/times.json
@app.route("/schedule/<date>", methods=['POST'])
def add_schedule(date):
    # Vérification existance date
    for s in schedule:
        if str(s["date"]) == str(date):
            return make_response(jsonify({"error": "schedule already exists for this date"}), 409)      
    # Vérification corps requête
    req = request.get_json()
    if not req or "movies" not in req:
        return make_response(jsonify({"error": "invalid request body"}), 400)
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
def delete_schedule(date):
    for s in schedule:
        if str(s["date"]) == str(date):
            schedule.remove(s)
            write(schedule)
            return make_response(jsonify(s), 200)
    return make_response(jsonify({"error": "no schedule found for this date"}), 404)


# Point d'entrée
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
