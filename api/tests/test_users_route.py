import unittest
import json
from api import app
from api.models.database import userdb_api
import datetime


class TestUsersRoute(unittest.TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        self.app_tester = app.test_client()
        self.user_data = {
            "firstname": "Jane",
            "lastname": "Jones",
            "othernames": "",
            "email": "jane@email.com",
            "phonenumber": "0775778887",
            "username": "jane",
            "password": """sha256$M0lFuN76$f4f847832c559f5a38c317d334aeb110184dad95063dd28559bb40a4b69be0d6""",
            "isAdmin" : False
        }
        self.user_data_admin = {
            "firstname": "Jane",
            "lastname": "Jones",
            "othernames": "",
            "email": "adminJane@email.com",
            "phonenumber": "0775778887",
            "username": "adminJane",
            "password": """sha256$M0lFuN76$f4f847832c559f5a38c317d334aeb110184dad95063dd28559bb40a4b69be0d6""",
            "isAdmin" : True
        }
        self.user_id = userdb_api.create_user(**self.user_data)
        self.admin_id = userdb_api.create_user(**self.user_data_admin)

    def tearDown(self):

        userdb_api.delete_user_by_email(
            self.user_data['email'])
        userdb_api.delete_user_by_email(
            self.user_data_admin['email'])


    def test_get_users_with_admin_user(self):

        response = self.app_tester.post(
            '/api/v1/auth/login',
            json={
            "username": "adminJane",
            "password": "entersaysme"
            })
        response_data = json.loads(response.data.decode())
        token = response_data['data'][0]['access_token']

        response = self.app_tester.get(
            '/api/v1/users',
            headers=dict(
                Authorization = 'Bearer ' + f"{token}"))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])


    def test_get_all_users_with_non_admin_user(self):

        response = self.app_tester.post(
            '/api/v1/auth/login',
            json={
            "username": "jane",
            "password": "entersaysme"
            })
        response_data = json.loads(response.data.decode())
        token = response_data['data'][0]['access_token']
        self.tearDown()

        response = self.app_tester.get(
            '/api/v1/users',
            headers=dict(
                Authorization = 'Bearer ' + f"{token}"))
        response_data = json.loads(response.data.decode())
        print(f'{response_data}')
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthorized - Cannot access this route",
                      response_data['error'])

    # def test_get_user_by_id_when_user_exsits(self):
    #     input_data = {
    #         "firstname": "Jane",
    #         "lastname": "Starr",
    #         "othernames": "",
    #         "email": "starry@email.com",
    #         "phonenumber": "0773287332",
    #         "username": "jstarr",
    #         "password": "W3l(0M3_"
    #     }
    #     response = self.app_tester.post('/api/v1/auth/signup', json=input_data)
    #     reponse_data = json.loads(response.data.decode())
    #     user_id = reponse_data["data"][0]["id"]

    #     response = self.app_tester.get(
    #         f'/api/v1/users/{user_id}')
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIs(type(response_data['data'][0]["id"]), int)
    #     self.assertEqual(user_id, response_data['data'][0]['id'])

    # def test_get_user_by_id_when_user_does_not_exist(self):

    #     input_data = {
    #         "user_id": 1
    #     }
    #     user_id = input_data['user_id']
    #     response = self.app_tester.get(
    #         f'/api/v1/users/{user_id}', json=input_data)
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("No user with ID: 1 was found", response_data['data'])
