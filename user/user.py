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









# Point d'entrée
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
