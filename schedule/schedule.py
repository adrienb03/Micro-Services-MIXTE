# IMPLÉMENTATION EN REST

from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3002
HOST = '0.0.0.0'

with open('{}/data/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]


# Route 1 : Acceuil 
# http://localhost:3002/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# Route 2 : Liste des séances
# http://localhost:3002/schedule
@app.route ("/schedule", methods=['GET'])
def seances ():
   res = make_response(jsonify(schedule), 200)
   return res
   

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
