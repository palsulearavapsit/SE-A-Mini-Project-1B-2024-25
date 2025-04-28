import re
from datetime import datetime

def validate_email(email):
    """
    Validates the format of an email address.
    :param email: The email address to validate.
    :return: True if valid, False otherwise.
    """
    if not email:
        return False
    
    # More comprehensive email regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def validate_mobile_number(mobile_number):
    """
    Validates the format of a mobile number.
    Assumes a 10-digit number for simplicity.
    :param mobile_number: The mobile number to validate.
    :return: True if valid, False otherwise.
    """
    if not mobile_number:
        return False
    
    # Strip any spaces or special characters for a more flexible check
    stripped_number = re.sub(r'[\s\-\(\)\+]', '', mobile_number)  
    mobile_regex = r'^\d{10}$'
    return re.match(mobile_regex, stripped_number) is not None


def validate_date(date_str, date_format="%Y-%m-%d"):
    """
    Validates the format of a date string.
    :param date_str: The date string to validate.
    :param date_format: The expected date format (default is YYYY-MM-DD).
    :return: True if valid, False otherwise.
    """
    if not date_str:
        return False
        
    try:
        date_obj = datetime.strptime(date_str, date_format)
        
        # Optional: Check if date is reasonable (e.g., not in distant past/future)
        today = datetime.now()
        hundred_years_ago = today.replace(year=today.year - 100)
        hundred_years_future = today.replace(year=today.year + 100)
        
        return hundred_years_ago <= date_obj <= hundred_years_future
    except ValueError:
        return False


def calculate_days_between_dates(start_date, end_date, date_format="%Y-%m-%d"):
    """
    Calculates the number of days between two dates.
    :param start_date: The start date as a string.
    :param end_date: The end date as a string.
    :param date_format: The date format (default is YYYY-MM-DD).
    :return: Number of days between the two dates, or None if dates are invalid.
    """
    if not start_date or not end_date:
        return None
        
    try:
        start = datetime.strptime(start_date, date_format)
        end = datetime.strptime(end_date, date_format)
        
        # Ensure end date is not before start date
        if end < start:
            return None
            
        delta = end - start
        return delta.days
    except ValueError:
        return None


def generate_unique_id(prefix="ID"):
    """
    Generates a unique ID based on the current timestamp and a random component.
    :param prefix: A prefix to prepend to the ID (optional).
    :return: A unique ID string.
    """
    import random
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices('0123456789ABCDEF', k=6))
    return f"{prefix}_{timestamp}_{random_suffix}"


def validate_password(password, confirm_password, min_length=8):
    """
    Validates that the password meets requirements and matches confirmation.
    :param password: The password entered by the user.
    :param confirm_password: The confirmation password entered by the user.
    :param min_length: Minimum required password length (default: 8).
    :return: Tuple of (is_valid, error_message).
    """
    if not password or not confirm_password:
        return False, "Password and confirmation are required."
        
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long."
    
    # Optional: Add more password strength requirements
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numeric characters."
        
    if password != confirm_password:
        return False, "Passwords do not match."
        
    return True, None


def validate_required_fields(fields):
    """
    Validates that all required fields are filled.
    :param fields: A dictionary of field names and their values.
    :return: Tuple of (is_valid, error_message).
    """
    if not fields:
        return False, "No fields provided for validation."
        
    for field_name, value in fields.items():
        # Check for None, empty string, or just whitespace
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return False, f"{field_name} is required."
    
    return True, None


def sanitize_input(input_text, allow_html=False):
    """
    Sanitizes user input to prevent SQL injection and XSS attacks.
    :param input_text: The input text to sanitize.
    :param allow_html: Whether to allow HTML tags (default: False).
    :return: Sanitized text.
    """
    if not input_text:
        return ""
        
    # Convert to string if not already
    if not isinstance(input_text, str):
        input_text = str(input_text)
    
    # Remove potentially dangerous SQL characters
    sql_chars = [';', '--', '/*', '*/', 'xp_', "'", '"']
    sanitized = input_text
    
    for char in sql_chars:
        sanitized = sanitized.replace(char, '')
    
    # If HTML isn't allowed, remove all tags
    if not allow_html:
        sanitized = re.sub(r'<[^>]*>', '', sanitized)
    
    return sanitized.strip()