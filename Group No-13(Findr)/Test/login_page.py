import tkinter as tk
from tkinter import messagebox
from database import create_connection
import mysql.connector

def open_login_page(previous_window, from_signup=False):
    if previous_window and not from_signup:
        previous_window.destroy()
    
    root = tk.Tk()
    root.title("Login")
    root.geometry("300x300")

    tk.Label(root, text="Email:").pack(pady=(20, 0))
    entry_email = tk.Entry(root)
    entry_email.pack()

    tk.Label(root, text="Password:").pack(pady=(10, 0))
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    def login():
        email = entry_email.get()
        password = entry_password.get()
        
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                from home_page import open_home_page
                open_home_page(root, user[0], user[1])
            else:
                messagebox.showerror("Error", "Invalid email or password")

    btn_login = tk.Button(root, text="Login", command=login)
    btn_login.pack(pady=(20, 0))

    def open_signup():
        from signup_page import open_signup_page
        open_signup_page(root)

    btn_signup = tk.Button(root, text="Sign Up", command=open_signup)
    btn_signup.pack(pady=(10, 0))

    root.mainloop()