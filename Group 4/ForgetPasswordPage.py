import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import mysql.connector
import smtplib
import random
import string
from email.mime.text import MIMEText
import requests
import re
from PIL import Image, ImageTk
from pathlib import Path
import LoginPage


class PasswordResetApp(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Carpooling App - Password Reset")
        self.geometry("500x450")
        self.configure(bg="white")

        # Center the window on screen
        self.center_window()

        # Define assets path
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(
            r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

        # Load all required images
        self.load_images()

        # Create a main container frame that will center content
        self.main_container = tk.Frame(self, bg="white")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Create the main canvas
        self.canvas = tk.Canvas(
            self.main_container,
            bg="#FFFFFF",
            height=450,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack()

        # Initialize frames and their contents
        self.create_email_frame()
        self.create_verification_frame()
        self.create_reset_frame()

        # Show the email frame
        self.show_email_frame()

    def center_window(self):
        """Center the window on the screen"""
        # Update the window to get accurate dimensions
        self.update_idletasks()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        x = (screen_width - 500) // 2
        y = (screen_height - 450) // 2

        # Set window position
        self.geometry(f"500x450+{x}+{y}")

    def load_images(self):
        # Load button images
        self.send_verification_img = tk.PhotoImage(file=self.relative_to_assets("SendVerificationButton.png"))
        self.verify_code_img = tk.PhotoImage(file=self.relative_to_assets("VerifyCodeButton.png"))
        self.reset_password_img = tk.PhotoImage(file=self.relative_to_assets("ResetPasswordButton.png"))

        # Load entry background image
        self.entry_bg_img = tk.PhotoImage(file=self.relative_to_assets("EntryImage1.png"))

    def relative_to_assets(self, path: str) -> Path:
        """Get the full path to an asset file"""
        return self.ASSETS_PATH / Path(path)

    def create_email_frame(self):
        self.email_frame = tk.Frame(self.main_container, bg="white", width=500, height=450)

        # Create a canvas for this frame
        self.email_canvas = tk.Canvas(
            self.email_frame,
            bg="#FFFFFF",
            height=450,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.email_canvas.place(x=0, y=0)

        # Add header text
        self.email_canvas.create_text(
            250, 50,
            text="Forgot Password",
            fill="#000000",
            font=("Poppins Bold", 24),
            anchor="center"
        )

        self.email_canvas.create_text(
            250, 100,
            text="Enter your registered email address to receive a verification code",
            fill="#000000",
            font=("Poppins Medium", 12),
            width=400,
            anchor="center"
        )

        # Email label
        self.email_canvas.create_text(
            60, 200,
            text="Email:",
            fill="#000000",
            font=("Poppins Medium", 14),
            anchor="w"
        )

        # Add entry background image
        self.email_canvas.create_image(
            250, 235,  # Center position
            image=self.entry_bg_img
        )

        # Create the email entry
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(
            self.email_frame,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Poppins Medium", 15),
            textvariable=self.email_var
        )
        self.email_entry.place(x=60, y=220, width=380, height=30)

        # Submit button with custom image - maintaining original size
        send_btn = tk.Button(
            self.email_frame,
            image=self.send_verification_img,
            command=self.submit_email,
            bd=0,
            bg="white",
            activebackground="white",
            cursor="hand2",
            relief="flat"
        )
        send_btn.place(x=125, y=300, width=250, height=40)  # Adjusted position since profile section was removed

        # Back to login link
        self.email_canvas.create_text(
            250, 360,  # Adjusted position
            text="Remember your password? Back to Login",
            fill="#1E88E5",
            font=("Poppins", 10),
            anchor="center"
        )

    def create_verification_frame(self):
        self.verification_frame = tk.Frame(self.main_container, bg="white", width=500, height=450)

        # Create canvas for this frame
        self.verify_canvas = tk.Canvas(
            self.verification_frame,
            bg="#FFFFFF",
            height=450,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.verify_canvas.place(x=0, y=0)

        # Add header text
        self.verify_canvas.create_text(
            250, 50,
            text="Verify Code",
            fill="#000000",
            font=("Poppins Bold", 24),
            anchor="center"
        )

        self.verify_canvas.create_text(
            250, 100,
            text="Enter the 6-digit verification code sent to your email",
            fill="#000000",
            font=("Poppins Medium", 12),
            width=400,
            anchor="center"
        )

        # Email display
        self.email_display = self.verify_canvas.create_text(
            250, 140,
            text="",
            fill="#555555",
            font=("Poppins Italic", 12),
            anchor="center"
        )

        # Verification code label
        self.verify_canvas.create_text(
            60, 200,
            text="Verification Code:",
            fill="#000000",
            font=("Poppins Medium", 14),
            anchor="w"
        )

        # Add entry background image
        self.verify_canvas.create_image(
            250, 235,  # Center position
            image=self.entry_bg_img
        )

        # Create the verification code entry
        self.code_var = tk.StringVar()
        self.code_entry = tk.Entry(
            self.verification_frame,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Poppins Medium", 15),
            textvariable=self.code_var
        )
        self.code_entry.place(x=60, y=220, width=380, height=30)

        # Verify button - maintaining original size
        verify_btn = tk.Button(
            self.verification_frame,
            image=self.verify_code_img,
            command=self.verify_code,
            bd=0,
            bg="white",
            activebackground="white",
            cursor="hand2",
            relief="flat"
        )
        verify_btn.place(x=125, y=280, width=250, height=40)

        # Resend code link
        self.verify_canvas.create_text(
            250, 350,
            text="Resend Code",
            fill="#1E88E5",
            font=("Poppins", 12),
            anchor="center"
        )
        # Bind click event to the text
        self.verify_canvas.tag_bind(
            self.verify_canvas.create_rectangle(200, 340, 300, 360, fill="", outline=""),
            "<Button-1>",
            lambda e: self.resend_code()
        )

    def create_reset_frame(self):
        self.reset_frame = tk.Frame(self.main_container, bg="white", width=500, height=450)

        # Create canvas for this frame
        self.reset_canvas = tk.Canvas(
            self.reset_frame,
            bg="#FFFFFF",
            height=450,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.reset_canvas.place(x=0, y=0)

        # Add header text
        self.reset_canvas.create_text(
            250, 50,
            text="Reset Password",
            fill="#000000",
            font=("Poppins Bold", 24),
            anchor="center"
        )

        self.reset_canvas.create_text(
            250, 100,
            text="Create a new password for your account",
            fill="#000000",
            font=("Poppins Medium", 12),
            width=400,
            anchor="center"
        )

        # New password label
        self.reset_canvas.create_text(
            60, 160,
            text="New Password:",
            fill="#000000",
            font=("Poppins Medium", 14),
            anchor="w"
        )

        # Add entry background image for new password
        self.reset_canvas.create_image(
            250, 195,  # Center position
            image=self.entry_bg_img
        )

        # Create the new password entry
        self.new_password_var = tk.StringVar()
        self.new_password_entry = tk.Entry(
            self.reset_frame,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Poppins Medium", 15),
            textvariable=self.new_password_var,
            show="*"
        )
        self.new_password_entry.place(x=60, y=180, width=380, height=30)

        # Confirm password label
        self.reset_canvas.create_text(
            60, 240,
            text="Confirm Password:",
            fill="#000000",
            font=("Poppins Medium", 14),
            anchor="w"
        )

        # Add entry background image for confirm password
        self.reset_canvas.create_image(
            250, 275,  # Center position
            image=self.entry_bg_img
        )

        # Create the confirm password entry
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = tk.Entry(
            self.reset_frame,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Poppins Medium", 15),
            textvariable=self.confirm_password_var,
            show="*"
        )
        self.confirm_password_entry.place(x=60, y=260, width=380, height=30)

        # Reset button - maintaining original size
        reset_btn = tk.Button(
            self.reset_frame,
            image=self.reset_password_img,
            command=self.reset_password,
            bd=0,
            bg="white",
            activebackground="white",
            cursor="hand2",
            relief="flat"
        )
        reset_btn.place(x=125, y=330, width=250, height=40)

    def show_email_frame(self):
        self.verification_frame.place_forget()
        self.reset_frame.place_forget()
        self.email_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_verification_frame(self):
        self.email_frame.place_forget()
        self.reset_frame.place_forget()
        self.verification_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Update the email display
        self.verify_canvas.itemconfig(
            self.email_display,
            text=f"Code sent to: {self.email_var.get()}"
        )

    def show_reset_frame(self):
        self.email_frame.place_forget()
        self.verification_frame.place_forget()
        self.reset_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Database connection function
    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="root", database="carpooling_db"
        )

    # Function to generate a random 6-digit verification code
    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))

    # Function to send email
    def send_email(self, receiver_email, verification_code):
        api_key = ""

        url = "https://api.brevo.com/v3/smtp/email"

        payload = {
            "sender": {"name": "Carpooling App", "email": "kmaan0828@gmail.com"},
            "to": [{"email": receiver_email}],
            "subject": "Password Reset Verification Code",
            "htmlContent": f"<p>Your verification code is: <strong>{verification_code}</strong></p>"
        }

        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 201:
                return True
            else:
                print(f"❌ Failed to send email: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False

    # Validate email format
    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    # Function to submit email and initiate password reset
    def submit_email(self):
        email = self.email_var.get().strip()

        if not email:
            messagebox.showerror("Error", "Please enter your email address.")
            return

        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Check if email exists in users table
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                verification_code = self.generate_verification_code()

                # Store the verification code in password_reset table
                cursor.execute("INSERT INTO password_reset (email, verification_code) VALUES (%s, %s)",
                               (email, verification_code))
                conn.commit()

                if self.send_email(email, verification_code):
                    self.current_email = email
                    messagebox.showinfo("Success", "Verification code has been sent to your email.")
                    self.show_verification_frame()
                else:
                    messagebox.showerror("Error", "Failed to send email. Please try again later.")
            else:
                messagebox.showerror("Error", "Email not registered in our system.")

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to verify the OTP
    def verify_otp(self, email, entered_code):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT verification_code FROM password_reset WHERE email = %s ORDER BY created_at DESC LIMIT 1",
                (email,))
            record = cursor.fetchone()

            if record and record[0] == entered_code:
                cursor.close()
                conn.close()
                return True

            cursor.close()
            conn.close()
            return False
        except Exception as e:
            print(f"Error verifying OTP: {str(e)}")
            return False

    # Function to handle verification code submission
    def verify_code(self):
        code = self.code_var.get().strip()

        if not code:
            messagebox.showerror("Error", "Please enter the verification code.")
            return

        if self.verify_otp(self.current_email, code):
            self.show_reset_frame()
        else:
            messagebox.showerror("Error", "Invalid verification code. Please try again.")

    # Function to reset password
    def reset_password(self):
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not new_password:
            messagebox.showerror("Error", "Please enter a new password.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Update the user's password
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, self.current_email))
            conn.commit()

            # Delete the verification record
            cursor.execute("DELETE FROM password_reset WHERE email = %s", (self.current_email,))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Password reset successful! You can now log in with your new password.")

            # Open the login page
            self.destroy()
            login_page = LoginPage.LoginPage()
            login_page.mainloop()

            # Clear all fields
            self.email_var.set("")
            self.code_var.set("")
            self.new_password_var.set("")
            self.confirm_password_var.set("")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to resend verification code
    def resend_code(self):
        try:
            verification_code = self.generate_verification_code()

            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Store the new verification code
            cursor.execute("INSERT INTO password_reset (email, verification_code) VALUES (%s, %s)",
                           (self.current_email, verification_code))
            conn.commit()

            cursor.close()
            conn.close()

            if self.send_email(self.current_email, verification_code):
                messagebox.showinfo("Success", "New verification code has been sent to your email.")
            else:
                messagebox.showerror("Error", "Failed to send email. Please try again later.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Main application
if __name__ == "__main__":
    app = PasswordResetApp()
    app.resizable(False, False)
    app.mainloop()