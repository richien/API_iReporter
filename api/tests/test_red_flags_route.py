import unittest
import json
from api import app
from datetime import datetime
from api.models.database import incidentdb_api
from api.models.database import userdb_api


class TestRedFlagsRoute(unittest.TestCase):

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
            "password": "my_password",
            "isAdmin" : False
        }
        user_id = userdb_api.create_user(**self.user_data)
        self.input_data = {
            "createdby": user_id['user_id'],
            "type": "red-flag",
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "images": ["image_1.png", "image_2.jpg"],
            "videos": ["vid_1.mp4"],
            "comment": "Accidental post!",
            "title": "Roads in poor condition"
         }
        self.data = incidentdb_api.create_incident(**self.input_data)

    def tearDown(self):
        incidentdb_api.delete_incidents_by_user(
            self.input_data['createdby'])


    def test_get_red_flags_with_data_present(self):

        response = self.app_tester.post(
            '/api/v1/auth/login',
            json={
            "username": "test1",
            "password": "my_password"
            })
        response_data = json.loads(response.data.decode())
        token = response_data['data'][0]['access_token']

        response = self.app_tester.get(
            '/api/v1/red-flags',
            headers=dict(
                Authorization = 'Bearer ' + f"{token}"))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])

    def test_get_red_flag_by_id(self):

        response = self.app_tester.post(
            '/api/v1/auth/login',
            json={
            "username": "test1",
            "password": "my_password"
            })
        response_data = json.loads(response.data.decode())
        token = response_data['data'][0]['access_token']

        red_flag_id = self.data['incident_id']
        response = self.app_tester.get(
            '/api/v1/red-flags/{0}'.format(red_flag_id),
            headers=dict(
                Authorization = 'Bearer ' + f"{token}"))
        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['data'][0]['id']), int)
        self.assertEqual(red_flag_id, response_data['data'][0]['id'])

    def test_get_red_flag_by_id_with_data_absent(self):

        response = self.app_tester.post(
            '/api/v1/auth/login',
            json={
            "username": "test1",
            "password": "my_password"
            })
        response_data = json.loads(response.data.decode())
        token = response_data['data'][0]['access_token']

        input_data = {"red_flag_id": 12}
        red_flag_id = input_data['red_flag_id']
        response = self.app_tester.get(
            f'/api/v1/red-flags/{red_flag_id}',
            headers=dict(
                Authorization = 'Bearer ' + f"{token}"))
        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])
        self.assertEqual("No record  with ID:12 was found",
                         response_data['data'][0]['message'])

    def test_create_red_flag_with_data(self):

        response = self.app_tester.post(
            '/api/v1/auth/login',
            json={
            "username": "test1",
            "password": "my_password"
            })
        response_data = json.loads(response.data.decode())
        token = response_data['data'][0]['access_token']

        response = self.app_tester.post(
            '/api/v1/red-flags',
            json=self.input_data,
            headers=dict(
                Authorization = 'Bearer ' + f"{token}"))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Created red-flag record",
                      response_data['data'][0]['message'])
        self.assertIs(type(response_data['data'][0]['id']), int)

    def test_create_red_flag_with_no_data(self):

        input_data = {}
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request - request body cannot be empty",
                      response_data["error"])

    def test_create_red_flag_with_invalid_type_field(self):

        response = self.app_tester.post(
            '/api/v1/auth/login',
            json={
            "username": "test1",
            "password": "my_password"
            })
        response_data = json.loads(response.data.decode())
        token = response_data['data'][0]['access_token']

        input_data = {
            "createdby": 1000,
            "type": "intervention",
            "location": "23.000, 55.90",
            "status": "draft",
            "images": ["image.png"],
            "videos": [],
            "comment": "Umeme employee asking for money to reconnect power.",
            "title": "No electricity after paying bill"
        }
        response = self.app_tester.post(
            '/api/v1/red-flags',
            json=input_data,
            headers=dict(
                Authorization = 'Bearer ' + f"{token}"))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Unrecorgnised Incident type",
            response_data['error'])

    def test_edit_red_flag_location(self):

        input_data = input_data = {
            "location": "00.0000, 00.0001"
        }

        red_flag_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/red-flags/{0}/location'.format(red_flag_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated red-flag record's location",
                      response_data['data'][0]['message'])
        self.assertEqual("00.0000, 00.0001",
                         response_data['data'][0]['content']['location'])
    
    def test_edit_red_flag_location_with_invalid_location(self):

        input_data = input_data = {
            "location": "11.12345"
        }

        red_flag_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/red-flags/{0}/location'.format(red_flag_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Failed to update red-flag record's location",
                      response_data['error'])

    def test_edit_red_flag_comment(self):

        input_data = input_data = {
            "comment": "Comment updated"
        }

        red_flag_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/red-flags/{0}/comment'.format(red_flag_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated red-flag record's comment",
                      response_data['data'][0]['message'])
        self.assertEqual("Comment updated",
                         response_data['data'][0]['content']['comment'])

    def test_edit_red_flag_unknown_field_in_request_body(self):

        input_data = input_data = {
            "coment": "Updated comment"
        }

        red_flag_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/red-flags/{0}/comment'.format(red_flag_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn("Invalid field in request body", response_data['error'])

    def test_edit_red_flag_with_data_absent(self):

        red_flag_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/red-flags/{0}/comment'.format(red_flag_id))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(400, response_data['status'])
        self.assertEqual("""Invalid request - request body cannot be empty""",
                         response_data['error'])


    def test_edit_red_flag_comment_with_empty_string(self):

        input_data = input_data = {
            "comment": " "
        }

        red_flag_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/red-flags/{0}/comment'.format(red_flag_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Failed to update red-flag record's comment", 
            response_data['error'])

    def test_delete_red_flag(self):

        red_flag_id = self.data["incident_id"]
        response = self.app_tester.delete(
            '/api/v1/red-flags/{0}'.format(red_flag_id))
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(red_flag_id, response_data['data'][0]['id'])

    def test_delete_red_flag_with_data_absent(self):

        input_data = {"red_flag_id": 0}
        red_flag_id = input_data['red_flag_id']
        response = self.app_tester.delete(
            '/api/v1/red-flags/{0}'.format(red_flag_id))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(404, response_data['status'])
        self.assertEqual(
            f"No record  with ID:{red_flag_id} was found", 
            response_data['error'])
