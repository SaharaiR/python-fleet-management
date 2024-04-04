from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import psycopg2

app = Flask(__name__)
api = Api(app)

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="fleetM-postgressPy",
    user="tu_usuario",
    password="tu_contraseña",
    host="tu_host",
    port="tu_puerto"
)