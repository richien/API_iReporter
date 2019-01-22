from api.models.database.connector import Connect


def create_tables():
    """
    Creates tables in the PostgreSQL database
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            firstname VARCHAR(50) NOT NULL, 
            lastname VARCHAR(50) NOT NULL,
            othernames VARCHAR(50), 
            email VARCHAR(50) NOT NULL,
            phonenumber VARCHAR(20), 
            username VARCHAR(20) NOT NULL,
            password TEXT NOT NULL,
            registered DATE NOT NULL DEFAULT CURRENT_DATE,
            isAdmin BOOLEAN NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id SERIAL PRIMARY KEY,
            createdOn DATE NOT NULL DEFAULT CURRENT_DATE,
            createdBy INTEGER NOT NULL, 
            type VARCHAR(15) NOT NULL, 
            location VARCHAR(20),
            status VARCHAR(30) NOT NULL,
            comment TEXT NOT NULL,
            images TEXT [], 
            videos TEXT [],
            title TEXT NOT NULL,
            FOREIGN KEY (createdBy)
            REFERENCES users (user_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )
    try:
        conn = Connect()
        cur = conn.up()
        counter = 0
        for command in commands:
            cur.execute(command)
            counter += 1
        cur.close()
        conn.commit()
        print(f"{counter} Table(s) Created")
    except Exception as error:
        print(error) 
    finally:
        conn.down()
        print("Database Connection closed")

if __name__ == '__main__':
    create_tables()