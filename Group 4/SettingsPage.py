import requests
import re
import json
import tkinter as tk
from tkinter import messagebox, Entry, Text, StringVar, ttk, Tk, Canvas, Button, PhotoImage, Label, Frame
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import WelcomePage
import DriverHomePage
from PIL import Image, ImageTk

# Load environment variables from .env file
load_dotenv()


class PlaceholderEntry(tk.Entry):
    """A custom Entry widget with placeholder functionality"""

    def __init__(self, master=None, placeholder="", user_email="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['fg']
        self.user_email = user_email

        # Prefill with user email if it's the email field
        if placeholder == "Your Email" and user_email:
            self.insert(0, user_email)
            self._has_placeholder = False
        else:
            self.insert(0, placeholder)
            self['fg'] = self.placeholder_color
            self._has_placeholder = True

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, e):
        if self._has_placeholder:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color
            self._has_placeholder = False

    def _add_placeholder(self, e):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color
            self._has_placeholder = True

    def get_actual_value(self):
        """Return the entry content, or empty string if placeholder is showing"""
        if self._has_placeholder:
            return ""
        return self.get()


class AppBase(Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self, user_email,user_type):
        super().__init__()
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.title("Poolify")
        self.resizable(False, False)
        self.image_references = []  # To store image references and prevent garbage collection
        self.user_email = user_email
        self.user_type = user_type
        self.current_content_frame = None
        self.SUPPORT_EMAIL = "poolify31@gmail.com"
        self.BREVO_API_KEY = ""
        self.BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
        self.setup_ui()
        self.pre_fill_old_password()

    def poolify(self):
        self.destroy()
        DriverHomePage.HomePage(self.user_email)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def pre_fill_old_password(self):
        """Pre-fill the old password field with the user's current password"""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            cursor = connection.cursor()

            # Get current password from database
            password_query = "SELECT password FROM users WHERE email = %s"
            cursor.execute(password_query, (self.user_email,))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            if result:
                current_password = result[0]
                # Clear any existing text first
                self.old_password.delete(0, 'end')
                # Set the old password entry to display the current password
                self.old_password.insert(0, current_password)
                # Make this field read-only since we're pre-filling it
                self.old_password.config(state="readonly")
            else:
                messagebox.showerror("Error", "User not found.", parent=self)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to retrieve password: {str(e)}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self)

    def change_password(self):
        """Handle password change functionality"""
        old_password = self.old_password.get().strip()
        new_password = self.new_password.get().strip()
        confirm_password = self.confirm_password.get().strip()

        # Validate inputs
        if not old_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.", parent=self)
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New password and confirm password do not match.", parent=self)
            return

        if len(new_password) < 6:
            messagebox.showerror("Error", "New password must be at least 6 characters long.", parent=self)
            return

        try:
            # Connect to database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            cursor = connection.cursor()

            # No need to verify old password since we pre-filled it from the database

            # Update the password
            update_query = "UPDATE users SET password = %s WHERE email = %s"
            cursor.execute(update_query, (new_password, self.user_email))
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Password changed successfully.", parent=self)
              # Close the window after successful password change

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to change password: {str(e)}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self)

    def setup_ui(self):
        # Create the main canvas
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Top black strip
        self.canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        # Bottom black strip
        self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        # App name in top strip
        self.canvas.create_text(15, 9, anchor="nw", text="POOLIFY", fill="#FFFFFF", font=("Italiana Regular", 18))

        # Profile/Menu button in top right
        # Note: You'll need to replace with your actual image file
        try:
            profile_img = PhotoImage(file=self.relative_to_assets("profile_icon.png"))
            self.image_references.append(profile_img)
        except:
            # Fallback if image is not found
            profile_img = None
            print("Warning: profile_icon.png not found in assets folder")

        self.profile_button = Button(
            self,
            image=profile_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            fg="#FFFFFF",
            bg="#000000",
            cursor="hand2",
            command=self.toggle_menu
        )

        # If no image is available, use text instead
        if profile_img is None:
            self.profile_button.configure(text="Menu", font=("Arial", 12))

        self.profile_button.place(x=1230, y=5, width=50, height=50)

        # Create the main content frame where all dynamic content will be displayed
        self.content_frame = Frame(self, bg="#FFFFFF")
        self.content_frame.place(x=0, y=60, width=1280, height=636)

        # Initial main content - Change Password page
        self.create_change_password_content()
        self.back_button = ttk.Button(self, text="← Back", command=self.go_home_back)
        self.back_button.place(x=5, y=65)

    def go_home_back(self):
        self.destroy()
        if self.user_type == "driver":
            import DriverHomePage
            DriverHomePage.HomePage(self.user_email)
        else:  # passenger
            import HomePage
            HomePage.HomePage(self.user_email)

    def toggle_menu(self):
        # Hide the profile button when menu is open
        self.profile_button.place_forget()

        # Create menu frame
        self.menu_frame = Frame(self, bg="white", width=300, height=636, bd=2, relief="solid",
                                highlightbackground="black", highlightcolor="black")
        self.menu_frame.place(x=980, y=60)

        # Function to close the menu
        def close_menu():
            self.menu_frame.destroy()
            self.profile_button.place(x=1230, y=5)

        # Close button
        try:
            back_button_img = PhotoImage(file=self.relative_to_assets("back_button.png"))
            self.image_references.append(back_button_img)
        except:
            back_button_img = None

        back_button = Button(
            self.menu_frame,
            image=back_button_img if back_button_img else None,
            text="Close" if back_button_img is None else "",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#FFFFFF",
            cursor="hand2",
            command=close_menu
        )
        back_button.place(x=10, y=10, width=80, height=30)

        # Display user profile data
        self.display_profile_data()

        # Menu options
        menu_options = [
            ("Change Password", self.display_change_password),
            ("Privacy Policy", self.display_privacy_policy),
            ("Contact Us", self.display_contact_us),
            ("Delete Account", self.display_delete_account),
            ("Log Out", self.logout)
        ]

        # Create menu buttons
        for i, (option, command) in enumerate(menu_options):
            # Create separator line above each option (except the first one)
            if i > 0:
                separator = Label(self.menu_frame, bg="#D9D9D9")
                separator.place(x=0, y=200 + (i * 60), width=300, height=1)

            # Create the button
            menu_button = Button(
                self.menu_frame,
                text=option,
                font=("Arial", 12),
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                bg="#FFFFFF",
                cursor="hand2",
                anchor="w",
                command=command
            )
            menu_button.place(x=20, y=210 + (i * 60), width=260, height=40)

    def display_profile_data(self):
        """Fetch and display the user profile data in the menu frame."""
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root",
                                                 database="carpooling_db")  # Change database name if needed
            cursor = connection.cursor(dictionary=True)
            query = "SELECT name, email FROM users WHERE email = %s"
            cursor.execute(query, (self.user_email,))
            user_data = cursor.fetchone()
            cursor.close()
            connection.close()

            if not user_data:
                # No user found, display default
                user_name = "User"
                user_email = self.user_email
            else:
                user_name = user_data["name"]
                user_email = user_data["email"]

        except Exception as e:
            print(f"Database error: {e}")
            # Fallback if database connection fails
            user_name = "User"
            user_email = self.user_email

        # Display profile image (replace with your actual image)
        try:
            profile_img = PhotoImage(file=self.relative_to_assets("profile_image.png"))
            self.image_references.append(profile_img)
            profile_label = Label(
                self.menu_frame,
                image=profile_img,
                bg="#FFFFFF"
            )
            profile_label.place(x=20, y=60)
        except:
            # Fallback if image is not found
            pass

        # Display user details
        name_label = Label(
            self.menu_frame,
            text=f"Name: {user_name}",
            bg="white",
            font=("Arial", 12)
        )
        name_label.place(x=15, y=150)

        email_label = Label(
            self.menu_frame,
            text=f"Email: {user_email}",
            bg="white",
            font=("Arial", 12)
        )
        email_label.place(x=15, y=175)

    def clear_content_frame(self):
        """Clear the current content from the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # Menu button functionalities that switch content
    def display_change_password(self):
        """Display the change password content"""
        self.clear_content_frame()
        self.create_change_password_content()
        # Close the menu if it's open
        if hasattr(self, 'menu_frame') and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
            self.profile_button.place(x=1230, y=5)

    def display_privacy_policy(self):
        """Display the privacy policy content"""
        self.clear_content_frame()
        self.create_privacy_policy_content()
        # Close the menu
        if hasattr(self, 'menu_frame') and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
            self.profile_button.place(x=1230, y=5)

    def display_contact_us(self):
        """Display the contact us content"""
        self.clear_content_frame()
        self.create_contact_us_content()
        # Close the menu
        if hasattr(self, 'menu_frame') and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
            self.profile_button.place(x=1230, y=5)

    def display_delete_account(self):
        """Display the delete account content"""
        self.clear_content_frame()
        self.create_delete_account_content()
        # Close the menu
        if hasattr(self, 'menu_frame') and self.menu_frame.winfo_exists():
            self.menu_frame.destroy()
            self.profile_button.place(x=1230, y=5)

    def logout(self):
        """Handle logout functionality"""
        response = messagebox.askyesno("Confirm", "Are you sure you want to log out?")
        if response:
            messagebox.showinfo("Action", "Logging out...")
            self.destroy()
            # Here you would import and call your WelcomePage or LoginPage
            # For example: from welcome_page import WelcomePage; WelcomePage()

    # Content creation methods for each page
    def create_change_password_content(self):
        """Create and display the change password page content"""
        canvas = Canvas(
            self.content_frame,
            bg="#FFFFFF",
            height=636,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Title
        canvas.create_text(
            455.0, 30.0, anchor="nw", text="Change Password",
            fill="#000000", font=("Poppins Medium", 36 * -1)
        )

        # Labels
        canvas.create_text(440.0, 110.0, anchor="nw", text="Old Password", fill="#000000",
                           font=("Poppins Medium", 18 * -1))
        canvas.create_text(440.0, 230.0, anchor="nw", text="New Password", fill="#000000",
                           font=("Poppins Medium", 18 * -1))
        canvas.create_text(440.0, 350.0, anchor="nw", text="Confirm Password", fill="#000000",
                           font=("Poppins Medium", 18 * -1))

        # Entry widgets
        try:
            entry_image = PhotoImage(file=self.relative_to_assets("OldPassword.png"))
            self.image_references.append(entry_image)
            canvas.create_image(620.0, 169.0, image=entry_image)
        except:
            canvas.create_rectangle(450, 155, 800, 185, outline="black")

        self.old_password = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,
                                  font=("Poppins Medium", 20))
        self.old_password.place(x=450, y=155, width=350.0, height=30.0)

        try:
            canvas.create_image(620.0, 290.0, image=entry_image)
        except:
            canvas.create_rectangle(450, 275, 800, 305, outline="black")

        self.new_password = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,
                                  font=("Poppins Medium", 20), show="*")
        self.new_password.place(x=450, y=275, width=350.0, height=30.0)

        try:
            canvas.create_image(620.0, 410.0, image=entry_image)
        except:
            canvas.create_rectangle(450, 395, 800, 425, outline="black")

        self.confirm_password = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,
                                      font=("Poppins Medium", 20), show="*")
        self.confirm_password.place(x=450, y=395, width=350.0, height=30.0)

        # Save Button
        try:
            button_image = PhotoImage(file=self.relative_to_assets("SaveButton.png"))
            self.image_references.append(button_image)
            self.save_button = Button(
                canvas, image=button_image, borderwidth=0, highlightthickness=0,
                command=self.change_password, relief="flat"
            )
        except:
            self.save_button = Button(
                canvas, text="Save Changes", borderwidth=0, highlightthickness=0,
                command=self.change_password, relief="flat", bg="#007BFF", fg="white",
                font=("Poppins Medium", 16)
            )
        self.save_button.place(x=450.0, y=490.0, width=340.0, height=54.0)

    def create_privacy_policy_content(self):
        """Create and display the privacy policy page content"""
        canvas = Canvas(
            self.content_frame,
            bg="#FFFFFF",
            height=636,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Title
        canvas.create_text(
            455.0, 30.0, anchor="nw", text="Privacy Policy",
            fill="#000000", font=("Poppins Medium", 36 * -1)
        )

        # Placeholder text - this is where you would put your actual privacy policy
        policy_text = """
            [Privacy Policy Content]

            This page will contain the full privacy policy content.
            The policy content will be added in the future implementation.

            For now, this is a placeholder for the privacy policy section.
            """

        canvas.create_text(
            100.0, 100.0,
            anchor="nw",
            text=policy_text,
            fill="#000000",
            font=("Arial", 14 * -1),
            width=1080  # Set width to allow for text wrapping
        )

    def create_contact_us_content(self):
        # Create main canvas
        self.canvas = Canvas(
            self.content_frame,
            bg="#FFFFFF",
            height=700,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Header
        # self.canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        # # Bottom black strip
        # self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")

        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -30), cursor="hand2")
        poolify_label.place(x=15, y=9)
        poolify_label.bind("<Button-1>", lambda e: self.poolify())

        # Title
        self.canvas.create_text(
            235.0, 40, anchor="nw", text="Address",
            fill="#000000", font=("Arial", 28)
        )

        self.canvas.create_text(
            23.0, 150.0, anchor="nw",
            text="House# 72, Road# 21, Banani, Dhaka-1213 (near\n\nBanani Bidyaniketon School &\n\nCollege, beside University of South Asia)\n\n\n\n\nCall : 1234567890 (24/7)\n\nEmail : supportemailpoolify@gmail.com",
            fill="#000000", font=("Arial", 16)
        )

        # Message section
        self.canvas.create_text(
            789.0, 40, anchor="nw", text="Submit Complaint",
            fill="#000000", font=("Arial", 28)
        )

        # Form fields
        custom_font = ("Arial", 16)

        # Name field
        self.canvas.create_rectangle(635.0, 100.0, 1185.0, 140.0, outline="black", width=2)
        self.name_entry = PlaceholderEntry(
            master=self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=custom_font,
            highlightthickness=0,
            placeholder="Your Name",
            user_email=self.user_email
        )
        self.name_entry.place(x=645.0, y=105.0, width=530.0, height=33.0)

        # Email field
        self.canvas.create_rectangle(635.0, 165.0, 1185.0, 210.0, outline="black", width=2)
        self.email_entry = PlaceholderEntry(
            master=self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=custom_font,
            highlightthickness=0,
            placeholder="Your Email",
            user_email=self.user_email
        )
        self.email_entry.place(x=645.0, y=171.0, width=530.0, height=33.0)

        # Booking reference
        self.canvas.create_rectangle(635.0, 226.0, 1185.0, 271.0, outline="black", width=2)
        self.booking_entry = PlaceholderEntry(
            master=self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=custom_font,
            highlightthickness=0,
            placeholder="Booking Reference (if applicable)",
            user_email=self.user_email
        )
        self.booking_entry.place(x=645.0, y=235.0, width=530.0, height=33.0)

        # Issue type dropdown
        self.canvas.create_text(
            635.0, 285.0, anchor="nw", text="Issue Type:",
            fill="#000000", font=custom_font)

        self.issue_type_var = tk.StringVar()
        issue_types = ["Booking Problem", "Payment Issue", "Car Condition", "Driver Behavior", "App Bug",
                       "Account Issue", "Other"]
        self.issue_dropdown = tk.OptionMenu(self.canvas, self.issue_type_var, *issue_types)
        self.issue_dropdown.config(font=custom_font, bg="#FFFFFF", width=30)
        self.issue_dropdown.place(x=635.0, y=320.0)
        self.issue_type_var.set(issue_types[0])

        # Subject field
        self.canvas.create_rectangle(635.0, 370.0, 1185.0, 415.0, outline="black", width=2)
        self.subject_entry = PlaceholderEntry(
            master=self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=custom_font,
            highlightthickness=0,
            placeholder="Subject",
            user_email=self.user_email
        )
        self.subject_entry.place(x=645.0, y=380.0, width=530.0, height=33.0)

        # Message field
        self.canvas.create_rectangle(635.0, 435.0, 1185.0, 535.0, outline="black", width=2)
        self.message_text = Text(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=custom_font,
            highlightthickness=0,
        )
        self.message_text.place(x=645.0, y=445.0, width=530.0, height=80.0)

        # Add placeholder behavior to the Text widget
        self.message_text.insert("1.0", "Write your message")
        self.message_text.config(fg="grey")
        self.message_text.bind("<FocusIn>", self.clear_placeholder_from_text)
        self.message_text.bind("<FocusOut>", self.add_placeholder_to_text)

        # Submit button
        self.submit_button = tk.Button(
            self.canvas,
            text="Submit Complaint",
            borderwidth=0,
            highlightthickness=0,
            command=self.send_complaint,
            relief="flat",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 16, "bold"),
            padx=10,
            pady=5
        )
        self.submit_button.place(x=759.0, y=550.0, width=280.0, height=54.0)

    def add_placeholder_to_text(self, event=None):
        if not self.message_text.get("1.0", "end-1c"):
            self.message_text.delete("1.0", "end")  # Clear any existing content first
            self.message_text.insert("1.0", "Write your message")
            self.message_text.config(fg="grey")

    def clear_placeholder_from_text(self, event):
        if self.message_text.get("1.0", "end-1c") == "Write your message" and self.message_text.cget("fg") == "grey":
            self.message_text.delete("1.0", "end")
            self.message_text.config(fg="#000716")

    def validate_email(self, email):
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    def send_complaint(self):
        """Handle complaint submission using Brevo API"""
        # Get form values
        name = self.name_entry.get_actual_value()
        email = self.email_entry.get_actual_value()
        booking_ref = self.booking_entry.get_actual_value()
        issue_type = self.issue_type_var.get()
        subject = self.subject_entry.get_actual_value()

        # Get message from Text widget
        message = self.message_text.get("1.0", "end-1c")
        if message == "Write your message" and self.message_text.cget("fg") == "grey":
            message = ""

        # Validation
        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return

        if not email:
            messagebox.showerror("Error", "Please enter your email")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not subject:
            messagebox.showerror("Error", "Please enter a subject")
            return

        if not message:
            messagebox.showerror("Error", "Please enter your message")
            return

        try:
            # Show sending status
            sending_window = tk.Toplevel(self)
            sending_window.title("Sending Complaint")
            sending_window.geometry("300x100")
            sending_window.transient(self)
            tk.Label(sending_window, text="Submitting your complaint, please wait...", font=("Arial", 12)).pack(pady=20)
            sending_window.update()

            # Prepare email content for Brevo API
            email_content = f"""
            Name: {name}
            Email: {email}
            Booking Reference: {booking_ref if booking_ref else 'N/A'}
            Issue Type: {issue_type}

            Message:
            {message}
            """

            # Prepare the API request payload
            payload = {
                "sender": {
                    "name": "CarBooking App",
                    "email": "kmaan0828@gmail.com"  # Use a verified sender email
                },
                "to": [
                    {
                        "email": self.SUPPORT_EMAIL,
                        "name": "CarBooking Support"
                    }
                ],
                "replyTo": {
                    "email": email,
                    "name": name
                },
                "subject": f"[{issue_type}] {subject}",
                "textContent": email_content
            }

            # Set up headers for the API request
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": self.BREVO_API_KEY
            }

            # Send request to Brevo API
            response = requests.post(
                self.BREVO_API_URL,
                headers=headers,
                data=json.dumps(payload)
            )

            print(f"API Response: {response.status_code}")
            print(f"Response body: {response.text}")

            # Close sending status window
            sending_window.destroy()

            # Check response with better error handling
            if response.status_code in [200, 201, 202]:
                messagebox.showinfo("Success",
                                    "Your complaint has been submitted successfully. Our support team will contact you soon.")

                # Clear form fields
                self.name_entry._clear_placeholder(None)
                self.name_entry.delete(0, tk.END)
                self.name_entry._add_placeholder(None)

                self.email_entry._clear_placeholder(None)
                self.email_entry.delete(0, tk.END)
                self.email_entry._add_placeholder(None)

                self.booking_entry._clear_placeholder(None)
                self.booking_entry.delete(0, tk.END)
                self.booking_entry._add_placeholder(None)

                self.subject_entry._clear_placeholder(None)
                self.subject_entry.delete(0, tk.END)
                self.subject_entry._add_placeholder(None)

                self.message_text.delete("1.0", "end")
                self.add_placeholder_to_text()

                # Reset issue type
                self.issue_type_var.set("Booking Problem")

            elif response.status_code == 429:
                # Rate limit exceeded
                messagebox.showerror("Error",
                                     "Email limit exceeded. Please try again later or contact support directly at " + self.SUPPORT_EMAIL)
            else:
                try:
                    error_details = response.json()
                    error_message = error_details.get('message', response.text)
                    messagebox.showerror("Error", f"Failed to submit complaint. Error: {error_message}")
                except:
                    messagebox.showerror("Error", f"Failed to submit complaint. Status code: {response.status_code}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit complaint: {str(e)}")

    def create_delete_account_content(self):
        """Create and display the delete account page content"""
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'carpooling_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'root')
        }

        # Get API key from environment variables
        self.api_key = os.getenv('BREVO_API_KEY')

        if not self.api_key:
            print("Warning: BREVO_API_KEY not found in environment variables")
            # For development only, never in production
            self.api_key = ""
            self.content_frame,
            bg="#FFFFFF",
            height=636,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        canvas.create_text(
            455.0, 30.0, anchor="nw", text="Delete Account",
            fill="#000000", font=("Poppins Medium", 36 * -1)
        )

        # Warning message
        canvas.create_text(
            300.0, 100.0, anchor="nw",
            text="WARNING: This action cannot be undone. All your data will be permanently deleted.",
            fill="#FF0000", font=("Poppins Medium", 16 * -1)
        )

        # Instructions
        canvas.create_text(
            300.0, 150.0, anchor="nw",
            text="To confirm deletion, please enter your email address. We will send you an OTP for verification.",
            fill="#000000", font=("Poppins Medium", 14 * -1)
        )

        # Email field
        canvas.create_text(440.0, 200.0, anchor="nw", text="Email Address", fill="#000000",
                           font=("Poppins Medium", 18 * -1))

        try:
            self.entry_image_delete = PhotoImage(file=self.relative_to_assets("OldPassword.png"))
            self.image_references.append(self.entry_image_delete)  # Store reference
            canvas.create_image(620.0, 250.0, image=self.entry_image_delete)
        except Exception as e:
            print(f"Could not load entry image for delete account: {e}")
            canvas.create_rectangle(450, 235, 800, 265, outline="black")

        self.email_entry = Entry(
            canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Poppins Medium", 20)
        )
        self.email_entry.place(x=450, y=235, width=350.0, height=30.0)
        # Pre-fill with user email if available
        if hasattr(self, 'user_email') and self.user_email:
            self.email_entry.insert(0, self.user_email)

        # Debug label for showing API responses
        self.debug_label = Label(
            canvas,
            text="",
            fg="blue",
            bg="#FFFFFF",
            font=("Poppins", 10),
            wraplength=800,
            justify="left"
        )
        self.debug_label.place(x=300, y=500, width=800, height=100)

        # Send OTP Button
        try:
            self.send_otp_button_image = PhotoImage(file=self.relative_to_assets("SendOTPButton.png"))
            self.image_references.append(self.send_otp_button_image)  # Store reference
            self.send_otp_button = Button(
                canvas,
                image=self.send_otp_button_image,
                borderwidth=0,
                highlightthickness=0,
                command=self.send_otp,
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load Send OTP button image: {e}")
            self.send_otp_button = Button(
                canvas,
                text="Send OTP",
                borderwidth=0,
                highlightthickness=0,
                command=self.send_otp,
                relief="flat",
                bg="#007BFF",
                fg="white",
                font=("Poppins Medium", 14)
            )
        self.send_otp_button.place(x=850.0, y=235.0, width=150.0, height=40.0)

        # OTP field
        canvas.create_text(440.0, 300.0, anchor="nw", text="Enter OTP", fill="#000000",
                           font=("Poppins Medium", 18 * -1))

        try:
            canvas.create_image(620.0, 350.0, image=self.entry_image_delete)
        except Exception as e:
            print(f"Could not use entry image for OTP field: {e}")
            canvas.create_rectangle(450, 335, 800, 365, outline="black")

        self.otp_entry = Entry(
            canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Poppins Medium", 20)
        )
        self.otp_entry.place(x=450, y=335, width=350.0, height=30.0)

        # Delete Account Button
        try:
            self.delete_button_image = PhotoImage(file=self.relative_to_assets("DeleteButton.png"))
            self.image_references.append(self.delete_button_image)  # Store reference
            self.delete_button = Button(
                canvas,
                image=self.delete_button_image,
                borderwidth=0,
                highlightthickness=0,
                command=self.confirm_delete_account,
                relief="flat"
            )
        except Exception as e:
            print(f"Could not load Delete button image: {e}")
            self.delete_button = Button(
                canvas,
                text="Delete Account",
                borderwidth=0,
                highlightthickness=0,
                command=self.confirm_delete_account,
                relief="flat",
                bg="#FF0000",
                fg="white",
                font=("Poppins Medium", 16)
            )
        self.delete_button.place(x=450.0, y=420.0, width=340.0, height=54.0)

        # # Back Button
        # try:
        #     self.back_button_image = PhotoImage(file=self.relative_to_assets("bb.png"))
        #     self.image_references.append(self.back_button_image)  # Store reference
        #     self.back_button = Button(
        #         canvas,
        #         image=self.back_button_image,
        #         borderwidth=0,
        #         highlightthickness=0,
        #         command=self.go_back,
        #         relief="flat"
        #     )
        # except Exception as e:
        #     print(f"Could not load Back button image: {e}")
        #     self.back_button = Button(
        #         canvas,
        #         text="Back",
        #         borderwidth=0,
        #         highlightthickness=0,
        #         command=self.go_back,
        #         relief="flat",
        #         bg="#CCCCCC",
        #         fg="black",
        #         font=("Poppins Medium", 14)
        #     )
        # self.back_button.place(x=50.0, y=30.0, width=100.0, height=40.0)

    def update_debug_label(self, text):
        """Update the debug label with text"""
        if hasattr(self, 'debug_label'):
            self.debug_label.config(text=text)
            self.update()

    def send_otp(self):
        """Send OTP to the provided email using Brevo API"""
        email = self.email_entry.get().strip()

        if not email:
            messagebox.showerror("Error", "Please enter your email address")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        # Verify if email exists in database
        if not self.verify_email_in_database(email):
            messagebox.showerror("Error", "Email address not found in our records")
            return

        # Brevo API endpoint for sending OTP via email
        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        # Generate a random 6-digit OTP
        import random
        otp = str(random.randint(100000, 999999))

        # Store OTP and email for verification
        self.current_otp = otp
        self.current_email = email

        # For debugging - show the OTP in the UI
        self.update_debug_label(f"Generated OTP: {otp}")

        payload = {
            "sender": {
                "name": "Poolify",
                "email": "kmaan0828@gmail.com"  # Make sure this is verified in Brevo
            },
            "to": [{"email": email}],
            "subject": "OTP for Account Deletion",
            "htmlContent": f"<html><body><p>Your OTP for account deletion is: <b>{otp}</b>. This code will expire in 10 minutes.</p></body></html>"
        }

        try:
            # Send the email
            print(f"Sending OTP to {email}")
            self.update_debug_label(f"Sending OTP to {email}...")

            response = requests.post(url, headers=headers, json=payload)
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")

            debug_text = f"Status: {response.status_code}\nResponse: {response.text[:100]}"
            self.update_debug_label(debug_text)

            if response.status_code >= 200 and response.status_code < 300:
                messagebox.showinfo("Success",
                                    "OTP has been sent to your email address. Please check and enter the OTP.")

                # Change button text to "Resend OTP"
                if hasattr(self.send_otp_button, "config"):
                    self.send_otp_button.config(text="Resend OTP")
            else:
                # Get error message from response if available
                try:
                    error_details = response.json()
                    error_msg = f"Code: {error_details.get('code', 'Unknown')}, Message: {error_details.get('message', 'Unknown error')}"
                except:
                    error_msg = f"Status code: {response.status_code}, Response: {response.text[:100]}"

                messagebox.showerror("Error", f"Failed to send OTP: {error_msg}")

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            self.update_debug_label(f"Exception: {str(e)}")
            messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

    def verify_email_in_database(self, email):
        """Verify if the email exists in the database"""
        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                query = "SELECT email FROM users WHERE email = %s"
                # Use the email parameter passed to the function, not self.user_email
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                # Make sure to consume all results
                cursor.fetchall()  # This ensures no unread results remain

                if result:
                    return True
                return False
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to verify email: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def validate_email(self, email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def confirm_delete_account(self):
        """Verify OTP and process account deletion"""
        email = self.email_entry.get().strip()
        otp = self.otp_entry.get().strip()

        if not email or not otp:
            messagebox.showerror("Error", "Please enter both email and OTP")
            return

        if not hasattr(self, 'current_otp') or not hasattr(self, 'current_email'):
            messagebox.showerror("Error", "Please request an OTP first")
            return

        # Check if the entered email matches the one OTP was sent to
        if email != self.current_email:
            messagebox.showerror("Error", "Email address does not match the one OTP was sent to")
            return

        # Verify OTP
        if otp != self.current_otp:
            messagebox.showerror("Error", "Invalid OTP. Please try again")
            return

        # Once OTP is verified, proceed with account deletion
        self.process_account_deletion(email)

    def process_account_deletion(self, email):
        """Process the actual account deletion after OTP verification"""
        # First delete from MySQL database
        if self.delete_from_database(email):
            # Then notify user of successful deletion
            messagebox.showinfo("Success",
                                "Your account has been successfully deleted. The application will now close.")
            self.destroy()
            WelcomePage.WelcomePage()
        else:
            messagebox.showerror("Error", "Failed to delete account from database")

    def delete_from_database(self, email):
        """Delete user account from MySQL database"""
        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                cursor = connection.cursor()

                # Start a transaction to ensure data integrity
                connection.start_transaction()

                try:
                    # Delete user data from related tables
                    # The order matters due to foreign key constraints

                    # First delete from tables that reference users (drivers and any other related tables)
                    cursor.execute("DELETE FROM drivers WHERE email = %s", (email,))

                    # Add any other related tables as needed
                    # cursor.execute("DELETE FROM other_table WHERE email = %s", (email,))

                    # Finally, delete from the main users table
                    cursor.execute("DELETE FROM users WHERE email = %s", (email,))

                    # Commit the transaction if all deletions were successful
                    connection.commit()
                    return True

                except Error as e:
                    # Rollback in case of error
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Failed to delete user data: {str(e)}")
                    return False

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def confirm_logout(self):
        """Handle logout with confirmation."""
        response = messagebox.askyesno("Confirm Logout", "Do you want to logout?", parent=self)
        if response:
            self.logout()

    def logout(self):
        """Perform logout actions."""
        # Here you would handle any logout operations
        # Such as clearing session data, etc.

        # Close the current window and return to login
        self.destroy()
        WelcomePage.WelcomePage()  # Close the main application window

        # Here you would normally redirect to login screen
        # For demonstration purposes
        print("User logged out successfully")

    def go_back(self):
        self.create_change_password_content()


if __name__ == "__main__":
    user_email = 'user@example.com'
    user_type = "user"
    app = AppBase(user_email,user_type)
    app.mainloop()