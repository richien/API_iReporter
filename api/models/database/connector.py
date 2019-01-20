from config import config
import psycopg2


class Connect():

    def __init__(self):
        self.cursor = None
        self.connect = None

    def up(self):
        """
        Connect to the PostgreSQL database server
        and return a Cursor object.
        """
        try:
            params = config()
            self.connect = psycopg2.connect(**params)
            self.cursor = self.connect.cursor()
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