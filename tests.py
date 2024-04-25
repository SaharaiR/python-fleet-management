import unittest
import requests
from api import app

class TestAPI(unittest.TestCase):

    #Prueba unitaria al primer endpoint de getTaxis
    def testGetTaxis(self):
        with app.test_client() as client:
            #Simular la solicitud GET al endpoint "/taxis"
            response = client.get('/taxis')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
    
    #Prueba unitaria al segundo endpoint de getTaxiLocations
    def testGetTaxiLocations(self):
        with app.test_client() as client:
            #Simular la solicitud GET al endpoint "/taxis/{taxi_id}/locations?date={YYYY-MM-DD}"
            response = client.get('/taxis/6598/locations?date=2008-02-03')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

    #Prueba uniaria al tercer endpoint de getLastLocation
    def testGetLastLocation(self):
        with app.test_client() as client:
            #Simular la solicitud GET al endpoint "/taxis/{taxi_id}/last-location"
            response = client.get('taxis/7088/last-location')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

    #Pruebas de integracion
    def testIntegration():
        response = requests.get('http://127.0.0.1:5000/taxis')
        data = response.json()
        assert response.status_code == 200
        assert isinstance(data, list)