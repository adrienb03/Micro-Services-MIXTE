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








# Point d'entrée
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
