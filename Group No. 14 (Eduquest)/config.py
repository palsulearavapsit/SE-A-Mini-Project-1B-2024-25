# config.py

# Application configuration settings

# Theme settings
DEFAULT_THEME = "dark"
DEFAULT_COLOR = "green"

# Application settings
APP_NAME = "EduQuest"
APP_VERSION = "1.2.0"
WINDOW_SIZE = "1400x900"

# News API settings - Replace with your actual API key if needed
NEWS_API_KEY = "4350e215f8284b6189cb79baf6d71cea"

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'eduquest',
    'password': 'password',
    'database': 'eduquest_db'
}

# API Keys
BREVO_API_KEY = "g2VdtNc8BAzTXpC7"  # Replace with your actual Brevo API key

# Email Configuration
EMAIL_SENDER = {
    'name': 'EduQuest Team',
    'email': 'eduquest12345@gmail.com'
}

# SMTP Configuration for fallback email mechanism
SMTP_CONFIG = {
    'server': 'smtp.gmail.com',     # Gmail SMTP server
    'port': 587,                    # Gmail TLS port
    'username': 'eduquest12345@gmail.com',  # Use the same email from EMAIL_SENDER
    'password': 'zwmg igfs tlqy cdkb'  # Your Gmail app password (not your regular password)
}

# Application Settings
DEBUG_MODE = False 