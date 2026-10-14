# IMPLÉMENTATION EN REST

from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3002
HOST = '0.0.0.0'

with open('{}/data/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
