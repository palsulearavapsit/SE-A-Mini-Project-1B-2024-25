import mysql.connector
from mysql.connector import Error
from database_config import DB_CONFIG
import hashlib
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            print("MySQL Database connection successful")
            # Initialize the user_progress table if it doesn't exist
            self.initialize_user_progress_table()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
    def execute_query(self, query, params=None):
        """Execute a query that modifies data (INSERT, UPDATE, DELETE)"""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return False
        finally:
            cursor.close()
    
    def execute_read_query(self, query, params=None):
        """Execute a query that reads data (SELECT)"""
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error executing read query: {e}")
            return None
        finally:
            cursor.close()
    
    def close_connection(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
    
    # User authentication methods
    def register_user(self, username, email, password, full_name=None):
        """
        Register a new user
        
        Args:
            username (str): The username for the new account
            email (str): The email address for the new account
            password (str): The password for the new account
            full_name (str, optional): The user's full name
            
        Returns:
            bool: True if registration is successful, False otherwise
        """
        try:
            # Check if username already exists
            query = "SELECT id FROM users WHERE username = %s"
            result = self.execute_read_query(query, (username,))
            if result:
                print(f"Username {username} already exists")
                return False
                
            # Check if email already exists
            query = "SELECT id FROM users WHERE email = %s"
            result = self.execute_read_query(query, (email,))
            if result:
                print(f"Email {email} already exists")
                return False
                
            # Hash the password for security
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
            # Insert new user
            query = """
                INSERT INTO users (username, email, password, full_name, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            # Store the hashed password instead of plaintext
            self.execute_query(query, (username, email, hashed_password, full_name))
            return True
            
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def authenticate_user(self, username, password):
        """
        Authenticate a user with username and password
        
        Args:
            username (str): The username to authenticate
            password (str): The plaintext password to verify
            
        Returns:
            dict: User data if authentication is successful, None otherwise
        """
        try:
            # Find user by username
            query = "SELECT * FROM users WHERE username = %s"
            user = self.execute_read_query(query, (username,))
            
            if not user:
                print(f"User {username} not found")
                return None
                
            user = user[0]  # Get the first (and should be only) user
            
            # Hash the provided password and compare with stored hash
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            if user['password'] == hashed_password:
                # Update last login timestamp
                update_query = "UPDATE users SET last_login = NOW() WHERE id = %s"
                self.execute_query(update_query, (user['id'],))
                
                # Return user data without the password
                user_data = {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user.get('full_name', '')  # Use get with default empty string
                }
                return user_data
            else:
                print("Password does not match")
                return None
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def update_password(self, username, new_password):
        """Update user password"""
        query = "UPDATE users SET password = %s WHERE username = %s"
        params = (new_password, username)
        success = self.execute_query(query, params)
        
        if success:
            return True, "Password updated successfully"
        else:
            return False, "Password update failed"
    
    def get_user_by_email(self, email):
        """Get user by email"""
        query = "SELECT id, username, email FROM users WHERE email = %s"
        params = (email,)
        result = self.execute_read_query(query, params)
        
        if result and len(result) > 0:
            return result[0]
        else:
            return None
            
    def create_password_reset_token(self, user_id):
        """Create a password reset token for a user"""
        # Generate a random token
        token = hashlib.sha256(f"{user_id}{datetime.now().timestamp()}".encode()).hexdigest()[:32]
        
        # Set expiration time (24 hours from now)
        expires_at = datetime.now() + timedelta(hours=24)
        
        # Delete any existing tokens for this user
        self.execute_query("DELETE FROM password_reset_tokens WHERE user_id = %s", (user_id,))
        
        # Insert new token
        query = """
            INSERT INTO password_reset_tokens (user_id, token, created_at, expires_at)
            VALUES (%s, %s, NOW(), %s)
        """
        success = self.execute_query(query, (user_id, token, expires_at))
        
        if success:
            return token
        else:
            return None
            
    def verify_reset_token(self, token):
        """Verify a password reset token"""
        query = """
            SELECT user_id FROM password_reset_tokens 
            WHERE token = %s AND expires_at > NOW()
        """
        result = self.execute_read_query(query, (token,))
        
        if result and len(result) > 0:
            return result[0]['user_id']
        else:
            return None
            
    def create_verification_code(self, email):
        """Create a verification code for email verification"""
        # Generate a 6-digit code
        import random
        code = ''.join(random.choices('0123456789', k=6))
        
        # Set expiration time (15 minutes from now)
        expires_at = datetime.now() + timedelta(minutes=15)
        
        # Delete any existing codes for this email
        self.execute_query("DELETE FROM verification_codes WHERE email = %s", (email,))
        
        # Insert new code
        query = """
            INSERT INTO verification_codes (email, code, created_at, expires_at)
            VALUES (%s, %s, NOW(), %s)
        """
        success = self.execute_query(query, (email, code, expires_at))
        
        if success:
            return code
        else:
            return None
            
    def verify_email_code(self, email, code):
        """Verify an email verification code"""
        query = """
            SELECT id FROM verification_codes 
            WHERE email = %s AND code = %s AND expires_at > NOW()
        """
        result = self.execute_read_query(query, (email, code))
        
        if result and len(result) > 0:
            # Delete the code after successful verification
            self.execute_query("DELETE FROM verification_codes WHERE email = %s", (email,))
            return True
        else:
            return False
    
    def initialize_user_progress_table(self):
        """Create the user_progress table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_progress (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            score DECIMAL(5,2) NOT NULL,
            total_marks INT NOT NULL,
            max_marks INT NOT NULL,
            correct_answers INT NOT NULL,
            incorrect_answers INT NOT NULL,
            not_attempted INT NOT NULL,
            time_spent INT NOT NULL,
            physics_marks INT,
            chemistry_marks INT,
            mathematics_marks INT,
            physics_percentage DECIMAL(5,2),
            chemistry_percentage DECIMAL(5,2),
            mathematics_percentage DECIMAL(5,2),
            physics_score DECIMAL(5,2),
            chemistry_score DECIMAL(5,2),
            mathematics_score DECIMAL(5,2),
            completed BOOLEAN DEFAULT TRUE,
            date_taken DATETIME NOT NULL
        )
        """
        self.execute_query(create_table_query)
        
        # Initialize questions table if it doesn't exist
        self.initialize_questions_table()
        
    def initialize_questions_table(self):
        """Create questions table if it doesn't exist"""
        create_questions_table = """
        CREATE TABLE IF NOT EXISTS questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer CHAR(1) NOT NULL,
            subject VARCHAR(50) NOT NULL,
            topic VARCHAR(100),
            difficulty VARCHAR(20) DEFAULT 'Medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.execute_query(create_questions_table)
        
        # Check if there are any questions in the table
        check_questions = "SELECT COUNT(*) as count FROM questions"
        result = self.execute_read_query(check_questions)
        
        # If no questions exist, add sample questions
        if result and result[0]['count'] == 0:
            print("No questions found in database. Adding sample questions...")
            self.add_sample_questions()
    
    def add_sample_questions(self):
        """Add sample questions to the database"""
        sample_questions = [
            # Physics Questions
            {
                "question_text": "A particle moves in a straight line with constant acceleration. If its initial velocity is 5 m/s and after 2 seconds its velocity becomes 15 m/s, what is its acceleration?",
                "option_a": "3 m/s²",
                "option_b": "5 m/s²",
                "option_c": "7 m/s²",
                "option_d": "10 m/s²",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Kinematics",
                "difficulty": "Easy"
            },
            {
                "question_text": "A body of mass 2 kg is thrown upwards with a velocity of 20 m/s. If g = 10 m/s², what is the potential energy of the body at the highest point?",
                "option_a": "200 J",
                "option_b": "400 J",
                "option_c": "600 J",
                "option_d": "800 J",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Energy",
                "difficulty": "Medium"
            },
            {
                "question_text": "What is the equivalent resistance when two resistors of 2Ω and 3Ω are connected in parallel?",
                "option_a": "1.2Ω",
                "option_b": "2.5Ω",
                "option_c": "5Ω",
                "option_d": "6Ω",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Electricity",
                "difficulty": "Medium"
            },
            
            # Chemistry Questions
            {
                "question_text": "Which of the following elements has the highest electronegativity?",
                "option_a": "Oxygen",
                "option_b": "Nitrogen",
                "option_c": "Fluorine",
                "option_d": "Chlorine",
                "correct_answer": "C",
                "subject": "Chemistry",
                "topic": "Periodic Properties",
                "difficulty": "Easy"
            },
            {
                "question_text": "What is the IUPAC name of CH₃-CH=CH-CHO?",
                "option_a": "1-Butanal",
                "option_b": "But-2-enal",
                "option_c": "But-3-enal",
                "option_d": "2-Butenal",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The pH of a 0.01M HCl solution is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "3",
                "option_d": "4",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Acids and Bases",
                "difficulty": "Medium"
            },
            
            # Mathematics Questions
            {
                "question_text": "If the roots of the equation x² - 5x + 6 = 0 are α and β, then what is the value of α² + β²?",
                "option_a": "13",
                "option_b": "25",
                "option_c": "37",
                "option_d": "49",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Algebra",
                "difficulty": "Medium"
            },
            {
                "question_text": "The value of ∫sin²x dx is:",
                "option_a": "sin2x/4 + C",
                "option_b": "x/2 - sin2x/4 + C",
                "option_c": "-cos2x/4 + C",
                "option_d": "cos2x/2 + C",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Hard"
            },
            {
                "question_text": "The slope of the line perpendicular to 3x + 4y = 7 is:",
                "option_a": "3/4",
                "option_b": "4/3",
                "option_c": "-3/4",
                "option_d": "-4/3",
                "correct_answer": "D",
                "subject": "Mathematics",
                "topic": "Coordinate Geometry",
                "difficulty": "Easy"
            }
        ]
        
        # Insert each sample question
        for question in sample_questions:
            query = """
                INSERT INTO questions (
                    question_text, option_a, option_b, option_c, option_d,
                    correct_answer, subject, topic, difficulty
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                question["question_text"],
                question["option_a"],
                question["option_b"],
                question["option_c"],
                question["option_d"],
                question["correct_answer"],
                question["subject"],
                question["topic"],
                question["difficulty"]
            )
            self.execute_query(query, params)
        
        print("Sample questions added to database successfully!")
    
    def get_questions_by_subject(self, subject, count=30):
        """Get a specified number of questions for a given subject"""
        # Parse subject if it contains multiple (comma separated)
        subjects = [s.strip() for s in subject.split(',')]
        
        # Construct the query with OR conditions for multiple subjects
        placeholders = ", ".join(["%s"] * len(subjects))
        query = f"""
            SELECT * FROM questions 
            WHERE subject IN ({placeholders})
            ORDER BY RAND()
            LIMIT %s
        """
        
        # Parameters include all subjects and the count
        params = subjects + [count]
        
        questions = self.execute_read_query(query, params)
        if not questions:
            return []
            
        return questions
    
    def get_question_by_id(self, question_id):
        """Get a specific question by ID"""
        query = "SELECT * FROM questions WHERE id = %s"
        result = self.execute_read_query(query, (question_id,))
        
        if result and len(result) > 0:
            return result[0]
        else:
            return None
    
    def save_progress_note(self, user_id, progress_id, note_text, highlight_color=None):
        """Save a note or annotation related to a test result
        
        Args:
            user_id (int): The user ID
            progress_id (int): The progress/test result ID
            note_text (str): The text of the note
            highlight_color (str, optional): Color code for highlighting
            
        Returns:
            bool: True if saving was successful, False otherwise
        """
        query = """
            INSERT INTO user_progress_notes 
            (user_id, progress_id, note_text, highlight_color, created_at) 
            VALUES (%s, %s, %s, %s, NOW())
        """
        params = (user_id, progress_id, note_text, highlight_color)
        
        return self.execute_query(query, params)
    
    def get_progress_notes(self, user_id, progress_id=None):
        """Get notes related to user's test results
        
        Args:
            user_id (int): The user ID
            progress_id (int, optional): Specific test result ID, or None for all notes
            
        Returns:
            list: List of note dictionaries
        """
        if progress_id:
            query = """
                SELECT * FROM user_progress_notes 
                WHERE user_id = %s AND progress_id = %s
                ORDER BY created_at DESC
            """
            params = (user_id, progress_id)
        else:
            query = """
                SELECT * FROM user_progress_notes 
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            params = (user_id,)
            
        return self.execute_read_query(query, params) or []
        
    def get_tests_taken_count(self, user_id):
        """Get the number of tests taken by the user
        
        Args:
            user_id (int): The user ID
            
        Returns:
            int: The number of tests taken
        """
        query = "SELECT COUNT(*) as count FROM user_progress WHERE user_id = %s"
        result = self.execute_read_query(query, (user_id,))
        
        if result and len(result) > 0:
            return result[0]['count']
        return 0
        
    def get_average_score(self, user_id):
        """Get the average score percentage of the user
        
        Args:
            user_id (int): The user ID
            
        Returns:
            float: The average score percentage
        """
        query = "SELECT AVG(score) as avg_score FROM user_progress WHERE user_id = %s"
        result = self.execute_read_query(query, (user_id,))
        
        if result and len(result) > 0 and result[0]['avg_score'] is not None:
            return round(result[0]['avg_score'], 1)
        return 0
        
    def get_best_score(self, user_id):
        """Get the best score percentage of the user
        
        Args:
            user_id (int): The user ID
            
        Returns:
            float: The best score percentage
        """
        query = "SELECT MAX(score) as best_score FROM user_progress WHERE user_id = %s"
        result = self.execute_read_query(query, (user_id,))
        
        if result and len(result) > 0 and result[0]['best_score'] is not None:
            return round(result[0]['best_score'], 1)
        return 0
        
    def get_study_streak(self, user_id):
        """Get the user's study streak in days
        
        Args:
            user_id (int): The user ID
            
        Returns:
            int: The number of consecutive days with activity
        """
        # Get the dates of all user activity in the last 30 days
        query = """
            SELECT DISTINCT DATE(date_taken) as activity_date 
            FROM user_progress 
            WHERE user_id = %s AND date_taken >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            ORDER BY activity_date DESC
        """
        result = self.execute_read_query(query, (user_id,))
        
        if not result:
            return 0
            
        # Calculate streak
        streak = 1
        today = datetime.now().date()
        
        # Check if there's activity today
        has_today = False
        for row in result:
            if row['activity_date'] == today:
                has_today = True
                break
                
        if not has_today:
            return 0
            
        # Calculate consecutive days
        for i in range(1, len(result)):
            prev_date = result[i-1]['activity_date']
            curr_date = result[i]['activity_date']
            
            # If the dates are consecutive (difference is 1 day)
            if (prev_date - curr_date).days == 1:
                streak += 1
            else:
                break
                
        return streak 