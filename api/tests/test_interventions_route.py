import unittest
import json
from api import app
from data import incidents_data

incidents = incidents_data['data']


class TestInterventions(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client()

    def test_create_intervention_with_valid_data(self):
        input_data = {
            "createdBy": 1000,
            "type": "intervention",
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
        self.assertEqual(response.status_code, 201)
        self.assertIn("Created intervention",
                      response_data['data'][0]['message'])
        self.assertIs(type(response_data['data'][0]['id']), int)

    def test_create_intervention_with_invalid_incident_type(self):

        input_data = {
            "createdBy": 1000,
            "type": "interventon",  # this Incident type is invalid
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
        self.assertIn("invalid Incident type", response_data['error'])

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
            "createdBy": 1000,
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
        data = {
            "comment": "I almost got runover by a car that was dodging potholes!",
            "createdBy": 5000,
            "createdOn": "Sun, 13 Jan 2019 00:00:00 GMT",
            "id": 73691,
            "images": [
                "image_1.png",
                "image_2.jpg"],
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "title": "Roads in poor condition",
            "type": "intervention",
            "videos": ["vid_1.mp4"]}
        incidents.append(data)
        response = self.app_tester.get('/api/v1/interventions')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])
        self.assertIn(data, response_data['data'][:])

    def test_get_interventions_with_data_absent(self):

        incidents.clear()
        response = self.app_tester.get('/api/v1/interventions')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])
        self.assertIn("No records found", response_data['data'])

    def test_get_intervention_by_id_with_valid_request_body(self):

        data = {
            "comment": "I almost got runover by a car that was dodging potholes!",
            "createdBy": 5000,
            "createdOn": "Sun, 13 Jan 2019 00:00:00 GMT",
            "id": 73691,
            "images": [
                "image_1.png",
                "image_2.jpg"],
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "title": "Roads in poor condition",
            "type": "intervention",
            "videos": ["vid_1.mp4"]}
        incidents.append(data)
        input_data = {"intervention_id": 73691}
        intervention_id = input_data['intervention_id']
        response = self.app_tester.get(
            f'/api/v1/interventions/{intervention_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])
        self.assertEqual(data, response_data['data'][0]['message'])

    def test_get_intervention_by_id_with_mismatch_in_request_id(self):

        data = {
            "comment": "I almost got runover by a car that was dodging potholes!",
            "createdBy": 5000,
            "createdOn": "Sun, 13 Jan 2019 00:00:00 GMT",
            "id": 73691,
            "images": [
                "image_1.png",
                "image_2.jpg"],
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "title": "Roads in poor condition",
            "type": "intervention",
            "videos": ["vid_1.mp4"]}
        incidents.append(data)
        input_data = {"intervention_id": 736}
        intervention_id = data['id']
        response = self.app_tester.get(
            f'/api/v1/interventions/{intervention_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(400, response_data['status'])
        self.assertIn("Invalid request", response_data['error'])

    def test_get_intervention_by_id_with_invalid_key_in_request(self):

        data = {
            "comment": "I almost got runover by a car that was dodging potholes!",
            "createdBy": 5000,
            "createdOn": "Sun, 13 Jan 2019 00:00:00 GMT",
            "id": 73691,
            "images": [
                "image_1.png",
                "image_2.jpg"],
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "title": "Roads in poor condition",
            "type": "intervention",
            "videos": ["vid_1.mp4"]}
        incidents.append(data)
        input_data = {"id": 73691}
        intervention_id = input_data['id']
        response = self.app_tester.get(
            f'/api/v1/interventions/{intervention_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(400, response_data['status'])
        self.assertIn("Invalid request", response_data['error'])

    def test_get_intervention_by_id_with_data_absent(self):

        incidents.clear()
        input_data = {"intervention_id": 12}
        intervention_id = input_data['intervention_id']
        response = self.app_tester.get(
            f'/api/v1/interventions/{intervention_id}', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(200, response_data['status'])
        self.assertEqual("No record  with intervention_id: 12 was found",
                         response_data['data'][0]['message'])
