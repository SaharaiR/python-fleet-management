from flask import Flask, jsonify, request, make_response
from database import connectDataBase
import psycopg2

app = Flask(__name__)
conn = connectDataBase()

#Endpoint de HOME
@app.route('/', methods=['GET'])
def home():
   return "<h1>Fleet Management API</h1>"    

#Endpoint de la información general
@app.route('/taxis', methods=['GET'])
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No se encontró el recurso solicitado'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
