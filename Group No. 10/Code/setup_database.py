import mysql.connector

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'M@nas1601'  # Change to your MySQL password
}

def setup_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartspend")
        print("Database created successfully!")
        
        # Switch to the smartspend database
        cursor.execute("USE smartspend")
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            currency VARCHAR(10) DEFAULT 'USD',
            auth_code VARCHAR(10)
        )
        ''')
        print("Users table created successfully!")
        
        # Create categories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(50) NOT NULL,
            color VARCHAR(20) DEFAULT '#3498db',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        print("Categories table created successfully!")
        
        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            type VARCHAR(20) NOT NULL,
            category_id INT,
            description TEXT,
            date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        ''')
        print("Transactions table created successfully!")
        
        conn.commit()
        conn.close()
        print("Database setup completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    setup_database()