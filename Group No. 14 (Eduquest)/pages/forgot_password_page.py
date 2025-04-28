import customtkinter as ctk
from tkinter import messagebox
import re

class ForgotPasswordPage(ctk.CTkFrame):
    def __init__(self, master, app):
        """
        Initialize the forgot password page
        
        :param master: The main application window
        :param app: The main application instance
        """
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout all widgets for the forgot password page
        """
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        container = ctk.CTkFrame(self, fg_color=('#1A1A1A', '#1A1A1A'))
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # Center frame for content
        center_frame = ctk.CTkFrame(container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # App title
        title = ctk.CTkLabel(
            center_frame,
            text="Reset Password",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        title.pack(pady=(0, 30))

        # Form frame
        form_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        form_frame.pack(pady=10)

        # Username field
        ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(size=14),
            text_color="white",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your username",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=(0, 15))

        # Email field
        ctk.CTkLabel(
            form_frame,
            text="Email",
            font=ctk.CTkFont(size=14),
            text_color="white",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter your email",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(pady=(0, 15))

        # New Password field
        ctk.CTkLabel(
            form_frame,
            text="New Password",
            font=ctk.CTkFont(size=14),
            text_color="white",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Password container (for the show/hide toggle)
        password_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_container.pack(fill="x", pady=(0, 15))
        
        self.new_password_entry = ctk.CTkEntry(
            password_container,
            placeholder_text="Enter new password",
            width=350,
            height=40,
            font=ctk.CTkFont(size=14),
            show="•"
        )
        self.new_password_entry.pack(side="left")
        
        # Show/hide password button
        self.show_password_var = ctk.BooleanVar(value=False)
        self.show_password_button = ctk.CTkButton(
            password_container,
            text="👁️",
            width=50,
            height=40,
            command=self.toggle_password_visibility,
            fg_color=("#3C3C3C", "#3C3C3C"),
            hover_color=("#2AB377", "#2AB377")
        )
        self.show_password_button.pack(side="left", padx=(5, 0))

        # Confirm Password field
        ctk.CTkLabel(
            form_frame,
            text="Confirm Password",
            font=ctk.CTkFont(size=14),
            text_color="white",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.confirm_password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Confirm new password",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14),
            show="•"
        )
        self.confirm_password_entry.pack(pady=(0, 20))

        # Password strength indicator
        self.password_strength_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.password_strength_frame.pack(fill="x", pady=(0, 20))
        
        self.password_strength_label = ctk.CTkLabel(
            self.password_strength_frame,
            text="Password Strength: Not Set",
            font=ctk.CTkFont(size=12),
            text_color="#B0B0B0"
        )
        self.password_strength_label.pack(side="left")
        
        # Bind password entry to strength checker
        self.new_password_entry.bind("<KeyRelease>", self.check_password_strength)

        # Reset Password button
        reset_button = ctk.CTkButton(
            form_frame,
            text="Reset Password",
            command=self.reset_password,
            width=400,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#2CC985", "#2CC985"),
            hover_color=("#2AB377", "#2AB377"),
            corner_radius=10
        )
        reset_button.pack(pady=(0, 15))

        # Back to Login button
        back_button = ctk.CTkButton(
            form_frame,
            text="Back to Login",
            command=self.app.show_login_page,
            width=400,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#3C3C3C", "#3C3C3C"),
            hover_color=("#2AB377", "#2AB377"),
            corner_radius=10
        )
        back_button.pack()

    def toggle_password_visibility(self):
        """Toggle password visibility between shown and hidden"""
        if self.new_password_entry.cget("show") == "•":
            self.new_password_entry.configure(show="")
            self.show_password_button.configure(text="🔒")
        else:
            self.new_password_entry.configure(show="•")
            self.show_password_button.configure(text="👁️")

    def check_password_strength(self, event):
        """Check password strength and update indicator"""
        password = self.new_password_entry.get()
        
        if not password:
            self.password_strength_label.configure(text="Password Strength: Not Set", text_color="#B0B0B0")
            return
            
        strength = 0
        remarks = []
        
        # Check length
        if len(password) >= 8:
            strength += 1
        else:
            remarks.append("Too short")
            
        # Check for digits
        if re.search(r"\d", password):
            strength += 1
        else:
            remarks.append("Add numbers")
            
        # Check for uppercase
        if re.search(r"[A-Z]", password):
            strength += 1
        else:
            remarks.append("Add uppercase")
            
        # Check for lowercase
        if re.search(r"[a-z]", password):
            strength += 1
        else:
            remarks.append("Add lowercase")
            
        # Check for special characters
        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password):
            strength += 1
        else:
            remarks.append("Add special chars")
            
        # Update strength indicator
        if strength == 0:
            self.password_strength_label.configure(text="Password Strength: Very Weak", text_color="#E74C3C")
        elif strength == 1:
            self.password_strength_label.configure(text="Password Strength: Weak", text_color="#E67E22")
        elif strength == 2:
            self.password_strength_label.configure(text="Password Strength: Fair", text_color="#F1C40F")
        elif strength == 3:
            self.password_strength_label.configure(text="Password Strength: Good", text_color="#2ECC71")
        elif strength >= 4:
            self.password_strength_label.configure(text="Password Strength: Strong", text_color="#27AE60")
            
        if remarks:
            self.password_strength_label.configure(text=f"{self.password_strength_label.cget('text')} ({', '.join(remarks)})")

    def reset_password(self):
        """Reset password using the app's reset_password method"""
        # Get input values
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate inputs
        if not username or not email or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Check if passwords match
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Check password strength
        if len(new_password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        
        # Call the reset_password method from the app
        success = self.app.reset_password(username, email, new_password, confirm_password)
        
        if success:
            # Clear form after successful password reset
            self.username_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.new_password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            
            # Show login page
            self.app.show_login_page()

def main():
    # Example of how this might be used
    root = ctk.CTk()
    root.title("EduQuest - Reset Password")
    root.geometry("1200x800")
    
    # Configure default theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    forgot_password_page = ForgotPasswordPage(root, root)
    root.mainloop()

if __name__ == "__main__":
    main()