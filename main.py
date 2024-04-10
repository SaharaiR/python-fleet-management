import os
from flask import Flask
import psycopg2

app = Flask(__name__)

#Configuración a la base de datos
dbName = os.environ.get('POSTGRES_DATABASE')
dbUser = os.environ.get('POSTGRES_USER')
dbPassword = os.environ.get('POSTGRES_PASSWORD')
dbHost = os.environ.get('POSTGRES_HOST')
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

@app.route('/')
def index():
    # Ejemplo de consulta a la base de datos
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tabla_ejemplo')
    results = cursor.fetchall()
    cursor.close()
    
    return str(results)

if __name__ == '__main__':
    app.run(debug=True)