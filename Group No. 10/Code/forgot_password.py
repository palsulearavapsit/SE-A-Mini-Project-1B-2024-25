import tkinter as tk
from tkinter import messagebox
import mysql.connector

class ForgotPassword:
    def __init__(self, parent, db_config):
        self.parent = parent
        self.db_config = db_config
        
        # Create the forgot password dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Forgot Password")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg="#C9C7BA")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, 
                                        parent.winfo_rooty() + 50))
        
        # Title
        title_label = tk.Label(self.dialog, text="Password Recovery", 
                              font=("Arial", 16, "bold"), bg="#C9C7BA", fg="#29292B")
        title_label.pack(pady=10)
        
        # Username entry
        username_frame = tk.Frame(self.dialog, bg="#C9C7BA")
        username_frame.pack(fill=tk.X, padx=20, pady=5)
        
        username_label = tk.Label(username_frame, text="Username:", 
                                 font=("Arial", 12), bg="#C9C7BA", fg="#29292B")
        username_label.pack(side=tk.LEFT)
        
        self.username_entry = tk.Entry(username_frame, font=("Arial", 12), width=25)
        self.username_entry.pack(side=tk.RIGHT, padx=10)
        
        # Email entry
        email_frame = tk.Frame(self.dialog, bg="#C9C7BA")
        email_frame.pack(fill=tk.X, padx=20, pady=5)
        
        email_label = tk.Label(email_frame, text="Email:", 
                              font=("Arial", 12), bg="#C9C7BA", fg="#29292B")
        email_label.pack(side=tk.LEFT)
        
        self.email_entry = tk.Entry(email_frame, font=("Arial", 12), width=25)
        self.email_entry.pack(side=tk.RIGHT, padx=10)
        
        # Verify button
        verify_button = tk.Button(self.dialog, text="Verify", font=("Arial", 12), 
                                 bg="#29292B", fg="white", command=self.verify_credentials)
        verify_button.pack(pady=15)
        
        # Cancel button
        cancel_button = tk.Button(self.dialog, text="Cancel", font=("Arial", 12), 
                                 bg="#C9C7BA", fg="#29292B", command=self.dialog.destroy)
        cancel_button.pack(pady=5)
        
        # Set focus to username entry
        self.username_entry.focus_set()
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
    def verify_credentials(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        
        if not username or not email:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if username and email match
            cursor.execute("SELECT id FROM users WHERE username = %s AND email = %s", 
                          (username, email))
            user = cursor.fetchone()
            
            conn.close()
            
            if user:
                # Credentials verified, show reset password dialog
                self.dialog.destroy()
                self.show_reset_password_dialog(user[0])
            else:
                messagebox.showerror("Error", "Invalid username or email")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def show_reset_password_dialog(self, user_id):
        reset_dialog = tk.Toplevel(self.parent)
        reset_dialog.title("Reset Password")
        reset_dialog.geometry("400x250")
        reset_dialog.configure(bg="#C9C7BA")
        reset_dialog.resizable(False, False)
        
        # Center the dialog
        reset_dialog.geometry("+%d+%d" % (self.parent.winfo_rootx() + 50, 
                                         self.parent.winfo_rooty() + 50))
        
        # Title
        title_label = tk.Label(reset_dialog, text="Reset Your Password", 
                              font=("Arial", 16, "bold"), bg="#C9C7BA", fg="#29292B")
        title_label.pack(pady=10)
        
        # New password entry
        new_pass_frame = tk.Frame(reset_dialog, bg="#C9C7BA")
        new_pass_frame.pack(fill=tk.X, padx=20, pady=5)
        
        new_pass_label = tk.Label(new_pass_frame, text="New Password:", 
                                 font=("Arial", 12), bg="#C9C7BA", fg="#29292B")
        new_pass_label.pack(side=tk.LEFT)
        
        new_pass_entry = tk.Entry(new_pass_frame, font=("Arial", 12), width=20, show="*")
        new_pass_entry.pack(side=tk.RIGHT, padx=10)
        
        # Confirm password entry
        confirm_frame = tk.Frame(reset_dialog, bg="#C9C7BA")
        confirm_frame.pack(fill=tk.X, padx=20, pady=5)
        
        confirm_label = tk.Label(confirm_frame, text="Confirm Password:", 
                                font=("Arial", 12), bg="#C9C7BA", fg="#29292B")
        confirm_label.pack(side=tk.LEFT)
        
        confirm_entry = tk.Entry(confirm_frame, font=("Arial", 12), width=20, show="*")
        confirm_entry.pack(side=tk.RIGHT, padx=10)
        
        # Reset button
        reset_button = tk.Button(reset_dialog, text="Reset Password", font=("Arial", 12), 
                                bg="#29292B", fg="white", 
                                command=lambda: self.reset_password(
                                    user_id, new_pass_entry.get(), 
                                    confirm_entry.get(), reset_dialog))
        reset_button.pack(pady=15)
        
        # Cancel button
        cancel_button = tk.Button(reset_dialog, text="Cancel", font=("Arial", 12), 
                                 bg="#C9C7BA", fg="#29292B", command=reset_dialog.destroy)
        cancel_button.pack(pady=5)
        
        # Set focus to new password entry
        new_pass_entry.focus_set()
        
        # Make dialog modal
        reset_dialog.transient(self.parent)
        reset_dialog.grab_set()

    
    
    def reset_password(self, user_id, new_password, confirm_password, dialog):
        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Password validation (optional)
        # if len(new_password) < 6:
        #     messagebox.showerror("Error", "Password must be at least 6 characters long")
        #     return
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Update password
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", 
                          (new_password, user_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Password has been reset successfully!")
            dialog.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")