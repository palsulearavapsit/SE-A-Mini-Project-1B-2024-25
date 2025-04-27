# Hey! Let's import all the stuff we need for our login system
import tkinter as tk
from tkinter import ttk, Frame, Label, Button, Entry, Checkbutton, messagebox, StringVar, IntVar, Toplevel
import mysql.connector  # For database operations
import re  # For password validation
from datetime import datetime

# Some basic settings for our window size
PAGE_WIDTH = 800
PAGE_HEIGHT = 600

# Password rules - keeping it secure but not too complicated
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 12

# Database settings - might want to move this to a config file later
DB_CONFIG = {
    'host': "127.0.0.1",
    'user': "root",
    'password': "Shardul203",  # Remember to change this in production!
    'database': "ev_station",
    'port': 3306
}

class LoginApp:
    def __init__(self, root):
        # Setting up the main window
        self.root = root
        self.root.title("Login System")
        
        # Making it fullscreen - better user experience
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')  # Windows-style fullscreen
        self.root.resizable(True, True)  # Let users resize if they want

        # Main frame where all our login stuff goes
        self.frame = Frame(self.root, bg="white")  
        self.frame.place(x=150, y=150, height=450, width=550)

        self._create_login_widgets()

    def _create_login_widgets(self):
        # This is where all our login form elements are created
        
        # Nice big heading at the top
        Label(self.root, text="EV Charging Station", font=("Impact", 40, "bold"), 
              fg="#008000", bg="white").place(x=150, y=50)
        
        # Login form title
        Label(self.frame, text="Login Here", font=("Impact", 35, "bold"), 
              fg="#008000", bg="white").place(x=90, y=30)
        
        # Just letting users know what kind of login this is
        Label(self.frame, text="Accountant User Login Area", 
              font=("Goudy Old Style", 15, "bold"), fg="#d25d17", 
              bg="white").place(x=90, y=100)

        # Username input field
        Label(self.frame, text="Username", font=("Goudy Old Style", 15, "bold"), 
              fg="gray", bg="white").place(x=90, y=140)
        self.username_var = StringVar()
        self.username_entry = Entry(self.frame, font=("Times New Roman", 15), 
                                  bg="lightgray", textvariable=self.username_var)
        self.username_entry.place(x=90, y=170, width=350, height=35)

        # Password input field - with dots for security
        Label(self.frame, text="Password", font=("Goudy Old Style", 15, "bold"), 
              fg="gray", bg="white").place(x=90, y=210)
        self.password_var = StringVar()
        self.password_entry = Entry(self.frame, font=("Times New Roman", 15), 
                                  bg="lightgray", show="•", textvariable=self.password_var)
        self.password_entry.place(x=90, y=240, width=350, height=35)

        # Checkbox to show/hide password - users love this feature
        self.show_password = IntVar()
        Checkbutton(self.frame, text="Show Password", variable=self.show_password, 
                   command=self.toggle_password, bg="white").place(x=90, y=280)

        # All our buttons - keeping them clean and simple
        Button(self.frame, text="Forgot Password?", bg="white", fg="#d77337", 
               bd=0, font=("Times New Roman", 12), 
               command=self.forgot_password).place(x=250, y=278)
        
        # Main login button - nice and prominent
        Button(self.root, text="Login", fg="white", bg="#d77337", 
               font=("Times New Roman", 20), command=self.login).place(x=230, y=470, width=180, height=40)
        
        # Sign up option for new users
        Button(self.root, text="Sign Up", fg="#000000", bg="#FFFFCC", 
               font=("Times New Roman", 20), 
               command=self.open_signup).place(x=430, y=470, width=180, height=40)

    def _create_password_requirements_label(self, parent):
        # Helper function to show password rules in a nice format
        requirements = """
Password Requirements:
• 8-12 characters long
• At least one uppercase letter
• At least one lowercase letter
• At least one number
• At least one special character (@$!%*?&)
        """
        Label(parent, text=requirements, bg="white", fg="#666666", 
              justify="left", font=("Helvetica", 10)).pack(pady=10)

    def _db_connect(self):
        # Quick way to get a database connection - keeps code DRY
        return mysql.connector.connect(**DB_CONFIG)

    def validate_password(self, password):
        # Making sure passwords are secure but not impossible to remember
        if not (PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH):
            return False, f"Password must be {PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH} characters long"
        
        # List of all our password rules - easy to modify if needed
        checks = [
            (r"[A-Z]", "uppercase letter"),
            (r"[a-z]", "lowercase letter"),
            (r"\d", "number"),
            (r"[@$!%*?&]", "special character (@$!%*?&)")
        ]
        
        # Check each rule one by one
        for pattern, msg in checks:
            if not re.search(pattern, password):
                return False, f"Password must contain at least one {msg}"
            
        return True, "Password is valid"

    def toggle_password(self):
        # Let users see what they typed - helps prevent typos
        if self.show_password.get():
            self.password_entry.config(show="")  # Show the password
        else:
            self.password_entry.config(show="•")  # Hide it again

    def login(self):
        # Get what the user typed
        username = self.username_var.get()
        password = self.password_var.get()

        # Make sure they actually typed something
        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Try to connect to our database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Look for the user in our database
            cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()

            # If we found them and the password matches
            if user and user[0] == password:
                messagebox.showinfo("Success", "Login successful!")
                # Keep track of who's logged in
                with open('current_user.txt', 'w') as f:
                    f.write(username)
                self.root.destroy()
                # Head to the main dashboard
                import Dashboard
                Dashboard.main(username)
            else:
                messagebox.showerror("Error", "Invalid username or password")

            # Clean up our database connection
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")

    def open_signup(self):
        # Create a new window for sign up
        signup_window = Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("800x600")
        signup_window.configure(bg="white")

        # Nice clean layout for the signup form
        Label(signup_window, text="Sign Up", font=("Helvetica", 18, "bold"), 
              bg="white", fg="#333333").pack(pady=20)

        # Username field
        Label(signup_window, text="Username", bg="white", fg="#666666").pack()
        username_entry = ttk.Entry(signup_window)
        username_entry.pack(pady=5)

        # Password field with the dot masking
        Label(signup_window, text="Password", bg="white", fg="#666666").pack()
        password_entry = ttk.Entry(signup_window, show="•")
        password_entry.pack(pady=5)

        # Show the password requirements
        self._create_password_requirements_label(signup_window)

        def register():
            # Grab the entered details
            username = username_entry.get()
            password = password_entry.get()

            # Basic validation
            if not username or not password:
                messagebox.showerror("Error", "All fields are required!")
                return

            # Make sure the password is strong enough
            is_valid, message = self.validate_password(password)
            if not is_valid:
                messagebox.showerror("Invalid Password", message)
                return

            try:
                # Connect and check if username is taken
                conn = self._db_connect()
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists!")
                    return

                # All good - create the new account
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                             (username, password))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "User registered successfully!")
                signup_window.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error connecting to database: {e}")

        # Nice green signup button
        Button(signup_window, text="Sign Up", bg="#00cc66", fg="white", 
               font=("Helvetica", 12), relief="flat", padx=20, pady=10, 
               cursor="hand2", command=register).pack(pady=20)

    def forgot_password(self):
        # Setting up a clean window for password reset
        forgot_window = Toplevel(self.root)
        forgot_window.title("Reset Password")
        forgot_window.geometry("800x600")
        forgot_window.configure(bg="white")

        # Nice big heading for the reset form
        Label(forgot_window, text="Reset Password", font=("Helvetica", 18, "bold"), 
              bg="white", fg="#333333").pack(pady=10)

        # Username field to identify the account
        Label(forgot_window, text="Username", bg="white", fg="#666666").pack()
        username_entry = ttk.Entry(forgot_window)
        username_entry.pack(pady=5)

        # New password field with security dots
        Label(forgot_window, text="New Password", bg="white", fg="#666666").pack()
        password_entry = ttk.Entry(forgot_window, show="•")
        password_entry.pack(pady=5)

        # Show the password rules to help users
        self._create_password_requirements_label(forgot_window)

        def reset_password():
            # Get the entered info
            username = username_entry.get()
            new_password = password_entry.get()

            # Make sure they filled everything out
            if not username or not new_password:
                messagebox.showerror("Error", "All fields are required!")
                return

            # Check if the new password meets our security rules
            is_valid, message = self.validate_password(new_password)
            if not is_valid:
                messagebox.showerror("Invalid Password", message)
                return

            try:
                # Connect to database and update the password
                conn = self._db_connect()
                cursor = conn.cursor()

                cursor.execute("UPDATE users SET password=%s WHERE username=%s", 
                             (new_password, username))
                conn.commit()

                cursor.close()
                conn.close()

                # Let them know it worked
                messagebox.showinfo("Success", "Password reset successfully!")
                forgot_window.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error connecting to database: {e}")

        # Reset button with a nice orange color to match our theme
        Button(forgot_window, text="Reset Password", bg="#d77337", fg="white", 
               command=reset_password).pack(pady=20)

# This is where our app starts running
if __name__ == "__main__":
    # Create the main window and start the app
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()