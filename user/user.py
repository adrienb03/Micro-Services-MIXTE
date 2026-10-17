# IMPLÉMENTATION EN REST

# Imports 
from flask import Flask, request, jsonify, make_response
import json
import os 
from pymongo import MongoClient

# Création de l'application Flask
app = Flask(__name__)

# Serveur
PORT = 3004
HOST = '0.0.0.0'

# Connexion à MongoDB
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["TP-MIXTE"]   


# Route 1 : Acceuil 
# http://localhost:3004/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>", 200)


# Route 2 : Liste des utilisateurs
# http://localhost:3004/users
@app.route("/users", methods=['GET'])
def get_users ():
   users = list(db.users.find({}, {"_id": 0}))
   res = make_response(jsonify(users), 200)
   return res


# Route 3 : Utilisateur par son ID
# http://localhost:3004/users/chris_rivers
@app.route("/users/<id>", methods=['GET'])
def get_user_by_id (id):
   user = db.users.find_one({"id": id}, {"_id": 0})
   if user:
      return make_response(jsonify(user), 200)
   return make_response(jsonify({"error" : "no user found for this id"}), 404)


# Route 4 : Ajouter un utilisateur
# POST http://localhost:3004/users
# {"id": "john_doe", "name": "John Doe", "last_active": 1360031010}
# git restore user/data/users.json
@app.route("/users", methods=['POST'])
def add_user():
    # Récupération et vérification requête
    req = request.get_json()
    if not req or "id" not in req or "name" not in req:
        return make_response(jsonify({"error": "invalid request body"}), 400)
    # Vérification de l'existence de l'utilisateur
    existing = db.users.find_one({"id": req["id"]}, {"_id": 0})
    if existing:
         return make_response(jsonify({"error": "user already exists"}), 409)
    # Ajout de l'utilisateur à la liste
    db.users.insert_one(req)
    return make_response(jsonify(req), 201)


# Route 5 : Supprimer un utilisateur
# DELETE http://localhost:3004/users/john_doe
# git restore user/data/users.json
@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
   deleted = db.users.find_one_and_delete({"id": id}, projection={"_id": 0})
   if deleted:
      return make_response(jsonify({"message": "user deleted"}), 200)
   return make_response(jsonify({"error": "no user found for this id"}), 404)


# Point d'entrée
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
