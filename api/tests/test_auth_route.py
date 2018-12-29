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

    def test_sign_in_with_valid_email_and_password(self):

        input_data = {
            "firstname" : "Peter",
            "lastname" : "Mercury",
            "othernames" : "Simon",
            "email" : "pms@email.com",
            "phonenumber" : "0713285332",
            "username" : "pms",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())
        token = response_data["data"]["access_token"]

        input_data = {
            "email" : "pms@email.com",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signin', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pms@email.com was successfully signed in", response_data["data"]["message"])
        self.assertTrue(response_data["data"]["access_token"])
        #self.assertEqual(token, response_data["data"]["access_token"])

    def test_sign_in_with_invalid_email(self):

        input_data = {
            "firstname" : "Peter",
            "lastname" : "Mercury",
            "othernames" : "Simon",
            "email" : "pms1@email.com",
            "phonenumber" : "0713285332",
            "username" : "pms1",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())

        input_data = {
            "email" : "pms@email.com",
            "password" : "W3l(0M3"
        }
        response = self.app_tester.post('/api/v1/auth/signin', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(f"User with email {input_data['email']} not found", response_data["error"])

    def test_sign_in_with_invalid_password(self):

        input_data = {
                "firstname" : "Peter",
                "lastname" : "Mercury",
                "othernames" : "Simon",
                "email" : "pms2@email.com",
                "phonenumber" : "0713285332",
                "username" : "pms2",
                "password" : "W3l(0M3"
            }
        response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
        response_data = json.loads(response.data.decode())

        input_data = {
                "email" : "pms2@email.com",
                "password" : "password"
            }
        response = self.app_tester.post('/api/v1/auth/signin', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(f"Unauthorized - Wrong signin credentials supplied", response_data["error"])
        
