import customtkinter as ctk
from tkinter import messagebox
import re

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, app):
        """
        Initialize the login page
        
        :param master: The main application window
        :param app: The main application instance
        """
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout all widgets for the login page
        """
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        container = ctk.CTkFrame(self, fg_color=('#1A1A1A', '#1A1A1A'))
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # Center frame for login content
        center_frame = ctk.CTkFrame(container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # App title
        title = ctk.CTkLabel(
            center_frame,
            text="EduQuest",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="white"
        )
        title.pack(pady=(0, 20))

        # Login form frame
        form_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        form_frame.pack(pady=20)

        # Username field
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Username",
            width=400,
            height=50,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=(0, 10))

        # Password field container (for show/hide functionality)
        password_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_container.pack(fill="x", pady=(0, 10))

        # Password field
        self.password_entry = ctk.CTkEntry(
            password_container,
            placeholder_text="Password",
            width=400,
            height=50,
            font=ctk.CTkFont(size=14),
            show="•"
        )
        self.password_entry.pack(side="left")

        # Show/hide password button
        self.show_password_var = ctk.BooleanVar(value=False)
        self.show_password_button = ctk.CTkButton(
            password_container,
            text="👁️",
            width=50,
            height=50,
            command=self.toggle_password_visibility,
            fg_color=("#3C3C3C", "#3C3C3C"),
            hover_color=("#2AB377", "#2AB377")
        )
        self.show_password_button.pack(side="left", padx=(5, 0))

        # Login button
        login_btn = ctk.CTkButton(
            form_frame,
            text="Login",
            command=self.login,
            width=400,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#2CC985", "#2CC985"),
            hover_color=("#2AB377", "#2AB377"),
            corner_radius=10
        )
        login_btn.pack(pady=(0, 10))

        # Create Account button
        create_account_btn = ctk.CTkButton(
            form_frame,
            text="Create Account",
            command=self.go_to_create_account,
            width=400,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#3C3C3C", "#3C3C3C"),
            hover_color=("#2AB377", "#2AB377"),
            corner_radius=10
        )
        create_account_btn.pack(pady=(0, 10))

        # Message label for feedback
        self.message_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="red"
        )
        self.message_label.pack(pady=(0, 10))

        # Forgot Password link
        forgot_password_btn = ctk.CTkButton(
            form_frame,
            text="Forgot Password?",
            command=self.forgot_password,
            width=400,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            text_color=("#2CC985", "#2CC985"),
            font=ctk.CTkFont(size=12)
        )
        forgot_password_btn.pack(pady=(5, 0))

    def toggle_password_visibility(self):
        """Toggle password visibility between shown and hidden"""
        if self.password_entry.cget("show") == "•":
            self.password_entry.configure(show="")
            self.show_password_button.configure(text="🔒")
        else:
            self.password_entry.configure(show="•")
            self.show_password_button.configure(text="👁️")

    def login(self):
        """Handle login button click."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate inputs
        if not username:
            self.message_label.configure(text="Please enter a username", text_color="red")
            return
            
        if not password:
            self.message_label.configure(text="Please enter a password", text_color="red")
            return
        
        # Attempt login via app's login method
        success = self.app.login(username, password)
        
        if success:
            self.message_label.configure(text="Login successful!", text_color="green")
            self.clear_form()
            self.app.show_dashboard_page()
        else:
            self.message_label.configure(text="Invalid username or password", text_color="red")
    
    def clear_form(self):
        """Clear the form fields."""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def go_to_create_account(self):
        """Navigate to create account page"""
        # Clear current entries before navigating
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        
        # Call method to show create account page
        self.app.show_create_account_page()

    def forgot_password(self):
        """Navigate to forgot password page"""
        # Clear current entries before navigating
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        
        # Call method to show forgot password page
        self.app.show_forgot_password()

def main():
    # Example of how this might be used
    root = ctk.CTk()
    root.title("EduQuest Login")
    root.geometry("1200x800")
    
    # Configure default theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Create a dummy app object for testing
    class DummyApp:
        def show_create_account_page(self):
            print("Show create account page")
            
        def show_forgot_password(self):
            print("Show forgot password page")
            
        def login(self, username, password):
            print(f"Login with username: {username} and password: {password}")
    
    dummy_app = DummyApp()
    
    login_page = LoginPage(root, dummy_app)
    login_page.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()