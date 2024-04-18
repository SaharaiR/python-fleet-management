import os
from dotenv import load_dotenv
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)
conn = None

# Cargar variables de entorno desde el archivo .env.development.local
load_dotenv('.env.development.local')

# Obtener las variables de entorno para la conexión a la base de datos
dbName = os.getenv('POSTGRES_DATABASE')
dbUser = os.getenv('POSTGRES_USER')
dbPassword = os.getenv('POSTGRES_PASSWORD')
dbHost = os.getenv('POSTGRES_HOST')
dbPort = '5432'

# Conexión a la base de datos PostgreSQL
try:
    conn = psycopg2.connect(
        dbname= dbName,
        user= dbUser,
        password= dbPassword,
        host= dbHost,
        port= dbPort
    )
    print("Conexión a la base de datos exitosa")
except psycopg2.Error as e:
    print("Error al conectar a la base de datos:", e)

# Endpoint para obtener la información de la API
@app.route('/taxis', methods=['GET'])
def dataApi(page=1, per_page=10):
    datos = dataApi(page=1, per_page=10)
    if datos is not None:
        print('Conexion a la API')
        return jsonify(datos)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de la API'}), 500

if __name__ == '__main__':
    app.run(debug=True)