import customtkinter as ctk
from pages.welcome_page import WelcomePage
from pages.login_page import LoginPage
from pages.create_account_page import CreateAccountPage
from pages.dashboard_page import DashboardPage
from pages.previous_year_questions_page import PreviousYearQuestionsPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.news_page import NewsPage
from pages.mock_test_result_page import MockTestResultPage
from pages.calendar_page import CalendarPage
from pages.jee_subjects_page import JEESubjectsPage
from pages.mock_tests_page import MockTestsPage
from pages.cet_subjects_page import CETSubjectsPage

from tkinter import messagebox
import hashlib
import re
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import config
import requests
from database_manager import DatabaseManager
from email_manager import EmailManager

class EduQuestApp:
    def __init__(self):
        self.root = ctk.CTk()  # Initialize the main window
        self.root.title("EduQuest - Your Ultimate Exam Preparation App")
        self.root.geometry("1400x900")  # Set the window size
        
        # Set a fixed appearance mode instead of allowing toggle
        ctk.set_appearance_mode("dark")  # Always use dark mode
        ctk.set_default_color_theme("green")  # Set default color theme

        # Initialize database connection
        self.db_manager = DatabaseManager()
        
        # Initialize email manager
        self.email_manager = EmailManager()
        
        # Initialize email authenticator for welcome emails
        self.email_authenticator = EmailAuthenticator()
        
        # Current user information (set after successful login)
        self.current_user_id = None
        self.current_username = None
        self.current_user_email = None

        # Add error handling for database connection
        if not hasattr(self.db_manager, 'connection') or not self.db_manager.connection:
            print("Warning: Database connection failed. Some features may not work correctly.")
            messagebox.showwarning(
                "Database Connection Issue", 
                "Connection to the database could not be established. Some features may not work correctly."
            )
            
        self.show_welcome_page()

    def show_welcome_page(self):
        self.clear_current_frame()  # Clear the current frame
        self.welcome_page = WelcomePage(self.root, self)
        self.welcome_page.pack(fill="both", expand=True)

    def show_login_page(self):
        self.clear_current_frame()  # Clear the current frame
        self.login_page = LoginPage(self.root, self)
        self.login_page.pack(fill="both", expand=True)

    def show_create_account_page(self):
        self.clear_current_frame()  # Clear the current frame   
        self.create_account_page = CreateAccountPage(self.root, self)
        self.create_account_page.pack(fill="both", expand=True)

    def show_dashboard_page(self):
        self.clear_current_frame()  # Clear the current frame
        self.dashboard_page = DashboardPage(self.root, self)
        self.dashboard_page.pack(fill="both", expand=True)

    def switch_page(self, page_name):
        if page_name == 'login':
            self.show_login_page()
        elif page_name == 'create_account':
            self.show_create_account_page()
        elif page_name == 'welcome':
            self.show_welcome_page()
        # Add more pages as needed

    def clear_current_frame(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        """Run the application main loop"""
        self.root.mainloop()

    def start_subject_test(self, subject):
        """Start a test for a specific subject"""
        self.clear_current_frame()
        from pages.mock_tests_page import QuestionPage
        self.question_page = QuestionPage(self.root, self, subject)
        self.question_page.pack(fill="both", expand=True)

    def show_mock_tests(self):
        """Display mock tests page with data from the mock_tests table"""
        self.clear_current_frame()
        from pages.mock_tests_page import MockTestsPage
        self.mock_tests_page = MockTestsPage(self.root, self)
        self.mock_tests_page.pack(fill="both", expand=True)

    def get_available_mock_tests(self):
        """Retrieve available mock tests"""
        # Mock test data as replacement for database queries
        mock_tests = [
            {"id": 1, "title": "Physics Mock Test 1", "description": "Basic mechanics and kinematics", "subject": "Physics", "difficulty": "Medium", "time_limit": 60, "passing_score": 70},
            {"id": 2, "title": "Chemistry Mock Test 1", "description": "Periodic table and chemical bonding", "subject": "Chemistry", "difficulty": "Easy", "time_limit": 45, "passing_score": 65},
            {"id": 3, "title": "Mathematics Mock Test 1", "description": "Algebra and calculus basics", "subject": "Mathematics", "difficulty": "Hard", "time_limit": 90, "passing_score": 75}
        ]
        return mock_tests

    def get_mock_test_details(self, test_id):
        """Get details of a specific mock test"""
        # Mock test questions as replacement for database queries
        mock_test_questions = {
            1: {
                "title": "Physics Mock Test 1",
                "description": "Basic mechanics and kinematics",
                "subject": "Physics",
                "time_limit": 60,
                "questions": [
                    {"id": 1, "question_text": "What is Newton's First Law of Motion?", "option_a": "F = ma", "option_b": "An object at rest stays at rest unless acted upon by an external force", "option_c": "For every action, there is an equal and opposite reaction", "option_d": "Energy can neither be created nor destroyed", "correct_answer": "B"},
                    {"id": 2, "question_text": "What is the unit of force in SI units?", "option_a": "Watt", "option_b": "Joule", "option_c": "Newton", "option_d": "Pascal", "correct_answer": "C"}
                ]
            },
            2: {
                "title": "Chemistry Mock Test 1",
                "description": "Periodic table and chemical bonding",
                "subject": "Chemistry",
                "time_limit": 45,
                "questions": [
                    {"id": 1, "question_text": "What is the atomic number of Carbon?", "option_a": "6", "option_b": "12", "option_c": "14", "option_d": "8", "correct_answer": "A"},
                    {"id": 2, "question_text": "What type of bond is formed between sodium and chlorine?", "option_a": "Covalent", "option_b": "Ionic", "option_c": "Metallic", "option_d": "Hydrogen", "correct_answer": "B"}
                ]
            },
            3: {
                "title": "Mathematics Mock Test 1",
                "description": "Algebra and calculus basics",
                "subject": "Mathematics",
                "time_limit": 90,
                "questions": [
                    {"id": 1, "question_text": "What is the derivative of x²?", "option_a": "x", "option_b": "2x", "option_c": "x²", "option_d": "2", "correct_answer": "B"},
                    {"id": 2, "question_text": "Solve for x: 3x + 5 = 14", "option_a": "x = 3", "option_b": "x = 4", "option_c": "x = 3.5", "option_d": "x = 3", "correct_answer": "A"}
                ]
            }
        }
        return mock_test_questions.get(test_id, None)

    def start_mock_test(self, test_id):
        """Start a mock test and record the attempt"""
        # Return sample test attempt ID
        return 100 + test_id  # Simple mock attempt ID

    def submit_mock_test_answer(self, attempt_id, question_id, user_answer):
        """Submit and record a user answer for a mock test question"""
        # In a real implementation, this would save to a database
        # For now, just return success
        return True

    def complete_mock_test(self, attempt_id):
        """Complete a mock test and calculate results"""
        # Check if we have a database connection
        if not hasattr(self, 'db_manager') or not self.db_manager.connection:
            # Return sample results if no database connection
            return {
                "score": 80,
                "percentage": 80.0,
                "passed": True,
                "time_taken": 1200,  # seconds
                "correct_answers": 8,
                "total_questions": 10
            }
            
        try:
            # Get the test attempt details - in a real implementation, you would fetch this from the database
            # For now, let's use a simulated approach
            
            # Get the user ID
            user_id = self.current_user_id
            if not user_id:
                raise ValueError("User is not logged in")
                
            # Simulate getting test results
            import random
            correct_answers = random.randint(5, 10)
            total_questions = 10
            score_percentage = (correct_answers / total_questions) * 100
            time_taken = random.randint(600, 1800)  # Between 10-30 minutes
            
            # Calculate subject-specific scores (for JEE tests)
            physics_correct = random.randint(1, 4)
            chemistry_correct = random.randint(1, 3)
            mathematics_correct = correct_answers - physics_correct - chemistry_correct
            
            physics_percentage = (physics_correct / 4) * 100
            chemistry_percentage = (chemistry_correct / 3) * 100
            mathematics_percentage = (mathematics_correct / 3) * 100
            
            # Save to database
            query = """
                INSERT INTO user_progress (
                    user_id, score, total_marks, max_marks, correct_answers, 
                    incorrect_answers, not_attempted, time_spent, 
                    physics_marks, chemistry_marks, mathematics_marks,
                    physics_percentage, chemistry_percentage, mathematics_percentage,
                    physics_score, chemistry_score, mathematics_score,
                    completed, date_taken
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                )
            """
            
            params = (
                user_id, score_percentage, correct_answers, total_questions, correct_answers,
                total_questions - correct_answers, 0, time_taken,
                physics_correct, chemistry_correct, mathematics_correct,
                physics_percentage, chemistry_percentage, mathematics_percentage,
                physics_percentage, chemistry_percentage, mathematics_percentage,
                1  # completed
            )
            
            self.db_manager.execute_query(query, params)
            
            # Return the results
            return {
                "score": correct_answers,
                "percentage": score_percentage,
                "passed": score_percentage >= 40,  # Pass threshold
                "time_taken": time_taken,
                "correct_answers": correct_answers,
                "total_questions": total_questions,
                "physics_score": physics_correct,
                "chemistry_score": chemistry_correct,
                "mathematics_score": mathematics_correct
            }
            
        except Exception as e:
            print(f"Error completing mock test: {e}")
            # Return sample results in case of error
            return {
                "score": 6,
                "percentage": 60.0,
                "passed": True,
                "time_taken": 1200,
                "correct_answers": 6,
                "total_questions": 10
            }

    def show_mock_test_result(self, result):
        """Display the result of a completed mock test"""
        self.clear_current_frame()
        self.result_page = MockTestResultPage(self.root, self, result)
        self.result_page.pack(fill="both", expand=True)

    def show_previous_year_questions(self):
        """Display previous year questions page"""
        self.clear_current_frame()
        self.previous_year_questions_page = PreviousYearQuestionsPage(self.root, self)
        self.previous_year_questions_page.pack(fill="both", expand=True)

    def show_forgot_password(self):
        """Show the forgot password page"""
        self.clear_current_frame()
        self.forgot_password_page = ForgotPasswordPage(self.root, self)
        self.forgot_password_page.pack(fill="both", expand=True)

    def reset_password(self, username, email, new_password, confirm_password):
        """Reset user password"""
        try:
            # Validate inputs
            if not username or not email or not new_password:
                messagebox.showerror("Error", "All fields are required")
                return False
                
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return False
                
            if len(new_password) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters")
                return False
            
            # Get user by email
            user = self.db_manager.get_user_by_email(email)
            if not user or user['username'] != username:
                messagebox.showerror("Error", "Username and email do not match")
                return False
            
            # Hash the new password
            hashed_password = self.hash_password(new_password)
            
            # Update the password
            success, message = self.db_manager.update_password(username, hashed_password)
            
            if success:
                messagebox.showinfo("Success", "Password has been reset successfully")
                return True
            else:
                messagebox.showerror("Error", message)
                return False
                
        except Exception as err:
            messagebox.showerror("Error", f"Failed to reset password: {err}")
            return False

    def validate_email(self, email):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, email, password, full_name=None):
        """
        Register a new user in the database
        
        Args:
            username (str): The username for the new account
            email (str): The email address for the new account
            password (str): The password for the new account
            full_name (str, optional): The user's full name
            
        Returns:
            bool: True if registration is successful, False otherwise
        """
        try:
            # Validate inputs
            if not username or not email or not password:
                messagebox.showerror("Error", "All fields are required")
                return False
                
            if not self.validate_email(email):
                messagebox.showerror("Error", "Invalid email format")
                return False
                
            # Register the user using the database manager
            success = self.db_manager.register_user(username, email, password, full_name)
            
            if success:
                messagebox.showinfo("Success", f"User {username} registered successfully")
                
                # Send welcome email
                try:
                    email_sent, response = self.email_manager.send_welcome_email(email, username)
                    if email_sent:
                        print(f"Welcome email sent to {email}")
                    else:
                        print(f"Failed to send welcome email: {response}")
                except Exception as email_err:
                    print(f"Error sending welcome email: {email_err}")
                
                return True
            else:
                messagebox.showerror("Error", "Registration failed - username or email already exists")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Registration error: {e}")
            return False

    def login(self, username, password):
        """
        Authenticate a user with the database
        
        Args:
            username (str): The username to authenticate
            password (str): The password to verify
            
        Returns:
            bool: True if authentication is successful, False otherwise
        """
        try:
            # Validate inputs
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required")
                return False
                
            user = self.db_manager.authenticate_user(username, password)
            if user:
                # Store user data in app instance
                self.current_user_id = user.get('id')
                self.current_username = user.get('username')
                self.current_user_email = user.get('email')
                # Store complete user object for other potential uses
                self.current_user = user
                
                print(f"User {username} logged in successfully")
                return True
            else:
                print("Login failed: Invalid username or password")
                return False
        except Exception as e:
            print(f"Login error: {e}")
            messagebox.showerror("Error", f"Login error: {e}")
            return False

    def logout(self):
        """Log out the current user"""
        self.current_user_id = None
        self.current_username = None
        self.current_user_email = None
        self.show_welcome_page()

    def __del__(self):
        """Clean up resources when object is deleted"""
        # Close database connection if it exists
        if hasattr(self, 'db_manager'):
            self.db_manager.close_connection()

    def start_exam(self, exam_type):
        """Start preparation for a specific exam type"""
        if exam_type == "JEE":
            self.show_jee_subjects()
        elif exam_type == "CET":
            self.show_cet_subjects()
        else:
            messagebox.showinfo("Exam Preparation", f"Starting {exam_type} preparation")
    
    def show_jee_subjects(self):
        """Show JEE subjects page"""
        self.clear_current_frame()
        from pages.jee_subjects_page import JEESubjectsPage
        self.jee_subjects_page = JEESubjectsPage(self.root, self)
        self.jee_subjects_page.pack(fill="both", expand=True)

    def show_cet_subjects(self):
        """Show CET subjects page"""
        self.clear_current_frame()
        from pages.cet_subjects_page import CETSubjectsPage
        self.cet_subjects_page = CETSubjectsPage(self.root, self)
        self.cet_subjects_page.pack(fill="both", expand=True)

    def show_calendar(self):
        """Show calendar page with study planner"""
        self.clear_current_frame()
        from pages.calendar_page import CalendarPage
        self.calendar_page = CalendarPage(self.root, self)
        self.calendar_page.pack(fill="both", expand=True)
        
    def show_reports(self):
        """Show test analysis reports page"""
        self.clear_current_frame()
        from pages.reports_page import ReportsPage
        self.reports_page = ReportsPage(self.root, self)
        self.reports_page.pack(fill="both", expand=True)
        
    def show_news_page(self):
        """Show news page with exam-related news"""
        self.clear_current_frame()
        self.news_page = NewsPage(self.root, self)
        self.news_page.pack(fill="both", expand=True)

    def setup_email_verification(self):
        verify_button = ctk.CTkButton(
            self,
            text="Get Welcome Email",
            command=self.show_welcome_email_dialog,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=200,
            height=40
        )
        verify_button.pack(pady=20)

    def show_welcome_email_dialog(self):
        """Show email dialog for welcome message"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Welcome Email")
        dialog.geometry("400x300")
        dialog.configure(fg_color="#1a1a1a")
        
        # Make dialog modal
        dialog.transient(self)
        dialog.grab_set()
        
        # Email entry
        email_label = ctk.CTkLabel(
            dialog,
            text="Enter your email address to receive a welcome message:",
            font=("Arial", 14)
        )
        email_label.pack(pady=(20, 5))
        
        email_entry = ctk.CTkEntry(
            dialog,
            width=300,
            height=35,
            placeholder_text="example@email.com"
        )
        email_entry.pack(pady=(0, 20))
        
        # Status label
        status_label = ctk.CTkLabel(
            dialog,
            text="",
            font=("Arial", 12),
            text_color="#ff6b6b"
        )
        status_label.pack(pady=5)
        
        def send_welcome():
            email = email_entry.get().strip()
            success, message = self.email_authenticator.send_welcome_email(email)
            
            if success:
                status_label.configure(text_color="#2ecc71", text="Welcome email sent successfully!")
                # Close dialog after 2 seconds
                dialog.after(2000, dialog.destroy)
            else:
                status_label.configure(text_color="#ff6b6b", text=message)
        
        # Send welcome button
        send_button = ctk.CTkButton(
            dialog,
            text="Send Welcome Email",
            command=send_welcome,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        send_button.pack(pady=10)

    def save_verified_email(self, email):
        """Save verified email to file instead of database"""
        try:
            # In a real implementation, this would save to a database
            # For this demo, we'll just print to console
            print(f"Email verified: {email}")
            return True
            
        except Exception as e:
            print(f"Error saving verified email: {e}")
            return False

    def fetch_exam_news(self):
        """Fetch news related to competitive exams in India"""
        try:
            # Get news from the last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')
            
            # Use proper OR query syntax for NewsAPI
            news = self.newsapi.get_everything(
                q='NEET OR JEE OR "entrance exam" OR "college admission"',
                language='en',
                from_param=from_date,
                to=to_date,
                sort_by='publishedAt',
                page_size=20
            )
            
            return news['articles'] if news['status'] == 'ok' else []
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []

    def fetch_specific_exam_news(self, exam_type):
        """Fetch news for a specific exam type"""
        try:
            # Get news from the last 30 days
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')
            
            # Broader query for better results
            news = self.newsapi.get_everything(
                q=f'{exam_type} OR "{exam_type} exam" OR "{exam_type} preparation" OR "{exam_type} result"',
                language='en',
                from_param=from_date,
                to=to_date,
                sort_by='publishedAt',
                page_size=15
            )
            
            return news['articles'] if news['status'] == 'ok' else []
        except Exception as e:
            print(f"Error fetching specific exam news: {str(e)}")
            return []

    def fallback_news_fetch(self):
        """Fallback method to fetch news directly via requests"""
        try:
            API_KEY = "4350e215f8284b6189cb79baf6d71cea"  # Replace with your actual API key
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            url = f"https://newsapi.org/v2/everything?q=education%20OR%20exam%20OR%20student&from={from_date}&sortBy=publishedAt&apiKey={API_KEY}&language=en&pageSize=15"
            
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "ok":
                    return data["articles"]
            return []
        except Exception as e:
            print(f"Fallback news fetch failed: {e}")
            return []

class EmailAuthenticator:
    def __init__(self):
        # Email configuration from config file
        self.smtp_server = config.SMTP_CONFIG.get('server', 'smtp.gmail.com')
        self.smtp_port = config.SMTP_CONFIG.get('port', 587)
        self.sender_email = config.SMTP_CONFIG.get('username', 'eduquest12345@gmail.com')
        self.sender_password = config.SMTP_CONFIG.get('password', '')  # From your app password

    def is_valid_email(self, email):
        """Check if email format is valid"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def send_welcome_email(self, recipient_email):
        """Send welcome email to new user"""
        try:
            if not self.is_valid_email(recipient_email):
                return False, "Invalid email format"

            print(f"Attempting to send welcome email to: {recipient_email}")
            print(f"Using SMTP settings: server={self.smtp_server}, port={self.smtp_port}, username={self.sender_email}")

            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "Welcome to EduQuest!"

            # Email body
            body = f"""
            <html>
            <body>
                <h1>Welcome to EduQuest!</h1>
                
                <p>Thank you for creating an account with us. We're excited to have you join our community of learners!</p>
                
                <p>With EduQuest, you can:</p>
                <ul>
                    <li>Prepare for various competitive exams like JEE and CET</li>
                    <li>Practice with mock tests and sample questions</li>
                    <li>Track your progress and analyze your performance</li>
                    <li>Stay updated with the latest exam-related news</li>
                </ul>
                
                <p>If you have any questions or need assistance, please feel free to reach out to our support team.</p>
                
                <p>Happy learning!</p>
                
                <p>Best regards,<br>
                The EduQuest Team</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))

            # Connect to SMTP server
            print("Connecting to SMTP server...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.set_debuglevel(1)  # Enable debug output
            
            print("Starting TLS...")
            server.starttls()
            
            print(f"Logging in with username: {self.sender_email}")
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            print(f"Sending email to {recipient_email}...")
            server.send_message(msg)
            
            print("Quitting SMTP server...")
            server.quit()
            
            print("Email sent successfully!")
            return True, "Welcome email sent successfully"
            
        except Exception as e:
            error_message = f"Error sending email: {str(e)}"
            print(error_message)
            
            # Check for common authentication errors
            if "Authentication" in str(e):
                print("This appears to be an authentication error. Please verify your Gmail app password.")
            elif "Timeout" in str(e):
                print("Timeout occurred. Check your internet connection and try again.")
            
            import traceback
            traceback.print_exc()
            
            return False, f"Failed to send welcome email: {str(e)}"

if __name__ == "__main__":
    try:
        # Initialize and run the application
        app = EduQuestApp()
        app.run()
    except Exception as e:
        print(f"Error during startup: {e}")
        import traceback
        traceback.print_exc()
        
        # Still try to run the app even if there was an error
        try:
            app = EduQuestApp()
            app.run()
        except Exception as app_error:
            print(f"Could not start application: {app_error}")