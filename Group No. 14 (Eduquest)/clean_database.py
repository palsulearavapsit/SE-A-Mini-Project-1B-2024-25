import mysql.connector
from mysql.connector import Error
from database_config import DB_CONFIG
import sys

def clean_and_setup_database():
    """
    Clean the database by dropping all tables and create new ones for login and registration
    """
    conn = None
    try:
        # Connect to the database
        print("Connecting to MySQL database...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Switch to the eduquest database
        db_name = DB_CONFIG['database']
        print(f"Using database '{db_name}'...")
        cursor.execute(f"USE {db_name}")
        
        # Get all table names
        print("Retrieving existing tables...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # Drop all existing tables
        print("Dropping all existing tables...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            table_name = table[0]
            print(f"Dropping table: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Create new tables for login and registration only
        print("Creating new tables for login and registration...")
        
        # Users table
        print("Creating users table...")
        cursor.execute("""
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME
        ) ENGINE=InnoDB;
        """)
        
        # Password reset tokens table
        print("Creating password_reset_tokens table...")
        cursor.execute("""
        CREATE TABLE password_reset_tokens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(100) NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)
        
        # Verification codes table
        print("Creating verification_codes table...")
        cursor.execute("""
        CREATE TABLE verification_codes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(100) NOT NULL,
            code VARCHAR(10) NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME NOT NULL
        ) ENGINE=InnoDB;
        """)
        
        # Commit changes
        conn.commit()
        print("Database cleanup and setup completed successfully!")
        
    except Error as e:
        print(f"Error: {e}")
        print("\nDatabase setup guide:")
        print("1. Make sure MySQL server is installed and running")
        print("2. Check your credentials in database_config.py")
        print("3. For XAMPP users: Start MySQL from the XAMPP control panel")
        print("4. For MySQL Server users: Ensure the service is running")
        sys.exit(1)
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    print("WARNING: This will delete ALL tables in the eduquest database.")
    clean_and_setup_database() 