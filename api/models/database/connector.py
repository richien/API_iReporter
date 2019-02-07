from urllib.parse import urlparse
import psycopg2
import psycopg2.extras
from api import app

uri = app.config['HEROKU_DATABASE_URI']

class Connect():

    def __init__(self):
        self.cursor = None
        self.connect = None
        self.dsn = None

    def up(self):
        """
        Connect to the PostgreSQL database server
        and return a Cursor object.
        """
        try:
            self.attributes
            params = self.attributes()
            self.connect = psycopg2.connect(**params)
            self.cursor = self.connect.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            return self.cursor
        except (Exception, psycopg2.DatabaseError) as error:
            return error.message
    
    def down(self):
        """
        Closes the cursor and connection to the 
        PostgreSQL database server.
        """
        if self.connect is not None:
            self.cursor.close()
            self.connect.close()
    
    def commit(self):
        self.connect.commit()


    def attributes(self):
        result = urlparse(uri)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        
        dsn = {
            'user': username,'password': password,
            'dbname': database,'host': hostname
        }
        return dsn

 
