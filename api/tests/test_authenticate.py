import unittest
from api.auth.authenticate import Authenticate
import json
from api import app


class TestAuthenticate(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client()

    def test_generate_token(self):
        token = Authenticate.generate_access_token(123, isAdmin=True)

        print("Token: {0}".format(token.split(".")))
        self.assertTrue(token.split(".")[0])
        self.assertTrue(token.split(".")[1])
        self.assertTrue(token.split(".")[2])

    def test_decode_token(self):
        token = Authenticate.generate_access_token(123, isAdmin=True)
        payload = Authenticate.decode_token(token)

        self.assertEqual(payload['user_id'], 123)
        self.assertEqual(payload['isAdmin'], True)
