import random
from datetime import date
import re
from api.models.database import userdb_api


class User:
    def __init__(self, user_id=None, registered=None, **kwargs):

        self.id = user_id 
        self.registered = registered
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.othernames = kwargs['othernames']
        self.email = kwargs['email']
        self.phonenumber = kwargs['phonenumber']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.isAdmin = kwargs['isAdmin']

    def to_dict(self):

        user_dict = {
            # 'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'othernames': self.othernames,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'username': self.username,
            'password': self.password,
            # 'registered': self.registered,
            'isAdmin': self.isAdmin
        }
        return user_dict

    def to_dict_minimal(self):

        user_dict = {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'othernames': self.othernames,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'username': self.username,
            'registered': self.registered,
            'isAdmin': self.isAdmin
        }
        return user_dict

    def create_user(self):
        result = userdb_api.create_user(**self.to_dict())
        return result

    def check_user_exists(self):
        result = userdb_api.check_username_or_email_exists(self.username, self.email)
        if result:
            if result[0]['username'] and result[0]['email']:
                message = {
                    "exists": True,
                    "error": "A user with that account already exists"
                }
            elif result[0]['username']:
                message = {
                    "exists": True,
                    "error": "A user with that username already exists"
                }
            elif result[0]['email']:
                message = {
                    "exists": True,
                    "error": "A user with that email address already exists"
                }
        else:
            message = {
                "exists": False,
            }
        return message

    @staticmethod
    def is_valid_password(pwd):

        is_valid = True
        if len(pwd) < 8:
            is_valid = False

        return is_valid
