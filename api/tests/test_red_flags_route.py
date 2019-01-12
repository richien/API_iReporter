import unittest
import json
from api import app
from datetime import datetime


class TestRedFlagsRoute(unittest.TestCase):

    def setUp(self):

        self.app_tester = app.test_client()

    def test_get_red_flags(self):

        response = self.app_tester.get('/api/v1/red-flags')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Roads in poor condition', data['data'][0]['title'])
        self.assertEqual(200, data['status'])

    def test_get_red_flag_by_id(self):

        input_data = {"red_flag_id" : 2}
        red_flag_id = input_data['red_flag_id']
        response = self.app_tester.get('/api/v1/red-flags/{0}'.format(red_flag_id), json=input_data)
        response_data = json.loads(response.data.decode())        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['data']['id']), int)
        self.assertEqual(red_flag_id, response_data['data']['id'])
    
    def test_create_red_flag_with_data(self):

        input_data =  { 
                        "createdBy" : 5000,
                        "type" : "red-flag",
                        "location" : "33.92300, 44.9084551",
                        "status" : "draft",
                        "images" : ["image_1.png", "image_2.jpg" ],
                        "videos" : ["vid_1.mp4"],
                        "comment" : "I almost got runover by a car that was dodging potholes!",
                        "title": "Roads in poor condition"
        }
        
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("Created red-flag record", response_data['data']['message'])
        self.assertIs(type(response_data['data']['id']), int)

    def test_create_red_flag_with_no_data(self):

        input_data = {}
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request body", response_data["error"])

    def test_create_red_flag_with_invalid_type_field(self):

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
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("field should be red-flag", response_data['error'])
    
    def test_edit_red_flag_location(self):

        input_data =  input_data =  { 
                        "red_flag_id" : 2,
                        "location" : "11.12345, 12.12345"
        }

        red_flag_id = input_data['red_flag_id']  
        response = self.app_tester.put('/api/v1/red-flags/{0}/location'.format(red_flag_id), json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated red-flag record's location", response_data['data']['message'])
        self.assertEqual("11.12345, 12.12345", response_data['data']['content']['location'])
    
    def test_edit_red_flag_comment(self):

        input_data =  input_data =  { 
                        "red_flag_id" : 2,
                        "comment" : "Comment updated"
        }

        red_flag_id = input_data['red_flag_id']  
        response = self.app_tester.put('/api/v1/red-flags/{0}/comment'.format(red_flag_id), json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated red-flag record's comment", response_data['data']['message'])
        self.assertEqual("Comment updated", response_data['data']['content']['comment'])

    def test_delete_red_flag(self):

        input_data =  { 
                        "createdBy" : 5000,
                        "type" : "red-flag",
                        "location" : "33.92300, 44.9084551",
                        "status" : "draft",
                        "images" : ["image_1.png", "image_2.jpg" ],
                        "videos" : ["vid_1.mp4"],
                        "comment" : "I almost got runover by a car that was dodging potholes!",
                        "title": "Roads in poor condition"
        } 

        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        red_flag_id = response_data['data']['id']

        input_data = {"red_flag_id" : red_flag_id}
        
        response = self.app_tester.delete('/api/v1/red-flags/{0}'.format(red_flag_id), json=input_data)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(red_flag_id, response_data['data']['id'])