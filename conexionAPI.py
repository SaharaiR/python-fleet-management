'''
import requests
from flask import jsonify, request
#from flask_cors import CORS, cross_origin

#app = Flask(__name__)
#CORS(app)

#Endpoint para obtener la información de swagger
#@app.route('/taxis', methods=['GET'])
#@cross_origin()
def dataApi(page=1, per_page=10):
    urlSwaggerHub = 'https://virtserver.swaggerhub.com/SAHARAROD/fleetAPI/1.0.0/taxis'

    params = {'page': page, 'per_page': per_page}
    #Solicitud GET a la API
    response = requests.get(urlSwaggerHub, params=params)
    #Verificar si la solicitud fue exitosa (codigo: 200)
    if response.status_code == 200:
        #Devuelve los datos de la API
        print('Conexion a la API exitosa')
        return jsonify(response.json())
    else:
        #Mandar mensaje de error
        print('Aparentemente hay error')
        return jsonify({'error':'No se pudo obtener los datos de la API en SwaggerHub'}), 500
        #return None
'''