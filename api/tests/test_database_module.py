import unittest
from api.models.database.connector import Connect


class TestConnector(unittest.TestCase):

    def test_setup_connection_to_database(self):
        conn = Connect()
        cur = conn.up()
        self.assertFalse(cur.closed)
        self.assertFalse(cur.connection.closed)
    
    def test_teardown_connection_to_database(self):
        conn = Connect()
        cur = conn.up()
        conn.down()
        self.assertTrue(cur.closed)
        self.assertTrue(cur.connection.closed)