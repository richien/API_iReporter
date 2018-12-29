import random
from datetime import date
import data
import re


class User:
    def __init__(self, **kwargs):
        self.id = random.randint(1000, 9000)    
        self.firstname = kwargs['firstname']
        self.lastname = kwargs['lastname']
        self.othernames = kwargs['othernames'] 
        self.email = kwargs['email']
        self.phonenumber = kwargs['phonenumber']
        self.username = kwargs['username']
        self.registered = date.today()
        self.isAdmin = kwargs['isAdmin']
    
    def to_dict(self):
        user_dict = {
            'id' : self.id,
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'othernames' : self.othernames,
            'email' : self.email,
            'phonenumber' : self.phonenumber,
            'username' : self.username,
            'registered' : self.registered,
            'isAdmin' : self.isAdmin
        }
        return user_dict

    def create_user(self):
        return data.do_create(self, self.to_dict())

    def check_user_exists(self):
        username = data.check_username(self.username)
        email = data.check_email(self.email)
        print("Username: {0}, email: {1}".format(username, email))

        if username and email:
                message = {
                    "exists" : True,
                    "error" : "A user with that account already exists"
                    }
        elif username :
            message = {
                    "exists" : True,
                    "error" : "A user with that username already exists"
                }
        elif email :
            message = {
                    "exists" : True,
                    "error" : "A user with that email address already exists"
                }
        else:
            message = {
                    "exists" : False,
                }
 
        return message
    
    
    


    
