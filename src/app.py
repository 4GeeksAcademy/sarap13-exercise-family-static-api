"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
# Importamos arriba la class
# creamos espacio de memoria y activamos la clase en el servidor
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# A partir de aqui crear endpoints

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    # print(member_id)
    # Creamos una variable member que sea el objeto jackson_family y accedemos a la función de la clase get_member pasandole
    # como parametro el id 
    member = jackson_family.get_member(member_id)
    # print(member)
    response_body = {
        "member": member
    }
    # En la respuesta en el body creamos una propiedad que se llame member y queremos que sea el 
    # Primero retornar respuesta con status code
    if member == {} :
        return jsonify("The user doesn't exist"), 404
    else : 
        return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
# Hemos importado el request para poder usar el request body ya en formato json.
def add_one_member():
    # try lo usamos para que el bloque de codigo que está dentro puedan ocurrir excepciones, como en este caso que falte un
    # keyError y podamos enviar el error 400 y no el que envia por defecto que es el 500.
    # Metemos dentro de try todo el codigo y fuera ponemos exception (ver mas abajo):
    try : 
        # El request_body o cuerpo de la solicitud ya está decodificado en formato JSON y se encuentra en la variable request.json
        request_body = request.json

        # Para que si no todos los campos estan rellenos aparezca un error 400 diciendo que faltan campos
        required_fields = ["first_name", "age", "lucky_numbers"]
        if not all(field in request_body for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Creamos la plantilla que utilizará el request body para que la respuesta sea esa 
        # Creamos la variable new_member con las caracteristicas y lo que el request body tiene que traer:
        # En el caso del ID recurrimos a la función generateId para generar el random id
        new_member = {
            "first_name" : request_body["first_name"],
            "age" : request_body["age"],
            "lucky_numbers" : request_body["lucky_numbers"],
            "id" : jackson_family._generateId(),
        }
    
    
        # Aqui recurrimos a la función add_member del datastrcuture y le añadimos el new_member con el append de la funcion del data
        jackson_family.add_member(new_member)
        # Buena practica siempre en el response_body poner que estamos devolviendo 

        response_body = {
            "new_member" : new_member
        }

        return jsonify(response_body), 200
    # Codigo referido a que si ocurre el error KeyError nos aparezca un mensaje 400 con lo que queremos, que en este caso es 
    # Missing required field
    except KeyError as e:
        # Capturar el KeyError y responder con un error 400
        # La expresión e.args[0] accede al primer argumento de la excepción KeyError, que es la clave que no pudo ser encontrada.
        # Una f-string es una forma de formatear cadenas que permite la interpolación de expresiones dentro de llaves {} directamente en la cadena. Por eso esta la f antes de missing para poder evaluar e.args[0]
        return jsonify({"error": f"Missing required field: {e.args[0]}"}), 400

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    # creamos espacio para coger la función delete_member del datastructure con el parametro de la id 
    member_to_delete = jackson_family.delete_member(member_id)
    # En el response el anunciado nos indica que tiene que ir esto
    response_body = {
    "done": True
    }
    
    if member_to_delete == {} :
        return jsonify("The user doesn't exist"), 404
    else : 
        return jsonify(response_body), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
