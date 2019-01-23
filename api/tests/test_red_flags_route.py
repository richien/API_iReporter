import unittest
import json
from api import app
from datetime import datetime
from data import incidents_data
from api.models.database import incidentdb_api

red_flags = incidents_data['data']


class TestRedFlagsRoute(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client()
        self.input_data = {
    #         "id": 2,
            # "createdOn": "12-12-2018",
            "createdBy": 498,
            "type": "red-flag",
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "images": ["image_1.png", "image_2.jpg"],
            "videos": ["vid_1.mp4"],
            "comment": "Accidental post!",
            "title": "Roads in poor condition"
         }
    def tearDown(self):
        incidentdb_api.delete_user_by_type_and_user_id(
            self.input_data['type'], self.input_data['createdBy'])


    # def test_get_red_flags_with_data_present(self):

    #     data = {
    #         "id": 2,
    #         "createdOn": "12-12-2018",
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": ["image_1.png", "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "Accidental post!",
    #         "title": "Roads in poor condition"
    #     }
    #     red_flags.append(data)
    #     response = self.app_tester.get('/api/v1/red-flags')
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(data, response_data['data'])
    #     self.assertEqual(200, response_data['status'])

    # def test_get_red_flags_with_data_absent(self):

    #     red_flags.clear()
    #     response = self.app_tester.get('/api/v1/red-flags')
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(200, response_data['status'])
    #     self.assertIn("No records found", response_data['data'])

    # def test_get_red_flags_with_data_structure_missing(self):

    #     response = self.app_tester.get('/api/v1/red-flags')
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(200, response_data['status'])

    # def test_get_red_flag_by_id(self):

    #     data = {
    #         "id": 2,
    #         "createdOn": "12-12-2018",
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": ["image_1.png", "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "Accidental post!",
    #         "title": "Roads in poor condition"
    #     }
    #     red_flags.append(data)
    #     red_flag_id = data['id']
    #     response = self.app_tester.get(
    #         '/api/v1/red-flags/{0}'.format(red_flag_id))
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(type(response_data['data']['id']), int)
    #     self.assertEqual(red_flag_id, response_data['data']['id'])

    # def test_get_red_flag_by_id_with_data_absent(self):

    #     red_flags.clear()
    #     input_data = {"red_flag_id": 12}
    #     red_flag_id = input_data['red_flag_id']
    #     response = self.app_tester.get(
    #         f'/api/v1/red-flags/{red_flag_id}')
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(200, response_data['status'])
    #     self.assertEqual("No record  with ID:12 was found",
    #                      response_data['data'][0]['message'])

    def test_create_red_flag_with_data(self):


        response = self.app_tester.post('/api/v1/red-flags', json=self.input_data)
        response_data = json.loads(response.data.decode())
        print(f"RESPONSE: {response_data}")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Created red-flag record",
                      response_data['data'][0]['message'])
        self.assertIs(type(response_data['data'][0]['id']['incident_id']), int)

    def test_create_red_flag_with_no_data(self):

        input_data = {}
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request - request body cannot be empty",
                      response_data["error"])

    def test_create_red_flag_with_invalid_type_field(self):

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
        response = self.app_tester.post('/api/v1/red-flags', json=input_data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn("field should be red-flag", response_data['error'])

    # def test_edit_red_flag_location(self):

    #     data = {
    #         "id": 2,
    #         "createdOn": "12-12-2018",
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": ["image_1.png", "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "Accidental post!",
    #         "title": "Roads in poor condition"
    #     }
    #     red_flags.append(data)
    #     input_data = input_data = {
    #         "location": "11.12345, 12.12345"
    #     }

    #     red_flag_id = data['id']
    #     response = self.app_tester.patch(
    #         '/api/v1/red-flags/{0}/location'.format(red_flag_id),
    #         json=input_data)
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Updated red-flag record's location",
    #                   response_data['data'][0]['message'])
    #     self.assertEqual("11.12345, 12.12345",
    #                      response_data['data'][0]['content']['location'])

    # def test_edit_red_flag_comment(self):

    #     data = {
    #         "id": 2,
    #         "createdOn": "12-12-2018",
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": ["image_1.png", "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "Accidental post!",
    #         "title": "Roads in poor condition"
    #     }
    #     red_flags.append(data)
    #     input_data = input_data = {
    #         "comment": "Comment updated"
    #     }

    #     red_flag_id = data['id']
    #     response = self.app_tester.patch(
    #         '/api/v1/red-flags/{0}/comment'.format(red_flag_id),
    #         json=input_data)
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Updated red-flag record's comment",
    #                   response_data['data'][0]['message'])
    #     self.assertEqual("Comment updated",
    #                      response_data['data'][0]['content']['comment'])

    # def test_edit_red_flag_unknown_field_in_request_body(self):

    #     data = {
    #         "id": 2,
    #         "createdOn": "12-12-2018",
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": ["image_1.png", "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "Accidental post!",
    #         "title": "Roads in poor condition"
    #     }
    #     red_flags.append(data)
    #     input_data = input_data = {
    #         "coment": "Updated comment"
    #     }

    #     red_flag_id = data['id']
    #     response = self.app_tester.patch(
    #         '/api/v1/red-flags/{0}/comment'.format(red_flag_id),
    #         json=input_data)
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn("Invalid field in request body", response_data['error'])

    # def test_edit_red_flag_with_data_absent(self):

    #     red_flags.clear()
    #     data = {"red_flag_id": 12}
    #     red_flag_id = data['red_flag_id']
    #     response = self.app_tester.patch(
    #         '/api/v1/red-flags/{0}/comment'.format(red_flag_id))
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(400, response_data['status'])
    #     self.assertEqual("""Invalid request - request body cannot be empty""",
    #                      response_data['error'])

    # def test_edit_red_flag_location_with_invalid_location(self):

    #     data = {
    #         "id": 2,
    #         "createdOn": "12-12-2018",
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": ["image_1.png", "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "Accidental post!",
    #         "title": "Roads in poor condition"
    #     }
    #     red_flags.append(data)
    #     input_data = input_data = {
    #         "location": "11.12345"
    #     }

    #     red_flag_id = data['id']
    #     response = self.app_tester.patch(
    #         '/api/v1/red-flags/{0}/location'.format(red_flag_id),
    #         json=input_data)
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("Failed to update red-flag record's location",
    #                   response_data['error'])

    # def test_edit_red_flag_comment_with_empty_string(self):

    #     data = {
    #         "id": 2,
    #         "createdOn": "12-12-2018",
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": ["image_1.png", "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "Accidental post!",
    #         "title": "Roads in poor condition"
    #     }
    #     red_flags.append(data)
    #     input_data = input_data = {
    #         "comment": " "
    #     }

    #     red_flag_id = data['id']
    #     response = self.app_tester.patch(
    #         '/api/v1/red-flags/{0}/comment'.format(red_flag_id),
    #         json=input_data)
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("Failed to update red-flag record's comment",
    #                   response_data['error'])

    # def test_delete_red_flag(self):

    #     input_data = {
    #         "createdBy": 5000,
    #         "type": "red-flag",
    #         "location": "33.92300, 44.9084551",
    #         "status": "draft",
    #         "images": [
    #             "image_1.png",
    #             "image_2.jpg"],
    #         "videos": ["vid_1.mp4"],
    #         "comment": "I almost got runover by a car that was dodging potholes!",
    #         "title": "Roads in poor condition"}

    #     response = self.app_tester.post('/api/v1/red-flags', json=input_data)
    #     response_data = json.loads(response.data.decode())
    #     red_flag_id = response_data['data'][0]['id']

    #     input_data = {"red_flag_id": red_flag_id}

    #     response = self.app_tester.delete(
    #         '/api/v1/red-flags/{0}'.format(red_flag_id), json=input_data)
    #     response_data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(red_flag_id, response_data['data'][0]['id'])

    # def test_delete_red_flag_with_data_absent(self):

    #     red_flags.clear()
    #     input_data = {"red_flag_id": 12}
    #     red_flag_id = input_data['red_flag_id']
    #     response = self.app_tester.delete(
    #         '/api/v1/red-flags/{0}'.format(red_flag_id))
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(404, response_data['status'])
    #     self.assertEqual(f"No record  with ID:{red_flag_id} was found",
    #                      response_data['error'])
