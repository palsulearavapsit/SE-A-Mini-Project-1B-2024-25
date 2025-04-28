# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection  # Custom database connection module

class LoginPage:
    """Class for the login page of the application"""
    
    def __init__(self, root, on_login_success):
        """
        Initialize the LoginPage
        
        Args:
            root: The parent tkinter widget
            on_login_success: Callback function when login is successful
        """
        self.root = root
        self.on_login_success = on_login_success
        self.create_widgets()  # Create the UI elements

    def create_widgets(self):
        """Create and arrange all widgets for the login page"""
        # Set background color for the root window
        self.root.configure(bg="#f2f2f2")

        # Title Frame with green background
        title_frame = tk.Frame(self.root, bg="#4CAF50", height=100)
        title_frame.pack(fill=tk.X)  # Fill horizontally
        tk.Label(title_frame, text="Login", font=("Arial", 24), fg="white", bg="#4CAF50").pack(pady=20)

        # Login Form Frame
        form_frame = tk.Frame(self.root, bg="#f2f2f2")
        form_frame.pack(pady=20)

        # Username (Email) Field
        tk.Label(form_frame, text="Email", font=("Arial", 12), bg="#f2f2f2").grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password Field
        tk.Label(form_frame, text="Password", font=("Arial", 12), bg="#f2f2f2").grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#f2f2f2")
        button_frame.pack(pady=10)

        # Login Button
        ttk.Button(button_frame, text="Login", command=self.login).pack(side=tk.LEFT, padx=10)

        # Forgot Password Link (styled as clickable text)
        forgot_password_label = tk.Label(
            button_frame, 
            text="Forgot Password?", 
            font=("Arial", 10, "underline"), 
            fg="blue", 
            cursor="hand2", 
            bg="#f2f2f2"
        )
        forgot_password_label.pack(side=tk.LEFT, padx=10)
        forgot_password_label.bind("<Button-1>", lambda e: self.forgot_password())

        # Registration Link (styled as clickable text)
        register_label = tk.Label(
            button_frame, 
            text="New User? Register Here", 
            font=("Arial", 10, "underline"), 
            fg="blue", 
            cursor="hand2", 
            bg="#f2f2f2"
        )
        register_label.pack(side=tk.RIGHT, padx=10)
        register_label.bind("<Button-1>", lambda e: self.register())

    def login(self):
        """Handle login button click event"""
        # Get username and password from entry fields
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate that fields are not empty
        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Connect to database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # First try to log in with role column
                try:
                    cursor.execute(
                        "SELECT id, username, role FROM users WHERE username=%s AND password=%s", 
                        (username, password)
                    )
                    user = cursor.fetchone()
                    if user:
                        messagebox.showinfo("Success", "Login Successful!")
                        # Pass the username and role to the success handler
                        self.on_login_success(user[1], user[2])  # username and role
                    else:
                        messagebox.showerror("Error", "Invalid credentials")
                except Exception as e:
                    # If role column doesn't exist, try without it
                    if "Unknown column 'role'" in str(e):
                        cursor.execute(
                            "SELECT id, username FROM users WHERE username=%s AND password=%s", 
                            (username, password)
                        )
                        user = cursor.fetchone()
                        if user:
                            messagebox.showinfo("Success", "Login Successful!")
                            # Pass only username with default role
                            self.on_login_success(user[1], "user")  # Default to user role
                        else:
                            messagebox.showerror("Error", "Invalid credentials")
                    else:
                        raise e  # Re-raise other exceptions
            except Exception as e:
                messagebox.showerror("Error", f"Login failed: {e}")
            finally:
                # Close database resources
                cursor.close()
                connection.close()

    def register(self):
        """Switch to registration page"""
        self.clear_window()
        RegistrationPage(self.root, self.show_login_page)

    def forgot_password(self):
        """Switch to password recovery page"""
        self.clear_window()
        PasswordRecoveryPage(self.root, self.show_login_page)

    def show_login_page(self):
        """Return to login page"""
        self.clear_window()
        LoginPage(self.root, self.on_login_success)

    def clear_window(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()


class RegistrationPage:
    """Class for the user registration page"""
    
    def __init__(self, root, on_register_success):
        """
        Initialize the RegistrationPage
        
        Args:
            root: The parent tkinter widget
            on_register_success: Callback function when registration is successful
        """
        self.root = root
        self.on_register_success = on_register_success
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all widgets for the registration page"""
        self.root.configure(bg="#f2f2f2")

        # Title Frame with green background
        title_frame = tk.Frame(self.root, bg="#4CAF50", height=100)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Register", font=("Arial", 24), fg="white", bg="#4CAF50").pack(pady=20)

        # Main container with scrolling capability
        main_container = tk.Frame(self.root, bg="#f2f2f2")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Registration Form Frame
        form_frame = tk.Frame(main_container, bg="#f2f2f2")
        form_frame.pack(pady=20)

        # Define registration form fields
        fields = [
            ("Full Name", "name_entry"),
            ("Contact Number", "contact_entry"),
            ("Email Address", "email_entry"),
            ("Password", "password_entry"),
            ("Confirm Password", "confirm_password_entry"),
        ]

        # Create entry fields dynamically
        self.entries = {}
        for i, (label_text, entry_name) in enumerate(fields):
            # Create label
            tk.Label(form_frame, text=label_text, font=("Arial", 12), bg="#f2f2f2").grid(
                row=i, column=0, sticky="w", padx=10, pady=5)
            
            # Create entry field
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[entry_name] = entry

        # Security Question dropdown
        row = len(fields)
        tk.Label(form_frame, text="Security Question", font=("Arial", 12), bg="#f2f2f2").grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        self.security_question = tk.StringVar(value="What is your pet's name?")
        questions = ["What is your pet's name?", "What is your favorite color?"]
        ttk.Combobox(
            form_frame, 
            textvariable=self.security_question, 
            values=questions, 
            state="readonly"
        ).grid(row=row, column=1, padx=10, pady=5)

        # Security Answer field
        row += 1
        tk.Label(form_frame, text="Security Answer", font=("Arial", 12), bg="#f2f2f2").grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        self.security_answer_entry = ttk.Entry(form_frame, width=30)
        self.security_answer_entry.grid(row=row, column=1, padx=10, pady=5)

        # Role Selection dropdown
        row += 1
        tk.Label(form_frame, text="Register as", font=("Arial", 12), bg="#f2f2f2").grid(
            row=row, column=0, sticky="w", padx=10, pady=5)
        self.role = tk.StringVar(value="user")
        role_combobox = ttk.Combobox(
            form_frame, 
            textvariable=self.role, 
            values=["user", "admin"], 
            state="readonly", 
            width=28
        )
        role_combobox.grid(row=row, column=1, padx=10, pady=5)
        role_combobox.current(0)  # Set default to first option (user)

        # Buttons Frame
        button_frame = tk.Frame(main_container, bg="#f2f2f2")
        button_frame.pack(pady=10)

        # Register and Back buttons
        ttk.Button(button_frame, text="Register Now", command=self.register).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Login", command=self.on_register_success).pack(side=tk.RIGHT, padx=10)

    def register(self):
        """Handle registration form submission"""
        # Get all field values
        name = self.entries["name_entry"].get().strip()
        contact = self.entries["contact_entry"].get().strip()
        email = self.entries["email_entry"].get().strip()
        password = self.entries["password_entry"].get().strip()
        confirm_password = self.entries["confirm_password_entry"].get().strip()
        security_question = self.security_question.get()
        security_answer = self.security_answer_entry.get().strip()
        role = self.role.get()

        # Validate required fields
        if not name or not contact or not email or not password or not confirm_password or not security_answer:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Validate password match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Connect to database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Check if role column exists
                try:
                    # Try inserting with role column
                    cursor.execute(
                        "INSERT INTO users (username, password, email, security_question, security_answer, role) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (email, password, email, security_question, security_answer, role)
                    )
                except Exception as e:
                    # If role column doesn't exist, try without it
                    if "Unknown column 'role'" in str(e):
                        # Attempt to add role column
                        try:
                            cursor.execute(
                                "ALTER TABLE users ADD COLUMN role ENUM('admin', 'user') NOT NULL DEFAULT 'user'"
                            )
                            connection.commit()
                            # Try insert again with role
                            cursor.execute(
                                "INSERT INTO users (username, password, email, security_question, security_answer, role) "
                                "VALUES (%s, %s, %s, %s, %s, %s)",
                                (email, password, email, security_question, security_answer, role)
                            )
                        except:
                            # If adding column fails, insert without role
                            cursor.execute(
                                "INSERT INTO users (username, password, email, security_question, security_answer) "
                                "VALUES (%s, %s, %s, %s, %s)",
                                (email, password, email, security_question, security_answer)
                            )
                    else:
                        raise e  # Re-raise other exceptions
                
                connection.commit()
                messagebox.showinfo("Success", "Registration Successful!")
                self.on_register_success()
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {e}")
            finally:
                # Close database resources
                cursor.close()
                connection.close()


class PasswordRecoveryPage:
    """Class for the password recovery page"""
    
    def __init__(self, root, on_recovery_success):
        """
        Initialize the PasswordRecoveryPage
        
        Args:
            root: The parent tkinter widget
            on_recovery_success: Callback function when password recovery is successful
        """
        self.root = root
        self.on_recovery_success = on_recovery_success
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all widgets for the password recovery page"""
        self.root.configure(bg="#f2f2f2")

        # Title Frame with green background
        title_frame = tk.Frame(self.root, bg="#4CAF50", height=100)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Password Recovery", font=("Arial", 24), fg="white", bg="#4CAF50").pack(pady=20)

        # Recovery Form Frame
        form_frame = tk.Frame(self.root, bg="#f2f2f2")
        form_frame.pack(pady=20)

        # Email field
        tk.Label(form_frame, text="Registered Email", font=("Arial", 12), bg="#f2f2f2").grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        # Security Question dropdown
        tk.Label(form_frame, text="Security Question", font=("Arial", 12), bg="#f2f2f2").grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        self.security_question = tk.StringVar(value="What is your pet's name?")
        questions = ["What is your pet's name?", "What is your favorite color?"]
        ttk.Combobox(
            form_frame, 
            textvariable=self.security_question, 
            values=questions, 
            state="readonly"
        ).grid(row=1, column=1, padx=10, pady=5)

        # Security Answer field
        tk.Label(form_frame, text="Security Answer", font=("Arial", 12), bg="#f2f2f2").grid(
            row=2, column=0, sticky="w", padx=10, pady=5)
        self.security_answer_entry = ttk.Entry(form_frame, width=30)
        self.security_answer_entry.grid(row=2, column=1, padx=10, pady=5)

        # New Password field
        tk.Label(form_frame, text="New Password", font=("Arial", 12), bg="#f2f2f2").grid(
            row=3, column=0, sticky="w", padx=10, pady=5)
        self.new_password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.new_password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#f2f2f2")
        button_frame.pack(pady=10)

        # Reset Password and Back buttons
        ttk.Button(button_frame, text="Reset Password", command=self.reset_password).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Login", command=self.on_recovery_success).pack(side=tk.RIGHT, padx=10)

    def reset_password(self):
        """Handle password reset request"""
        # Get field values
        email = self.email_entry.get().strip()
        security_question = self.security_question.get()
        security_answer = self.security_answer_entry.get().strip()
        new_password = self.new_password_entry.get().strip()

        # Validate required fields
        if not email or not security_answer or not new_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Connect to database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Verify security question and answer
                cursor.execute(
                    "SELECT * FROM users WHERE email=%s AND security_question=%s AND security_answer=%s",
                    (email, security_question, security_answer)
                )
                user = cursor.fetchone()
                
                if user:
                    # Update password if verification succeeds
                    cursor.execute(
                        "UPDATE users SET password=%s WHERE email=%s", 
                        (new_password, email)
                    )
                    connection.commit()
                    messagebox.showinfo("Success", "Password reset successfully!")
                    self.on_recovery_success()
                else:
                    messagebox.showerror("Error", "Invalid email, security question, or answer.")
            except Exception as e:
                messagebox.showerror("Error", f"Password reset failed: {e}")
            finally:
                # Close database resources
                cursor.close()
                connection.close()