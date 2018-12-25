import unittest
import json
from api import app
from datetime import datetime


class TestRedFlagsRoute(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client()

    def test_get_red_flag_with_data(self):
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
        print("DATA : {0}".format(response_data))
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
        self.assertIn("red-flag", response_data['data']['type'])

    def test_create_red_flag_with_no_data(self):
        input_data = {}
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request body", response_data["data"])
    