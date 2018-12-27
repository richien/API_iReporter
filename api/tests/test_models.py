import unittest
from api.models.incident_model  import Incident
from api.models.user_model  import User
from datetime import date, datetime
import data
from api.models.validator import Validate


class TestIncidentModel(unittest.TestCase):

    def test_initialize_incident_without_id(self):
        kwargs = {  
            'createdBy' : "1020",
            'type' : "red-flag",
            'location' : "77.8334334, 65.09873",
            'status' : "draft",
            'images' : [],
            'videos' : ['vid_1.mp4'],
            'comment' : "bad road",
            'title' : 'really needs repair'
        }
        incident = Incident(**kwargs)
        self.assertIsInstance(incident, Incident)
        self.assertIn("vid_1.mp4", incident.videos)
        self.assertIs(type(incident.createdOn), date)

    def test_initialize_incident_with_id(self):
        kwargs = {
            'createdBy' : "1020",
            'type' : "red-flag",
            'location' : "77.8334334, 65.09873",
            'status' : "draft",
            'images' : [],
            'videos' : ['vid_1.mp4'],
            'comment' : "bad road",
            'title' : 'really needs repair'
        }
        incident = Incident(id=1, **kwargs)
        self.assertIsInstance(incident, Incident)
        self.assertEqual(1, incident.id)
        self.assertIs(type(incident.createdOn), date)

    def test_initialize_incident_with_date(self):
        kwargs = {
            'createdBy' : "1020",
            'createdOn' : datetime.strptime('20181212', '%Y%m%d').date(),
            'type' : "red-flag",
            'location' : "77.8334334, 65.09873",
            'status' : "draft",
            'images' : [],
            'videos' : ['vid_1.mp4'],
            'comment' : "bad road",
            'title' : 'really needs repair'
        }
        incident = Incident(id=1, **kwargs)
        self.assertIsInstance(incident, Incident)
        self.assertEqual(1, incident.id)
        self.assertIs(type(incident.createdOn), date)

    def test_to_dict_method_returns_dictionary(self):
        kwargs = {
            'createdOn' : "12-Dec-2018",
            'createdBy' : "1020",
            'type' : "red-flag",
            'location' : "77.8334334, 65.09873",
            'status' : "draft",
            'images' : [],
            'videos' : ['vid_1.mp4'],
            'comment' : "bad road",
            'title' : 'really needs repair'
        }
        incident = Incident(**kwargs)
        indent_dict = incident.to_dict()
        self.assertIs(type(incident.to_dict()), dict)
        self.assertEqual(incident.location, indent_dict['location'])
    
    def test_to_dict_method_returns_all_expected__keys(self):
        kwargs = {
            'createdBy' : "1020",
            'type' : "red-flag",
            'location' : "77.8334334, 65.09873",
            'status' : "draft",
            'images' : [],
            'videos' : ['vid_1.mp4'],
            'comment' : "bad road",
            'title' : 'really needs repair'
        }

        incident = Incident(**kwargs)
        expectedKeys = ['id', 'createdOn', 'createdBy', 'type', 'location', 'status', 'images', 'videos', 'comment','title']
        to_dictKeys = []
        for key in incident.to_dict().keys():
            to_dictKeys.append(key)
        self.assertEqual(to_dictKeys, expectedKeys)
    
    def test_create_incident(self):
        kwargs = {
            'createdBy' : "1020",
            'type' : "red-flag",
            'location' : "77.8334334, 65.09873",
            'status' : "draft",
            'images' : [],
            'videos' : ['vid_1.mp4'],
            'comment' : "bad road",
            'title' : 'really needs repair'
        }

        incident = Incident(**kwargs)
        self.assertTrue(incident.create_incident())
        self.assertEqual("red-flag", data.incidents_data['data'][1]['type'])


class TestUserModel(unittest.TestCase):

    def test_initialize_user(self):
        kwargs = {
            'firstname' : "James",
            'lastname' : "Blunt",
            'othernames' : "",
            'email' : "james@email.com",
            'phonenumber' : "778334334",
            'username' : "jamblu",
            'isAdmin' : True,
        }
        user = User(**kwargs)
        self.assertIsInstance(user, User)
        self.assertEqual("James", user.firstname)
        self.assertTrue(user.isAdmin)

    def test_create_user(self):
        kwargs = {
            'firstname' : "James",
            'lastname' : "Blunt",
            'othernames' : "",
            'email' : "james@email.com",
            'phonenumber' : "778334334",
            'username' : "jamblu",
            'isAdmin' : True,
        }
        user = User(**kwargs)
        self.assertTrue(user.create_user())
        self.assertEqual("James", data.incidents_data['users'][0]['firstname'])

    def test_user_has_id(self):
        kwargs = {
            'firstname' : "James",
            'lastname' : "Blunt",
            'othernames' : "",
            'email' : "james@email.com",
            'phonenumber' : "778334334",
            'username' : "jamblu",
            'isAdmin' : True,
        }
        user = User(**kwargs)
        user_id = user.id
        self.assertIs(type(user_id), int)
    
    def test_user_has_date_registered(self):
        kwargs = {
            'firstname' : "James",
            'lastname' : "Blunt",
            'othernames' : "",
            'email' : "james@email.com",
            'phonenumber' : "778334334",
            'username' : "jamblu",
            'isAdmin' : True,
        }
        user = User(**kwargs)
        user_id = user.id
        self.assertIs(type(user.registered), date)

    def test_to_dict_method_returns_dictionary(self):
        kwargs = {
            'firstname' : "James",
            'lastname' : "Blunt",
            'othernames' : "",
            'email' : "james@email.com",
            'phonenumber' : "778334334",
            'username' : "jamblu",
            'isAdmin' : True,
        }
        user = User(**kwargs)
        user_dict = user.to_dict()
        self.assertIs(type(user.to_dict()), dict)
        self.assertEqual(user.email, user_dict['email'])

    def test_to_dict_method_returns_all_expected__keys(self):
        expectedKeys = ['id', 'firstname', 'lastname', 'othernames', 'email', 'phonenumber', 'username', 'registered', 'isAdmin']
        kwargs = {
            'firstname' : "James",
            'lastname' : "Blunt",
            'othernames' : "",
            'email' : "james@email.com",
            'phonenumber' : "778334334",
            'username' : "jamblu",
            'isAdmin' : True,
        }
        user = User(**kwargs)
        to_dict_keys = []
        for key in user.to_dict().keys():
            to_dict_keys.append(key)
        self.assertEqual(to_dict_keys, expectedKeys)

    # def test_is_valid_email_format(self):
    #     email = "email@email.com"
    #     is_valid = Validate.is_valid_email_format(email)
    #     self.assertTrue(is_valid)