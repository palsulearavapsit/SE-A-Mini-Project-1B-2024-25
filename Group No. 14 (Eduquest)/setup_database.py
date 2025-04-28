import mysql.connector
from mysql.connector import Error
from database_config import DB_CONFIG
import sys

def setup_database():
    """
    Set up the MySQL database and tables for EduQuest
    """
    conn = None
    try:
        # First try to connect directly to the database
        try:
            print("Connecting to MySQL database...")
            conn = mysql.connector.connect(**DB_CONFIG)
            print(f"Connected to '{DB_CONFIG['database']}' database successfully.")
        except Error as db_connect_error:
            if "Unknown database" in str(db_connect_error):
                # Connect without database and create it
                conn_params = {**DB_CONFIG}
                conn_params.pop('database', None)
                
                print("Database doesn't exist. Connecting to MySQL server...")
                conn = mysql.connector.connect(**conn_params)
                cursor = conn.cursor()
                
                db_name = DB_CONFIG['database']
                print(f"Creating database '{db_name}'...")
                cursor.execute(f"CREATE DATABASE {db_name}")
                
                print(f"Switching to database '{db_name}'...")
                cursor.execute(f"USE {db_name}")
            else:
                raise db_connect_error
                
        cursor = conn.cursor()
        
        # Create tables
        print("Creating tables if they don't exist...")
        
        # We'll use try/except for each table creation to handle any errors
        try:
            # Users table
            print("Creating users table...")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                created_at DATETIME NOT NULL,
                last_login DATETIME
            )
            """)
        except Error as e:
            print(f"Note: {e}")
            
        try:
            # Password reset tokens table
            print("Creating password_reset_tokens table...")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                token VARCHAR(100) NOT NULL,
                created_at DATETIME NOT NULL,
                expires_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """)
        except Error as e:
            print(f"Note: {e}")
        
        try:
            # Verification codes table
            print("Creating verification_codes table...")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                code VARCHAR(10) NOT NULL,
                created_at DATETIME NOT NULL,
                expires_at DATETIME NOT NULL
            )
            """)
        except Error as e:
            print(f"Note: {e}")
        
        try:
            # User sessions table
            print("Creating user_sessions table...")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                session_token VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL,
                expires_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """)
        except Error as e:
            print(f"Note: {e}")
        
        # Commit changes
        conn.commit()
        print("Database setup completed successfully!")
        
    except Error as e:
        print(f"Error setting up database: {e}")
        print("\nDatabase setup guide:")
        print("1. Make sure MySQL server is installed and running")
        print("2. Check your credentials in database_config.py")
        print("3. For XAMPP users: Start MySQL from the XAMPP control panel")
        print("4. For MySQL Server users: Ensure the service is running")
        print("\nDefault MySQL credentials:")
        print("- XAMPP: username 'root' with empty password")
        print("- MySQL Server: username 'root' with password set during installation")
        sys.exit(1)
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    setup_database() 