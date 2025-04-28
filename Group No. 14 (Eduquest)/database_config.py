# MySQL Database Configuration
# Update these settings with your MySQL server credentials
# If you're using XAMPP, the default username is 'root' with no password
# For security in production, use a dedicated user with a strong password

DB_CONFIG = {
    'host': 'localhost',      # Usually 'localhost' or '127.0.0.1'
    'user': 'root',           # Replace with your MySQL username
    'password': 'aetherAlb071@',       # Replace with your MySQL password (updated from empty)
    'database': 'eduquest',   # Database name (will be created if it doesn't exist)
    'raise_on_warnings': True
}

# Note: If you encounter connection errors:
# 1. Make sure MySQL service is running
# 2. Verify your username and password are correct
# 3. Check that you have sufficient privileges to create databases 