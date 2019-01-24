import unittest
from api.validator import Validate
from api import app


class TestValidate(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client()

    def test_validate_incident_post_request_with_valid_request_data(self):

        request_data = {
            "createdby": 5000,
            "type": "red-flag",
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "images": [
                "image_1.png",
                "image_2.jpg"],
            "videos": ["vid_1.mp4"],
            "comment": "I almost got runover by a car that was dodging potholes!",
            "title": "Roads in poor condition"}
        is_valid = Validate.validate_incident_post_request(request_data)
        self.assertTrue(is_valid['is_valid'])
        self.assertIs(type(is_valid), dict)

    def test_validate_incident_post_request_with_invalid_request_data(self):

        request_data = {
            "type": "red-flag",
            "location": "33.92300, 44.9084551",
            "status": "draft",
            "images": [
                "image_1.png",
                "image_2.jpg"],
            "videos": ["vid_1.mp4"],
            "comment": "I almost got runover by a car that was dodging potholes!",
            "title": "Roads in poor condition"}
        is_valid = Validate.validate_incident_post_request(request_data)
        self.assertFalse(is_valid['is_valid'])
        self.assertEqual(400, is_valid['message']['status'])
        self.assertIn(
            "Invalid request body - error in request body",
            is_valid['message']['error'])

    def test_validate_signin_details_with_username_and_valid_request_data(
            self):

        request_data = {
            "username": "peter",
            "password": "my_password"
        }
        is_valid = Validate.validate_signin_request(request_data)
        self.assertTrue(is_valid['is_valid'])
        self.assertIs(type(is_valid), dict)

    def test_validate_signin_details_with_username_and_invalid_request_data(
            self):

        request_data = {
            "user": "peter",
            "password": "my_password"
        }
        is_valid = Validate.validate_signin_request(request_data)
        self.assertFalse(is_valid['is_valid'])
        self.assertEqual(400, is_valid['message']['status'])
        self.assertIn(
            "Invalid request body - error in request body",
            is_valid['message']['error'])

    def test_validate_signin_details_with_email_and_valid_request_data(self):

        request_data = {
            "email": "peter",
            "password": "my_password"
        }
        is_valid = Validate.validate_signin_request(request_data)
        self.assertTrue(is_valid['is_valid'])
        self.assertIs(type(is_valid), dict)

    def test_validate_signin_details_without_password_in_request_data(self):

        request_data = {
            "username": "peter",
        }
        is_valid = Validate.validate_signin_request(request_data)
        self.assertFalse(is_valid['is_valid'])
        self.assertEqual(400, is_valid['message']['status'])
        self.assertIn(
            "error in request body, missing required field 'password",
            is_valid['message']['error'])

    def test_validate_signup_details_with_valid_request_data(self):

        request_data = {
            "firstname": "Peter",
            "lastname": "Jones",
            "othernames": "Henry",
            "email": "pete@email.com",
            "phonenumber": "0773287332",
            "username": "petter",
            "password": "my_password",
            "isAdmin": True
        }
        is_valid = Validate.validate_signup_details(request_data)
        self.assertTrue(is_valid['is_valid'])
        self.assertIs(type(is_valid), dict)

    def test_validate_signup_details_with_invalid_request_data(self):

        request_data = {
            "firstname": "Peter",
            "lastname": "Jones",
            "othernames": "Henry",
            "phonenumber": "0773287332",
            "username": "petter",
            "password": "my_password",
            "isAdmin": True
        }
        is_valid = Validate.validate_signup_details(request_data)
        self.assertFalse(is_valid['is_valid'])
        self.assertEqual(400, is_valid['message']['status'])
        self.assertIn(
            "Invalid request body - error in request body",
            is_valid['message']['error'])

    def test_validate_signup_details_with_invalid_password_in_request_data(
            self):

        request_data = {
            "firstname": "Peter",
            "lastname": "Jones",
            "othernames": "Simon",
            "email": "pete@email.com",
            "phonenumber": "0773287332",
            "username": "petter",
            "password": "passwd",
            "isAdmin": True
        }
        is_valid = Validate.validate_signup_details(request_data)
        self.assertFalse(is_valid['is_valid'])
        self.assertEqual(400, is_valid['message']['status'])
        self.assertIn(
            "Password cannot be less than 8 characters",
            is_valid['message']['error'])

    def test_validate_signup_details_with_valid_request_data_and_without_othernames_field(
            self):

        request_data = {
            "firstname": "Peter",
            "lastname": "Jones",
            "email": "pete@email.com",
            "phonenumber": "0773287332",
            "username": "petter",
            "password": "my_password",
            "isAdmin": True
        }
        is_valid = Validate.validate_signup_details(request_data)
        self.assertTrue(is_valid['is_valid'])
        self.assertIs(type(is_valid), dict)
        self.assertEqual(is_valid['request']['othernames'], "")

    def test_validate_signup_details_with_valid_request_data_and_without_phonenumber_field(
            self):

        request_data = {
            "firstname": "Peter",
            "lastname": "Jones",
            "email": "pete@email.com",
            "username": "petter",
            "password": "my_password",
            "isAdmin": True
        }
        is_valid = Validate.validate_signup_details(request_data)
        self.assertTrue(is_valid['is_valid'])
        self.assertIs(type(is_valid), dict)
        self.assertEqual(is_valid['request']['phonenumber'], "")

    def test_validate_signup_details_with_valid_request_data_and_without_isAdmin_field(
            self):

        request_data = {
            "firstname": "Peter",
            "lastname": "Jones",
            "email": "pete@email.com",
            "phonenumber": "0773287332",
            "username": "petter",
            "password": "my_password"
        }
        is_valid = Validate.validate_signup_details(request_data)
        self.assertTrue(is_valid['is_valid'])
        self.assertIs(type(is_valid), dict)
        self.assertEqual(is_valid['request']['isAdmin'], False)
