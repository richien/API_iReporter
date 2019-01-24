import unittest
import json
from api import app
from data import incidents_data
from api.models.database import incidentdb_api
from api.models.database import userdb_api

incidents = incidents_data['data']


class TestInterventions(unittest.TestCase):

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
            "type": "intervention",
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
        userdb_api.delete_user_by_email(self.user_data['email'])


    def test_create_intervention_with_valid_data(self):

        response = self.app_tester.post(
            '/api/v1/interventions', json=self.input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Created intervention",
                      response_data['data'][0]['message'])
        self.assertIs(type(response_data['data'][0]['id']), int)

    def test_create_intervention_with_invalid_incident_type(self):

        input_data = {
            "createdby": 498,
            "type": "red-flag",
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "images": ["image_1.png", "image_2.jpg"],
            "videos": ["vid_1.mp4"],
            "comment": "Accidental post!",
            "title": "Roads in poor condition"
         }
        response = self.app_tester.post(
            '/api/v1/interventions', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_create_intervention_with_missing_fields(self):

        input_data = {
            "createdBy": 1000,
            "type": "intervention",
            "location": "23.000, 55.90",
            "comment": "Umeme employee asking for money to reconnect power.",
            "title": "No electricity after paying bill"
        }
        response = self.app_tester.post(
            '/api/v1/interventions', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request body ", response_data['error'])

    def test_create_intervention_with_invalid_type_field(self):

        input_data = {
            "createdby": 1000,
            "type": "red-flag",
            "location": "23.000, 55.90",
            "status": "draft",
            "images": ["image.png"],
            "videos": [],
            "comment": "Umeme employee asking for money to reconnect power.",
            "title": "No electricity after paying bill"
        }
        response = self.app_tester.post(
            '/api/v1/interventions', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("field should be intervention", response_data['error'])

    def test_get_interventions_with_data_present(self):
        
        response = self.app_tester.get('/api/v1/interventions')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])

  
    def test_get_intervention_by_id_with_valid_request_body(self):

        intervention_id = self.data['incident_id']
        response = self.app_tester.get(
            f'/api/v1/interventions/{intervention_id}', json=self.input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])

    def test_get_intervention_by_id_with_data_absent(self):

        data = {"id": 12}
        intervention_id = data['id']
        response = self.app_tester.get(
            f'/api/v1/interventions/{intervention_id}')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])
        self.assertEqual(
            "No record  with ID:12 was found", 
            response_data['data'][0]['message'])
    
    def test_edit_intervention_location(self):

        input_data = input_data = {
            "location": "00.0000, 00.0001"
        }

        intervention_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/interventions/{0}/location'.format(intervention_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated intervention record's location",
                      response_data['data'][0]['message'])
        self.assertEqual("00.0000, 00.0001",
                         response_data['data'][0]['content']['location'])
    
    def test_edit_intervention_location_with_invalid_location(self):

        input_data = input_data = {
            "location": "11.12345"
        }

        intervention_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/interventions/{0}/location'.format(intervention_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Failed to update intervention record's location",
                      response_data['error'])

    def test_edit_intervention_comment(self):

        input_data = input_data = {
            "comment": "Comment updated"
        }

        intervention_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/interventions/{0}/comment'.format(intervention_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated intervention record's comment",
                      response_data['data'][0]['message'])
        self.assertEqual("Comment updated",
                         response_data['data'][0]['content']['comment'])

    def test_edit_intervention_unknown_field_in_request_body(self):

        input_data = input_data = {
            "coment": "Updated comment"
        }

        intervention_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/interventions/{0}/comment'.format(intervention_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn("Invalid field in request body", response_data['error'])

    def test_edit_intervention_with_data_absent(self):

        intervention_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/interventions/{0}/comment'.format(intervention_id))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(400, response_data['status'])
        self.assertEqual("""Invalid request - request body cannot be empty""",
                         response_data['error'])


    def test_edit_intervention_comment_with_empty_string(self):

        input_data = input_data = {
            "comment": " "
        }

        intervention_id = self.data['incident_id']
        response = self.app_tester.patch(
            '/api/v1/interventions/{0}/comment'.format(intervention_id),
            json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Failed to update intervention record's comment", 
            response_data['error'])
    
