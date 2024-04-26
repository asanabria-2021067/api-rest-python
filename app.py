from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo, ObjectId
from dotenv import load_dotenv
from flask_cors import CORS
import os
import re
import bcrypt

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
    for animal in animals:
        animal['_id'] = str(animal['_id'])  # Convertir ObjectId a cadena
    return jsonify(animals)

# ANIMALS BY REGION OR NAME
@app.route('/get/animals/<id>', methods=['GET'])
def get_animal(id):
    regex = re.compile(f'{id}', re.IGNORECASE)
    animals_list = mongo.db.animals.find({'$or': [{'nombre': {'$regex': regex}}, {'region': {'$regex': regex}}], 'status': True})
    animals = []
    for animal in animals_list:
        animal['_id'] = str(animal['_id'])
        animals.append(animal)
    if animals:
        return jsonify(animals)
    else:
        return not_found()

@app.route('/get/all_animals', methods=['GET'])
def get_all_animals():
    animals_list = mongo.db.animals.find()
    animals = [animal for animal in animals_list]
    for animal in animals:
        animal['_id'] = str(animal['_id'])
    return jsonify(animals)
    
# UPDATE ANIMALS (STATUS)
@app.route('/update/animals/<id>', methods=['PUT'])
def update_animal(id):
    data = request.json
    response = mongo.db.animals.update_one({'_id': ObjectId(id)}, {'$set': data})
    if response.modified_count >= 1:
        return jsonify({'message': 'Animal updated'})
    else:
        return not_found()

# DELETE ANIMAL
@app.route('/delete/animals/<id>', methods=['DELETE'])
def delete_animal(id):
    deleted_animal = mongo.db.animals.find_one_and_delete({'_id': ObjectId(id)})
    if deleted_animal:
        return jsonify({'message': 'Animal deleted'})
    else:
        return not_found()



# POST USERS
@app.route('/post/users', methods=['POST'])
def create_user():
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    logged = data.get('logged', False)
    status = False

    if nombre and apellido and correo and contrasena:
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        
        row = mongo.db.users.insert_one({
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contrasena": hashed_password.decode('utf-8'),
            "logged": logged,
            "status": status
        })
        response = {
            'id': str(row.inserted_id),
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            "logged": logged,
            "status": status
        }
        return jsonify(response)
    else:
        return not_found()

    
# UPDATE USER
@app.route('/update/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    logged = data.get('logged')
    status = data.get('status')

    if nombre is not None or apellido is not None or correo is not None or contrasena is not None or logged is not None or status is not None:
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if apellido is not None:
            update_data['apellido'] = apellido
        if correo is not None:
            update_data['correo'] = correo
        if contrasena is not None:
            hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
            update_data['contrasena'] = hashed_password.decode('utf-8')
        if logged is not None:
            update_data['logged'] = logged
        if status is not None:
            update_data['status'] = status
        
        response = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': update_data})
        if response.modified_count >= 1:
            return jsonify({'message': 'Usuario actualizado'})
        else:
            return not_found("El usuario no fue encontrado")
    else:
        return jsonify({'message': 'Nada para actualizar'})



# DELETE USER
@app.route('/delete/users/<id>', methods=['DELETE'])
def delete_user(id):
    deleted_user = mongo.db.users.find_one_and_delete({'_id': ObjectId(id)})
    if deleted_user:
        return jsonify({'message': 'Usuario eliminado'})
    else:
        return not_found("El usuario no fue encontrado")



# Autenticar usuario
def authenticate_user(correo, contrasena):
    user = mongo.db.users.find_one({'correo': correo})
    if user:
        hashed_password = user.get('contrasena').encode('utf-8')
        if bcrypt.checkpw(contrasena.encode('utf-8'), hashed_password):
            return True
    return False

    

# GET USERS
@app.route('/get/users', methods=['GET'])
def get_users():
    users_list = mongo.db.users.find()
    users = [user for user in users_list]
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)


logged_in_user = None

# LOGIN ROUTE
@app.route('/login', methods=['POST'])
def login():
    global logged_in_user

    data = request.json
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    if correo and contrasena:
        user = mongo.db.users.find_one({'correo': correo})
        if user:
            if user.get('status'):
                hashed_password = user.get('contrasena').encode('utf-8')
                if bcrypt.checkpw(contrasena.encode('utf-8'), hashed_password):
                    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'logged': True}})
                    logged_in_user = correo
                    return jsonify({'message': 'Inicio de sesión exitoso'})
                else:
                    return jsonify({'message': 'Contraseña inválida'}), 401
            else:
                return jsonify({'message': 'El usuario no tiene permiso para iniciar sesión'}), 403
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    else:
        return jsonify({'message': 'Email o contraseña faltante'}), 400

# LOGOUT ROUTE
@app.route('/logout', methods=['POST'])
def logout():
    global logged_in_user

    if logged_in_user:
        user = mongo.db.users.find_one({'correo': logged_in_user})
        if user:
            mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'logged': False}})
        logged_in_user = None
        return jsonify({'message': 'Cierre de sesión exitoso'})
    else:
        return jsonify({'message': 'No hay un usuario loggeado'}), 400
    

# Cantidad de animales
@app.route('/count/animals', methods=['GET'])
def count_animals():
    count = mongo.db.animals.count_documents({})
    return jsonify({'Cantidad de animales': count})

# Cantidad de usuarios
@app.route('/count/users', methods=['GET'])
def count_users():
    count = mongo.db.users.count_documents({})
    return jsonify({'Cantidad de usuarios': count})


    

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

