import mysql.connector
import tkinter as Tk
from tkinter import messagebox, Canvas, PhotoImage, Button, Entry, Label, Frame
from pathlib import Path
from PIL import Image, ImageTk
import SignUp
import WelcomePage
import HomePage
import DriverHomePage
import GoogleLogin
import ForgetPasswordPage


class LoginPage(Tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")

        # Initialize frames for content
        self.main_frame = Frame(self, bg="#FFFFFF")
        self.main_frame.pack(fill="both", expand=True)

        # Initialize user type (default to passenger)
        self.user_type = "passenger"

        self.setup_ui()
        self.google_auth = GoogleLogin.GoogleAuth()

    def switch_frame(self, setup_function):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Call the setup function to rebuild UI
        setup_function()

    def set_user_type(self, user_type):
        """Set whether we're logging in as a driver or passenger"""
        self.user_type = user_type
        # Update the login message to reflect current mode
        self.welcome_text.config(text=f"Login as {user_type.capitalize()}")

    # You may also need to update the GoogleAuth.store_or_fetch_user method to properly fetch results:
    def store_or_fetch_user(self, email, name):
        """Stores a new user in the database or logs in an existing user."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            cursor = conn.cursor(buffered=True)  # Use buffered cursor

            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()  # Explicitly fetch the result

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

            return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            # Always close cursor and connection in finally block
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def check_email_exists(self, email):
        """Check if email exists in the database for the selected user type."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            cursor = conn.cursor(buffered=True)  # Use buffered cursor

            # Determine which table to check based on user type
            table = "drivers" if self.user_type == "driver" else "users"

            # Execute the query to check if email exists
            cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))

            # Explicitly fetch the results
            result = cursor.fetchall()

            return len(result) > 0

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        finally:
            # Always close cursor and connection in finally block
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def google_authenticate(self):
        """Handles Google Authentication for Login."""
        # Get user info from Google
        user_info = self.google_auth.authenticate_user()

        if not user_info:
            messagebox.showerror("Error", "Google authentication failed.")
            return None

        email = user_info["email"]
        name = user_info["name"]

        # Important: First check if user exists in users table before checking role table
        # This prevents issues with unread results by separating database operations
        user_exists = self.store_or_fetch_user(email, name)

        if not user_exists:
            messagebox.showerror("Error", "Failed to authenticate user.")
            return

        # Now check if user has the correct role
        role_exists = self.check_email_exists(email)

        if role_exists:
            # User exists with the correct role - proceed to homepage
            self.destroy()
            if self.user_type == "driver":
                DriverHomePage.HomePage(email)
            else:
                HomePage.HomePage(email)
        else:
            messagebox.showerror("Error", f"No {self.user_type} account found with this email.")

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def poolify(self, event=None):
        self.destroy()  # Destroys the current window or frame
        WelcomePage.WelcomePage()

    def signup_page(self):
        self.destroy()
        SignUp.SignupPage()

    def forget_page(self):
        reset_app = ForgetPasswordPage.PasswordResetApp(self)

    def create_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="carpooling_db"
        )

    def verify_login(self, in_email, in_password):
        conn = None
        cursor = None
        try:
            conn = self.create_db_connection()
            cursor = conn.cursor()

            if self.user_type == "driver":
                # Only check drivers table
                cursor.execute("SELECT * FROM drivers WHERE email = %s AND password = %s", (in_email, in_password))
            else:
                # Only check users table
                cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (in_email, in_password))

            # Fetch the result and store it
            result = cursor.fetchone()

            # Consume any remaining results
            while cursor.nextset():
                pass

            return result

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    print(f"Error closing cursor: {e}")

            if conn:
                try:
                    conn.close()
                except Exception as e:
                    print(f"Error closing connection: {e}")

    def on_login(self):
        in_email = self.email.get().strip()
        in_password = self.password.get().strip()

        user_data = self.verify_login(in_email, in_password)

        if user_data:
            messagebox.showinfo("Login Successful", f"Welcome {self.user_type}!")

            self.destroy()

            # Redirect based on current user type
            if self.user_type == "driver":
                driver_page = DriverHomePage.HomePage(in_email)
                driver_page.mainloop()
            else:
                passenger_page = HomePage.HomePage(in_email)
                passenger_page.mainloop()
        else:
            messagebox.showerror("Login Failed", f"Invalid {self.user_type} username or password")

    def setup_ui(self):
        canvas = Canvas(self.main_frame, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0,
                        relief="ridge")
        canvas.place(x=0, y=0)

        # Load and display image
        image_path = r"C:\Users\Nikhil\OneDrive\Pictures\poolify\Blue_half_page.png"
        image = Image.open(image_path)
        image_1 = ImageTk.PhotoImage(image)
        canvas.create_image(950.0, 377.0, image=image_1)
        self.image_1 = image_1  # Keep reference

        # Black frames and text
        canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        canvas.create_text(51.0, 92.0, anchor="nw", text="Welcome back!", fill="#000000",
                           font=("Poppins Medium", 32 * -1))

        # Welcome message that changes based on login type
        self.welcome_text = Label(self.main_frame, text="Login as Passenger", bg="#FFFFFF", fg="#000000",
                                  font=("Poppins Medium", 16))
        self.welcome_text.place(x=51.0, y=150.0)

        # Poolify Label
        poolify_label = Label(self.main_frame, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -30), cursor="hand2")
        poolify_label.place(x=15, y=9)
        poolify_label.bind("<Button-1>", self.poolify)

        # Entry fields and labels
        canvas.create_text(51.0, 203.0, anchor="nw", text="Email address", fill="#000000",
                           font=("Poppins Medium", 14 * -1))
        canvas.create_text(55.0, 282.0, anchor="nw", text="Password", fill="#000000", font=("Poppins Medium", 14 * -1))

        entry_image = PhotoImage(file=self.relative_to_assets("EntryImage1.png"))
        canvas.create_image(253.0, 324.0, image=entry_image)
        canvas.create_image(249.0, 245.0, image=entry_image)
        self.entry_image = entry_image  # Keep reference

        self.email = Entry(self.main_frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,
                           font=("Poppins Medium", 15))
        self.email.place(x=57.0, y=229.0, width=384.0, height=30.0)

        self.password = Entry(self.main_frame, bd=0, bg="#FFFFFF", fg="#000716", show="*", highlightthickness=0,
                              font=("Poppins Medium", 15))
        self.password.place(x=61.0, y=308.0, width=384.0, height=30.0)

        # Driver/Passenger selection buttons
        button_image_3 = PhotoImage(file=self.relative_to_assets("driver_button.png"))
        self.button_3 = Button(self.main_frame, image=button_image_3, borderwidth=0, cursor="hand2",
                               highlightthickness=0,
                               command=lambda: self.set_user_type("driver"),
                               relief="flat", bg="#FFFFFF")
        self.button_3.place(x=91.0, y=390, width=80.0, height=50)
        self.button_image_3 = button_image_3

        button_image_4 = PhotoImage(file=self.relative_to_assets("passenger_button.png"))
        self.button_4 = Button(self.main_frame, image=button_image_4, borderwidth=0, highlightthickness=0,
                               cursor="hand2", command=lambda: self.set_user_type("passenger"), relief="flat")
        self.button_4.place(x=240.0, y=390.0, width=80.0, height=52.0)
        self.button_image_4 = button_image_4

        # Login button - moved down to accommodate driver/passenger buttons
        button_image_1 = PhotoImage(file=self.relative_to_assets("Login.png"))
        self.button_1 = Button(self.main_frame, image=button_image_1, borderwidth=0, highlightthickness=0,
                               cursor="hand2",
                               command=self.on_login, relief="flat", bg="#FFFFFF")
        self.button_1.place(x=51.0, y=460.0, width=404.0, height=35)
        self.button_image_1 = button_image_1  # Keep reference

        # "Or" text - moved down
        canvas.create_text(245.0, 510.0, anchor="nw", text="Or", fill="#000000", font=("Poppins Medium", 15 * -1))

        # Google login button - moved down
        button_image_2 = PhotoImage(file=self.relative_to_assets("Google.png"))
        self.button_2 = Button(self.main_frame, image=button_image_2, borderwidth=0, cursor="hand2",
                               highlightthickness=0,
                               command=self.google_authenticate, relief="flat")
        self.button_2.place(x=159.0, y=544.0, width=210.0, height=32.0)
        self.button_image_2 = button_image_2  # Keep reference

        # Signup and forgot password buttons
        signup_button = Button(self.main_frame, text="Don't have an account? Sign Up", borderwidth=0, cursor="hand2",
                               highlightthickness=0,
                               command=self.signup_page, relief="flat", fg="blue", bg="#FFFFFF", font=("Arial", 10))
        signup_button.place(x=140.0, y=636.0, width=200.0, height=30)

        forgot_button = Button(self.main_frame, text="forgot password?", borderwidth=0, cursor="hand2",
                               highlightthickness=0, command=self.forget_page, relief="flat",
                               fg="blue", bg="#FFFFFF", font=("Arial", 10))
        forgot_button.place(x=51.0, y=350.0, width=100.0, height=30)


if __name__ == "__main__":
    app = LoginPage()
    app.resizable(False, False)
    app.mainloop()