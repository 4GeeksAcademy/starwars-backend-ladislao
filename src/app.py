"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

# BASE DE DATOS: Usamos SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///starwars.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
setup_admin(app)

# Crear las tablas automáticamente
with app.app_context():
    db.create_all()

# Manejar errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint básico de prueba
@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response"
    }
    return jsonify(response_body), 200

# Endpoint: listar todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Endpoint: listar todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

# Endpoint: listar todos los personajes
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

# Endpoint: listar todos los favoritos
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

# Solo corre si ejecutas `python src/app.py`
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
