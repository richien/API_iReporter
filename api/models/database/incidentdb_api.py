from api.models.database.connector import Connect


def create_incident(**incident):
    """
    Insert a new user into the users table.
    Return the user's autogenerated ID.
    """
    sql = """
        INSERT INTO incidents (
            createdby,
            type,
            location,
            status,
            comment,
            images,
            videos,
            title )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s, %s) RETURNING incident_id;
        """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql, (
            incident['createdby'],
            incident['type'],
            incident['location'],
            incident['status'],
            incident['comment'],
            incident['images'],
            incident['videos'],
            incident['title']
        ))
        incident_id = cur.fetchone()
        conn.commit()
        return incident_id
    except Exception as error:
        return error
    finally:
        conn.down()

def get_all_redflag_incidents():
    """
    Retrieve all redflags with most 
    recent records first.
    """
    sql = """
        SELECT *
        FROM incidents
        WHERE type = 'red-flag'
        ORDER BY createdOn DESC
    """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Exception as error:
        return error
    finally:
        conn.down()

def get_all_intervention_incidents():
    """
    Retrieve all intervention with most 
    recent records first.
    """
    sql = """
        SELECT *
        FROM incidents
        WHERE type = 'intervention'
        ORDER BY createdOn DESC
    """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Exception as error:
        return error
    finally:
        conn.down()

def get_incident_by_id(incident_id):
    """
    Retrieve an incident by ID
    """
    sql = f"""
        SELECT *
        FROM incidents
        WHERE incident_id = {incident_id}
    """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql)
        row = cur.fetchone()
        return row
    except Exception as error:
        return error
    finally:
        conn.down()

def update_location(incident_id, location=None):
    """
    Update an incident's location.
    """
    sql = f"""
        UPDATE incidents
        SET location='{location}'
        WHERE incident_id = {incident_id}
        RETURNING incident_id
    """    
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql)
        row = cur.fetchone()
        conn.commit()
        return row
    except Exception as error:
        return error
    finally:
        conn.down()

def update_comment(incident_id, comment=None):
    """
    Update an incident's comment.
    """
    sql = f"""
        UPDATE incidents
        SET comment='{comment}'
        WHERE incident_id = {incident_id}
        RETURNING incident_id
    """    
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql)
        row = cur.fetchone()
        conn.commit()
        return row
    except Exception as error:
        return error
    finally:
        conn.down()

def delete_user_by_type_and_user_id(type, user_id):
    """
    Delete a user by incident type and user ID.
    """
    sql_delete = f"""
        DELETE FROM users
        WHERE type = '{type}'
        AND user_id = {user_id}; 
    """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql_delete)
        conn.commit()
    except Exception as error:
        return error
    finally:
        conn.down()
    
def delete_incident_by_id(incident_id):
    """
    Delete incident by id.
    """
    sql_delete = f"""
        DELETE FROM incidents
        WHERE incident_id = {incident_id}; 
    """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql_delete)
        conn.commit()
    except Exception as error:
        return error
    finally:
        conn.down()

def delete_incidents_by_user(user_id):
    """
    Delete all incidents by a user.
    """
    sql_delete = f"""
        DELETE FROM incidents
        WHERE createdby = {user_id}; 
    """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql_delete)
        conn.commit()
    except Exception as error:
        return error
    finally:
        conn.down()
    
def delete_all_incidents():
    """
    Delete all incidents.
    """
    sql_delete = f"""
        DELETE FROM incidents; 
    """
    try:
        conn = Connect()
        cur = conn.up()
        cur.execute(sql_delete)
        conn.commit()
    except Exception as error:
        return error
    finally:
        conn.down()