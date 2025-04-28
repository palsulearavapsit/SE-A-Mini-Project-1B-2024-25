import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aayush@0909",
            database="findr",
            auth_plugin='mysql_native_password'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None