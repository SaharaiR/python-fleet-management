from flask import Flask, jsonify, request, make_response
from database import connectDataBase
from datetime import datetime
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
import psycopg2

app = Flask(__name__)
conn = connectDataBase()
# Create an APISpec
spec = APISpec(
    title="Swagger Fleet Management API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

#Endpoint de HOME
@app.route('/', methods=['GET'])
def home():
    """
    Página de inicio de la API de Fleet Management
    """
    return "<h1>Fleet Management API</h1>"

#HISTORIA DE USUARIO 2 - LISTADO DE TODOS LOS TAXIS CON SU ID Y PLACA

#Esquema para la respuesta de la API
class TaxiSchema(Schema):
     id = fields.Int(description="ID del taxi", required=True)
     plate = fields.Str(description="Placa del taxi", required=True)

#Endpoint de la información general paginada (endpoint para paginacion: http://127.0.0.1:5000/taxis?page=1)
@app.route('/taxis', methods=['GET'])
def getTaxis():
    """
    Lista todos los taxis con su ID y placa
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: Número de página para la paginación
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        description: Taxis por página
        default: 10
    responses:
      200:
        description: Lista de taxis obtenida exitosamente
        content:
            application/json:
              schema: 
                type: array
                items: 
                  $ref: '#/components/schemas/TaxiSchema'
      500:
        description: Error al obtener los datos de la base de datos
    """
    # Obtener parámetros de paginación de la solicitud
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page
    
    try:
        cursor = conn.cursor()
        # Consulta SQL con paginación
        cursor.execute("SELECT * FROM taxis LIMIT %s OFFSET %s", (per_page, offset))
        data = cursor.fetchall()
        cursor.close()        
        return jsonify(data)
    except psycopg2.Error as e:
        print("Error al obtener los datos de la base de datos:", e)
        return jsonify({'error': 'No se pudieron obtener los datos de la base de datos'}), 500

# Registrar el esquema con Flask y apispec
spec.components.schema("TaxiSchema", schema=TaxiSchema)
# Registrar la ruta y las entidades dentro de ella con apispec
with app.test_request_context():
    spec.path(view=getTaxis)

#HISTORIA DE USUARIO 3 - LISTAR LAS LOCALIZACIONES DE UN TAXI, SEGUN EL ID Y SU FECHA

#Esquema para la respuesta de la API
class TaxiLocationSchema(Schema):
    fecha = fields.Date(description="Fecha de la ubicacion", required=True)
    latitud = fields.Float(description="Latitud de la ubicacion", required=True)
    longitud = fields.Float(description="Longitud de la ubicacion", required=True)

#Endpoint para localizaciones del taxi segun ID y fecha (/taxis/6418/locations?date=2008-02-02)
@app.route('/taxis/<int:taxi_id>/locations', methods=['GET'])
def getTaxiLocations(taxi_id):
    """
    Lista todos las localizaciones de un taxi, según ID y fecha
    ---
    parameters:
      - name: taxi_id
        in: path
        type: integer
        required: true
        description: ID del taxi
      - name: date
        in: query
        type: string
        required: true
        description: Fecha en formato YYYY-MM-DD
    responses:
      200:
        description: Localizaciones del taxi obtenidas exitosamente
        content:
            application/json:
              schema: 
                type: array
                items: 
                  $ref: '#/components/schemas/TaxiLocationSchema'
      500:
        description: Error al obtener los datos de la base de datos
    """    
    try:
        # Obtener el parámetro de la fecha (en formato YYYY-MM-DD)
        date_param = request.args.get('date')
        if date_param is None:
            return jsonify({'error': 'Se requiere el parámetro de fecha en formato YYYY-MM-DD'}), 400

        cursor = conn.cursor()
        # Consulta SQL para obtener las localizaciones del taxi para la fecha especificada
        cursor.execute("SELECT date, latitude, longitude FROM trajectories WHERE taxi_id = %s AND date::date = %s ORDER BY date", (taxi_id, date_param))
        data = cursor.fetchall()
        cursor.close()

        locations = []
        for row in data:
            location = {
                'fecha': row[0],
                'latitud': row[1],
                'longitud': row[2]
            }
            locations.append(location)

        return jsonify(locations)
    except psycopg2.Error as e:
        print("Error al obtener las localizaciones del taxi:", e)
        return jsonify({'error': 'No se pudieron obtener los datos de la base de datos'}), 500
    
# Registrar el esquema con Flask y apispec
spec.components.schema("TaxiLocationSchema", schema=TaxiLocationSchema)
# Registrar la ruta y las entidades dentro de ella con apispec
with app.test_request_context():
    spec.path(view=getTaxiLocations)
    

#HISTORIA DE USUARIO 4 - MOSTRAR LA ULTIMA LOCALIZACION DE UN TAXI, DADO SU ID
        
#Schema para la respuesta de la API
class LastLocationSchema(Schema):
    id = fields.Int(description= "ID del taxi", required=True)
    fecha = fields.Date(description="Fecha de ultima localizacion", required=True)
    latitud = fields.Float(description="Latitud de la ultima localizacion", required=True)
    longitud = fields.Float(description="Longitud de la ultima localizacion", required=True)

#Endopoint para la ultima localizacion del taxi
@app.route('/taxis/<int:taxi_id>/last-location', methods=['GET'])
def getLastLocation(taxi_id):
    """
    Lista todos las localizaciones de un taxi, según ID y fecha
    ---
    parameters:
      - name: taxi_id
        in: path
        type: integer
        required: true
        description: ID del taxi
    responses:
      200:
        description: Ultima localizacion del taxi obtenida exitosamente
        content:
            application/json:
              schema: 
                type: array
                items: 
                  $ref: '#/components/schemas/LastLocationSchema'
      404:
        description: No se encontraron ubicaciones para el taxi con ID proporcionado
      500:
        description: Error al obtener los datos de la base de datos
    """
    try:
        cursor = conn.cursor()
        # Consulta SQL para obtener la última ubicación del taxi
        cursor.execute("SELECT date, latitude, longitude FROM trajectories WHERE taxi_id = %s ORDER BY date DESC LIMIT 1", (taxi_id,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            date_str = str(data[0])  # Convertir la fecha a cadena
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%Y-%m-%d')  # Convertir la fecha al formato YYYY-MM-DD

            location = {
                'fecha': formatted_date,
                'latitud': data[1],
                'longitud': data[2]
            }
            return jsonify(location)
        else:
            return jsonify({'error': 'No se encontraron ubicaciones para el taxi con el ID proporcionado'}), 404
    except psycopg2.Error as e:
        print("Error al obtener la última ubicación del taxi:", e)
        return jsonify({'error': 'No se pudieron obtener los datos de la base de datos'}), 500
    
# Registrar el esquema con Flask y apispec
spec.components.schema("LastLocationSchema", schema=LastLocationSchema)
# Registrar la ruta y las entidades dentro de ella con apispec
with app.test_request_context():
    spec.path(view=getLastLocation)


#Generar el archivo de documentación
with open('swagger.json', 'w') as f:
    f.write(spec.to_yaml())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No se encontró el recurso solicitado'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
