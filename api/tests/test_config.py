import unittest
from config import config


class TestConfigFile(unittest.TestCase):
    
    def test_read_configs_from_existing_ini_file(self):
        db = config()
        self.assertIs(type(db), dict)
        self.assertIn('database', db.keys())
    
    def test_read_configs_from_non_existing_ini_file(self):
        self.assertRaises(Exception,
            config(filename='db.ini'),
            "Section postgresql not found in db.ini")
        
        