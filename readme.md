

# API Fleet Management

Objetivo General: Nuestra cliente ha instalado dispositivos GPS en sus taxis. Estos dispositivos utilizan señales satelitales para determinar con precisión las coordenadas geográficas del taxi.

Nuestra clienta requiere:

- Cargar la información de archivos SQL a una base de datos Postgresql.
- Desarrollar una API REST que permita consultar, mediante peticiones HTTP, la información almancenada en la base de datos.

## HISTORIA DE USUARIO 1. Cargar información a base de datos.

Cargar la información almacenada hasta ahora en archivos sql en una base de datos PostgreSQL, para facilitar su consulta y análisis.

## HISTORIA DE USUARIO 2. Endpoint listado de taxis

Como clienta de la API REST requiero un endpoint para listar todos los taxis.

#### Listado de todos los taxis con ID y placa

```http
  GET /taxis
  GET /taxis?page=1
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `page`    | `integer`| Numero de página para la paginación |
| `per_page`| `integer`| Taxis por página |

Respuestas HTTP:
- 200: OK
- 500: Error al obtener los datos de la base de datos.

Esquema de resultado:

```sql
{
  "id": 0,
  "plate": "string"
}
```
## HISTORIA DE USUARIO 3. Endpoint historial de ubicaciones

Como clienta de la API REST requiero un endpoint para consultar todas las ubicaciones de un taxi dado el id y una fecha.

#### Listado de localizaciones según ID y fecha

```http
  GET /taxis/{taxi_id}/locations
  GET /taxis/{taxi_id}/locations?date=YYYY/MM/DD
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer`| **Required**. ID del taxi |
| `date`    | `string` | **Required**. Fecha de búsqueda

Respuestas HTTP:
- 200: OK
- 500: Error al obtener los datos

Esquema de resultado:

```sql
{
  "fecha": "YYYY-MM-DD",
  "latitud": 0,
  "longitud": 0
}
```
## HISTORIA DE USUARIO 4. Endpoint última ubicación

Como clienta de la API REST requiero un endpoint para consultar la última ubicación reportada por cada taxi.

#### Listado de la última localización de un taxi según su ID

```http
  GET /taxis/{taxi_id}/last-location
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer`| **Required**. ID del taxi |

Respuestas HTTP:
- 200: OK
- 404: No se encontraron ubicaciones para el ID proporcionado
- 500: Error al obtener datos de la base de datos.

Esquema de resultado:
```sql
{
  "id": 0,
  "fecha": "YYYY-MM-DD",
  "latitud": 0,
  "longitud": 0
}
```

## API Publicada en Swagger:

https://app.swaggerhub.com/apis/SAHARAROD/APIFleetM/1.0.0#/info


## Stack de tecnologías:
- Python
- Flask

## Consultas:

- Tutorial crear BD en Vercel: https://vercel.com/docs/storage/vercel-postgres/quickstart

- APISPEC: https://apispec.readthedocs.io/en/latest/using_plugins.html#example-flask-and-marshmallow-plugins
  
  https://github.com/marshmallow-code/apispec/tree/dev?
- Documentación para swagger: https://www.peterspython.com/es/blog/documentacion-de-un-flask-restful-api-con-openapi-swagger-utilizando-apispec

- Conexion con flask: 
  
  https://realpython.com/flask-connexion-rest-api/
  
   https://datascientest.com/es/programacion-de-api-web-en-python-con-flask

- Pruebas unitarias y de integración para una API REST: 
  https://apuntes.de/python/desarrollo-de-una-api-rest-con-flask-en-python-creacion-de-una-interfaz-de-programacion-de-aplicaciones-restful/#gsc.tab=0

- Consulta SQL con paginación:
  https://www.sqlshack.com/es/sql-server-2012-introduccion-paginacion/