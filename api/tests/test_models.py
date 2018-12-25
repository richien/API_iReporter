import unittest
from api.models.incident_model  import Incident
from datetime import date, datetime


class TestIncident(unittest.TestCase):

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
        expectedKeys = ['id', 'createdOn', 'createdBy', 'type', 'location', 'status', 'images', 'videos', 'comment','title']
        to_dictKeys = []
        for key in incident.to_dict().keys():
            to_dictKeys.append(key)
        self.assertEqual(to_dictKeys, expectedKeys)