import os
from dotenv import load_dotenv
from flask import Flask
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

#Función para conexión a la base de datos PostgreSQL
def connectDataBase():
    try:
        conn = psycopg2.connect(
            dbname= dbName,
            user= dbUser,
            password= dbPassword,
            host= dbHost,
            port= dbPort
        )
        print("Conexión a la base de datos exitosa")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)