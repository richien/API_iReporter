import unittest
import json
from api import app


class TestUsersRoute(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client() 

    def test_get_all_users(self):
        input_data = {
            "firstname" : "Henry",
            "lastname" : "Jones",
            "othernames" : "",
            "email" : "hjones@email.com",
            "phonenumber" : "0773287332",
            "username" : "hjones",
            "password" : "W3l(0M3"
        }
        self.app_tester.post('/api/v1/auth/signup', json=input_data)

        response = self.app_tester.get('/api/v1/users')
        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data["data"]["message"]), list)

    def test_get_user_by_id(self):
        input_data = {
            "firstname" : "Jane",
            "lastname" : "Starr",
            "othernames" : "",
            "email" : "starry@email.com",
            "phonenumber" : "0773287332",
            "username" : "jstarr",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        reponse_data = json.loads(response.data.decode())
        user_id = reponse_data["data"]["id"]

        input_data = {
            "user_id" : user_id
        }
        response = self.app_tester.get(f'/api/v1/users/{user_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(input_data["user_id"], response_data['data']["id"])
