from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# POST ANIMALS
@app.route('/animals' , methods = ['POST'])
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
@app.route('/animals', methods = ['GET'])
def get_animals():
    animals_list = mongo.db.animals.find({'status': True})
    response = json_util.dumps(animals_list)
    return Response(response, mimetype='application/json')

# ANIMALS BY REGION OR NAME
@app.route('/animals/<id>', methods = ['GET'])
def get_animal(id):
    animals_list = mongo.db.animals.find_one(({'nombre': id} or {'region': id}) and {'status':True})
    response = json_util.dumps(animals_list)
    return Response(response, mimetype='application/json')

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