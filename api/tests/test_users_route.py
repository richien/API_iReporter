import unittest
import json
from api import app
from data import incidents_data
import datetime

users = incidents_data['users']

class TestUsersRoute(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client() 

    def test_get_all_users_with_users_present(self):
       
        data = {
            'id': 3589, 
            'firstname': 'Henry', 
            'lastname': 'Jones', 
            'othernames': '', 
            'email': 'hjones@email.com', 
            'phonenumber': '0773287332',
             'username': 'hjones', 
             'password': 'sha256$FJFz4dTw$e02642d454ee9de9fdd7bfb5e12969e633d86f899dd541a0f7ca80cebc872ef7', 
             'registered': datetime.date(2019, 1, 13), 
             'isAdmin': False
             }
        users.append(data)
        response = self.app_tester.get('/api/v1/users')
        response_data = json.loads(response.data.decode())
        expected_response =  {
                    'email': 'hjones@email.com',
                    'firstname': 'Henry', 
                    'id': 3589, 
                    'isAdmin': False, 
                    'lastname': 'Jones',
                    'othernames': '', 
                    'phonenumber': '0773287332', 
                    'registered': 'Sun, 13 Jan 2019 00:00:00 GMT', 
                    'username': 'hjones'
                }
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data["data"][0]["message"]), list)
        self.assertIn(expected_response, response_data['data'][0]['message'])
    
    def test_get_all_users_with_users_absent(self):
       
        users.clear()
        response = self.app_tester.get('/api/v1/users')
        response_data = json.loads(response.data.decode())       
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data["data"]), list)
        self.assertIn("There are no users registered", response_data['data'][0])

    def test_get_user_by_id_with_valid_id(self):
        input_data = {
            "firstname" : "Jane",
            "lastname" : "Starr",
            "othernames" : "",
            "email" : "starry@email.com",
            "phonenumber" : "0773287332",
            "username" : "jstarr",
            "password" : "W3l(0M3_"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        reponse_data = json.loads(response.data.decode())
        user_id = reponse_data["data"][0]["id"]

        input_data = {
            "user_id" : user_id
        }
        response = self.app_tester.get(f'/api/v1/users/{user_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(input_data["user_id"], response_data['data'][0]["id"])

    def test_get_user_by_id_with_invalid_request_id(self):
        input_data = {
            "firstname" : "Jane",
            "lastname" : "Starr",
            "othernames" : "",
            "email" : "starr@email.com",
            "phonenumber" : "0773287332",
            "username" : "starr",
            "password" : "W3l(0M3_"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        reponse_data = json.loads(response.data.decode())
        user_id = reponse_data["data"][0]["id"]

        input_data = {
            "user_id" : 1
        }
        response = self.app_tester.get(f'/api/v1/users/{user_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request", response_data['error'])
    
    def test_get_user_by_id_when_user_does_not_exist(self):

        input_data = {
            "user_id" : 1
        }
        user_id = input_data['user_id']
        response = self.app_tester.get(f'/api/v1/users/{user_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("No user with ID: 1 was found", response_data['data'])
        
