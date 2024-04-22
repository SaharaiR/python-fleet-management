import unittest
from api import app

class TestAPI(unittest.TestCase):

    def test_get_users(self):
        with app.test_client() as client:
            response = client.get('/taxis')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
