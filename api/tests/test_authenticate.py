import unittest
from api.auth.authenticate import Authenticate
import json
from api import app


class TestAuthenticate(unittest.TestCase):

    def setUp(self):
        self.app_tester = app.test_client()

    def test_generate_token(self):
        token = Authenticate.generate_access_token(123, isAdmin=True )

        print("Token: {0}".format(token.split(".")))
        self.assertTrue(token.split(".")[0])
        self.assertTrue(token.split(".")[1])
        self.assertTrue(token.split(".")[2])

    def test_decode_token(self):
        token = Authenticate.generate_access_token(123, isAdmin=True )
        payload = Authenticate.decode_token(token)

        self.assertEqual(payload['user_id'], 123)
        self.assertEqual(payload['isAdmin'], True)

    # def test_retrieve_token_from_request(self):
    #     # request_header = jsonify({ "headers" : {
    #     #         # POST /api/v1/auth/signup? HTTP/1.1
    #     #         # Host: localhost:5000
    #     #         # Content-Type: application/json
    #     #         "Authorization": "Bearer 23423adasdc45gst"
    #     #         # cache-control: no-cache
        
    #     input_data =  input_data =  { 
    #                     "headers" : {
    #                         "Authorization" : "Bearer xde435rgklffnvcHDu67SdefGaPrf"
    #                     }
    #     }
 
    #     response = self.app_tester.put('/api/v1/red-flags', json=input_data)
    #     token = Authenticate.retrieve_token_from_request(response)
    #     # response_data = json.loads(response.data.decode())
    #     # token = Authenticate.retrieve_token_from_request(request_header)
    #     print("Token: {0}".format(token))
    #     self.assertEqual("xde435rgklffnvcHDu67SdefGaPrf", token)
        