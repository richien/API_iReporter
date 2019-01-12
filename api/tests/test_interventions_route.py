import unittest
import json
from api import app


class TestInterventions(unittest.TestCase):
    
    def setUp(self):
        self.app_tester = app.test_client()

    def test_create_intervention_with_valid_data(self):
        input_data = {
            "createdBy" : 1000,
            "type" : "intervention",
            "location" : "23.000, 55.90",
            "status" : "draft",
            "images" : ["image.png"],
            "videos" : [],
            "comment" : "Umeme employee asking for money to reconnect power.",
            "title" : "No electricity after paying bill"
        }

        response = self.app_tester.post('/api/v1/interventions', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Created intervention", response_data['data'][0]['message'])
        self.assertIs(type(response_data['data'][0]['id']), int)

    def test_create_intervention_with_invalid_incident_type(self):
        
        input_data = {
            "createdBy" : 1000,
            "type" : "interventon", # this Incident type is invalid
            "location" : "23.000, 55.90",
            "status" : "draft",
            "images" : ["image.png"],
            "videos" : [],
            "comment" : "Umeme employee asking for money to reconnect power.",
            "title" : "No electricity after paying bill"
        }
        response = self.app_tester.post('/api/v1/interventions', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid Incident type", response_data['error'])

    def test_create_intervention_with_missing_fields(self):
        
        input_data = {
            "createdBy" : 1000,
            "type" : "intervention", 
            "location" : "23.000, 55.90",
            "comment" : "Umeme employee asking for money to reconnect power.",
            "title" : "No electricity after paying bill"
        }
        response = self.app_tester.post('/api/v1/interventions', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request body ", response_data['error'])

    def test_create_intervention_with_invalid_type_field(self):

        input_data = {
            "createdBy" : 1000,
            "type" : "red-flag",
            "location" : "23.000, 55.90",
            "status" : "draft",
            "images" : ["image.png"],
            "videos" : [],
            "comment" : "Umeme employee asking for money to reconnect power.",
            "title" : "No electricity after paying bill"
        }
        response = self.app_tester.post('/api/v1/interventions', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("field should be intervention", response_data['error'])
    
   


