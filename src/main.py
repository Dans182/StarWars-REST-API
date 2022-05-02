"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import  db, User, Character, Planet, Vehicle, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['POST'])
def create_user():
    #aca vendría lo que se indica desde React
    #body_name = request.json.get (Lo utilizaremos cuando necesitamos agarrar el valor de una key dentro de un JSON, una string JSON)
    #si envíamos o traemos datos, tienen que ser en formato json
    #el stringify se usa para enviar cuando tenemos un objeto js y necesitamos enviarlo a una API. el stringify permite transformarlo en un JSON.
    #Cuanto te lo traes y quieres transformarlo en un objeto, utilizamos un .json. Enviamos con stringify y traemos con .json
    #En python, cuando va a recibir, necesita parsearlo a diccionario (request.json), aca transforma la peticion en un json. 
    # y para enviar, en python, usa el jsonify, que transforma un diccionario, lista, string en un json. Es el equivalente del stringify de react
    body_name = request.json.get("name")
    body_username = request.json.get("username")
    body_email = request.json.get("email")
    body_password = request.json.get("password")
    user = User(name = body_name, username = body_username, email = body_email, password = body_password)
    db.session.add(User)
    db.session.commit()
    return jsonify({"name" : user.name, "msg" : "creado el usuario con id: " + str(user.id)}), 200


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    users_serialized = list(map(lambda x: x.serialize(), users))
    return jsonify ({"response": user.name}), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.filter_by(id=user_id).first() 
    return jsonify ({"response": user.serialize()}), 200

@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify ({"response": characters_serialized}), 200

@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify ({"response": planets_serialized}), 200

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    vehicles_serialized = list(map(lambda x: x.serialize(), vehicles))
    return jsonify ({"response": vehicles_serialized}), 200

@app.route('/favorite', methods=['GET'])
def get_all_favorites():
    favorites = Favorite.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    favorites_serialized = list(map(lambda x: x.serialize(), favorites))
    return jsonify ({"response": favorites_serialized}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
