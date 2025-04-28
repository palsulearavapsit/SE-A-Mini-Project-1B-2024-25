from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Label, Frame, messagebox
import mysql.connector
import CreateRide
import SearchRide
import subprocess
import os
import sys
import SettingsPage
import HistoryPage
import WelcomePage
import WalletPage
import DriverProfile
import datetime

class HomePage(Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self,user_email):
        super().__init__()
        self.geometry("1280x720")
        self.configure(bg="#000000")
        self.image_references = []  # To store image references and prevent garbage collection
        self.user_email = user_email
        self.user_type = "driver"
        self.setup_ui()


    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def launch_poolify_bot(self):
        self.destroy()

        # Import the PoolifyBotApp if not already imported
        import os
        import sys
        # Add the parent directory to sys.path if needed to ensure imports work
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)

        # Import the module (make sure the import path is correct)
        import PoolifyBot  # adjust this import path if needed

        # Create and run the PoolifyBotApp with both user_email and user_type
        bot_app = PoolifyBot.PoolifyBotApp(self.user_email, self.user_type)
        bot_app.mainloop()

    def poolify(self):
        self.destroy()  # Destroys the current window or frame
        WelcomePage.WelcomePage()

    def profile(self):
        self.destroy()
        DriverProfile.DriverProfileApp(self.user_email)

    def createride(self):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root",
                                                 database="carpooling_db")
            cursor = connection.cursor(dictionary=True)

            # Get user data
            query = "SELECT status, full_name FROM drivers WHERE email = %s"
            cursor.execute(query, (self.user_email,))
            user_data = cursor.fetchone()

            if user_data:
                status = user_data["status"].upper() if user_data["status"] else "PENDING"

                # Check if driver status is pending
                if status == "PENDING":
                    # Create a frame with a message that driver cannot create ride until verified
                    pending_frame = Tk()
                    pending_frame.title("Driver Verification Required")
                    pending_frame.geometry("400x200")

                    message_label = Label(pending_frame,
                                             text="You cannot create a ride since your driver account\nis not verified yet. Please wait for verification.",
                                             font=("Arial", 12))
                    message_label.pack(pady=40)

                    pending_frame.mainloop()
                else:
                    # Driver is verified, proceed to create ride page
                    self.destroy()
                    CreateRide.CreateRidePage(self.user_email)
            else:
                # If user data not found, redirect to create ride page
                self.destroy()
                CreateRide.CreateRidePage(self.user_email)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check driver status: {str(e)}")
            print(f"Error in createride method: {str(e)}")


    def searchride(self):
        self.destroy()
        SearchRide.RideBookingApp(self.user_email)

    def settings(self):
        self.destroy()
        SettingsPage.AppBase(self.user_email,self.user_type)

    def walletpage(self):
        self.destroy()  # Destroys the current window or frame
        wallet_page = WalletPage.WalletApp(self.user_email,self.user_type)
        wallet_page.mainloop()

    def chatbot(self):
        self.destroy()

    def setup_ui(self):
        # Set up asset paths
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(
            r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.relative_to_assets = relative_to_assets

        # Create the main canvas
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Static Elements
        self.canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        self.canvas.create_text(15, 9, anchor="nw", text="POOLIFY", fill="#FFFFFF", font=("Italiana Regular", -36))

        # Profile image button
        profile_img = PhotoImage(file=self.relative_to_assets("ProfileTry.png"))
        self.image_references.append(profile_img)  # Keep a reference

        self.profile_button = Button(
            self,
            image=profile_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            fg="#FFFFFF",
            bg="#000000",
            cursor="hand2",
            command=self.toggle_button
        )
        self.profile_button.place(x=1230, y=5, width=50, height=50)

        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root",
                                                 database="carpooling_db")
            cursor = connection.cursor(dictionary=True)

            # Get user data
            query = "SELECT status, full_name FROM drivers WHERE email = %s"
            cursor.execute(query, (self.user_email,))
            user_data = cursor.fetchone()
            print(f"User query executed with email: {self.user_email}")
            print(f"User data retrieved: {user_data}")

            # This is important - fetch all remaining results to clear the cursor
            if cursor.with_rows:
                cursor.fetchall()

            # Get latest ride data - only if user data exists
            user_data1 = None
            if user_data:
                # Use a query that gets the latest entry based on id (assuming higher id = newer entry)
                latest_ride_query = """
                    SELECT start_location, end_location, ride_date, ride_time, seats_available, price 
                    FROM createride 
                    WHERE email = %s
                    ORDER BY id DESC  
                    LIMIT 1
                """
                print(f"About to execute ride query with email: {self.user_email}")
                cursor.execute(latest_ride_query, (self.user_email,))
                user_data1 = cursor.fetchone()
                print(f"Ride data retrieved: {user_data1}")

                # Again, fetch all remaining results
                if cursor.with_rows:
                    cursor.fetchall()
            else:
                print("No user data found, skipping ride query")

            cursor.close()
            connection.close()

            # Set default values first
            status = "PENDING"
            name = "User"
            start = "Not set"
            end = "Not set"
            fare = "0"
            seats = "0"
            ride_date = "Not scheduled"
            ride_time = "Not scheduled"

            # Override with actual data if available
            if user_data:
                status = user_data["status"].upper() if user_data["status"] else "PENDING"
                name = user_data["full_name"] if user_data["full_name"] else "User"
                print(f"User name: {name}, Status: {status}")

            if user_data1:
                start = user_data1["start_location"].upper() if user_data1["start_location"] else "Not set"
                end = user_data1["end_location"].upper() if user_data1["end_location"] else "Not set"
                fare = str(user_data1["price"]) if user_data1["price"] is not None else "0"
                seats = str(user_data1["seats_available"]) if user_data1["seats_available"] is not None else "0"
                ride_date = str(user_data1["ride_date"]) if user_data1["ride_date"] else "Not scheduled"
                ride_time = str(user_data1["ride_time"]) if user_data1["ride_time"] else "Not scheduled"
                print(f"Ride details: {start} to {end}, Date: {ride_date}, Time: {ride_time}")

            # Create and place labels
            status_label = Label(
                self,
                text=status,
                fg="white",
                bg="black",
                font=("Poppins Medium", 20)
            )
            status_label.place(x=940, y=125)

            name_label = Label(
                self,
                text=name,
                fg="black",
                bg="white",
                font=("Poppins Medium", 30)
            )
            name_label.place(x=35, y=155)

            start_label = Label(
                self,
                text=start,
                fg="white",
                bg="black",
                font=("Poppins Medium", 14)
            )
            start_label.place(x=600, y=505)

            fare_label = Label(
                self,
                text=f"₹ {fare}",
                fg="white",
                bg="black",
                font=("Poppins Medium", 14)
            )
            fare_label.place(x=920, y=505)

            end_label = Label(
                self,
                text=end,
                fg="white",
                bg="black",
                font=("Poppins Medium", 14)
            )
            end_label.place(x=590, y=552)

            seats_label = Label(
                self,
                text=seats,
                fg="white",
                bg="black",
                font=("Poppins Medium", 14)
            )
            seats_label.place(x=520, y=597)

            ride_label = Label(
                self,
                text=f"{ride_date} and {ride_time}",
                fg="white",
                bg="black",
                font=("Poppins Medium", 14)
            )
            ride_label.place(x=660, y=643)

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()

        # Welcome page elements
        image_image_1 = PhotoImage(file=self.relative_to_assets("VerificationStatusImage.png"))
        image_1 = self.canvas.create_image(854.0, 143.0, image=image_image_1)
        self.image_references.append(image_image_1)  # Keep a reference

        image_image_2 = PhotoImage(file=self.relative_to_assets("TotalEarningsImage.png"))
        image_2 = self.canvas.create_image(558.0, 331.0, image=image_image_2)
        self.image_references.append(image_image_2)  # Keep a reference

        image_image_3 = PhotoImage(file=self.relative_to_assets("TotalRidesImage.png"))
        image_3 = self.canvas.create_image(973.0, 331.0, image=image_image_3)
        self.image_references.append(image_image_3)  # Keep a reference

        image_image_4 = PhotoImage(file=self.relative_to_assets("YourRideImage.png"))
        image_4 = self.canvas.create_image(765.0, 561.0, image=image_image_4)
        self.image_references.append(image_image_4)  # Keep a reference

        self.canvas.create_text(
            32.0,
            100.0,
            anchor="nw",
            text="Welcome Back ,",
            fill="#000000",
            font=("Poppins Medium", 42 * -1)
        )

    def display_profile_data(self):
        """Fetch and display the user profile data inside menu_frame."""
        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="root",
                                                 database="carpooling_db")
            cursor = connection.cursor(dictionary=True)
            query = "SELECT full_name, email, profile_image FROM drivers WHERE email = %s"
            cursor.execute(query, (self.user_email,))
            user_data = cursor.fetchone()

            # Explicitly consume any remaining results
            while cursor.nextset():
                pass

            cursor.close()
            cursor = None  # Set to None so we don't try to close it again in finally

            if not user_data:
                return  # No user found, skip UI update

            u_name = user_data["full_name"]
            u_email = user_data["email"]
            u_profile_binary = user_data["profile_image"]  # Binary image data

            # Display user details
            name_label = Label(
                self.menu_frame,
                text=f"Name: {u_name}",
                bg="white",
                font=("Poppins Medium", 12)
            )
            name_label.place(x=15, y=150)

            email_label = Label(
                self.menu_frame,
                text=f"Email: {u_email}",
                bg="white",
                font=("Poppins Medium", 12)
            )
            email_label.place(x=15, y=185)

            # Initialize image_references if it doesn't exist
            if not hasattr(self, 'image_references'):
                self.image_references = []

            # Check if user has a profile image
            if u_profile_binary:
                try:
                    from PIL import Image, ImageTk
                    import io

                    # Convert binary data to image
                    image_stream = io.BytesIO(u_profile_binary)
                    pil_image = Image.open(image_stream)

                    # Resize if needed
                    pil_image = pil_image.resize((80, 80))  # Adjust size as needed

                    # Convert PIL image to Tkinter PhotoImage
                    tk_image = ImageTk.PhotoImage(pil_image)

                    # Keep a reference to prevent garbage collection
                    self.image_references.append(tk_image)

                    # Display the image
                    profile_label = Label(
                        self.menu_frame,
                        image=tk_image,
                        bg="#FFFFFF"
                    )
                    profile_label.place(x=20.0, y=60.0)

                except Exception as e:
                    print(f"Error processing profile image: {e}")
                    self.display_default_profile()
            else:
                self.display_default_profile()

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            self.display_default_profile()
        except Exception as main_error:
            print(f"Error in user profile display: {main_error}")
            self.display_default_profile()
        finally:
            # Always close cursor and connection in finally block
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

            if connection:
                try:
                    # Force close connection without checking is_connected
                    connection.close()
                except:
                    pass

    def display_default_profile(self):
        """Display default profile image as fallback."""
        try:
            default_img = PhotoImage(file=self.relative_to_assets("ProfileImage.png"))
            self.image_references.append(default_img)
            profile_label = Label(
                self.menu_frame,
                image=default_img,
                bg="#FFFFFF"
            )
            profile_label.place(x=20.0, y=60.0)
        except Exception:
            # Last resort if even default image fails
            profile_label = Label(
                self.menu_frame,
                text="[Profile]",
                bg="white",
                font=("Poppins Medium", 12)
            )
            profile_label.place(x=20.0, y=60.0)
            print(f"Unexpected error: {e}")

    def toggle_button(self):
        def close_button():
            self.menu_frame.destroy()
            self.profile_button.place(x=1230, y=5)

        self.profile_button.place_forget()

        # Create menu frame
        self.menu_frame = Frame(self, bg="white", width=550, height=638, bd=2, relief="solid", highlightbackground="black",
                               highlightcolor="black")
        self.menu_frame.place(x=1040, y=60)

        # Profile image in menu
        # profile_img_label = PhotoImage(file=self.relative_to_assets("ProfileImage.png"))
        # self.image_references.append(profile_img_label)
        # profile_label = Label(
        #     self.menu_frame,
        #     image=profile_img_label,
        #     bg="#FFFFFF"
        # )
        # profile_label.place(x=20.0, y=60.0)
        # Button details: (image file, x, y, width, command)
        buttons = [
            ("BackButton.png", 0, 15, 105, close_button),
            ("ProfileHome.png", 0, 243, 105, self.profile),
            ("WalletIcon.png", 0, 303, 105, self.walletpage),
            # ("RideHistory.png", 0, 363, 150, self.history_button),
            ("Drive.png", 0, 363, 95, self.createride),
            ("SettingsButton.png", 0, 423, 115, self.settings),
            ("HelpButton.png", 0, 483, 180, self.launch_poolify_bot),
            ("LogOut.png", 0, 543, 95, self.poolify)
        ]

        # Create buttons dynamically
        for img_file, x, y, width, cmd in buttons:
            button_img = PhotoImage(file=self.relative_to_assets(img_file))

            btn = Button(
                self.menu_frame,
                image=button_img,
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                bg="#FFFFFF",
                cursor="hand2",
                command=cmd
            )
            btn.place(x=x, y=y, width=width)

            self.image_references.append(button_img)  # Prevent garbage collection

            separator_positions = [220, 280, 340, 400, 460, 520, 580]

            # Create 8 separator lines
            for sep_y in separator_positions:
                Label(self.menu_frame, bg="#D9D9D9").place(x=0, y=sep_y, width=294, height=1)

        self.display_profile_data()


    def history_button(self):
        self.destroy()
        HistoryPage.HistoryPage(self.user_email)



if __name__ == "__main__":
    user_email = "fg"
    app = HomePage(user_email)
    app.resizable(False, False)
    app.mainloop()
