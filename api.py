from flask import Flask, jsonify, request, make_response
from database import connectDataBase
from datetime import datetime
#from flask_restplus import Api, Resource
import psycopg2

app = Flask(__name__)
conn = connectDataBase()
#api = Api(version='1.0', title='API Fleet Management', description='API de taxis')

#Endpoint de HOME
@app.route('/', methods=['GET'])
#class Home(Resource):
    #def get(self):
def home():
        return "<h1>Fleet Management API</h1>"

#HISTORIA DE USUARIO 2 - LISTADO DE TODOS LOS TAXIS CON SU ID Y PLACA
#Endpoint de la información general paginada (endpoint para paginacion: http://127.0.0.1:5000/taxis?page=1)
@app.route('/taxis', methods=['GET'])
#class Taxis(Resource):
    #def get(self):
def get_taxis():
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
    
#HISTORIA DE USUARIO 3 - LISTAR LAS LOCALIZACIONES DE UN TAXI, SEGUN EL ID Y SU FECHA
#Endpoint para localizaciones del taxi segun ID y fecha (/taxis/6418/locations?date=2008-02-02)
@app.route('/taxis/<int:taxi_id>/locations', methods=['GET'])
#class Locations(Resource):
    #def get(self, taxi_id):
def get_taxi_locations(taxi_id):
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
    

#HISTORIA DE USUARIO 4 - MOSTRAR LA ULTIMA LOCALIZACION DE UN TAXI, DADO SU ID
#Endopoint para la ultima localizacion del taxi
@app.route('/taxis/<int:taxi_id>/last-location', methods=['GET'])
#class LastLocation(Resource):
    #def get(self, taxi_id):
def getLastLocation(taxi_id):
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No se encontró el recurso solicitado'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
