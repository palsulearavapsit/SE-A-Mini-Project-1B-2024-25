-- Initialize Database
CREATE DATABASE IF NOT EXISTS ev_station;
USE ev_station;

-- Drop existing tables if they exist to avoid conflicts
DROP TABLE IF EXISTS booking_bills;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS charging_sessions;
DROP TABLE IF EXISTS station_rates;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS states;
DROP TABLE IF EXISTS user_profiles;
DROP TABLE IF EXISTS users;

-- Core User Management
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active'
);

-- User Profiles with Membership Info
CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
     date_of_birth DATE,
    phone_number VARCHAR(20),
    country VARCHAR(100),
    city VARCHAR(100),
    full_name VARCHAR(100),
    email VARCHAR(100),
    is_member BOOLEAN DEFAULT FALSE,
    membership_start_date DATE,
    membership_end_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- States Table
CREATE TABLE states (
    state_id INT AUTO_INCREMENT PRIMARY KEY,
    state_name VARCHAR(255) NOT NULL UNIQUE
);

-- Stations Table with Enhanced Details
CREATE TABLE stations (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_id INT,
    charging_types VARCHAR(255) DEFAULT 'Type 2,CCS',
    total_chargers INT DEFAULT 4,
    available_chargers INT DEFAULT 4,
    amenities TEXT,
    operating_hours VARCHAR(100) DEFAULT '24/7',
    rating DECIMAL(3,1) DEFAULT 4.0,
    address TEXT,
    FOREIGN KEY (state_id) REFERENCES states(state_id) ON DELETE CASCADE
);

-- Bookings Table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    station_id INT NOT NULL,
    booking_date DATE NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE CASCADE
);

-- Bills Table
CREATE TABLE booking_bills (
    bill_id VARCHAR(50) PRIMARY KEY,
    booking_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    booking_date DATE NOT NULL,
    booking_time VARCHAR(20) NOT NULL,
    location VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    booking_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- Insert initial data
INSERT INTO users (username, password, status) VALUES 
('admin', 'admin', 'active'),
('test_user', 'test123', 'active');

INSERT INTO user_profiles (user_id, username, is_member) 
SELECT id, username, TRUE FROM users;

-- Insert states
INSERT INTO states (state_name) VALUES 
('Mumbai'),
('Pune'),
('Thane'),
('Nashik');

-- Insert stations with amenities
INSERT INTO stations (name, state_id, charging_types, total_chargers, available_chargers, amenities, operating_hours) VALUES
('EcoCharge Mumbai', 1, 'Type 1,CCS', 4, 4, 'Café,Waiting Area,WiFi', '24/7'),
('PowerHub Pune', 2, 'Type 2,CCS,CHAdeMO', 6, 6, 'Parking,WiFi,Restaurant', '24/7'),
('GreenStation Thane', 3, 'Type 2,CCS', 4, 4, 'Café,Restrooms,Shopping', '24/7'),
('VoltStop Nashik', 4, 'Type 2,CCS,CHAdeMO', 5, 5, 'Café,WiFi,Parking', '24/7'),
('ChargePro Mumbai', 1, 'Type 2,CCS', 4, 4, 'WiFi,Vending Machines', '24/7'),
('EVoasis Pune', 2, 'Type 2,CCS,CHAdeMO', 6, 6, 'Café,Lounge,WiFi', '24/7'),
('PowerZone Thane', 3, 'CCS,CHAdeMO', 4, 4, 'Restaurant,Parking,WiFi', '24/7'),
('ElectroHub Nashik', 4, 'Type 2,CCS', 5, 5, 'Café,Shopping,WiFi', '24/7');

-- Charging Types and Rates
CREATE TABLE IF NOT EXISTS charging_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL,
    max_power INT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS station_rates (
    rate_id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT,
    charging_type_id INT,
    rate_per_kwh DECIMAL(10, 2),
    FOREIGN KEY (station_id) REFERENCES stations(station_id),
    FOREIGN KEY (charging_type_id) REFERENCES charging_types(type_id)
);

-- Charging Sessions
CREATE TABLE IF NOT EXISTS charging_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    station_id INT,
    vehicle_name VARCHAR(100),
    charging_type VARCHAR(50),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    energy_delivered DECIMAL(10, 2),
    cost DECIMAL(10, 2),
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (station_id) REFERENCES stations(station_id)
);

-- Create admin user
INSERT INTO users (username, password, status) 
VALUES ('admin', 'admin', 'active')
ON DUPLICATE KEY UPDATE status = 'active';

-- Create indexes for better performance
CREATE INDEX idx_station_state ON stations(state_id);
CREATE INDEX idx_session_user ON charging_sessions(user_id);
CREATE INDEX idx_session_station ON charging_sessions(station_id);
CREATE INDEX idx_station_rates ON station_rates(station_id, charging_type_id);

-- Create view for station details
CREATE OR REPLACE VIEW station_details AS
SELECT 
    s.station_id,
    s.name,
    st.state_name,
    s.address,
    s.charging_types,
    s.total_chargers,
    s.available_chargers,
    s.operating_hours,
    s.amenities,
    GROUP_CONCAT(CONCAT(ct.type_name, ': ₹', sr.rate_per_kwh, '/kWh') SEPARATOR ', ') as rates
FROM 
    stations s
    JOIN states st ON s.state_id = st.state_id
    LEFT JOIN station_rates sr ON s.station_id = sr.station_id
    LEFT JOIN charging_types ct ON sr.charging_type_id = ct.type_id
GROUP BY 
    s.station_id;
    
-- Create bills table
CREATE TABLE IF NOT EXISTS bills ( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    bill_number VARCHAR(50) NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE stations 
ADD COLUMN ratings DECIMAL(3,1) DEFAULT 0.0,
ADD COLUMN addres VARCHAR(255),
ADD COLUMN operating_hour VARCHAR(100);

-- Update existing stations with some default values
UPDATE stations 
SET rating = 4.0,
    address = CONCAT('Address for ', name),
    operating_hours = '24/7';
    
    