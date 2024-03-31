from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

CORS(app)

# HOME ROUTE
@app.route('/', methods=['GET'])
def home():
    response = "BIENVENIDO AL BACKEND DE SEASOS"
    return Response(response, mimetype='text/plain')

# POST ANIMALS
@app.route('/post/animals', methods=['POST'])
def create_animal():
    data = request.json
    nombre = data.get('nombre')
    cientifico = data.get('cientifico')
    region = data.get('region')
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    img = data.get('img')
    status = False

    if nombre and cientifico and region and latitud and longitud:
        row = mongo.db.animals.insert_one({
            "nombre": nombre,
            "cientifico": cientifico,
            "region": region,
            "latitud": latitud,
            "longitud": longitud,
            "img": img,
            "status": status
        })
        response = {
            'id': str(row.inserted_id),
            'nombre': nombre,
            'cientifico': cientifico,
            'region': region,
            "latitud": latitud,
            "longitud": longitud,
            "img": img,
            "status": status
        }
        return jsonify(response)
    else:
        return not_found()

# GET ANIMALS
@app.route('/get/animals', methods=['GET'])
def get_animals():
    animals_list = mongo.db.animals.find({'status': True})
    animals = [animal for animal in animals_list]
    return jsonify(animals)

# ANIMALS BY REGION OR NAME
@app.route('/get/animals/<id>', methods=['GET'])
def get_animal(id):
    animals_list = mongo.db.animals.find({'$or': [{'nombre': id}, {'region': id}], 'status': True})
    animals = [animal for animal in animals_list]
    return jsonify(animals)

# UPDATE ANIMALS (STATUS)
@app.route('/update/animals/<id>', methods=['PUT'])
def update_animal(id):
    data = request.json
    response = mongo.db.animals.update_one({'_id': id}, {'$set': data})
    if response.modified_count >= 1:
        return jsonify({'message': 'Animal updated'})
    else:
        return not_found()

# DELETE ANIMAL
@app.route('/delete/animals/<id>', methods=['DELETE'])
def delete_animal(id):
    deleted_animal = mongo.db.animals.find_one_and_delete({'_id': id})
    if deleted_animal:
        return jsonify({'message': 'Animal deleted'})
    else:
        return not_found()

# ERROR HANDLER
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': "Resource not found: " + request.url,
        "status": 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)
