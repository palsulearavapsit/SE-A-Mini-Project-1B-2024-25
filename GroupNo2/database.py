import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="arav",
            database="rent_and_ride"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def initialize_database():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    security_question VARCHAR(255),
                    security_answer VARCHAR(255),
                    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
                )
            """)

            # Create customers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    father_name VARCHAR(100),
                    gender ENUM('Male', 'Female') NOT NULL,
                    pincode VARCHAR(10),
                    mobile_number VARCHAR(15) UNIQUE NOT NULL,
                    email VARCHAR(100),
                    nationality VARCHAR(50),
                    id_proof_type ENUM('Aadhar', 'PAN', 'License', 'Address'),
                    id_proof_number VARCHAR(50)
                )
            """)

            # Create vehicles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    model VARCHAR(100) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    type ENUM('SUV', 'Sedan', 'Hatchback', 'Bike') NOT NULL,
                    luggage_capacity INT,
                    fuel_type ENUM('Petrol', 'Diesel', 'Electric') NOT NULL,
                    price_per_day DECIMAL(10, 2),
                    vehicle_number VARCHAR(20) UNIQUE NOT NULL
                )
            """)

            # Create bookings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT,
                    vehicle_id INT,
                    check_in_date DATE,
                    check_out_date DATE,
                    total_cost DECIMAL(10, 2),
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
                )
            """)

            # Create feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_name VARCHAR(100),
                    mobile_number VARCHAR(15),
                    review TEXT,
                    rating INT CHECK (rating BETWEEN 1 AND 5)
                )
            """)
            connection.commit()
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()