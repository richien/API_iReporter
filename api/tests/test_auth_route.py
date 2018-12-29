import unittest
import json
from api import app


class TestAuthenticationRoutes(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client()

    def test_signup_with_correct_data(self):
        input_data = {
            "firstname" : "Henry",
            "lastname" : "Jones",
            "othernames" : "",
            "email" : "hjones@email.com",
            "phonenumber" : "0773287332",
            "username" : "hjones",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("registered successfully", response_data["data"]["message"])
    
    def test_signup_with_empty_required_fields(self):
        input_data = {
            "firstname" : "",
            "lastname" : "Jones",
            "othernames" : "",
            "email" : "hj@email.com",
            "phonenumber" : "0773287332",
            "username" : "hjon",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())
        print("RESPONSE_DATA: {0}".format(response_data))
        self.assertEqual(response.status_code, 400)
        self.assertIn("'firstname' cannot be empty", response_data["error"]["message"])

    def test_signup_with_existing_username(self):
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
        input_data = {
            "firstname" : "Henry",
            "lastname" : "Jones",
            "othernames" : "",
            "email" : "hjones1@email.com",
            "phonenumber" : "0773287332",
            "username" : "hjones",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("username already exists", response_data["error"])

    def test_signup_with_existing_email(self):
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
        input_data = {
            "firstname" : "Henry",
            "lastname" : "Jones",
            "othernames" : "",
            "email" : "hjones@email.com",
            "phonenumber" : "0773287332",
            "username" : "hjones1",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("email address already exists", response_data["error"])

    def test_signup_with_existing_username_and_email(self):
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
        input_data = {
            "firstname" : "Henry",
            "lastname" : "Jones",
            "othernames" : "",
            "email" : "hjones@email.com",
            "phonenumber" : "0773287332",
            "username" : "hjones",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("that account already exists", response_data["error"])
        
