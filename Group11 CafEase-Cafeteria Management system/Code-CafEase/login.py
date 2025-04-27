from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
import mysql.connector
import subprocess

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1150x600+100+50")
        self.root.resizable(False, False)
        
        # ====== Background Image ======
        self.bg = ImageTk.PhotoImage(file="C:/images/cafetria23.jpg")  # Ensure correct path
        self.bg_label = Label(self.root, image=self.bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # ====== Login Frame ======
        self.frame = Frame(self.root, bg="white")
        self.frame.place(x=150, y=150, height=450, width=550)

        Label(self.frame, text="Login Here", font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=90, y=30)
        Label(self.frame, text="Accountant User Login Area", font=("Goudy Old Style", 15, "bold"), fg="#d25d17", bg="white").place(x=90, y=100)

        # Username Entry
        Label(self.frame, text="Username", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=90, y=140)
        self.username_var = StringVar()
        self.username_entry = Entry(self.frame, font=("Times New Roman", 15), bg="lightgray", textvariable=self.username_var)
        self.username_entry.place(x=90, y=170, width=350, height=35)

        # Password Entry
        Label(self.frame, text="Password", font=("Goudy Old Style", 15, "bold"), fg="gray", bg="white").place(x=90, y=210)
        self.password_var = StringVar()
        self.password_entry = Entry(self.frame, font=("Times New Roman", 15), bg="lightgray", show="•", textvariable=self.password_var)
        self.password_entry.place(x=90, y=240, width=350, height=35)

        # Show/Hide Password Checkbox
        self.show_password = IntVar()
        Checkbutton(self.frame, text="Show Password", variable=self.show_password, command=self.toggle_password, bg="white").place(x=90, y=280)

        # Buttons
        self.forgot_btn = Button(self.frame, text="Forgot Password?", bg="white", fg="#d77337", bd=0, font=("Times New Roman", 12), command=self.forgot_password)
        self.forgot_btn.place(x=250, y=278)

        self.login_btn = Button(self.root, text="Login", fg="white", bg="#d77337", font=("Times New Roman", 20), command=self.login)
        self.login_btn.place(x=230, y=470, width=180, height=40)

        self.signup_btn = Button(self.root, text="Sign Up", fg="white", bg="#00cc66", font=("Times New Roman", 20), command=self.open_signup)
        self.signup_btn.place(x=430, y=470, width=180, height=40)

    def toggle_password(self):
        """Show or Hide Password."""
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = mysql.connector.connect(host="127.0.0.1", user="root", password="12345", database="cafe_billing")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()

            if user and user[0] == password:
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()  # Close login window
                subprocess.Popen(["python", "dashboard.py"])  # Open dashboard.py

            else:
                messagebox.showerror("Error", "Invalid username or password")

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")

    def open_signup(self):
        """Open the sign-up window."""
        signup_window = Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("400x300")
        signup_window.configure(bg="white")

        Label(signup_window, text="Sign Up", font=("Helvetica", 18, "bold"), bg="white", fg="#333333").pack(pady=20)

        Label(signup_window, text="Username", bg="white", fg="#666666").pack()
        username_entry = ttk.Entry(signup_window)
        username_entry.pack(pady=5)

        Label(signup_window, text="Password", bg="white", fg="#666666").pack()
        password_entry = ttk.Entry(signup_window, show="•")
        password_entry.pack(pady=5)

        def register():
            """Register new user in MySQL database."""
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                conn = mysql.connector.connect(host="127.0.0.1", user="root", password="12345", database="cafe_billing")
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists!")
                    return

                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "User  registered successfully!")
                signup_window.destroy()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error connecting to database: {e}")

        Button(signup_window, text="Sign Up", bg="#00cc66", fg="white", font=("Helvetica", 12), relief="flat", padx=20, pady=10, cursor="hand2", command=register).pack(pady=20)

    def forgot_password(self):
        """Reset password functionality."""
        forgot_window = Toplevel(self.root)
        forgot_window.title("Reset Password")
        forgot_window.geometry("400x250")
        forgot_window.configure(bg="white")

        Label(forgot_window, text="Reset Password", font=("Helvetica", 18, "bold"), bg="white", fg="#333333").pack(pady=10)

        Label(forgot_window, text="Username", bg="white", fg="#666666").pack()
        username_entry = ttk.Entry(forgot_window)
        username_entry.pack(pady=5)

        Label(forgot_window, text="New Password", bg="white", fg="#666666").pack()
        password_entry = ttk.Entry(forgot_window, show="•")
        password_entry.pack(pady=5)

        def reset_password():
            username = username_entry.get()
            new_password = password_entry.get()

            if not username or not new_password:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                conn = mysql.connector.connect(host="127.0.0.1", user="root", password="12345", database="cafe_billing")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Password reset successfully!")
                forgot_window.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error connecting to database: {e}")

if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()