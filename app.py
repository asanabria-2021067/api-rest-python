from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

CORS(app)

# HOME ROUTE
@app.route('/' , methods = ['GET'])
def home():
    return "BIENVENIDO AL BACKEND DE SEASOS"

# POST ANIMALS
@app.route('/post/animals' , methods = ['POST'])
def create_animal():
    nombre = request.json['nombre']
    cientifico = request.json['cientifico']
    region = request.json['region']
    latitud = request.json['latitud']
    longitud = request.json['longitud']
    img = request.json['img']
    status = False

    if nombre and cientifico and region and latitud and longitud:
        row = mongo.db.animals.insert_one({
            "nombre" : nombre,
            "cientifico" :cientifico,
            "region" : region,
            "latitud": latitud,
            "longitud": longitud,
            "img": img,
            "status": status
        })
        response = {
            'id': str(row),
            'nombre': nombre,
            'cientifico':cientifico,
            'region' : region,
            "latitud": latitud,
            "longitud": longitud,
            "img": img,
            "status": status
        }
        return response
    else:
        return not_found()

    return{'message': 'received'}

# GET ANIMALS
@app.route('/get/animals', methods = ['GET'])
def get_animals():
    animals_list = mongo.db.animals.find({'status': True})
    response = json_util.dumps(animals_list)
    return Response(response, mimetype='application/json')

# ANIMALS BY REGION OR NAME
@app.route('/get/animals/<id>', methods = ['GET'])
def get_animal(id):
    animals_list = mongo.db.animals.find_one(({'nombre': id} or {'region': id}) and {'status':True})
    response = json_util.dumps(animals_list)
    return Response(response, mimetype='application/json')

# UPDATE ANIMALS (STATUS)
@app.route('/update/animals/<id>', methods = ['PUT'])
def update_animal(id):
    data = request.get_json()
    response = mongo.db.animals.update_one({'_id': ObjectId(id)}, {'$set': data})
    if response.modified_count >=1:
        return{'message': 'Animal update'}
    else:
        not_found()

# DELETE ANIMAL
@app.route('/delete/animals/<id>', methods=['DELETE'])
def delete_animal(id):
    deleted_animal = mongo.db.animals.find_one_and_delete({'_id': ObjectId(id)})
    
    if deleted_animal:
        return {'message': 'Animal deleted'}
    else:
        return not_found()
    
# ERROR HANDLER
@app.errorhandler(404)
def not_found(error = None):
    response = jsonify({
        'message': "Resource not found: " + request.url,
        "status": 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)