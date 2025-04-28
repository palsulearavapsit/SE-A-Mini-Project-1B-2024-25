from pathlib import Path
import tkinter as Tk
from tkinter import Canvas, Entry, Button, PhotoImage, filedialog, messagebox, Label
import mysql.connector
from PIL import Image, ImageTk
import io
import CreateRide
import WalletPage
import DriverHomePage
import LoginPage

class DriverVerificationApp(Tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self, user_email):
        super().__init__()
        self.title("Poolify App")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.user_email = user_email

        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="carpooling_db"
        )
        self.cursor = self.conn.cursor()

        # Initialize global variables for image paths
        self.profile_image_path = None
        self.car_front_image_path = None
        self.car_side_image_path = None

        # Build the UI
        self.create_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def upload_image(self, image_label, image_type):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    image_data = file.read()

                img = Image.open(io.BytesIO(image_data))
                img = img.resize((180, 150), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img  # Keep a reference to avoid garbage collection

                # Assign image data to the respective variable
                if image_type == "profile":
                    self.profile_image_data = image_data
                elif image_type == "car_front":
                    self.car_front_image_data = image_data
                elif image_type == "car_side":
                    self.car_side_image_data = image_data

            except IOError as e:
                messagebox.showerror("Error", f"Error opening image file: {e}")

    def save_data(self):
        phone_number = self.entry_1.get()
        car_description = self.entry_2.get()

        # Validate input
        if not phone_number or not car_description:
            messagebox.showerror("Error", "Please fill all fields")
            return

        # Check if images are uploaded
        if not hasattr(self, 'profile_image_data') or not hasattr(self, 'car_front_image_data') or not hasattr(self,
                                                                                                               'car_side_image_data'):
            messagebox.showerror("Error", "Please upload all required images")
            return

        # Debug info
        print(f"Email length: {len(self.user_email)}")

        try:
            # Update driver information with phone number and profile image
            update_query = "UPDATE drivers SET phoneno = %s, profile_image = %s WHERE email = %s"
            self.cursor.execute(update_query, (phone_number, self.profile_image_data, self.user_email))

            # Check if driver was updated
            if self.cursor.rowcount == 0:
                print("No driver record was updated. Creating a new record.")
                # Insert driver record if doesn't exist
                insert_query = "INSERT INTO drivers (email, phoneno, profile_image) VALUES (%s, %s, %s)"
                self.cursor.execute(insert_query, (self.user_email, phone_number, self.profile_image_data))

            # Check if car record exists
            self.cursor.execute("SELECT 1 FROM cars WHERE email = %s", (self.user_email,))
            car_exists = self.cursor.fetchone()

            if car_exists:
                # Update existing car record
                car_update = "UPDATE cars SET description = %s, front_image = %s, side_image = %s WHERE email = %s"
                self.cursor.execute(car_update, (
                car_description, self.car_front_image_data, self.car_side_image_data, self.user_email))
            else:
                # Insert car information
                car_insert = "INSERT INTO cars (email, description, front_image, side_image) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(car_insert, (
                self.user_email, car_description, self.car_front_image_data, self.car_side_image_data))

            self.conn.commit()
            messagebox.showinfo("Success", "Information saved successfully!")
            self.destroy()
            LoginPage.LoginPage()
        except mysql.connector.Error as db_error:
            self.conn.rollback()
            error_msg = f"Database error ({db_error.errno}): {db_error.msg}"
            print(error_msg)
            messagebox.showerror("Database Error", error_msg)
        except Exception as e:
            self.conn.rollback()
            print(f"Unexpected error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def create_ui(self):
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        elements = [
            ((0, 0, 1280, 50), "#000000", ""),
            ((0, 696, 1280, 721), "#000000", ""),
            ((19, 146, 632, 646), "#FFFFFF", "black"),
            ((20, 146, 632, 227), "#D9D9D9", "black"),
            ((649, 146, 1262, 646), "#FFFFFF", "black"),
            ((650, 146, 1262, 227), "#D9D9D9", "black"),
            ((212, 422, 412, 572), "#DEDEDE", ""),
            ((691, 422, 891, 572), "#DEDEDE", ""),
            ((995, 422, 1195, 572), "#DEDEDE", "")
        ]
        for coords in elements:
            self.canvas.create_rectangle(*coords[0], fill=coords[1], outline=coords[2])

        texts = [
            (497, 72, "Driver Verification", 32),
            (277, 117, "Complete your profile to become a complete verified driver on our platform.", 20),
            (102, 187, "Your personal identification details", 20),
            (59, 254, "Phone Number", 24),
            (59, 369, "Profile Photo", 24), (732, 158, "Car Information", 24),
            (732, 187, "Details about the vehicle you’ll be using", 20),
            (689, 241, "Car Description & Plate Number", 24),
            (691, 341, "Please include the color, model, and license plate number", 20), (691, 376, "Car Photos", 24),
            (723, 485, "Front view", 24), (1034, 485, "Side view", 24)
        ]
        for x, y, text, size, color in [(t[0], t[1], t[2], t[3], t[4] if len(t) > 4 else "#000000") for t in texts]:
            self.canvas.create_text(x, y, anchor="nw", text=text, fill=color, font=("Inter", size * -1))

        images = [("profile_image1.png", 58, 180), ("car_image1.png", 693, 180)]
        for img, x, y in images:
            setattr(self, f"image_{img.split('_')[0]}", PhotoImage(file=self.relative_to_assets(img)))
            setattr(self, f"image_{img.split('_')[0]}_id", self.canvas.create_image(x, y,
                                                                                    image=getattr(self,
                                                                                                  f"image_{img.split('_')[0]}")))

        # Load the entry field background image
        self.entry_bg = PhotoImage(file=self.relative_to_assets("EntryImage1.png"))

        # Create images behind entry fields
        self.entry_bg_1 = self.canvas.create_image(255, 310, image=self.entry_bg)
        self.entry_bg_2 = self.canvas.create_image(890, 310, image=self.entry_bg)

        # Create entry fields on top of the images
        self.entry_1 = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=60, y=290, width=380, height=35)

        self.entry_2 = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=700, y=290, width=380, height=35)

        image_labels = [(212, 422), (691, 422), (995, 422)]
        for idx, (x, y) in enumerate(image_labels, 1):
            setattr(self, f"label_{idx}", Label(self, bg="#DEDEDE"))
            getattr(self, f"label_{idx}").place(x=x, y=y, width=200, height=150)

        buttons = [
            ("Upload_button.png", 212, 581, lambda: self.upload_image(self.label_1, "profile")),
            ("Upload_button.png", 689, 585, lambda: self.upload_image(self.label_2, "car_front")),
            ("Upload_button.png", 995, 585, lambda: self.upload_image(self.label_3, "car_side")),
            ("Submit_button.png", 545, 655, self.save_data)
        ]
        for i, (file, x, y, cmd) in enumerate(buttons, 1):
            setattr(self, f"button_img_{i}", PhotoImage(file=self.relative_to_assets(file)))
            setattr(self, f"button_{i}", Button(image=getattr(self, f"button_img_{i}"), borderwidth=0,
                                                highlightthickness=0, command=cmd, relief="flat"))
            getattr(self, f"button_{i}").place(x=x, y=y, width=200, height=42 if i != 4 else 38)


if __name__ == "__main__":
    app = DriverVerificationApp("user@example.com")
    app.resizable(False, False)
    app.mainloop()
