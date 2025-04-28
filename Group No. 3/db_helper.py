from config import get_db_connection

def execute_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    connection.commit()
    cursor.close()
    connection.close()

def fetch_all(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def fetch_one(query, params=None):
    """Fetch a single record from the database."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    result = cursor.fetchone()
    cursor.close()
    connection.close()
    
    return result

