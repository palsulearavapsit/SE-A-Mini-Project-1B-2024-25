import customtkinter as ctk
from tkinter import messagebox
import re

class CreateAccountPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Main container with gradient background
        container = ctk.CTkFrame(
            self, 
            fg_color=("#1A1A1A", "#1A1A1A"),
            corner_radius=0
        )
        container.pack(fill="both", expand=True, padx=0, pady=0)

        # Center frame for create account content
        center_frame = ctk.CTkFrame(
            container, 
            fg_color="transparent",
            corner_radius=0
        )
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = ctk.CTkLabel(
            center_frame,
            text="Create Account",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#2CC985"
        )
        title.pack(pady=(0, 20))

        # Subtitle
        subtitle = ctk.CTkLabel(
            center_frame,
            text="Join EduQuest Today",
            font=ctk.CTkFont(size=18, weight="normal"),
            text_color="#E0E0E0"
        )
        subtitle.pack(pady=(0, 30))

        # Form frame
        form_frame = ctk.CTkFrame(
            center_frame, 
            fg_color="transparent"
        )
        form_frame.pack(pady=20)

        # Username field with icon
        username_frame = ctk.CTkFrame(
            form_frame, 
            fg_color="transparent"
        )
        username_frame.pack(fill="x", pady=(0, 15))

        username_icon = ctk.CTkLabel(
            username_frame, 
            text="👤", 
            font=ctk.CTkFont(size=20)
        )
        username_icon.pack(side="left", padx=(0, 10))

        self.username_entry = ctk.CTkEntry(
            username_frame,
            placeholder_text="Username",
            width=350,
            height=50,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=("#2CC985", "#2CC985"),
            fg_color="transparent"
        )
        self.username_entry.pack(side="left", expand=True, fill="x")

        # Email field with icon
        email_frame = ctk.CTkFrame(
            form_frame, 
            fg_color="transparent"
        )
        email_frame.pack(fill="x", pady=(0, 15))

        email_icon = ctk.CTkLabel(
            email_frame, 
            text="✉️", 
            font=ctk.CTkFont(size=20)
        )
        email_icon.pack(side="left", padx=(0, 10))

        self.email_entry = ctk.CTkEntry(
            email_frame,
            placeholder_text="Email",
            width=350,
            height=50,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=("#2CC985", "#2CC985"),
            fg_color="transparent"
        )
        self.email_entry.pack(side="left", expand=True, fill="x")

        # Password field with icon
        password_frame = ctk.CTkFrame(
            form_frame, 
            fg_color="transparent"
        )
        password_frame.pack(fill="x", pady=(0, 15))

        password_icon = ctk.CTkLabel(
            password_frame, 
            text="🔒", 
            font=ctk.CTkFont(size=20)
        )
        password_icon.pack(side="left", padx=(0, 10))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Password",
            width=350,
            height=50,
            font=ctk.CTkFont(size=14),
            show="•",
            border_width=2,
            border_color=("#2CC985", "#2CC985"),
            fg_color="transparent"
        )
        self.password_entry.pack(side="left", expand=True, fill="x")

        # Confirm Password field with icon
        confirm_password_frame = ctk.CTkFrame(
            form_frame, 
            fg_color="transparent"
        )
        confirm_password_frame.pack(fill="x", pady=(0, 15))

        confirm_password_icon = ctk.CTkLabel(
            confirm_password_frame, 
            text="🔑", 
            font=ctk.CTkFont(size=20)
        )
        confirm_password_icon.pack(side="left", padx=(0, 10))

        self.confirm_password_entry = ctk.CTkEntry(
            confirm_password_frame,
            placeholder_text="Confirm Password",
            width=350,
            height=50,
            font=ctk.CTkFont(size=14),
            show="•",
            border_width=2,
            border_color=("#2CC985", "#2CC985"),
            fg_color="transparent"
        )
        self.confirm_password_entry.pack(side="left", expand=True, fill="x")

        # Create Account button
        create_account_btn = ctk.CTkButton(
            form_frame,
            text="Create Account",
            command=self.create_account,
            width=400,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#2CC985", "#2CC985"),
            hover_color=("#25A36F", "#25A36F"),
            corner_radius=15,
            border_width=2,
            border_color=("white", "white")
        )
        create_account_btn.pack(pady=(20, 10))

        # Back to Login button
        back_to_login_btn = ctk.CTkButton(
            form_frame,
            text="Back to Login",
            command=self.go_to_login,
            width=400,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover_color=("#3C3C3C", "#3C3C3C"),
            text_color=("white", "white"),
            border_width=2,
            border_color=("#2CC985", "#2CC985"),
            corner_radius=15
        )
        back_to_login_btn.pack(pady=(10, 0))

        # Add hover and focus effects
        self.add_entry_effects(self.username_entry)
        self.add_entry_effects(self.email_entry)
        self.add_entry_effects(self.password_entry)
        self.add_entry_effects(self.confirm_password_entry)

    def add_entry_effects(self, entry):
        """Add hover and focus effects to entry widgets"""
        entry.bind("<FocusIn>", lambda e: entry.configure(border_color=("#2CC985", "#2CC985")))
        entry.bind("<FocusOut>", lambda e: entry.configure(border_color=("#4A4A4A", "#4A4A4A")))

    def validate_username(self, username):
        """Validate username format"""
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            messagebox.showerror("Invalid Username", "Username must be 3-20 characters long and contain only letters, numbers, and underscores")
            return False
        return True

    def validate_email(self, email):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return False
        return True

    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 8:
            messagebox.showerror("Weak Password", "Password must be at least 8 characters long")
            return False
        
        # Check for at least one uppercase, one lowercase, one number
        if not re.search(r'[A-Z]', password):
            messagebox.showerror("Weak Password", "Password must contain at least one uppercase letter")
            return False
        
        if not re.search(r'[a-z]', password):
            messagebox.showerror("Weak Password", "Password must contain at least one lowercase letter")
            return False
        
        if not re.search(r'\d', password):
            messagebox.showerror("Weak Password", "Password must contain at least one number")
            return False
        
        return True

    def create_account(self):
        """Create a new user account"""
        # Get input values
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate username
        if not username:
            messagebox.showerror("Error", "Username is required")
            return
        
        if not self.validate_username(username):
            messagebox.showerror("Error", "Username must be at least 4 characters and contain only letters, numbers, and underscores")
            return
        
        # Validate email
        if not email:
            messagebox.showerror("Error", "Email is required")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Validate password
        if not password or not confirm_password:
            messagebox.showerror("Error", "Password and Confirm Password are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not self.validate_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters and include uppercase, lowercase, numbers, and special characters")
            return
        
        # Call register method from the app with full_name set to None for now (could add this field later)
        success = self.app.register(username, email, password)
        
        if success:
            # Clear form after successful registration
            self.username_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            
            # Show login page
            self.app.show_login_page()

    def go_to_login(self):
        """Navigate to login page"""
        self.app.show_login_page()