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
#from models import User, Character, Planet, Vehicle, Favorite

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

#ENDPOINTS DE USER (POST, GET, GET ONE, DELETE, POST CHARACTER/PLANET/VEHICLE FAVORITE
# DELETE CHARACTER/PLANET/VEHICLE FAVORITE)

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
    db.session.add(user)
    db.session.commit()
    return jsonify({"name" : user.name, "msg" : "creado el usuario con id: " + str(user.id)}), 200

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    users_serialized = list(map(lambda x: x.serialize(), users))
    return jsonify ({"response": users_serialized}), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.filter_by(id=user_id).first() 
    return jsonify ({"response": user.serialize()}), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_one_user_favorites(user_id):
    favo = Favorite.query.filter(Favorite.user_id == user_id).all()
    favo_serialized = list(map(lambda x: x.serialize(), favo))    
    return jsonify ({"result": favo_serialized}), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    user = User.query.filter_by(id = user_id).first() 
    db.session.delete(user)
    db.session.commit()
    return jsonify ({"deleted":True}), 200

@app.route('/user/<int:user_id>/favorite/character/<int:ch_id>', methods=['POST'])
def favorite_character(ch_id, user_id):
    user = User.query.get(user_id)
    new_favorite = Favorite(user_id = user_id, character_id = ch_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({"created": True, "character": new_favorite.serialize()}), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:pl_id>', methods=['POST'])
def favorite_planet(pl_id, user_id):
    user = User.query.get(user_id)
    new_favorite = Favorite(user_id = user_id, planet_id = pl_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({"created": True, "planet": new_favorite.serialize()}), 200

@app.route('/user/<int:user_id>/favorite/vehicle/<int:vh_id>', methods=['POST'])
def favorite_vehicle(vh_id, user_id):
    user = User.query.get(user_id)
    new_favorite = Favorite(user_id = user_id, vehicle_id = vh_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({"created": True, "vehicle": new_favorite.serialize()}), 200

@app.route('/user/<int:user_id>/favorite/character/<int:ch_id>', methods=['DELETE'])
def delete_favorite_character_by_id(ch_id, user_id):
    fav = Favorite.query.filter_by(user_id = user_id).filter_by(character_id = ch_id).first()
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"deleted": True}), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:pl_id>', methods=['DELETE'])
def delete_favorite_planet_by_id(pl_id, user_id):
    fav = Favorite.query.filter_by(user_id = user_id).filter_by(planet_id = pl_id).first()
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"deleted": True}), 200

@app.route('/user/<int:user_id>/favorite/vehicle/<int:vh_id>', methods=['DELETE'])
def delete_favorite_vehicle_by_id(vh_id, user_id):
    fav = Favorite.query.filter_by(user_id = user_id).filter_by(vehicle_id = vh_id).first()
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"deleted": True}), 200

#ENDPOINTS DE CHARACTER (POST, GET, GET ONE, DELETE)

@app.route('/character', methods=['POST'])
def create_character():
    body_name = request.json.get("name")
    body_age = request.json.get("age")
    body_gender = request.json.get("gender")
    body_skin_color = request.json.get("skin_color")
    character = Character(name = body_name, age = body_age, gender = body_gender, skin_color = body_skin_color)
    db.session.add(character)
    db.session.commit()
    return jsonify({"name" : character.name, "msg" : "creado el character con id: " + str(character.id)}), 200

@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify ({"response": characters_serialized}), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character = Character.query.filter_by(id=character_id).first() 
    return jsonify ({"response": character.serialize()}), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_one_character(character_id):
    character = Character.query.filter_by(id = character_id).first() 
    db.session.delete(character)
    db.session.commit()
    return jsonify ({"deleted":True}), 200

#ENDPOINTS DE PLANET (POST, GET, GET ONE, DELETE)

@app.route('/planet', methods=['POST'])
def create_planet():
    body_name = request.json.get("name")
    body_gravity = request.json.get("gravity")
    body_population = request.json.get("population")
    body_climate = request.json.get("climate")
    body_terrain = request.json.get("terrain")
    planet = Planet(name = body_name, gravity = body_gravity, population = body_population, climate = body_climate, terrain = body_terrain)
    db.session.add(planet)
    db.session.commit()
    return jsonify({"name" : planet.name, "msg" : "creado el planet con id: " + str(planet.id)}), 200

@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify ({"response": planets_serialized}), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first() 
    return jsonify ({"response": planet.serialize()}), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_one_planet(planet_id):
    planet = Planet.query.filter_by(id = planet_id).first() 
    db.session.delete(planet)
    db.session.commit()
    return jsonify ({"deleted":True}), 200

#ENDPOINTS DE VEHICLE (POST, GET, GET ONE, DELETE)

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    body_name = request.json.get("name")
    body_gravity = request.json.get("gravity")
    body_population = request.json.get("population")
    body_climate = request.json.get("climate")
    body_terrain = request.json.get("terrain")
    vehicle = Vehicle(name = body_name, gravity = body_gravity, population = body_population, climate = body_climate, terrain = body_terrain)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({"name" : vehicle.name, "msg" : "creado el vehicle con id: " + str(vehicle.id)}), 200

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    vehicles_serialized = list(map(lambda x: x.serialize(), vehicles))
    return jsonify ({"response": vehicles_serialized}), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first() 
    return jsonify ({"response": vehicle.serialize()}), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_one_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(id = vehicle_id).first() 
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify ({"deleted":True}), 200

#ENDPOINT DE GET FAVORITE

@app.route('/favorite', methods=['GET'])
def get_all_favorites():
    favorites = Favorite.query.all() #esto me devuelve una lista de instancia de clases, que hay que hacerles serialize
    favorites_serialized = list(map(lambda x: x.serialize(), favorites))
    return jsonify ({"response": favorites_serialized}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
