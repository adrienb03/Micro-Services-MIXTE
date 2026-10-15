# IMPLÉMENTATION EN REST

# Imports 
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# Création de l'application Flask
app = Flask(__name__)

# Serveur
PORT = 3004
HOST = '0.0.0.0'

# Chargement fichier json user
with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

# Écriture fichier json user
def write(users):
    with open('{}/data/users.json'.format("."), 'w') as f:
        full = {}
        full['users'] = users
        json.dump(full, f)       


# Route 1 : Acceuil 
# http://localhost:3004/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>", 200)


# Route 2 : Liste des utilisateurs
# http://localhost:3004/users
@app.route("/users", methods=['GET'])
def get_users ():
   res = make_response(jsonify(users), 200)
   return res


# Route 3 : Utilisateur par son ID
# http://localhost:3004/users/chris_rivers
# http://localhost:3004/users/0
@app.route("/users/<id>", methods=['GET'])
def get_user_by_id (id):
   for user in users:
      if str(user["id"]) == str(id):
         return make_response(jsonify(user), 200)
   return make_response(jsonify({"error" : "no user found for this id"}), 404)


# Route 4 : Ajouter un utilisateur
# http://localhost:3004/users
# {"id": "john_doe", "name": "John Doe", "last_active": 1360031010}
# git restore user/data/users.json
@app.route("/users", methods=['POST'])
def add_user():
    # Récupération et vérification requête
    req = request.get_json()
    if not req or "id" not in req:
        return make_response(jsonify({"error": "invalid request body"}), 400)
    # Vérification de l'existence de l'utilisateur
    for user in users:
        if str(user["id"]) == str(req["id"]):
            return make_response(jsonify({"error": "user already exists"}), 409)
    # Ajout de l'utilisateur à la liste
    users.append(req)
    write(users)
    return make_response(jsonify(req), 201)


# Route 5 : Supprimer un utilisateur
# http://localhost:3004/users/john_doe
# git restore user/data/users.json
@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
   for user in users:
      if str(user["id"]) == str(id):
         users.remove(user)
         write(users)
         return make_response(jsonify({"message": "user deleted"}), 200)
   return make_response(jsonify({"error": "no user found for this id"}), 404)


# Point d'entrée
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
