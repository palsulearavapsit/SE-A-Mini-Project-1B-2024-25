import tkinter as tk
from tkinter import messagebox
from database import create_connection
import mysql.connector

def open_signup_page(previous_window):
    if previous_window:
        previous_window.destroy()
    
    root = tk.Tk()
    root.title("Sign Up")
    root.geometry("300x300")

    tk.Label(root, text="Name:").pack(pady=(20, 0))
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="Email:").pack(pady=(10, 0))
    entry_email = tk.Entry(root)
    entry_email.pack()

    tk.Label(root, text="Password:").pack(pady=(10, 0))
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    def signup():
        name = entry_name.get()
        email = entry_email.get()
        password = entry_password.get()
        
        if not name or not email or not password:
            messagebox.showerror("Error", "Name, Email and Password are required")
            return
            
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, password)
                )
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Account created successfully!")
                from login_page import open_login_page
                open_login_page(root, from_signup=True)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to create account: {err}")

    btn_signup = tk.Button(root, text="Sign Up", command=signup)
    btn_signup.pack(pady=(20, 0))

    root.mainloop()