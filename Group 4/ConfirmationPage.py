from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Label
from PIL import Image, ImageTk
import mysql.connector
import HomePage

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="carpooling_db"
)
cursor = conn.cursor()


class PaymentPage(tk.Toplevel):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\Poolify\Tkinter-Designer-master\build\assets\frame0"
    )

    def __init__(self, ride_amount=2500, passenger_email=None, driver_email=None):
        super().__init__()
        self.title("Pay for Ride")
        self.geometry("400x350")
        self.configure(bg="#FFFFFF")
        self.center_window(400, 350)
        self.canvas = tk.Canvas(self, bg="#FFFFFF", height=350, width=400, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Store ride details
        self.ride_amount = ride_amount
        self.passenger_email = passenger_email
        self.driver_email = driver_email

        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'carpooling_db'
        }

        # Fetch wallet balance for display
        self.passenger_balance = self.get_wallet_balance(self.passenger_email)

        self.create_widgets()

    def center_window(self, width, height):
        """Centers the window on the screen."""
        screen_width = self.winfo_screenwidth()  # Get screen width
        screen_height = self.winfo_screenheight()  # Get screen height

        x_position = (screen_width // 2) - (width // 2)  # Calculate X coordinate
        y_position = (screen_height // 2) - (height // 2)  # Calculate Y coordinate

        self.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_widgets(self):
        # Status message area (initially hidden)
        self.status_text = tk.Text(self, height=3, width=45, wrap=tk.WORD, bg="#F0F0F0")
        self.status_text.place(x=28, y=170, width=350, height=35)
        self.status_text.config(state=tk.DISABLED)
        self.status_text.place_forget()  # Hide initially

        texts = [
            (142, 24, "Pay for Ride", "Inter Bold", 20),
            (170, 77, f" {self.ride_amount}", "Inter", 32),
            (142, 77, "₹", "Inter SemiBold", 32),
            (283, 211, "₹", "Inter Medium", 14),
            (43, 210, "Wallet Balance", "Inter Medium", 16),
            (301, 211, str(self.passenger_balance), "Inter Medium", 14),
            (156, 121, "Total Amount", "Inter", 14),
        ]

        for x, y, text, font, size in texts:
            self.canvas.create_text(x, y, anchor="nw", text=text, fill="#000000", font=(font, -size))

        self.canvas.create_rectangle(28, 197, 378, 239, fill="#B5B5B5", outline="")

        # Load button image
        img_path = self.relative_to_assets("Pay_button.png")
        pil_image = Image.open(img_path)  # Open image using PIL
        self.button_image = ImageTk.PhotoImage(pil_image)  # Convert to Tk-compatible format

        self.pay_button = tk.Button(self, image=self.button_image, borderwidth=0, highlightthickness=0,
                                    command=self.on_pay_click, relief="flat")
        self.pay_button.place(x=28, y=268, width=350, height=42)

    def connect_to_db(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except mysql.connector.Error as err:
            self.update_status(f"Database connection error: {err}")
            return None

    def get_wallet_balance(self, email):
        """Get the wallet balance for a given email"""
        if not email:
            return 0  # Default value if no email provided

        conn = None
        cursor = None
        try:
            conn = self.connect_to_db()
            if not conn:
                return 0

            cursor = conn.cursor(dictionary=True)

            # Get wallet ID
            cursor.execute("SELECT wallet_id FROM wallet WHERE email = %s", (email,))
            wallet = cursor.fetchone()

            if not wallet:
                return 0

            wallet_id = wallet['wallet_id']

            # Get sum of credits
            cursor.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM wallettransactions "
                "WHERE wallet_id = %s AND transaction_type = 'credit'",
                (wallet_id,)
            )
            credits = cursor.fetchone()['total']

            # Get sum of debits
            cursor.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM wallettransactions "
                "WHERE wallet_id = %s AND transaction_type = 'debit'",
                (wallet_id,)
            )
            debits = cursor.fetchone()['total']

            # Calculate balance
            from decimal import Decimal
            balance = Decimal(credits) - Decimal(debits)
            return float(balance)

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_status(self, message):
        """Update the status message area"""
        self.status_text.place(x=28, y=170, width=350, height=35)  # Show the text area
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, message)
        self.status_text.config(state=tk.DISABLED)
        print(message)  # Also print to console for debugging

    def on_pay_click(self):
        """Process the payment when Pay button is clicked"""
        if not self.passenger_email or not self.driver_email:
            self.update_status("Error: Missing passenger or driver information")
            return

        try:
            from decimal import Decimal
            amount = Decimal(str(self.ride_amount))
            if amount <= 0:
                self.update_status("Error: Invalid payment amount")
                return
        except:
            self.update_status("Error: Invalid payment amount")
            return

        conn = None
        cursor = None

        try:
            conn = self.connect_to_db()
            if not conn:
                return

            cursor = conn.cursor(dictionary=True)

            # Get passenger wallet
            cursor.execute("SELECT wallet_id FROM wallet WHERE email = %s", (self.passenger_email,))
            passenger_wallet = cursor.fetchone()

            # Get driver wallet
            cursor.execute("SELECT wallet_id FROM wallet WHERE email = %s", (self.driver_email,))
            driver_wallet = cursor.fetchone()

            if not passenger_wallet:
                self.update_status(f"Passenger wallet not found for this account")
                return

            if not driver_wallet:
                self.update_status(f"Driver wallet not found")
                return

            # Get passenger balance
            passenger_balance = self.get_wallet_balance(self.passenger_email)

            # Check if passenger has enough balance
            if passenger_balance < float(amount):
                self.update_status(f"Insufficient balance. Available: ₹{passenger_balance}")
                return

            # Make sure any existing transactions are completed
            conn.rollback()  # This will clear any lingering transactions

            # Begin transaction
            conn.start_transaction()

            # 1. Debit from passenger wallet
            cursor.execute(
                "INSERT INTO wallettransactions (wallet_id, transaction_type, amount, email) VALUES (%s, %s, %s, %s)",
                (passenger_wallet['wallet_id'], 'debit', amount, self.driver_email)
            )

            # 2. Credit to driver wallet
            cursor.execute(
                "INSERT INTO wallettransactions (wallet_id, transaction_type, amount, email) VALUES (%s, %s, %s, %s)",
                (driver_wallet['wallet_id'], 'credit', amount, self.passenger_email)
            )

            # 3. Update seats_available in createride table
            cursor.execute(
                "UPDATE createride SET seats_available = seats_available - 1 WHERE email = %s AND seats_available > 0",
                (self.driver_email,)
            )

            # Check if any rows were affected by the update
            if cursor.rowcount == 0:
                conn.rollback()
                self.update_status("Error: No available seats or ride not found")
                return

            # Commit transaction
            conn.commit()

            # Show success message
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Payment Successful",
                                f"₹{amount} transferred successfully!\nThank you for using Poolify.")

            # Close the payment window
            self.destroy()

        except mysql.connector.Error as err:
            self.update_status(f"Payment failed: {err}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass  # Ignore errors during rollback
        finally:
            # Always close resources in finally block
            if cursor:
                cursor.close()
            if conn:
                conn.close()


class RideConfirmationPage(tk.Tk):
    def __init__(self, passenger_email, driver_email, start, end):
        super().__init__()
        self.title("Ride Confirmation")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")

        self.passenger_email = passenger_email
        self.driver_email = driver_email
        self.start = start
        self.end = end

        # Fetch ride details from database
        self.ride_details = self.fetch_ride_details()

        self.ASSETS_PATH = Path(r"C:\Users\Nikhil\PycharmProjects\Poolify\Tkinter-Designer-master\build\assets\frame0")

        self.setup_ui()

    def fetch_ride_details(self):
        """Fetch ride details from the createride table based on driver email, start and end location"""
        try:
            # Query to fetch ride details based on the createride table structure
            query = """
                SELECT id, driver_name, email, car_details, 
                       start_location, end_location, ride_date, ride_time, 
                       price, seats_available
                FROM createride
                WHERE email = %s AND start_location = %s AND end_location = %s
                ORDER BY ride_date DESC, ride_time DESC
                LIMIT 1
            """
            cursor.execute(query, (self.driver_email, self.start, self.end))
            result = cursor.fetchone()

            if result:
                ride_details = {
                    'ride_id': result[0],
                    'driver_name': result[1],
                    'driver_email': result[2],
                    'vehicle': result[3],
                    'start_location': result[4],
                    'end_location': result[5],
                    'ride_date': result[6],
                    'ride_time': result[7],
                    'price': result[8] if result[8] is not None else 2500,  # Default price if NULL
                    'seats_available': result[9]
                }
                return ride_details
            else:
                # Default values if no ride is found
                return {
                    'ride_id': 0,
                    'driver_name': "Driver Not Found",
                    'driver_email': self.driver_email,
                    'vehicle': "Vehicle Not Found",
                    'start_location': self.start,
                    'end_location': self.end,
                    'ride_date': "N/A",
                    'ride_time': "N/A",
                    'price': 2500,
                    'seats_available': 0
                }
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            # Default values in case of error
            return {
                'ride_id': 0,
                'driver_name': "Database Error",
                'driver_email': self.driver_email,
                'vehicle': "Error fetching vehicle",
                'start_location': self.start,
                'end_location': self.end,
                'ride_date': "N/A",
                'ride_time': "N/A",
                'price': 2500,
                'seats_available': 0
            }

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def poolify(self, event=None):
        self.destroy()
        HomePage.HomePage(self.passenger_email)


    def paymentpage(self):
        PaymentPage(
            ride_amount=self.ride_details['price'],
            passenger_email=self.passenger_email,
            driver_email=self.driver_email
        )

    def setup_ui(self):
        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        canvas.create_rectangle(0.0, 0.0, 1280.0, 50.0, fill="#000000", outline="")
        canvas.create_rectangle(0.0, 696.0, 1280.0, 721.0, fill="#000000", outline="")

        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -36), cursor="hand2")
        poolify_label.place(x=15, y=3)
        poolify_label.bind("<Button-1>", self.poolify)

        # Define rectangles as (x1, y1, x2, y2, fill color)
        rectangles = [
            (0.0, 725.0, 1280.0, 750.0, "#000000"),
            (240.0, 182.0, 1040.0, 257.0, "#FFFFFF"),
            (240.0, 273.0, 1040.0, 619.0, "#FFFFFF"),
            (256.0, 548.0, 1011.0, 551.0, "#959595")
        ]

        for rect in rectangles:
            canvas.create_rectangle(*rect[:4], fill=rect[4], outline="black")

        # Define images as (file_name, x, y)
        # Removed Star.png, Clock.png, and Location.png
        image_files = [
            ("GreenCircle.png", 640.0, 88.0),
            ("CarImage1.png", 640.0, 89.0),
            ("GreyCircle.png", 300.0, 218.0),
            ("BlueLocation.png", 281.0, 369.0),
            ("RedLocation.png", 280.0, 482.0),
            ("PriceRupee.png", 907.0, 577.0)
        ]

        self.image_objects = []
        for img_file, x, y in image_files:
            img = PhotoImage(file=self.relative_to_assets(img_file))
            self.image_objects.append(img)  # Store references to avoid garbage collection
            canvas.create_image(x, y, image=img)

        # Define text elements using the fetched ride details
        # Removed driver_rating, duration, and distance text elements
        text_elements = [
            (513.0, 127.0, "Ride Confirmed!", "#000000", ("Inter Bold", 32 * -1)),
            (373.0, 191.0, self.ride_details['driver_name'], "#000000", ("Inter Bold", 24 * -1)),
            (373.0, 226.0, self.ride_details['vehicle'], "#201C1C", ("Inter SemiBold", 20 * -1)),
            (267.0, 288.0, "Journey Details", "#000000", ("PontanoSans Bold", 24 * -1)),
            (319.0, 351.0, "Pickup Location", "#000000", ("PontanoSans Bold", 24 * -1)),
            (319.0, 463.0, "Dropoff Location", "#000000", ("PontanoSans Bold", 24 * -1)),
            (321.0, 382.0, self.ride_details['start_location'], "#1E1E1E", ("PontanoSans Bold", 20 * -1)),
            (319.0, 494.0, self.ride_details['end_location'], "#1E1E1E", ("PontanoSans Bold", 20 * -1)),
            (924.0, 564.0, str(self.ride_details['price']), "#1E1E1E", ("PontanoSans Bold", 20 * -1))
        ]

        for x, y, text, fill, font in text_elements:
            canvas.create_text(x, y, anchor="nw", text=text, fill=fill, font=font)

        # Create the buttons
        button_image = PhotoImage(file=self.relative_to_assets("OpenGoogle1.png"))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_click,
            relief="flat"
        )
        button.image = button_image  # Prevent garbage collection
        button.place(x=236.0, y=641.0, width=370.0, height=53.0)

        button_image = PhotoImage(file=self.relative_to_assets("Pay_now1.png"))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.paymentpage,
            relief="flat"
        )
        button.image = button_image  # Prevent garbage collection
        button.place(x=706.0, y=641.0, width=340.0, height=50.0)


    def on_button_click(self):
        print("Button clicked!")


if __name__ == "__main__":
    passenger_email = "123"
    driver_email = "321"
    start_location = "mumbai"
    end_location = "thane"
    app = RideConfirmationPage(passenger_email, driver_email, start_location, end_location)
    app.mainloop()