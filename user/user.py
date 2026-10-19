# SERVICE USER
# Chaque utilisateur a un ID, un nom et une date de dernière activité

# Imports 
from flask import Flask, request, jsonify, make_response
from database import users_collection, init_database

# Création de l'application Flask
app = Flask(__name__)

# Serveur
PORT = 3004
HOST = '0.0.0.0'


# Route 1 : Acceuil 
# http://localhost:3004/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>", 200)


# Route 2 : Liste des utilisateurs
# http://localhost:3004/users
@app.route("/users", methods=['GET'])
def get_users ():
   users = list(users_collection.find({}, {"_id": 0}))
   res = make_response(jsonify(users), 200)
   return res


# Route 3 : Utilisateur par son ID
# http://localhost:3004/users/chris_rivers
@app.route("/users/<id>", methods=['GET'])
def get_user_by_id (id):
   user = users_collection.find_one({"id": id}, {"_id": 0})
   if user:
      return make_response(jsonify(user), 200)
   return make_response(jsonify({"error" : "no user found for this id"}), 404)


# Route 4 : Ajouter un utilisateur
# POST http://localhost:3004/users
# {"id": "john_doe", "name": "John Doe", "last_active": 1360031010}
@app.route("/users", methods=['POST'])
def add_user():
    # Récupération et vérification requête
    req = request.get_json()
    if not req or "id" not in req or "name" not in req:
        return make_response(jsonify({"error": "invalid request body"}), 400)
    # Vérification de l'existence de l'utilisateur
    existing = users_collection.find_one({"id": req["id"]})
    if existing:
         return make_response(jsonify({"error": "user already exists"}), 409)
    # Ajout de l'utilisateur à la liste
    users_collection.insert_one(req.copy())
    return make_response(jsonify(req), 201)


# Route 5 : Supprimer un utilisateur
# DELETE http://localhost:3004/users/john_doe
@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
   deleted = users_collection.find_one_and_delete({"id": id}, projection={"_id": 0})
   if deleted:
      return make_response(jsonify({"message": "user deleted"}), 200)
   return make_response(jsonify({"error": "no user found for this id"}), 404)


# Point d'entrée
if __name__ == "__main__":
   # Initialisation de la base de données avec des données d'exemple si elle est vide
   init_database()

   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
