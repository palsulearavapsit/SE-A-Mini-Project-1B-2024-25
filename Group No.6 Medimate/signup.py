from logging import root
import tkinter as tk
from tkinter import ttk
import os
import sys
import pymysql
import re
from tkinter import PhotoImage

class SignupPage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sign Up")
        self.window.geometry("1280x853")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        # Background Image
        self.background_image = PhotoImage(file=r"F:\MINIPROJECT\Signup.png")
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.frame = tk.Frame(self.window, bg='white')
        self.frame.pack(pady=310)

        fields = [
            ("Name:", "name"),
            ("Username:", "username"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Password:", "password", "*")
        ]

        self.entries = {}
        for i, field in enumerate(fields):
            label_text = field[0]
            field_name = field[1]
            show_char = field[2] if len(field) > 2 else ""
            
            label = tk.Label(self.frame, text=label_text)
            label.grid(row=i, column=0, padx=7, pady=1, sticky="e")
            
            entry = tk.Entry(self.frame, show=show_char)
            entry.grid(row=i, column=1, padx=7, pady=1)
            self.entries[field_name] = entry

        self.error_label = tk.Label(self.frame, text="", fg="red")
        self.error_label.grid(row=len(fields), column=0, columnspan=2, pady=1)

        self.submit_button = tk.Button(self.frame, text="Submit", command=self.submit_form, bg="lightgreen")
        self.submit_button.grid(row=len(fields)+1, column=0, columnspan=2, pady=1)

        self.back_button = tk.Button(self.frame, text="Back to Login", command=self.back_to_login, bg="lightgreen")
        self.back_button.grid(row=len(fields)+2, column=0, columnspan=2, pady=1)

    def submit_form(self):
        name = self.entries["name"].get()
        username = self.entries["username"].get()
        phone = self.entries["phone"].get()
        email = self.entries["email"].get()
        password = self.entries["password"].get()

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            self.error_label.config(text="Invalid email format.", fg="red")
            return

        # Phone number validation (10 digits)
        if not phone.isdigit() or len(phone) != 10:
            self.error_label.config(text="Phone number must be exactly 10 digits.", fg="red")
            return

        # Save to database
        connection = pymysql.connect(host='localhost', user='root', password='Drishti2005@', database='medimate')
        cur = connection.cursor()
        sql = "INSERT INTO login(name, username, phone, email, password) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (name, username, phone, email, password))
        connection.commit()
        connection.close()

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.error_label.config(text="Signup successful! Please login.", fg="green")
        self.window.after(2000, self.back_to_login)

    def back_to_login(self):
        self.window.destroy()
        from login import LoginPage
        login_page = LoginPage()

    def run(self):
        self.window.mainloop()

# To run the app
if __name__ == "__main__":
    app = SignupPage()
    app.run()