import unittest
from api.models.database import userdb_api
from api.models.user_model import User
from api import app


class TestUserDbApi(unittest.TestCase):

    def setUp(self):
        self.user_data = {
            "firstname": "Henry",
            "lastname": "Jones",
            "othernames": "",
            "email": "email@email.com",
            "phonenumber": "0775778887",
            "username": "henry",
            "password": "my_password",
            "isAdmin": False
        }
    def tearDown(self):
        userdb_api.delete_user_by_email(self.user_data['email'])

    def test_create_user_with_no_existing_user(self):
        user_id = userdb_api.create_user(**self.user_data)
        self.assertIs(type(user_id['user_id']), int) 
    
    def test_create_user_with_required_field_missing(self):
        self.user_data.popitem()
        userdb_api.create_user(**self.user_data)
        self.assertRaises(Exception)

    def test_check_username_or_email_exists_for_existing_user(self):
        userdb_api.create_user(**self.user_data)
        result = userdb_api.check_username_or_email_exists(
            self.user_data['username'], self.user_data['email'])
        self.assertIs(type(result), list) 

    

   

        
        
        