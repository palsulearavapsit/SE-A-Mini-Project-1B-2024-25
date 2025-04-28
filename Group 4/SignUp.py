import mysql.connector
import tkinter as Tk
from tkinter import messagebox, Canvas, PhotoImage, Button, Entry, Label
from pathlib import Path
from PIL import Image, ImageTk
import LoginPage
import WelcomePage
import GoogleLogin
import HomePage
import DriverVerification_Page

class SignupPage(Tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\Poolify3\Tkinter-Designer-master\build\assets\frame0")
    entries = []

    def __init__(self):
        super().__init__()
        self.title("Poolify App")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.passenger_setup_ui()
        self.google_auth = GoogleLogin.GoogleAuth()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def passenger_google_authenticate(self):
        """Handles Google Authentication for Signup & Login."""
        user_info = self.google_auth.authenticate_user()

        if not user_info:
            messagebox.showerror("Error", "Google authentication failed.")
            return None

        email = user_info["email"]
        name = user_info["name"]

        if self.google_auth.store_or_fetch_user(email, name):
            # ✅ Redirect to HomePage with the authenticated email
            self.destroy()
            HomePage.HomePage(email)

    def driver_google_authenticate(self):
        """Handles Google Authentication for Signup & Login."""
        user_info = self.google_auth.authenticate_user()

        if not user_info:
            messagebox.showerror("Error", "Google authentication failed.")
            return None

        email = user_info["email"]
        name = user_info["name"]

        if self.google_auth.store_or_fetch_user(email, name):
            # ✅ Redirect to HomePage with the authenticated email
            self.destroy()
            DriverVerification_Page.DriverVerificationApp(email)

    def poolify(self, event=None):
        self.destroy()  # Destroys the current window or frame
        WelcomePage.WelcomePage()  # Initializes the WelcomePage

    def login_page(self, event=None):
        self.destroy()
        LoginPage.LoginPage()

    def driververification_page(self, email):
        self.destroy()
        DriverVerification_Page.DriverVerificationApp(email)


    def create_db_connection(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            return conn
        except mysql.connector.Error as err:
            print("Database connection error:", err)
            return None

    def store_or_fetch_user(self, email, name):
        """Stores a new user in the database or logs in an existing user."""
        try:
            conn = self.create_db_connection()  # Use the existing method
            if not conn:
                return False  # Connection failed

            cursor = conn.cursor(buffered=True)  # Use buffered cursor to automatically consume results

            # Check if user exists in users table
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()  # Make sure to fetch the result

            if not existing_user:
                # Insert new user
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, email, "google_auth"))
                conn.commit()
                print("New user registered!")
                messagebox.showinfo("Signup Successful", f"Welcome, {name}!\nYour account has been created.")
            else:
                print("User exists. Logging in...")
                messagebox.showinfo("Login Successful", f"Welcome back, {name}!")

            cursor.close()
            conn.close()
            return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # Make sure connection is closed even if there's an error
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            return False
    # Updated passenger_google_authenticate and driver_google_authenticate methods
    def passenger_insert_user(self, name, email, password):
        try:
            conn = self.create_db_connection()  # Use the existing method
            if not conn:
                return False  # Connection failed

            cursor = conn.cursor(buffered=True)
            # Fixed the SQL query - "password" was missing from column list
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            conn.commit()
            print("New user registered!")
            messagebox.showinfo("Signup Successful", f"Welcome, {name}!\nYour account has been created.")

            # Added missing code to close connections and return result
            cursor.close()
            conn.close()
            return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # Make sure connection is closed even if there's an error
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            return False

    def driver_insert_user(self, name, email, password):
        try:
            conn = self.create_db_connection()  # Use the existing method
            if not conn:
                return False  # Connection failed

            cursor = conn.cursor(buffered=True)
            # Fixed the SQL query - "password" was missing from column list
            query = "INSERT INTO drivers (full_name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            conn.commit()
            print("New user registered!")
            messagebox.showinfo("Signup Successful", f"Welcome, {name}!\nYour account has been created.")

            # Added missing code to close connections and return result
            cursor.close()
            conn.close()
            return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # Make sure connection is closed even if there's an error
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
            return False

    def switch_frame(self, frame_method):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_method()

    def passenger_setup_ui(self):
        canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.current_frame = canvas

        #65
        canvas.create_rectangle(0, 0, 1280, 50, fill="#000000", outline="")
        canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        canvas.create_text(51.0, 90.0, anchor="nw", text="Welcome Passenger!", fill="#000000",
                           font=("Poppins Medium", 32 * -1))
        #Poolify Label
        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -30), cursor="hand2")
        poolify_label.place(x=15, y=9)
        poolify_label.bind("<Button-1>", self.poolify)

        button_image_3 = PhotoImage(file=self.relative_to_assets("passenger_button.png"))
        self.button_3 = Button(image=button_image_3, borderwidth=0, cursor="hand2", highlightthickness=0,
                               command=lambda: self.switch_frame(self.driver_setup_ui),
                               relief="flat", bg="#FFFFFF")
        self.button_3.place(x=91.0, y=390, width=80.0, height=50)
        self.button_image_3 = button_image_3

        button_image_4 = PhotoImage(file=self.relative_to_assets("driver_button.png"))
        self.button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0,
                               cursor="hand2", command=lambda: self.switch_frame(self.driver_setup_ui), relief="flat")
        self.button_4.place(x=240.0, y=390.0, width=80.0, height=52.0)
        self.button_image_4 = button_image_4

        # Load and display image
        image_path = r"C:\Users\Nikhil\OneDrive\Pictures\poolify\Blue_half_page.png"
        image = Image.open(image_path)
        image_1 = ImageTk.PhotoImage(image)
        canvas.create_image(950.0, 377.0, image=image_1)
        self.image_1 = image_1  # Keep reference

        # Text elements dynamically
        texts = [
            # (51.0, 110.0, "Welcome", 20 * -1),
            (50.0, 154.0, "Name", 17),
            (50.0, 230.0, "Email address", 17),
            (50.0, 307.0, "Password", 17),
            # (75.0, 383.0, "I agree to the terms & policy", 9),
            (210.0, 540.0, "Or", 15)
        ]
        for x, y, text, font_size in texts:
            canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=("Poppins Medium", font_size * -1))

        entry_image = PhotoImage(file=self.relative_to_assets("EntryImage1.png"))
        canvas.create_image(249.0, 196.0, image=entry_image)
        canvas.create_image(249.0, 272.0, image=entry_image)
        canvas.create_image(249.0, 349.0, image=entry_image)

        # Keep a reference to the image to prevent garbage collection
        self.entry_image = entry_image

        # Create the entry fields and place them on the canvas
        self.name_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Poppins Medium", 15))
        self.name_entry.place(x=56.0, y=179.0, width=350.0, height=30.0)

        self.email_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Poppins Medium", 15))
        self.email_entry.place(x=56.0, y=256.0, width=350.0, height=30.0)

        self.password_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716",show="*", highlightthickness=0, font=("Poppins Medium", 15))
        self.password_entry.place(x=56.0, y=332.0, width=350.0, height=30.0)

        # Buttons
        button_image_1 = PhotoImage(file=self.relative_to_assets("Sign_Up.png"))
        self.button_1 = Button(image=button_image_1, borderwidth=0,cursor="hand2", highlightthickness=0, command=self.passenger_handle_submit,
                               relief="flat", bg="#FFFFFF")
        self.button_1.place(x=59.0, y=462.0, width=340.0, height=50)
        self.button_image_1 = button_image_1  # Keep reference

        button_image_2 = PhotoImage(file=self.relative_to_assets("Google.png"))
        self.button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0,
                               cursor="hand2",command=self.passenger_google_authenticate, relief="flat")
        self.button_2.place(x=130.0, y=580.0, width=210.0, height=32.0)
        self.button_image_2 = button_image_2  # Keep reference

        login_label = Label(self, text="Already have an account? Login In", borderwidth=0, highlightthickness=0,
                             relief="flat", fg="#000000", bg="#FFFFFF", font=("Arial", 10), cursor="hand2")
        login_label.place(x=130.0, y=636.0, width=200.0, height=30)
        login_label.bind("<Button-1>", self.login_page)

    def driver_setup_ui(self):
        canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.current_frame = canvas

        #65
        canvas.create_rectangle(0, 0, 1280, 50, fill="#000000", outline="")
        canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        canvas.create_text(51.0, 90.0, anchor="nw", text="Welcome Driver!", fill="#000000",
                           font=("Poppins Medium", 32 * -1))
        #Poolify Label
        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -30), cursor="hand2")
        poolify_label.place(x=15, y=9)
        poolify_label.bind("<Button-1>", self.poolify)

        button_image_3 = PhotoImage(file=self.relative_to_assets("driver_button.png"))
        self.button_3 = Button(image=button_image_3, borderwidth=0, cursor="hand2", highlightthickness=0,
                               command=lambda: self.switch_frame(self.passenger_setup_ui),
                               relief="flat", bg="#FFFFFF")
        self.button_3.place(x=91.0, y=390, width=80.0, height=50)
        self.button_image_3 = button_image_3

        button_image_4 = PhotoImage(file=self.relative_to_assets("passenger_button.png"))
        self.button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0,
                               cursor="hand2", command=lambda: self.switch_frame(self.passenger_setup_ui), relief="flat")
        self.button_4.place(x=240.0, y=390.0, width=80.0, height=52.0)
        self.button_image_4 = button_image_4

        # Load and display image
        image_path = r"C:\Users\Nikhil\OneDrive\Pictures\poolify\Blue_half_page.png"
        image = Image.open(image_path)
        image_1 = ImageTk.PhotoImage(image)
        canvas.create_image(950.0, 377.0, image=image_1)
        self.image_1 = image_1  # Keep reference

        # Text elements dynamically
        texts = [
            # (51.0, 110.0, "Welcome", 20 * -1),
            (50.0, 154.0, "Name", 17),
            (50.0, 230.0, "Email address", 17),
            (50.0, 307.0, "Password", 17),
            # (75.0, 383.0, "I agree to the terms & policy", 9),
            (210.0, 540.0, "Or", 15)
        ]
        for x, y, text, font_size in texts:
            canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=("Poppins Medium", font_size * -1))

        entry_image = PhotoImage(file=self.relative_to_assets("EntryImage1.png"))
        canvas.create_image(249.0, 196.0, image=entry_image)
        canvas.create_image(249.0, 272.0, image=entry_image)
        canvas.create_image(249.0, 349.0, image=entry_image)

        # Keep a reference to the image to prevent garbage collection
        self.entry_image = entry_image

        # Create the entry fields and place them on the canvas
        self.name_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Poppins Medium", 15))
        self.name_entry.place(x=56.0, y=179.0, width=350.0, height=30.0)

        self.email_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Poppins Medium", 15))
        self.email_entry.place(x=56.0, y=256.0, width=350.0, height=30.0)

        self.password_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716",show="*", highlightthickness=0, font=("Poppins Medium", 15))
        self.password_entry.place(x=56.0, y=332.0, width=350.0, height=30.0)

        # Buttons
        button_image_1 = PhotoImage(file=self.relative_to_assets("Sign_Up.png"))
        self.button_1 = Button(image=button_image_1, borderwidth=0,cursor="hand2", highlightthickness=0, command=self.driver_handle_submit,
                               relief="flat", bg="#FFFFFF")
        self.button_1.place(x=59.0, y=462.0, width=340.0, height=50)
        self.button_image_1 = button_image_1  # Keep reference

        button_image_2 = PhotoImage(file=self.relative_to_assets("Google.png"))
        self.button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0,
                               cursor="hand2",command=self.driver_google_authenticate, relief="flat")
        self.button_2.place(x=130.0, y=580.0, width=210.0, height=32.0)
        self.button_image_2 = button_image_2  # Keep reference

        login_label = Label(self, text="Already have an account? Login In", borderwidth=0, highlightthickness=0,
                             relief="flat", fg="#000000", bg="#FFFFFF", font=("Arial", 10), cursor="hand2")
        login_label.place(x=130.0, y=636.0, width=200.0, height=30)
        login_label.bind("<Button-1>", self.login_page)

    def passenger_handle_submit(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if name and email and password:
            self.passenger_insert_user(name, email, password)
            # messagebox.showinfo("Signup Successful", "Your account has been created successfully!")
            self.login_page()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def driver_handle_submit(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if name and email and password:
            self.driver_insert_user(name, email, password)
            # messagebox.showinfo("Signup Successful", "Your account has been created successfully!")
            self.driververification_page(email)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")


if __name__ == "__main__":
    app = SignupPage()
    app.resizable(False, False)
    app.mainloop()
