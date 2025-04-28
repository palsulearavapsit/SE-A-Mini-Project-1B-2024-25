import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
from pdf_export import PDFExport
import pandas as pd


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartSpend Application")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'primary': "#2C3E50",      # Dark blue-gray
            'secondary': "#ECF0F1",    # Light gray
            'accent1': "#3498DB",      # Bright blue
            'accent2': "#E74C3C",      # Red
            'text_dark': "#2C3E50",    # Dark text
            'text_light': "#FFFFFF",   # Light text
            'success': "#2ECC71",      # Green
            'warning': "#F1C40F",      # Yellow
            'background': "#F5F6FA"    # Light background
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Configure styles
        self.configure_styles()
        
        # MySQL connection settings
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'M@nas1601',
            'database': 'expense_tracker'
        }
        
        # Initialize database
        self.create_database()
        
        # Variables
        self.current_user = None
        self.current_frame = None
        self.show_password = False
        self.auth_code = None
        
        # Start with login page
        self.show_login_page()
    
    def configure_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        
        # Notebook style (tabs)
        style.configure("TNotebook", background=self.colors['background'])
        style.configure("TNotebook.Tab", padding=[20, 10], background=self.colors['secondary'],
                       foreground=self.colors['text_dark'])
        style.map("TNotebook.Tab",
                 background=[("selected", self.colors['primary'])],
                 foreground=[("selected", self.colors['text_light'])])
        
        # Treeview style
        style.configure("Treeview",
                       background=self.colors['secondary'],
                       foreground=self.colors['text_dark'],
                       fieldbackground=self.colors['secondary'])
        style.configure("Treeview.Heading",
                       background=self.colors['primary'],
                       foreground=self.colors['text_light'],
                       relief="flat")
        style.map("Treeview.Heading",
                 background=[('active', self.colors['accent1'])])
        
        # Combobox style
        style.configure("TCombobox",
                       background=self.colors['secondary'],
                       foreground=self.colors['text_dark'])
        
        # Entry style
        style.configure("TEntry",
                       background=self.colors['secondary'],
                       foreground=self.colors['text_dark'])
    
    def create_custom_button(self, parent, text, command, color=None, width=None):
        if color is None:
            color = self.colors['primary']
        
        # Create a frame to hold the button (for shadow effect)
        frame = tk.Frame(parent, bg=self.colors['background'])
        
        btn = tk.Button(frame, text=text, command=command,
                       bg=color, fg=self.colors['text_light'],
                       font=("Helvetica", 11),
                       relief="flat", borderwidth=0,
                       padx=20, pady=8,
                       cursor="hand2")
        
        if width:
            btn.configure(width=width)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self.colors['accent1'])
            frame.configure(cursor="hand2")
        
        def on_leave(e):
            btn.configure(bg=color)
            frame.configure(cursor="")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        btn.pack(padx=2, pady=2)  # Add padding for shadow effect
        return frame
    
    def create_custom_entry(self, parent, width=20, show=None):
        # Create a frame with border effect
        frame = tk.Frame(parent, bg=self.colors['accent1'], padx=1, pady=1)
        
        entry = tk.Entry(frame,
                        font=("Helvetica", 11),
                        bg=self.colors['secondary'],
                        fg=self.colors['text_dark'],
                        relief="flat",
                        width=width)
        
        if show:
            entry.configure(show=show)
        
        # Hover and focus effects
        def on_enter(e):
            frame.configure(bg=self.colors['primary'])
        
        def on_leave(e):
            if entry != entry.focus_get():
                frame.configure(bg=self.colors['accent1'])
        
        def on_focus_in(e):
            frame.configure(bg=self.colors['primary'])
        
        def on_focus_out(e):
            frame.configure(bg=self.colors['accent1'])
        
        entry.bind("<Enter>", on_enter)
        entry.bind("<Leave>", on_leave)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        entry.pack()
        return entry
    
    def create_custom_label(self, parent, text, size=11, bold=False):
        font_weight = "bold" if bold else "normal"
        return tk.Label(parent,
                       text=text,
                       font=("Helvetica", size, font_weight),
                       bg=self.colors['background'],
                       fg=self.colors['text_dark'])

    def show_login_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create main frame with padding
        login_frame = tk.Frame(self.root, bg=self.colors['background'])
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo/Title
        title_label = self.create_custom_label(login_frame, "SmartSpend", 24, True)
        subtitle_label = self.create_custom_label(login_frame, "Comprehensive Expense Tracking and Management Tool", 12)
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 5))
        subtitle_label.grid(row=1, column=0, columnspan=4, pady=(0, 30))
        
        # Create a container frame for login form with background
        form_frame = tk.Frame(login_frame, bg=self.colors['secondary'], padx=40, pady=30)
        form_frame.grid(row=2, column=0, columnspan=4)
        
        # Username
        username_label = tk.Label(form_frame, text="Username", font=("Helvetica", 11),
                                bg=self.colors['secondary'], fg=self.colors['text_dark'])
        username_label.grid(row=0, column=0, sticky=tk.E, padx=(0, 10))
        
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 11), width=20)
        self.username_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Password
        password_label = tk.Label(form_frame, text="Password", font=("Helvetica", 11),
                                bg=self.colors['secondary'], fg=self.colors['text_dark'])
        password_label.grid(row=0, column=2, sticky=tk.E, padx=(20, 10))
        
        # Password entry with show/hide button
        password_frame = tk.Frame(form_frame, bg=self.colors['secondary'])
        password_frame.grid(row=0, column=3, sticky=tk.W)
        
        self.password_entry = tk.Entry(password_frame, font=("Helvetica", 11), width=20, show="*")
        self.password_entry.pack(side=tk.LEFT)
        
        show_password_btn = tk.Button(password_frame, text="👁", font=("Helvetica", 11),
                                    bg=self.colors['secondary'], fg=self.colors['text_dark'],
                                    relief="flat", command=self.toggle_password_visibility)
        show_password_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Login button
        login_button = tk.Button(form_frame, text="Login", font=("Helvetica", 11),
                               bg=self.colors['primary'], fg=self.colors['text_light'],
                               command=self.login, width=20)
        login_button.grid(row=1, column=0, columnspan=4, pady=(20, 15))
        
        # Links
        links_frame = tk.Frame(form_frame, bg=self.colors['secondary'])
        links_frame.grid(row=2, column=0, columnspan=4)
        
        forgot_password_label = tk.Label(links_frame, text="Forgot Password?",
                                       font=("Helvetica", 10), bg=self.colors['secondary'],
                                       fg=self.colors['accent1'], cursor="hand2")
        forgot_password_label.pack(pady=5)
        forgot_password_label.bind("<Button-1>", lambda e: self.show_forgot_password())
        
        signup_label = tk.Label(links_frame, text="Don't have an account? Sign up",
                              font=("Helvetica", 10), bg=self.colors['secondary'],
                              fg=self.colors['accent1'], cursor="hand2")
        signup_label.pack(pady=5)
        signup_label.bind("<Button-1>", lambda e: self.show_signup_page())
        
        self.current_frame = login_frame
        
        # Add hover effects to links
        for label in [forgot_password_label, signup_label]:
            label.bind("<Enter>", lambda e, l=label: l.configure(fg=self.colors['primary']))
            label.bind("<Leave>", lambda e, l=label: l.configure(fg=self.colors['accent1']))

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def show_forgot_password(self):
        # Create a new window for forgot password
        forgot_window = tk.Toplevel(self.root)
        forgot_window.title("Account Recovery")
        forgot_window.geometry("700x700")
        forgot_window.configure(bg=self.colors['background'])
        forgot_window.resizable(False, False)
        
        # Center the window
        forgot_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                          self.root.winfo_rooty() + 50))
        
        # Title
        title_label = tk.Label(forgot_window, text="Account Recovery", 
                              font=("Arial", 16, "bold"),
                              bg=self.colors['background'], 
                              fg=self.colors['text_dark'])
        title_label.pack(pady=20)
        
        # Username entry
        username_label = tk.Label(forgot_window, text="Username:", 
                                 font=("Arial", 12), 
                                 bg=self.colors['background'], 
                                 fg=self.colors['text_dark'])
        username_label.pack(pady=10)
        
        username_entry = tk.Entry(forgot_window, font=("Arial", 12), width=25)
        username_entry.pack(pady=5)
        
        # Display the security question (will be updated when username is entered) 
        security_label = tk.Label(forgot_window, text="", 
                                 font=("Arial", 12), 
                                 bg=self.colors['background'], 
                                 fg=self.colors['text_dark'])
        security_label.pack(pady=10)
        
        # Security answer entry
        answer_entry = tk.Entry(forgot_window, font=("Arial", 12), width=25)
        answer_entry.pack(pady=5)
        
        # New password entry
        new_password_label = tk.Label(forgot_window, text="New Password:", 
                                     font=("Arial", 12), 
                                     bg=self.colors['background'], 
                                     fg=self.colors['text_dark'])
        new_password_label.pack(pady=10)
        
        # Create a frame for password entry and show/hide button
        password_frame = tk.Frame(forgot_window, bg=self.colors['background'])
        password_frame.pack(pady=5)
        
        new_password_entry = tk.Entry(password_frame, font=("Arial", 12), width=25, show="*")
        new_password_entry.pack(side=tk.LEFT)
        
        # Show/Hide password button
        show_password_var = tk.BooleanVar(value=False)
        show_password_btn = tk.Button(password_frame, text="👁", font=("Arial", 12),
                                    bg=self.colors['background'], fg=self.colors['text_dark'],
                                    relief="flat", command=lambda: self.toggle_forgot_password_visibility(
                                        new_password_entry, show_password_var))
        show_password_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # New auth code entry (initially hidden)
        new_auth_label = tk.Label(forgot_window, text="New Auth Code (6 digits):", 
                                 font=("Arial", 12), 
                                 bg=self.colors['background'], 
                                 fg=self.colors['text_dark'])
        new_auth_entry = tk.Entry(forgot_window, font=("Arial", 12), width=25)
        
        # Reset type selection
        reset_type = tk.StringVar(value="password")
        password_radio = tk.Radiobutton(forgot_window, text="Reset Password", 
                                       variable=reset_type, value="password",
                                       bg=self.colors['background'], 
                                       fg=self.colors['text_dark'],
                                       command=lambda: self.toggle_reset_fields(
                                           forgot_window, reset_type.get(),
                                           new_password_label, new_password_entry,
                                           new_auth_label, new_auth_entry))
        password_radio.pack(pady=10)
        
        auth_radio = tk.Radiobutton(forgot_window, text="Reset Auth Code", 
                                   variable=reset_type, value="auth",
                                   bg=self.colors['background'], 
                                   fg=self.colors['text_dark'],
                                   command=lambda: self.toggle_reset_fields(
                                       forgot_window, reset_type.get(),
                                       new_password_label, new_password_entry,
                                       new_auth_label, new_auth_entry))
        auth_radio.pack(pady=5)
        
        def update_security_question(*args):
            username = username_entry.get()
            if username:
                try:
                    conn = mysql.connector.connect(**self.db_config)
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT security_question FROM users WHERE username = %s", (username,))
                    result = cursor.fetchone()
                    
                    if result:
                        security_label.config(text=result[0])
                    else:
                        security_label.config(text="Username not found")
                    
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                security_label.config(text="")
        
        # Bind username entry to update security question
        username_entry.bind('<KeyRelease>', update_security_question)
        
        def verify_and_reset():
            username = username_entry.get()
            answer = answer_entry.get()
            reset_type_value = reset_type.get()
            
            if not username or not answer:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            try:
                conn = mysql.connector.connect(**self.db_config)
                cursor = conn.cursor()
                
                # Get user's security question and answer
                cursor.execute("""
                    SELECT id, security_question, security_answer 
                    FROM users 
                    WHERE username = %s
                """, (username,))
                
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Error", "Username not found")
                    conn.close()
                    return
                
                user_id, stored_question, stored_answer = result
                
                # Verify answer
                if answer.lower() != stored_answer.lower():
                    messagebox.showerror("Error", "Incorrect security answer")
                    conn.close()
                    return
                
                if reset_type_value == "password":
                    new_password = new_password_entry.get()
                    if not new_password:
                        messagebox.showerror("Error", "Please enter a new password")
                        conn.close()
                        return
                    
                    # Update password
                    cursor.execute("UPDATE users SET password = %s WHERE id = %s", 
                                  (new_password, user_id))
                else:
                    new_auth = new_auth_entry.get()
                    if not new_auth:
                        messagebox.showerror("Error", "Please enter a new auth code")
                        conn.close()
                        return
                    
                    # Validate auth code (6 digits)
                    if not re.match(r"^\d{6}$", new_auth):
                        messagebox.showerror("Error", "Authentication code must be 6 digits")
                        conn.close()
                        return
                    
                    # Update auth code
                    cursor.execute("UPDATE users SET auth_code = %s WHERE id = %s", 
                                  (new_auth, user_id))
                
                conn.commit()
                conn.close()
                
                success_message = "Password has been reset successfully!" if reset_type_value == "password" else "Authentication code has been reset successfully!"
                messagebox.showinfo("Success", success_message)
                forgot_window.destroy()
                self.show_login_page()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
                try:
                    conn.close()
                except:
                    pass
        
        # Verify button
        verify_button = tk.Button(forgot_window, text="Verify & Reset", 
                                 font=("Arial", 12), 
                                 bg=self.colors['primary'], 
                                 fg=self.colors['text_light'], 
                                 command=verify_and_reset)
        verify_button.pack(pady=20)
        
        # Make window modal
        forgot_window.transient(self.root)
        forgot_window.grab_set()
        self.root.wait_window(forgot_window)
    
    def toggle_reset_fields(self, window, reset_type, password_label, password_entry, 
                           auth_label, auth_entry):
        if reset_type == "password":
            password_label.pack(pady=10)
            password_entry.pack(pady=5)
            auth_label.pack_forget()
            auth_entry.pack_forget()
        else:
            password_label.pack_forget()
            password_entry.pack_forget()
            auth_label.pack(pady=10)
            auth_entry.pack(pady=5)
    
    def show_signup_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        signup_frame = tk.Frame(self.root, bg=self.colors['background'])
        signup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title_label = tk.Label(signup_frame, text="SmartSpend - Sign Up", font=("Arial", 20, "bold"), bg=self.colors['background'], fg=self.colors['text_dark'])
        title_label.grid(row=0, column=0, columnspan=3, pady=20)
        
        # Username
        username_label = tk.Label(signup_frame, text="Username:", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        username_label.grid(row=1, column=0, sticky=tk.W, pady=10)
        self.new_username_entry = tk.Entry(signup_frame, font=("Arial", 12), width=25)
        self.new_username_entry.grid(row=1, column=1, columnspan=2, pady=10)
        
        # Email
        email_label = tk.Label(signup_frame, text="Email:", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        email_label.grid(row=2, column=0, sticky=tk.W, pady=10)
        self.email_entry = tk.Entry(signup_frame, font=("Arial", 12), width=25)
        self.email_entry.grid(row=2, column=1, columnspan=2, pady=10)
        
        # Password
        password_label = tk.Label(signup_frame, text="Password:", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        password_label.grid(row=3, column=0, sticky=tk.W, pady=10)
        self.new_password_entry = tk.Entry(signup_frame, font=("Arial", 12), width=25, show="*")
        self.new_password_entry.grid(row=3, column=1, columnspan=2, pady=10)
        
        # Show/Hide Password Button
        show_password_btn = tk.Button(signup_frame, text="👁", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'], 
                                     command=self.toggle_new_password_visibility)
        show_password_btn.grid(row=3, column=4, padx=5, pady=10)
        
        # Confirm Password
        confirm_label = tk.Label(signup_frame, text="Confirm Password:", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        confirm_label.grid(row=4, column=0, sticky=tk.W, pady=10)
        self.confirm_entry = tk.Entry(signup_frame, font=("Arial", 12), width=25, show="*")
        self.confirm_entry.grid(row=4, column=1, columnspan=3, pady=10)
        
        # Authentication Code
        auth_label = tk.Label(signup_frame, text="Set Auth Code (6 digits):", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        auth_label.grid(row=5, column=0, sticky=tk.W, pady=10)
        self.auth_entry = tk.Entry(signup_frame, font=("Arial", 12), width=25)
        self.auth_entry.grid(row=5, column=1, columnspan=2, pady=10)
        
        # Security Question
        security_label = tk.Label(signup_frame, text="Security Question:", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        security_label.grid(row=6, column=0, sticky=tk.W, pady=10)
        self.security_questions = [
            "What is your mother's maiden name?",
            "What was your first pet's name?",
            "What is your favorite childhood book?",
            "What is the name of your first school?",
            "What is your favorite color?"
        ]
        self.security_var = tk.StringVar(value=self.security_questions[0])
        security_menu = ttk.Combobox(signup_frame, textvariable=self.security_var, values=self.security_questions, 
                                    state="readonly", font=("Arial", 12), width=25)
        security_menu.grid(row=6, column=1, columnspan=2, pady=10)
        
        # Security Answer
        answer_label = tk.Label(signup_frame, text="Security Answer:", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        answer_label.grid(row=7, column=0, sticky=tk.W, pady=10)
        self.security_answer_entry = tk.Entry(signup_frame, font=("Arial", 12), width=25)
        self.security_answer_entry.grid(row=7, column=1, columnspan=2, pady=10)
        
        # Signup button
        signup_button = tk.Button(signup_frame, text="Sign Up", font=("Arial", 12), bg=self.colors['primary'], fg=self.colors['text_light'], 
                                 command=self.signup, width=10)
        signup_button.grid(row=8, column=0, columnspan=3, pady=20)
        
        # Login link
        login_label = tk.Label(signup_frame, text="Already have an account? Login", font=("Arial", 10), 
                              bg=self.colors['background'], fg=self.colors['accent1'], cursor="hand2")
        login_label.grid(row=9, column=0, columnspan=3)
        login_label.bind("<Button-1>", lambda e: self.show_login_page())
        
        self.current_frame = signup_frame
    
    def toggle_new_password_visibility(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.new_password_entry.config(show="")
        else:
            self.new_password_entry.config(show="*")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, username, auth_code FROM users WHERE username = %s AND password = %s", 
                          (username, password))
            user = cursor.fetchone()
            
            conn.close()
            
            if user:
                # Show 2-step authentication dialog
                self.auth_user_id = user[0]
                self.auth_username = user[1]
                self.auth_code_from_db = user[2]
                self.show_auth_dialog()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def show_auth_dialog(self):
        auth_dialog = tk.Toplevel(self.root)
        auth_dialog.title("Two-Step Authentication")
        auth_dialog.geometry("300x150")
        auth_dialog.configure(bg=self.colors['background'])
        auth_dialog.resizable(False, False)
        
        # Center the dialog
        auth_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                        self.root.winfo_rooty() + 50))
        
        # Authentication code entry
        auth_label = tk.Label(auth_dialog, text="Enter your authentication code:", 
                             font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        auth_label.pack(pady=10)
        
        auth_entry = tk.Entry(auth_dialog, font=("Arial", 12), width=10, show="*")
        auth_entry.pack(pady=10)
        
        def verify_auth():
            entered_code = auth_entry.get()
            
            try:
                conn = mysql.connector.connect(**self.db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT auth_code FROM users WHERE id = %s", (self.auth_user_id,))
                stored_code = cursor.fetchone()[0]
                conn.close()
                
                if entered_code == stored_code:
                    auth_dialog.destroy()
                    self.current_user = {"id": self.auth_user_id, "username": self.auth_username}
                    self.show_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid authentication code")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        
        # Verify button
        verify_button = tk.Button(auth_dialog, text="Verify", font=("Arial", 12), 
                                 bg=self.colors['primary'], fg=self.colors['text_light'], command=verify_auth)
        verify_button.pack(pady=10)
        
        # Make dialog model
        auth_dialog.transient(self.root)
        auth_dialog.grab_set()
        self.root.wait_window(auth_dialog)
    
    def signup(self):
        username = self.new_username_entry.get()
        email = self.email_entry.get()
        password = self.new_password_entry.get()
        confirm = self.confirm_entry.get()
        auth_code = self.auth_entry.get()
        security_question = self.security_var.get()
        security_answer = self.security_answer_entry.get()
        
        # Validate fields (makes sure that the user has not left any field empty)
        if not username or not email or not password or not confirm or not auth_code or not security_answer:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        #Validate password (makes sure the confirmed password matches with the current password)
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Validate email (makes sure the email is in a valid format)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Validate auth code (6 digits)
        if not re.match(r"^\d{6}$", auth_code):
            messagebox.showerror("Error", "Authentication code must be 6 digits")
            return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (username, email, password, auth_code, security_question, security_answer) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, email, password, auth_code, security_question, security_answer))
            conn.commit()
            
            # Get the user ID for the new user
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()[0]
            
            # Add default categories
            default_categories = [
                ("Food", "#e74c3c", user_id),
                ("Transportation", "#3498db", user_id),
                ("Entertainment", "#2ecc71", user_id),
                ("Shopping", "#f39c12", user_id),
                ("Bills", "#9b59b6", user_id),
                ("Salary", "#1abc9c", user_id)
            ]
            
            cursor.executemany("INSERT INTO categories (name, color, user_id) VALUES (%s, %s, %s)", 
                              default_categories)
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Account created successfully! You can now login.")
            self.show_login_page()
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry error
                messagebox.showerror("Error", "Username or email already exists")
            else:
                messagebox.showerror("Database Error", f"Error: {err}")
    
    def show_dashboard(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X)
        
        welcome_label = tk.Label(header_frame, text=f"Welcome, {self.current_user['username']}", 
                                font=("Arial", 14, "bold"), bg=self.colors['primary'], fg=self.colors['text_light'], padx=10, pady=5)
        welcome_label.pack(side=tk.LEFT)
        
        logout_button = tk.Button(header_frame, text="Logout", font=("Arial", 12), bg=self.colors['background'], fg=self.colors['text_dark'], 
                                 command=self.logout)
        logout_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Tab control
        tab_control = ttk.Notebook(main_frame)
        
        # Style for tabs
        style = ttk.Style()
        style.configure("TNotebook", background=self.colors['background'])
        style.configure("TNotebook.Tab", background=self.colors['secondary'], foreground=self.colors['text_dark'], padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", self.colors['primary'])], foreground=[("selected", self.colors['text_light'])])
        
        # Dashboard tab
        dashboard_tab = tk.Frame(tab_control, bg=self.colors['background'])
        tab_control.add(dashboard_tab, text="DASHBOARD")
        
        # Analysis tab
        analysis_tab = tk.Frame(tab_control, bg=self.colors['background'])
        tab_control.add(analysis_tab, text="ANALYSIS")
        
        # Account info tab
        account_tab = tk.Frame(tab_control, bg=self.colors['background'])
        tab_control.add(account_tab, text="ACCOUNT INFO")
        
        # Category tab
        category_tab = tk.Frame(tab_control, bg=self.colors['background'])
        tab_control.add(category_tab, text="CATEGORY")
        
        tab_control.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)
        
        # Setup each tab
        self.setup_dashboard_tab(dashboard_tab)
        self.setup_analysis_tab(analysis_tab)
        self.setup_account_tab(account_tab)
        self.setup_category_tab(category_tab)
        
        self.current_frame = main_frame
    
    def setup_dashboard_tab(self, parent):
        # Main container with padding
        main_container = tk.Frame(parent, bg=self.colors['background'], padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for adding transactions
        top_frame = tk.Frame(main_container, bg=self.colors['secondary'], padx=20, pady=20)
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add subtle shadow effect to frames
        def add_shadow(widget):
            widget.configure(relief="ridge", borderwidth=1)
        
        add_shadow(top_frame)
        
        # Title for transaction section with icon
        title_label = tk.Label(top_frame, text="💸 Add New Transaction",
                             font=("Helvetica", 14, "bold"),
                             bg=self.colors['secondary'],
                             fg=self.colors['text_dark'])
        title_label.grid(row=0, column=0, columnspan=6, pady=(0, 20), sticky=tk.W)
        
        # Amount
        amount_label = tk.Label(top_frame, text="Amount:", font=("Helvetica", 11),
                                bg=self.colors['secondary'], fg=self.colors['text_dark'])
        amount_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = tk.Entry(top_frame, font=("Helvetica", 11), bg=self.colors['secondary'], fg=self.colors['text_dark'])
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Type (Income/Expense)
        type_label = tk.Label(top_frame, text="Type:", font=("Helvetica", 11),
                                bg=self.colors['secondary'], fg=self.colors['text_dark'])
        type_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.transaction_type = tk.StringVar(value="Expense")
        type_menu = ttk.Combobox(top_frame, textvariable=self.transaction_type,
                                values=["Income", "Expense"], state="readonly",
                                font=("Helvetica", 11), width=10)
        type_menu.grid(row=1, column=3, padx=5, pady=5)
        
        # Category
        category_label = tk.Label(top_frame, text="Category:", font=("Helvetica", 11),
                                bg=self.colors['secondary'], fg=self.colors['text_dark'])
        category_label.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(top_frame, textvariable=self.category_var,
                                         state="readonly", font=("Helvetica", 11), width=15)
        self.category_menu.grid(row=1, column=5, padx=5, pady=5)
        
        # Description
        desc_label = tk.Label(top_frame, text="Description:", font=("Helvetica", 11),
                                bg=self.colors['secondary'], fg=self.colors['text_dark'])
        desc_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.desc_entry = tk.Entry(top_frame, font=("Helvetica", 11), bg=self.colors['secondary'], fg=self.colors['text_dark'])
        self.desc_entry.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky=tk.W)
        
        # Add button
        add_button = tk.Button(top_frame, text="Add Transaction", font=("Helvetica", 11),
                              bg=self.colors['primary'], fg=self.colors['text_light'],
                              command=self.add_transaction)
        add_button.grid(row=2, column=5, padx=5, pady=5)
        
        # Middle frame for summary
        middle_frame = tk.Frame(main_container, bg=self.colors['secondary'], padx=20, pady=20)
        middle_frame.pack(fill=tk.X, pady=(0, 20))
        add_shadow(middle_frame)
        
        # Summary cards
        summary_title = tk.Label(middle_frame, text="📊 Financial Summary",
                               font=("Helvetica", 14, "bold"),
                               bg=self.colors['secondary'],
                               fg=self.colors['text_dark'])
        summary_title.pack(anchor=tk.W, pady=(0, 20))
        
        cards_frame = tk.Frame(middle_frame, bg=self.colors['secondary'])
        cards_frame.pack(fill=tk.X)
        
        # Create summary cards with shadow effect
        income_card, self.income_value = self.create_summary_card(
            cards_frame, "Total Income", "$0.00", self.colors['success'])
        income_card.grid(row=0, column=0, padx=10)
        
        expenses_card, self.expense_value = self.create_summary_card(
            cards_frame, "Total Expenses", "$0.00", self.colors['accent2'])
        expenses_card.grid(row=0, column=1, padx=10)
        
        balance_card, self.balance_value = self.create_summary_card(
            cards_frame, "Current Balance", "$0.00", self.colors['success'])
        balance_card.grid(row=0, column=2, padx=10)
        
        # Bottom frame for transaction history
        bottom_frame = tk.Frame(main_container, bg=self.colors['secondary'], padx=20, pady=20)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        add_shadow(bottom_frame)
        
        # Transaction history title with icon
        history_label = tk.Label(bottom_frame, text="📝 Transaction History",
                               font=("Helvetica", 14, "bold"),
                               bg=self.colors['secondary'],
                               fg=self.colors['text_dark'])
        history_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Treeview with custom style
        style = ttk.Style()
        style.configure("Custom.Treeview",
                       background=self.colors['secondary'],
                       foreground=self.colors['text_dark'],
                       fieldbackground=self.colors['secondary'],
                       borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                       background=self.colors['primary'],
                       foreground=self.colors['text_light'],
                       relief="flat")
        style.map("Custom.Treeview.Heading",
                 background=[('active', self.colors['accent1'])])
        
        # Create Treeview with custom style
        columns = ("id", "date", "type", "category", "amount", "description")
        self.transaction_tree = ttk.Treeview(bottom_frame, columns=columns,
                                           show="headings", height=10,
                                           style="Custom.Treeview")
        
        # Define headings with icons
        icons = {"id": "🔢", "date": "📅", "type": "📋",
                "category": "🏷️", "amount": "💵", "description": "📝"}
        
        for col in columns:
            self.transaction_tree.heading(col, text=f"{icons[col]} {col.title()}")
            self.transaction_tree.column(col, width=100)
        
        # Adjust column widths
        self.transaction_tree.column("id", width=50)
        self.transaction_tree.column("description", width=200)
        
        # Create a frame for the treeview and scrollbar
        tree_frame = tk.Frame(bottom_frame, bg=self.colors['secondary'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL,
                                command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons frame
        button_frame = tk.Frame(bottom_frame, bg=self.colors['secondary'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Export button with icon
        export_button = self.create_custom_button(
            button_frame, "📤 Export to PDF", self.export_to_pdf,
            color=self.colors['accent1'])
        export_button.pack(side=tk.LEFT)
        
        # Delete button with icon
        delete_button = self.create_custom_button(
            button_frame, "🗑️ Delete Selected", self.delete_transaction,
            color=self.colors['accent2'])
        delete_button.pack(side=tk.RIGHT)
        
        # Load initial data
        self.load_categories()
        self.load_transactions()
        self.update_summary()
    
    def create_summary_card(self, parent, title, value, color):
        # Create a frame with shadow effect
        outer_frame = tk.Frame(parent, bg=self.colors['background'])
        
        # Card frame with background color
        card = tk.Frame(outer_frame, bg=color, padx=20, pady=15)
        card.pack(padx=2, pady=2)  # Padding for shadow effect
        
        # Title with icon
        icon = "💰" if "Income" in title else "💳" if "Expenses" in title else "🏦"
        title_label = tk.Label(card, text=f"{icon} {title}",
                             font=("Helvetica", 12),
                             bg=color, fg=self.colors['text_light'])
        title_label.pack()
        
        # Value
        value_label = tk.Label(card, text=value,
                             font=("Helvetica", 16, "bold"),
                             bg=color, fg=self.colors['text_light'])
        value_label.pack()
        
        # Hover effect
        def on_enter(e):
            card.configure(relief="raised", borderwidth=1)
            outer_frame.configure(cursor="hand2")
        
        def on_leave(e):
            card.configure(relief="flat", borderwidth=0)
            outer_frame.configure(cursor="")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return outer_frame, value_label
    
    def export_to_pdf(self):
        # Create authentication dialog
        auth_dialog = tk.Toplevel(self.root)
        auth_dialog.title("Authentication Required")
        auth_dialog.geometry("300x150")
        auth_dialog.configure(bg=self.colors['background'])
        auth_dialog.resizable(False, False)
        
        # Center the dialog
        auth_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                        self.root.winfo_rooty() + 50))
        
        # Authentication code entry
        auth_label = tk.Label(auth_dialog, text="Enter your authentication code:", 
                             font=("Helvetica", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        auth_label.pack(pady=10)
        
        auth_entry = tk.Entry(auth_dialog, font=("Helvetica", 12), width=10, show="*")
        auth_entry.pack(pady=10)
        
        def verify_and_export():
            entered_code = auth_entry.get()
            
            try:
                conn = mysql.connector.connect(**self.db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT auth_code FROM users WHERE id = %s", (self.current_user["id"],))
                stored_code = cursor.fetchone()[0]
                conn.close()
                
                if entered_code == stored_code:
                    auth_dialog.destroy()
                    self._proceed_with_pdf_export()
                else:
                    messagebox.showerror("Error", "Invalid authentication code")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        
        # Verify button
        verify_button = tk.Button(auth_dialog, text="Verify & Export", font=("Helvetica", 12), 
                                 bg=self.colors['primary'], fg=self.colors['text_light'], command=verify_and_export)
        verify_button.pack(pady=10)
    
    def _proceed_with_pdf_export(self):
        # Ask user where to save the PDF file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Financial Report As"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Get currency symbol
        currency_symbol = self.get_currency_symbol()
        
        # Create PDF exporter
        exporter = PDFExport(
            self.db_config,
            self.current_user["id"],
            self.current_user["username"],
            currency_symbol
        )
        
        # Show progress dialog
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title("Exporting to PDF")
        progress_dialog.geometry("300x100")
        progress_dialog.configure(bg=self.colors['background'])
        progress_dialog.resizable(False, False)
        
        # Center the dialog
        progress_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                           self.root.winfo_rooty() + 50))
        
        # Progress message
        progress_label = tk.Label(progress_dialog, text="Generating PDF report...", 
                                 font=("Helvetica", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        progress_label.pack(pady=20)
        
        # Update the UI
        self.root.update()
        
        # Generate the PDF
        success = exporter.generate_pdf(file_path)
        
        # Close progress dialog
        progress_dialog.destroy()
        
        if success:
            messagebox.showinfo("Success", f"Financial report exported successfully to:\n{file_path}")
            
            # Ask if user wants to open the PDF
            if messagebox.askyesno("Open PDF", "Would you like to open the PDF now?"):
                try:
                    import os
                    import platform
                    
                    if platform.system() == 'Darwin':  # macOS
                        os.system(f'open "{file_path}"')
                    elif platform.system() == 'Windows':  # Windows
                        os.system(f'start "" "{file_path}"')
                    else:  # Linux
                        os.system(f'xdg-open "{file_path}"')
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open the PDF: {e}")
        else:
            messagebox.showerror("Error", "Failed to generate PDF report")
    
    def setup_analysis_tab(self, parent):
        # Frame for filters
        filter_frame = tk.Frame(parent, bg=self.colors['background'])
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Period selection
        period_label = tk.Label(filter_frame, text="Period:", font=("Helvetica", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        period_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.period_var = tk.StringVar(value="This Month")
        period_menu = ttk.Combobox(filter_frame, textvariable=self.period_var, 
                                  values=["This Month", "Last Month", "Last 3 Months", "This Year", "All Time"], 
                                  state="readonly", font=("Helvetica", 11), width=15)
        period_menu.grid(row=0, column=1, padx=5, pady=5)
        
        # Generate button
        generate_button = tk.Button(filter_frame, text="Generate Report", font=("Helvetica", 11), bg=self.colors['primary'], fg=self.colors['text_light'], 
                                   command=self.generate_report)
        generate_button.grid(row=0, column=2, padx=20, pady=5)
        
        # Frame for charts
        chart_frame = tk.Frame(parent, bg=self.colors['background'])
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs for different charts
        chart_tabs = ttk.Notebook(chart_frame)
        
        # Income vs Expense tab
        income_expense_tab = tk.Frame(chart_tabs, bg=self.colors['background'])
        chart_tabs.add(income_expense_tab, text="Income vs Expense")
        
        # Category breakdown tab
        category_tab = tk.Frame(chart_tabs, bg=self.colors['background'])
        chart_tabs.add(category_tab, text="Category Breakdown")
        
        # Monthly trend tab
        trend_tab = tk.Frame(chart_tabs, bg=self.colors['background'])
        chart_tabs.add(trend_tab, text="Monthly Trend")
        
        chart_tabs.pack(expand=1, fill=tk.BOTH)
        
        # Setup chart frames
        self.income_expense_frame = tk.Frame(income_expense_tab, bg=self.colors['background'])
        self.income_expense_frame.pack(fill=tk.BOTH, expand=True)
        
        self.category_chart_frame = tk.Frame(category_tab, bg=self.colors['background'])
        self.category_chart_frame.pack(fill=tk.BOTH, expand=True)
        
        self.trend_chart_frame = tk.Frame(trend_tab, bg=self.colors['background'])
        self.trend_chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Generate initial report
        self.generate_report()
    
    def setup_account_tab(self, parent):
        # Account info frame
        account_frame = tk.Frame(parent, bg=self.colors['background'])
        account_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        # Get user info
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT username, email, currency, auth_code FROM users WHERE id = %s", 
                          (self.current_user["id"],))
            user_info = cursor.fetchone()
            conn.close()
            
            if not user_info:
                return
            
            # Title
            title_label = tk.Label(account_frame, text="Account Information", font=("Helvetica", 18, "bold"), 
                                  bg=self.colors['background'], fg=self.colors['text_dark'])
            title_label.grid(row=0, column=0, columnspan=2, pady=20)
            
            # Username
            username_label = tk.Label(account_frame, text="Username:", font=("Helvetica", 14), bg=self.colors['background'], fg=self.colors['text_dark'])
            username_label.grid(row=1, column=0, sticky=tk.W, pady=10)
            username_value = tk.Label(account_frame, text=user_info[0], font=("Helvetica", 14), bg=self.colors['background'], fg=self.colors['text_dark'])
            username_value.grid(row=1, column=1, sticky=tk.W, pady=10)
            
            # Email
            email_label = tk.Label(account_frame, text="Email:", font=("Helvetica", 14), bg=self.colors['background'], fg=self.colors['text_dark'])
            email_label.grid(row=2, column=0, sticky=tk.W, pady=10)
            self.email_value = tk.Entry(account_frame, font=("Helvetica", 14), bg="white", fg="#29292B", width=25)
            self.email_value.insert(0, user_info[1])
            self.email_value.grid(row=2, column=1, sticky=tk.W, pady=10)
            
            # Currency
            currency_label = tk.Label(account_frame, text="Currency:", font=("Helvetica", 14), bg=self.colors['background'], fg=self.colors['text_dark'])
            currency_label.grid(row=3, column=0, sticky=tk.W, pady=10)
            self.currency_var = tk.StringVar(value=user_info[2])
            currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "INR", "CNY"]
            currency_menu = ttk.Combobox(account_frame, textvariable=self.currency_var, values=currencies, 
                                        state="readonly", font=("Helvetica", 14), width=10)
            currency_menu.grid(row=3, column=1, sticky=tk.W, pady=10)
            
            # Authentication Code
            auth_label = tk.Label(account_frame, text="Auth Code:", font=("Helvetica", 14), bg=self.colors['background'], fg=self.colors['text_dark'])
            auth_label.grid(row=4, column=0, sticky=tk.W, pady=10)
            self.auth_value = tk.Entry(account_frame, font=("Helvetica", 14), bg="white", fg="#29292B", width=10)
            self.auth_value.insert(0, user_info[3])
            self.auth_value.grid(row=4, column=1, sticky=tk.W, pady=10)
            
            # Update button
            update_button = tk.Button(account_frame, text="Update Information", font=("Helvetica", 14), bg=self.colors['primary'], fg=self.colors['text_light'], 
                                     command=self.update_account_info)
            update_button.grid(row=5, column=0, columnspan=2, pady=20)
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def setup_category_tab(self, parent):
        # Left frame for adding categories
        left_frame = tk.Frame(parent, bg=self.colors['background'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(left_frame, text="Add New Category", font=("Helvetica", 16, "bold"), 
                              bg=self.colors['background'], fg=self.colors['text_dark'])
        title_label.pack(anchor=tk.W, pady=10)
        
        # Category name
        name_frame = tk.Frame(left_frame, bg=self.colors['background'])
        name_frame.pack(fill=tk.X, pady=10)
        
        name_label = tk.Label(name_frame, text="Category Name:", font=("Helvetica", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        name_label.pack(side=tk.LEFT, padx=5)
        
        self.new_category_entry = tk.Entry(name_frame, font=("Helvetica", 12), width=20)
        self.new_category_entry.pack(side=tk.LEFT, padx=5)
        
        # Category color
        color_frame = tk.Frame(left_frame, bg=self.colors['background'])
        color_frame.pack(fill=tk.X, pady=10)
        
        color_label = tk.Label(color_frame, text="Category Color:", font=("Helvetica", 12), bg=self.colors['background'], fg=self.colors['text_dark'])
        color_label.pack(side=tk.LEFT, padx=5)
        
        self.category_color = "#3498db"  # Default color
        self.color_button = tk.Button(color_frame, text="Select Color", font=("Helvetica", 12), bg=self.category_color, 
                                     fg=self.colors['text_light'], command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5)
        
        # Add button
        add_button = tk.Button(left_frame, text="Add Category", font=("Helvetica", 12), bg=self.colors['primary'], fg=self.colors['text_light'], 
                              command=self.add_category)
        add_button.pack(pady=10)
        
        # Right frame for category list and limits
        right_frame = tk.Frame(parent, bg=self.colors['background'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        list_label = tk.Label(right_frame, text="Your Categories", font=("Helvetica", 16, "bold"), 
                             bg=self.colors['background'], fg=self.colors['text_dark'])
        list_label.pack(anchor=tk.W, pady=10)
        
        # Treeview for categories
        columns = ("id", "name", "color", "monthly_limit", "spent", "remaining")
        self.category_tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        self.category_tree.heading("id", text="ID")
        self.category_tree.heading("name", text="Category Name")
        self.category_tree.heading("color", text="Color")
        self.category_tree.heading("monthly_limit", text="Monthly Limit")
        self.category_tree.heading("spent", text="Spent This Month")
        self.category_tree.heading("remaining", text="Remaining")
        
        # Define columns
        self.category_tree.column("id", width=50)
        self.category_tree.column("name", width=150)
        self.category_tree.column("color", width=100)
        self.category_tree.column("monthly_limit", width=100)
        self.category_tree.column("spent", width=100)
        self.category_tree.column("remaining", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.category_tree.yview)
        self.category_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.category_tree.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(right_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=10)
        
        # Set Limit button
        set_limit_button = tk.Button(button_frame, text="Set Monthly Limit", font=("Helvetica", 12), 
                                    bg=self.colors['primary'], fg=self.colors['text_light'], command=self.show_set_limit_dialog)
        set_limit_button.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        delete_button = tk.Button(button_frame, text="Delete Selected", font=("Helvetica", 12), 
                                 bg=self.colors['accent2'], fg=self.colors['text_light'], command=self.delete_category)
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        # Load categories
        self.load_category_tree()
    
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.category_color)[1]
        if color:
            self.category_color = color
            self.color_button.config(bg=color)
    
    def load_categories(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name FROM categories WHERE user_id = %s", (self.current_user["id"],))
            categories = cursor.fetchall()
            
            conn.close()
            
            self.category_menu['values'] = [category[1] for category in categories]
            self.categories_dict = {category[1]: category[0] for category in categories}
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def load_category_tree(self):
        # Clear existing data
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get current month
            current_month = datetime.now().strftime("%Y-%m")
            
            # Get categories with their limits and spending
            cursor.execute("""
                SELECT 
                    c.id, 
                    c.name, 
                    c.color,
                    COALESCE(cl.limit_amount, 0) as monthly_limit,
                    COALESCE(SUM(CASE WHEN t.type = 'Expense' AND DATE_FORMAT(t.date, '%Y-%m') = %s THEN t.amount ELSE 0 END), 0) as spent
                FROM categories c
                LEFT JOIN category_limits cl ON c.id = cl.category_id 
                    AND cl.user_id = c.user_id 
                    AND cl.month_year = %s
                LEFT JOIN transactions t ON c.id = t.category_id 
                    AND t.user_id = c.user_id
                WHERE c.user_id = %s
                GROUP BY c.id, c.name, c.color, cl.limit_amount
            """, (current_month, current_month, self.current_user["id"]))
            
            categories = cursor.fetchall()
            conn.close()
            
            # Get currency symbol
            currency_symbol = self.get_currency_symbol()
            
            for category in categories:
                cat_id, name, color, monthly_limit, spent = category
                remaining = monthly_limit - spent if monthly_limit > 0 else 0
                
                # Format monetary values
                monthly_limit_str = f"{currency_symbol}{monthly_limit:.2f}" if monthly_limit > 0 else "No Limit"
                spent_str = f"{currency_symbol}{spent:.2f}"
                remaining_str = f"{currency_symbol}{remaining:.2f}" if monthly_limit > 0 else "N/A"
                
                # Determine tag for spending status
                if monthly_limit > 0:
                    spent_percentage = (spent / monthly_limit) * 100
                    if spent_percentage >= 100:
                        status_tag = "exceeded"
                    elif spent_percentage >= 80:
                        status_tag = "warning"
                    else:
                        status_tag = "normal"
                else:
                    status_tag = "normal"
                
                # Insert with both category color and status tags
                item_id = self.category_tree.insert("", tk.END, values=(
                    cat_id, name, color, monthly_limit_str, spent_str, remaining_str
                ), tags=(f"color_{color}", status_tag))
                
                # Configure tag with category color
                self.category_tree.tag_configure(f"color_{color}", background=color)
                
                # Configure status tags
                self.category_tree.tag_configure("exceeded", foreground="red")
                self.category_tree.tag_configure("warning", foreground="orange")
                self.category_tree.tag_configure("normal", foreground="black")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def add_category(self):
        category_name = self.new_category_entry.get()
        
        if not category_name:
            messagebox.showerror("Error", "Please enter a category name")
            return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO categories (user_id, name, color) VALUES (%s, %s, %s)", 
                          (self.current_user["id"], category_name, self.category_color))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Category added successfully!")
            self.new_category_entry.delete(0, tk.END)
            self.category_color = "#3498db"  # Reset to default color
            self.color_button.config(bg=self.category_color)
            
            self.load_category_tree()
            self.load_categories()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def delete_category(self):
        selected = self.category_tree.selection()
        
        if not selected:
            messagebox.showerror("Error", "Please select a category to delete")
            return
        
        category_id = self.category_tree.item(selected[0])['values'][0]
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if category is in use
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE category_id = %s", (category_id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                messagebox.showerror("Error", "Cannot delete category that is in use")
                conn.close()
                return
            
            cursor.execute("DELETE FROM categories WHERE id = %s AND user_id = %s", 
                          (category_id, self.current_user["id"]))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Category deleted successfully!")
            self.load_category_tree()
            self.load_categories()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def show_set_limit_dialog(self):
        selected = self.category_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a category to set limit")
            return
        
        category_id = self.category_tree.item(selected[0])['values'][0]
        category_name = self.category_tree.item(selected[0])['values'][1]
        
        # Create dialog
        limit_dialog = tk.Toplevel(self.root)
        limit_dialog.title(f"Set Monthly Limit - {category_name}")
        limit_dialog.geometry("400x200")
        limit_dialog.configure(bg=self.colors['background'])
        limit_dialog.resizable(False, False)
        
        # Center the dialog
        limit_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                        self.root.winfo_rooty() + 50))
        
        # Month selection
        month_frame = tk.Frame(limit_dialog, bg=self.colors['background'])
        month_frame.pack(fill=tk.X, padx=20, pady=10)
        
        month_label = tk.Label(month_frame, text="Select Month:", font=("Helvetica", 12), 
                              bg=self.colors['background'], fg=self.colors['text_dark'])
        month_label.pack(side=tk.LEFT, padx=5)
        
        # Get current month and year
        current_date = datetime.now()
        months = []
        for i in range(-2, 3):  # Show 2 months before and after current month
            date = current_date.replace(day=1) + pd.DateOffset(months=i)
            months.append(date.strftime("%Y-%m"))
        
        self.month_var = tk.StringVar(value=current_date.strftime("%Y-%m"))
        month_menu = ttk.Combobox(month_frame, textvariable=self.month_var, values=months, 
                                 state="readonly", font=("Helvetica", 11), width=10)
        month_menu.pack(side=tk.LEFT, padx=5)
        
        # Limit amount
        amount_frame = tk.Frame(limit_dialog, bg=self.colors['background'])
        amount_frame.pack(fill=tk.X, padx=20, pady=10)
        
        amount_label = tk.Label(amount_frame, text="Limit Amount:", font=("Helvetica", 12), 
                               bg=self.colors['background'], fg=self.colors['text_dark'])
        amount_label.pack(side=tk.LEFT, padx=5)
        
        # Get currency symbol
        currency_symbol = self.get_currency_symbol()
        currency_label = tk.Label(amount_frame, text=currency_symbol, font=("Helvetica", 12), 
                                 bg=self.colors['background'], fg=self.colors['text_dark'])
        currency_label.pack(side=tk.LEFT)
        
        self.limit_amount_entry = tk.Entry(amount_frame, font=("Helvetica", 12), width=15)
        self.limit_amount_entry.pack(side=tk.LEFT, padx=5)
        
        # Try to get existing limit
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT limit_amount 
                FROM category_limits 
                WHERE user_id = %s AND category_id = %s AND month_year = %s
            """, (self.current_user["id"], category_id, self.month_var.get()))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                self.limit_amount_entry.insert(0, str(result[0]))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        
        # Save button
        def save_limit():
            try:
                amount = float(self.limit_amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than zero")
                    return
                
                conn = mysql.connector.connect(**self.db_config)
                cursor = conn.cursor()
                
                # Use REPLACE INTO to handle both insert and update
                cursor.execute("""
                    REPLACE INTO category_limits 
                    (user_id, category_id, month_year, limit_amount) 
                    VALUES (%s, %s, %s, %s)
                """, (self.current_user["id"], category_id, self.month_var.get(), amount))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Category limit set successfully!")
                limit_dialog.destroy()
                self.load_category_tree()  # Refresh the tree view
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        
        save_button = tk.Button(limit_dialog, text="Save Limit", font=("Helvetica", 12), 
                               bg=self.colors['primary'], fg=self.colors['text_light'], command=save_limit)
        save_button.pack(pady=20)
    
    def add_transaction(self):
        amount_str = self.amount_entry.get()
        transaction_type = self.transaction_type.get()
        category = self.category_var.get()
        description = self.desc_entry.get()
        
        # Input validation
        if not amount_str or not category:
            messagebox.showerror("Error", "Please fill in amount and select a category")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero")
                return
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        
        # Get category ID
        category_id = self.categories_dict.get(category)
        if not category_id:
            messagebox.showerror("Error", "Invalid category")
            return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # For expenses, check balance and limits
            if transaction_type == "Expense":
                # Get total income and expenses
                cursor.execute("""
                    SELECT 
                        COALESCE(SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END), 0) as total_income,
                        COALESCE(SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END), 0) as total_expenses
                    FROM transactions 
                    WHERE user_id = %s
                """, (self.current_user["id"],))
                
                result = cursor.fetchone()
                total_income = float(result[0])
                total_expenses = float(result[1])
                current_balance = total_income - total_expenses
                
                # Check if sufficient balance
                if amount > current_balance:
                    messagebox.showerror("Error", 
                        f"Insufficient balance for this expense.\nCurrent Balance: {self.get_currency_symbol()}{current_balance:.2f}")
                    conn.close()
                    return
                
                # Check category monthly limit
                current_month = datetime.now().strftime("%Y-%m")
                cursor.execute("""
                    SELECT 
                        c.name,
                        COALESCE(cl.limit_amount, 0) as monthly_limit,
                        COALESCE(SUM(CASE WHEN t.type = 'Expense' AND DATE_FORMAT(t.date, '%Y-%m') = %s THEN t.amount ELSE 0 END), 0) as spent
                    FROM categories c
                    LEFT JOIN category_limits cl ON c.id = cl.category_id 
                        AND cl.user_id = c.user_id 
                        AND cl.month_year = %s
                    LEFT JOIN transactions t ON c.id = t.category_id 
                        AND t.user_id = c.user_id
                    WHERE c.id = %s AND c.user_id = %s
                    GROUP BY c.name, cl.limit_amount
                """, (current_month, current_month, category_id, self.current_user["id"]))
                
                limit_info = cursor.fetchone()
                
                if limit_info:
                    category_name, monthly_limit, current_spent = limit_info
                    # Convert Decimal to float for calculations
                    monthly_limit = float(monthly_limit)
                    current_spent = float(current_spent)
                    new_total = current_spent + amount
                    
                    if monthly_limit > 0:  # Only check if limit is set
                        if new_total > monthly_limit:
                            # Calculate overage
                            over_amount = new_total - monthly_limit
                            over_percent = (over_amount / monthly_limit) * 100
                            
                            warning = f"""
⚠️ Monthly Limit Warning for {category_name}

Current Status:
• Monthly Limit: {self.get_currency_symbol()}{monthly_limit:.2f}
• Already Spent: {self.get_currency_symbol()}{current_spent:.2f}
• This Expense: {self.get_currency_symbol()}{amount:.2f}
• New Total: {self.get_currency_symbol()}{new_total:.2f}

This expense will exceed your monthly limit by:
• Amount Over: {self.get_currency_symbol()}{over_amount:.2f}
• Percentage Over: {over_percent:.1f}%

Would you like to proceed with this expense anyway?"""
                            
                            if not messagebox.askyesno("Monthly Limit Warning", warning, icon='warning'):
                                conn.close()
                                return
                        
                        elif new_total >= monthly_limit * 0.8:  # Warning at 80%
                            remaining = monthly_limit - current_spent
                            warning = f"""
ℹ️ Budget Alert for {category_name}

This expense will bring you close to your monthly limit:
• Monthly Limit: {self.get_currency_symbol()}{monthly_limit:.2f}
• Currently Spent: {self.get_currency_symbol()}{current_spent:.2f}
• This Expense: {self.get_currency_symbol()}{amount:.2f}
• Remaining After: {self.get_currency_symbol()}{(remaining - amount):.2f}
• Percentage Used: {(new_total / monthly_limit * 100):.1f}%

Would you like to proceed?"""
                            
                            if not messagebox.askyesno("Budget Alert", warning, icon='info'):
                                conn.close()
                                return
            
            # Add the transaction
            cursor.execute("""
                INSERT INTO transactions (user_id, amount, type, category_id, description, date) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.current_user["id"], amount, transaction_type, category_id, description, datetime.now().strftime("%Y-%m-%d")))
            
            conn.commit()
            conn.close()
            
            # Clear fields and refresh data
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.load_transactions()
            self.update_summary()
            self.load_category_tree()
            
            messagebox.showinfo("Success", "Transaction added successfully!")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            try:
                conn.close()
            except:
                pass
    
    def load_transactions(self):
        # Clear existing data
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT t.id, t.date, t.type, c.name, t.amount, t.description, c.color
                FROM transactions t 
                JOIN categories c ON t.category_id = c.id 
                WHERE t.user_id = %s 
                ORDER BY t.date DESC
            """, (self.current_user["id"],))
            
            transactions = cursor.fetchall()
            conn.close()
            
            # Get currency symbol
            currency_symbol = self.get_currency_symbol()
            
            for transaction in transactions:
                # Format amount with currency symbol
                amount = f"{currency_symbol}{transaction[4]:.2f}" if transaction[2] == "Income" else f"-{currency_symbol}{transaction[4]:.2f}"
                
                # Insert into treeview with color tag
                self.transaction_tree.insert("", tk.END, values=(
                    transaction[0], transaction[1], transaction[2], transaction[3], amount, transaction[5]
                ), tags=(transaction[6],))
                
                # Configure tag with category color
                self.transaction_tree.tag_configure(transaction[6], background=transaction[6])
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def delete_transaction(self):
        selected = self.transaction_tree.selection()
        
        if not selected:
            messagebox.showerror("Error", "Please select a transaction to delete")
            return
        
        transaction_id = self.transaction_tree.item(selected[0])['values'][0]
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM transactions WHERE id = %s AND user_id = %s", 
                          (transaction_id, self.current_user["id"]))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Transaction deleted successfully!")
            
            # Refresh data
            self.load_transactions()
            self.update_summary()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def update_summary(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get currency
            cursor.execute("SELECT currency FROM users WHERE id = %s", (self.current_user["id"],))
            currency = cursor.fetchone()[0]
            
            # Get total income
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = %s AND type = 'Income'
            """, (self.current_user["id"],))
            total_income = cursor.fetchone()[0]
            
            # Get total expenses
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = %s AND type = 'Expense'
            """, (self.current_user["id"],))
            total_expenses = cursor.fetchone()[0]
            
            conn.close()
            
            # Calculate balance
            balance = float(total_income) - float(total_expenses)
            
            # Update labels
            currency_symbol = self.get_currency_symbol(currency)
            self.income_value.config(text=f"{currency_symbol}{total_income:.2f}")
            self.expense_value.config(text=f"{currency_symbol}{total_expenses:.2f}")
            
            if balance >= 0:
                self.balance_value.config(text=f"{currency_symbol}{balance:.2f}", fg="blue")
            else:
                self.balance_value.config(text=f"{currency_symbol}{balance:.2f}", fg="red")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def get_currency_symbol(self, currency=None):
        if not currency:
            try:
                conn = mysql.connector.connect(**self.db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT currency FROM users WHERE id = %s", (self.current_user["id"],))
                currency = cursor.fetchone()[0]
                conn.close()
            except mysql.connector.Error:
                return "$"  # Default if error
        
        symbols = {
            "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", 
            "CAD": "C$", "AUD": "A$", "INR": "₹", "CNY": "¥"
        }
        return symbols.get(currency, "$")
    
    def update_account_info(self):
        email = self.email_value.get()
        currency = self.currency_var.get()
        auth_code = self.auth_value.get()
        
        if not email or not auth_code:
            messagebox.showerror("Error", "Email and Auth Code cannot be empty")
            return
        
        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Validate auth code (6 digits)
        if not re.match(r"^\d{6}$", auth_code):
            messagebox.showerror("Error", "Authentication code must be 6 digits")
            return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get current currency
            cursor.execute("SELECT currency FROM users WHERE id = %s", (self.current_user["id"],))
            old_currency = cursor.fetchone()[0]
            
            cursor.execute("UPDATE users SET email = %s, currency = %s, auth_code = %s WHERE id = %s", 
                          (email, currency, auth_code, self.current_user["id"]))
            conn.commit()
            
            # If currency changed, update all transactions display
            if old_currency != currency:
                self.load_transactions()
            
            conn.close()
            
            messagebox.showinfo("Success", "Account information updated successfully!")
            self.update_summary()
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry error
                messagebox.showerror("Error", "Email already exists")
            else:
                messagebox.showerror("Database Error", f"Error: {err}")
    
    def generate_report(self):
        period = self.period_var.get()
        
        # Clear existing charts
        for widget in self.income_expense_frame.winfo_children():
            widget.destroy()
        for widget in self.category_chart_frame.winfo_children():
            widget.destroy()
        for widget in self.trend_chart_frame.winfo_children():
            widget.destroy()
        
        # Get date range based on period
        today = datetime.now()
        if period == "This Month":
            start_date = datetime(today.year, today.month, 1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
        elif period == "Last Month":
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            start_date = datetime(last_month_year, last_month, 1).strftime("%Y-%m-%d")
            if last_month == 12:
                end_date = datetime(last_month_year, last_month, 31).strftime("%Y-%m-%d")
            else:
                end_date = datetime(last_month_year, last_month + 1, 1).strftime("%Y-%m-%d")
        elif period == "Last 3 Months":
            three_months_ago = today.month - 3
            year_offset = 0
            if three_months_ago <= 0:
                three_months_ago += 12
                year_offset = -1
            start_date = datetime(today.year + year_offset, three_months_ago, 1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
        elif period == "This Year":
            start_date = datetime(today.year, 1, 1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
        else:  # All Time
            start_date = "1900-01-01"
            end_date = today.strftime("%Y-%m-%d")
        
        # Generate charts
        self.generate_income_expense_chart(start_date, end_date)
        self.generate_category_chart(start_date, end_date)
        self.generate_trend_chart(start_date, end_date)
    
    def generate_income_expense_chart(self, start_date, end_date):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get total income
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = %s AND type = 'Income' AND date BETWEEN %s AND %s
            """, (self.current_user["id"], start_date, end_date))
            total_income = cursor.fetchone()[0]
            
            # Get total expenses
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = %s AND type = 'Expense' AND date BETWEEN %s AND %s
            """, (self.current_user["id"], start_date, end_date))
            total_expenses = cursor.fetchone()[0]
            
            conn.close()
            
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            
            # Bar chart
            categories = ['Income', 'Expenses']
            values = [float(total_income), float(total_expenses)]
            colors = ['green', 'red']
            
            bars = ax.bar(categories, values, color=colors)
            
            # Get currency symbol
            currency_symbol = self.get_currency_symbol()
            
            # Add values on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{currency_symbol}{height:.2f}', ha='center', va='bottom')
            
            ax.set_title('Income vs Expenses', color=self.colors['text_dark'])
            ax.set_ylabel(f'Amount ({currency_symbol})', color=self.colors['text_dark'])
            ax.tick_params(axis='x', colors=self.colors['text_dark'])
            ax.tick_params(axis='y', colors=self.colors['text_dark'])
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.income_expense_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def generate_category_chart(self, start_date, end_date):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get expenses by category
            cursor.execute("""
                SELECT c.name, SUM(t.amount), c.color
                FROM transactions t 
                JOIN categories c ON t.category_id = c.id 
                WHERE t.user_id = %s AND t.type = 'Expense' AND t.date BETWEEN %s AND %s
                GROUP BY c.name, c.color
            """, (self.current_user["id"], start_date, end_date))
            
            category_data = cursor.fetchall()
            conn.close()
            
            if not category_data:
                # No data to display
                label = tk.Label(self.category_chart_frame, text="No expense data available for this period", 
                                font=("Helvetica", 14), bg=self.colors['background'], fg=self.colors['text_dark'])
                label.pack(pady=50)
                return
            
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            
            # Pie chart
            labels = [item[0] for item in category_data]
            sizes = [float(item[1]) for item in category_data]
            colors = [item[2] for item in category_data]
            
            wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%', 
                                             startangle=90, colors=colors)
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')
            ax.set_title('Expense Breakdown by Category', color=self.colors['text_dark'])
            
            # Add legend
            ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            # Make text color visible
            for autotext in autotexts:
                autotext.set_color('white')
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.category_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def generate_trend_chart(self, start_date, end_date):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get monthly income and expenses
            cursor.execute("""
                SELECT DATE_FORMAT(date, '%Y-%m') as month, 
                       SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) as income,
                       SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) as expense
                FROM transactions 
                WHERE user_id = %s AND date BETWEEN %s AND %s
                GROUP BY month
                ORDER BY month
            """, (self.current_user["id"], start_date, end_date))
            
            monthly_data = cursor.fetchall()
            conn.close()
            
            if not monthly_data:
                # No data to display
                label = tk.Label(self.trend_chart_frame, text="No data available for this period", 
                                font=("Helvetica", 14), bg=self.colors['background'], fg=self.colors['text_dark'])
                label.pack(pady=50)
                return
            
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            
            # Line chart
            months = [item[0] for item in monthly_data]
            incomes = [float(item[1]) for item in monthly_data]
            expenses = [float(item[2]) for item in monthly_data]
            
            ax.plot(months, incomes, 'o-', color='green', label='Income')
            ax.plot(months, expenses, 'o-', color='red', label='Expenses')
            
            # Format x-axis
            if len(months) > 6:
                plt.xticks(rotation=45, ha='right')
            
            # Get currency symbol
            currency_symbol = self.get_currency_symbol()
            
            ax.set_title('Monthly Income and Expenses Trend', color=self.colors['text_dark'])
            ax.set_xlabel('Month', color=self.colors['text_dark'])
            ax.set_ylabel(f'Amount ({currency_symbol})', color=self.colors['text_dark'])
            ax.tick_params(axis='x', colors=self.colors['text_dark'])
            ax.tick_params(axis='y', colors=self.colors['text_dark'])
            ax.legend()
            
            # Adjust layout
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.trend_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def logout(self):
        self.current_user = None
        self.show_login_page()
    
    def create_database(self):
        try:
            # First try to connect to MySQL server and create database if it doesn't exist
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            cursor.execute(f"USE {self.db_config['database']}")
            
            # Create users table with security question fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    auth_code VARCHAR(6) NOT NULL,
                    currency VARCHAR(3) DEFAULT 'USD',
                    security_question VARCHAR(100) NOT NULL,
                    security_answer VARCHAR(100) NOT NULL
                )
            """)
            
            # Create categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    color VARCHAR(7) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Create transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    type ENUM('Income', 'Expense') NOT NULL,
                    category_id INT NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
                )
            """)
            
            # Create category_limits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS category_limits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    category_id INT NOT NULL,
                    month_year VARCHAR(7) NOT NULL,
                    limit_amount DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_limit (user_id, category_id, month_year)
                )
            """)
            
            conn.commit()
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", 
                f"Failed to initialize database: {err}\n\nPlease ensure MySQL server is running and credentials are correct.")
            self.root.destroy()
    
    def toggle_forgot_password_visibility(self, entry, show_var):
        show_var.set(not show_var.get())
        if show_var.get():
            entry.config(show="")
        else:
            entry.config(show="*")



if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()