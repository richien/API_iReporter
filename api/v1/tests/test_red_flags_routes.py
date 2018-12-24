import unittest
import json
from app import app
from datastructures import DataStructures
from datetime import datetime


class TestRedFlags(unittest.TestCase):
    def setUp(self):
        self.app_tester = app.test_client()

    def test_get_red_flag_with_data(self):
        response = self.app_tester.get('api/v1/red-flags')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Roads in poor condition', data['data'][0]['title'])
        self.assertEqual(200, data['status'])