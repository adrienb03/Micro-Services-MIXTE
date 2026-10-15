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




# Point d'entrée
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
