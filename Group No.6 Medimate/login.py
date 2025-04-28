import tkinter as tk
import tkinter.messagebox as messagebox
import pymysql
from DocDash import DoctorDashboard
from userdashboard import NavigationApp

class LoginPage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("1280x853")
        self.window.configure(bg="white")

        # Add a logo
        self.logo = tk.PhotoImage(file=r"F:\MINIPROJECT\logo.png")  # Update the path to your logo file

        self.logo_label = tk.Label(self.window, image=self.logo, bg="white")
        self.logo_label.pack(pady=50)
        
        # Create the frame for the login form
        self.frame = tk.Frame(self.window, bg="#12962b",width=1920 ,height=1080)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the label and entry for the ID
        self.id_label = tk.Label(self.frame, text="Username:", bg="lightgreen")
        self.id_label.grid(row=0, column=0, padx=5, pady=2)
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Create the label and entry for the password
        self.pass_label = tk.Label(self.frame, text="Password:", bg="lightgreen")
        self.pass_label.grid(row=2, column=0, padx=5, pady=5)
        self.pass_entry = tk.Entry(self.frame, show="*")
        self.pass_entry.grid(row=2, column=1, padx=5, pady=5)

        # Login button
        self.login_button = tk.Button(self.frame, text="Login", bg="lightgreen", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Create the signup button
        self.signup_button = tk.Button(self.frame, text="Not registered? Signup", 
                                     bg="lightgreen", command=self.open_signup)
        self.signup_button.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        user_id = self.id_entry.get()
        password = self.pass_entry.get()

        try:
            conn = pymysql.connect(host="localhost", user="root", password="Drishti2005@", database="medimate")
            cur = conn.cursor()

            # Check user in user_login table
            user_query = "SELECT * FROM login WHERE username = %s AND password = %s"
            cur.execute(user_query, (user_id, password))
            self.user_result = cur.fetchone()

            # Check user in doctor_login table
            doctor_query = "SELECT * FROM doc_info WHERE username = %s AND password = %s"
            cur.execute(doctor_query, (user_id, password))
            self.doctor_result = cur.fetchone()

            if self.user_result:
                self.open_userdashboard()
            elif self.doctor_result:
                self.open_docdashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")

        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")

        finally:
            cur.close()
            conn.close()

    def open_signup(self):
        self.window.destroy()  # Close login window
        from signup import SignupPage
        signup_page = SignupPage()

    def open_userdashboard(self):
        self.window.destroy()
        user_name = self.user_result[0]  # Name from database
        username = self.user_result[1]   # Username from database
        
        root = tk.Tk()
        app = NavigationApp(root, user_name, username)
        root.mainloop()

    def open_docdashboard(self):
        self.window.destroy()
    
        try:
            # Get doctor information
            doctor_name = self.doctor_result[2]  # Assuming name is at index 2
            doc_username = self.doctor_result[0]  # Assuming username is at index 0
            
            # Create the doctor dashboard directly
            root = tk.Tk()
            app = DoctorDashboard(root, doc_username, doctor_name)
            root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error opening doctor dashboard: {e}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.run()