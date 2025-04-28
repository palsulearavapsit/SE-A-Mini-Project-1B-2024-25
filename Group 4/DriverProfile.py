from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, END, filedialog, CENTER, NORMAL, DISABLED, \
    Label
import mysql.connector
from PIL import Image, ImageTk, ImageDraw, ImageEnhance
import io
import base64
import os
import HomePage
import uuid
import time
import DriverHomePage

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="carpooling_db"
)
cursor = conn.cursor()


def get_car_details(email):
    try:
        cursor = conn.cursor()  # Create cursor here
        cursor.execute("""
            SELECT description, front_image, side_image
            FROM cars
            WHERE email = %s
        """, (email,))

        car_data = cursor.fetchone()

        if car_data:
            car_description, front_image_data, side_image_data = car_data
            return {
                "description": car_description,
                "front_image": front_image_data,
                "side_image": side_image_data
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching car data: {e}")
        return None
    finally:
        cursor.close()  # Always close the cursor


class ProfileImageUploader:
    def __init__(self, master, initial_image_data=None, title="Upload Image"):
        self.master = master
        self.original_image = None
        self.profile_image_data = initial_image_data
        self.image_changed = False

        # Create a canvas for circular image preview
        self.image_canvas = Canvas(master, width=200, height=200, bg='white', highlightthickness=0)
        self.image_canvas.place(x=540.0, y=136.0)

        # Create upload button
        self.upload_button = Button(
            master,
            text=title,
            command=self.upload_image,
            bg="#D9D9D9",
            fg="#000000",
            state=DISABLED
        )
        self.upload_button.place(x=540.0, y=350.0, width=200.0, height=40.0)

        # Load initial image if provided
        if initial_image_data:
            self.load_image_from_data(initial_image_data)
        else:
            self.draw_placeholder()

    def upload_image(self):
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(
            title="Choose Picture",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                # Read the image file as binary data
                with open(file_path, "rb") as img_file:
                    self.profile_image_data = img_file.read()

                self.image_changed = True
                self.load_image_from_data(self.profile_image_data)
            except Exception as e:
                messagebox.showerror("Image Upload Error", str(e))

    def load_image_from_data(self, image_data):
        try:
            # Convert binary data to image
            image_stream = io.BytesIO(image_data)
            original_image = Image.open(image_stream)

            # Resize and crop to square
            width, height = original_image.size
            size = min(width, height)
            left = (width - size) / 2
            top = (height - size) / 2
            right = left + size
            bottom = top + size

            # Crop and resize
            cropped_image = original_image.crop((left, top, right, bottom))
            resized_image = cropped_image.resize((200, 200), Image.LANCZOS)

            # Create circular mask
            mask = Image.new('L', (200, 200), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 200, 200), fill=255)

            # Apply mask
            output = ImageTk.PhotoImage(resized_image)

            # Clear previous content
            self.image_canvas.delete("all")

            # Draw circular image
            self.image_canvas.create_image(
                100, 100,
                image=output,
                anchor=CENTER
            )

            # Keep a reference to prevent garbage collection
            self.original_image = output
        except Exception as e:
            messagebox.showerror("Image Processing Error", str(e))
            self.draw_placeholder()

    def draw_placeholder(self):
        # Clear previous content
        self.image_canvas.delete("all")

        # Draw a circular placeholder
        self.image_canvas.create_oval(
            0, 0, 200, 200,
            outline="#D9D9D9",
            width=2
        )
        self.image_canvas.create_text(
            100, 100,
            text="No Image",
            fill="#D9D9D9"
        )

    def get_profile_image_data(self):
        return self.profile_image_data

    def has_image_changed(self):
        return self.image_changed

    def enable_upload(self):
        self.upload_button.config(state=NORMAL)

    def disable_upload(self):
        self.upload_button.config(state=DISABLED)


class DriverProfileApp(Tk):
    def __init__(self, user_email):
        super().__init__()
        self.title("Poolify App")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)
        self.user_email = user_email

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(
            r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

        # Store button images
        self.edit_image = None
        self.save_image = None
        self.edit_active_overlay = None
        self.edit_inactive_overlay = None
        self.save_active_overlay = None
        self.save_inactive_overlay = None

        # Store original values from DB
        self.original_name = ""
        self.original_phone = ""
        self.original_car_description = ""

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create UI first
        self.create_ui_without_buttons()

        # Now load button images and create buttons
        self.create_button_images()
        self.create_buttons()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def poolify(self, event=None):
        self.destroy()
        DriverHomePage.HomePage(self.user_email)

    def create_ui_without_buttons(self):
        # Title and background elements
        # Black frames and Poolify label
        self.canvas.create_rectangle(0, 0, 1280, 50, fill="#000000", outline="")
        self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")

        # Poolify Label
        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -36), cursor="hand2")
        poolify_label.place(x=15, y=3)
        poolify_label.bind("<Button-1>", self.poolify)

        # Fetch user and car data from database
        try:
            # Get driver details - removed driver_id from SELECT
            cursor.execute("""
                SELECT full_name, phoneno, email, profile_image
                FROM drivers 
                WHERE email = %s
            """, (self.user_email,))
            driver_data = cursor.fetchone()

            # Get car details using the function
            car_data_dict = get_car_details(self.user_email)

            # Extract car data
            if car_data_dict:
                car_description = car_data_dict["description"]
                front_image_data = car_data_dict["front_image"]
                side_image_data = car_data_dict["side_image"]
                # Store original values
                self.original_car_description = car_description if car_description else ""
            else:
                car_description = ""
                front_image_data = side_image_data = None

            # Extract driver data
            if driver_data:
                name, phone_number, email, profile_image_data = driver_data
                # Store original values (convert None to empty string)
                self.original_name = name if name else ""
                self.original_phone = phone_number if phone_number else ""
            else:
                name = phone_number = email = ""
                profile_image_data = None

        except Exception as e:
            print(f"Error fetching user data: {e}")
            name = phone_number = email = car_description = ""
            profile_image_data = front_image_data = side_image_data = None

        # Profile Image Uploader (Driver Profile)
        self.profile_image_uploader = ProfileImageUploader(
            self,
            initial_image_data=profile_image_data,
            title="Upload Profile Picture"
        )
        self.profile_image_uploader.image_canvas.place(x=80.0, y=70.0)
        self.profile_image_uploader.upload_button.place(x=80.0, y=290.0, width=200.0, height=40.0)

        # Car Front Image Uploader
        self.front_image_uploader = ProfileImageUploader(
            self,
            initial_image_data=front_image_data,
            title="Upload Front Car Image"
        )
        self.front_image_uploader.image_canvas.place(x=540.0, y=70.0)
        self.front_image_uploader.upload_button.place(x=540.0, y=290.0, width=200.0, height=40.0)

        # Car Side Image Uploader
        self.side_image_uploader = ProfileImageUploader(
            self,
            initial_image_data=side_image_data,
            title="Upload Side Car Image"
        )
        self.side_image_uploader.image_canvas.place(x=1000.0, y=70.0)
        self.side_image_uploader.upload_button.place(x=1000.0, y=290.0, width=200.0, height=40.0)

        # Labels
        labels = [
            (80.0, 370.0, "Name:"),
            (540.0, 370.0, "Car Description:"),
            (80.0, 480.0, "Phone No:"),
            (540.0, 480.0, "Email:")
        ]

        label_font = ("Inter Bold", 14)
        label_color = "#000000"

        # Create labels
        for x, y, text in labels:
            self.canvas.create_text(
                x, y,
                text=text,
                font=label_font,
                fill=label_color,
                anchor="w"
            )

        # Entry Widgets - Create in NORMAL state, insert text, then disable
        self.name_entry = Entry(self, font=("Inter Bold", 24 * -1), width=20)
        self.name_entry.place(x=80.0, y=400.0, width=391.0, height=63.0)
        # Insert the actual name or placeholder
        if name:
            self.name_entry.insert(0, name)
        else:
            self.name_entry.insert(0, "Enter your name")
        self.name_entry.config(state=DISABLED)  # Disable after inserting text

        self.car_description_entry = Entry(self, font=("Inter Bold", 24 * -1), width=20)
        self.car_description_entry.place(x=540.0, y=400.0, width=391.0, height=63.0)
        # Insert the actual car description or placeholder
        if car_description:
            self.car_description_entry.insert(0, car_description)
        else:
            self.car_description_entry.insert(0, "Enter car description")
        self.car_description_entry.config(state=DISABLED)  # Disable after inserting text

        self.mobile_entry = Entry(self, font=("Inter Bold", 24 * -1), width=20)
        self.mobile_entry.place(x=80.0, y=500.0, width=391.0, height=63.0)
        # Insert the actual phone number or placeholder
        if phone_number:
            self.mobile_entry.insert(0, phone_number)
        else:
            self.mobile_entry.insert(0, "Enter your mobile number")
        self.mobile_entry.config(state=DISABLED)  # Disable after inserting text

        self.email_entry = Entry(self, font=("Inter Bold", 24 * -1), width=20)
        self.email_entry.place(x=540.0, y=500.0, width=391.0, height=63.0)
        # Email is always set to readonly since it's the identifier
        if email:
            self.email_entry.insert(0, email)
        else:
            self.email_entry.insert(0, self.user_email)
        self.email_entry.config(state='readonly')  # Set to readonly after inserting text

        self.canvas.create_text(
            800.0, 590.0,
            text="Click EDIT to update your profile information",
            fill="#000000",
            font=("Inter", 16 * -1),
            anchor="nw"
        )

    def create_button_images(self):
        # Load external button images
        try:
            # Check if ASSETS_PATH exists
            if not os.path.exists(self.ASSETS_PATH):
                # Try to find the assets in common locations
                possible_paths = [
                    Path(__file__).parent / "assets" / "frame0",
                    Path(__file__).parent / "build" / "assets" / "frame0",
                    Path.cwd() / "assets" / "frame0",
                ]

                for p in possible_paths:
                    if os.path.exists(p):
                        self.ASSETS_PATH = p
                        break

            # Paths to button images
            edit_button_path = Path(self.ASSETS_PATH) / "EditInfoButton.png"
            save_button_path = Path(self.ASSETS_PATH) / "SaveInfoButton.png"

            # Check if files exist before loading
            if os.path.exists(edit_button_path) and os.path.exists(save_button_path):
                # Load Edit button images
                edit_img = Image.open(edit_button_path)
                self.edit_image = ImageTk.PhotoImage(edit_img)

                # Create inactive version for Edit button
                edit_inactive = edit_img.copy()
                enhancer = ImageEnhance.Brightness(edit_inactive)
                edit_inactive = enhancer.enhance(0.7)
                self.edit_inactive_overlay = ImageTk.PhotoImage(edit_inactive)
                self.edit_active_overlay = self.edit_image

                # Load Save button images
                save_img = Image.open(save_button_path)
                self.save_image = ImageTk.PhotoImage(save_img)

                # Create inactive version for Save button
                save_inactive = save_img.copy()
                enhancer = ImageEnhance.Brightness(save_inactive)
                save_inactive = enhancer.enhance(0.7)
                self.save_inactive_overlay = ImageTk.PhotoImage(save_inactive)
                self.save_active_overlay = self.save_image
            else:
                raise FileNotFoundError("Button image files not found")

        except Exception as e:
            print(f"Error loading button images: {e}")
            # Fallback to basic buttons without images if loading fails
            # Create black rectangles with text for the buttons

            # Save Info button
            save_img = Image.new('RGB', (221, 50), (0, 0, 0))
            self.save_image = ImageTk.PhotoImage(save_img)

            # Create darkened version for inactive state
            save_inactive = save_img.copy()
            enhancer = ImageEnhance.Brightness(save_inactive)
            save_inactive = enhancer.enhance(0.7)
            self.save_inactive_overlay = ImageTk.PhotoImage(save_inactive)
            self.save_active_overlay = self.save_image

            # Edit Info button
            edit_img = Image.new('RGB', (221, 50), (0, 0, 0))
            self.edit_image = ImageTk.PhotoImage(edit_img)

            # Create darkened version for inactive state
            edit_inactive = edit_img.copy()
            enhancer = ImageEnhance.Brightness(edit_inactive)
            edit_inactive = enhancer.enhance(0.7)
            self.edit_inactive_overlay = ImageTk.PhotoImage(edit_inactive)
            self.edit_active_overlay = self.edit_image

    def create_buttons(self):
        # Edit Button with image
        self.edit_button = Button(
            self,
            text="Edit Info" if not self.edit_image else "",
            image=self.edit_image,
            compound=CENTER,
            fg="white",
            bg="black",
            borderwidth=0,
            highlightthickness=0,
            command=self.toggle_edit_mode,
            relief="flat"
        )
        self.edit_button.place(x=800.0, y=629.0, width=221.0, height=50.0)

        # Save Button with image
        self.save_button = Button(
            self,
            text="Save Info" if not self.save_image else "",
            image=self.save_inactive_overlay,  # Start with inactive image
            compound=CENTER,
            fg="white",
            bg="black",
            borderwidth=0,
            highlightthickness=0,
            command=self.save_profile,
            relief="flat",
            state=DISABLED
        )
        self.save_button.place(x=1050.0, y=629.0, width=221.0, height=50.0)

        # View Car Details button removed as requested

    def toggle_edit_mode(self):
        # Get current values
        current_name = self.name_entry.get()
        current_phone = self.mobile_entry.get()
        current_car_description = self.car_description_entry.get()

        # Clear fields
        self.name_entry.config(state=NORMAL)
        self.mobile_entry.config(state=NORMAL)
        self.car_description_entry.config(state=NORMAL)

        self.name_entry.delete(0, END)
        self.mobile_entry.delete(0, END)
        self.car_description_entry.delete(0, END)

        # Restore actual values (not placeholders)
        if current_name == "Enter your name":
            self.name_entry.insert(0, self.original_name)
        else:
            self.name_entry.insert(0, current_name)

        if current_phone == "Enter your mobile number":
            self.mobile_entry.insert(0, self.original_phone)
        else:
            self.mobile_entry.insert(0, current_phone)

        if current_car_description == "Enter car description":
            self.car_description_entry.insert(0, self.original_car_description)
        else:
            self.car_description_entry.insert(0, current_car_description)

        # Enable image uploads
        self.profile_image_uploader.enable_upload()
        self.front_image_uploader.enable_upload()
        self.side_image_uploader.enable_upload()

        # Enable save button
        self.save_button.config(state=NORMAL)
        if self.save_active_overlay:
            self.save_button.config(image=self.save_active_overlay)

        # Disable edit button
        self.edit_button.config(state=DISABLED)
        if self.edit_inactive_overlay:
            self.edit_button.config(image=self.edit_inactive_overlay)

    def save_profile(self):
        # Get values from entry fields
        name = self.name_entry.get()
        phone_number = self.mobile_entry.get()
        car_description = self.car_description_entry.get()
        email = self.email_entry.get()

        # Get image data
        profile_image_data = self.profile_image_uploader.get_profile_image_data()
        front_image_data = self.front_image_uploader.get_profile_image_data()
        side_image_data = self.side_image_uploader.get_profile_image_data()

        # Validate inputs
        if not name or name == "Enter your name":
            messagebox.showwarning("Validation Error", "Please enter your name")
            return

        if not phone_number or phone_number == "Enter your mobile number":
            messagebox.showwarning("Validation Error", "Please enter your mobile number")
            return

        if not car_description or car_description == "Enter car description":
            messagebox.showwarning("Validation Error", "Please enter car description")
            return

        try:
            # First check if driver exists
            cursor.execute("SELECT email FROM drivers WHERE email = %s", (email,))
            driver_record = cursor.fetchone()

            if driver_record:
                # Update existing driver
                cursor.execute("""
                    UPDATE drivers 
                    SET 
                        full_name = %s, 
                        phoneno = %s, 
                        profile_image = %s
                    WHERE 
                        email = %s;
                """, (name, phone_number, profile_image_data, email))
            else:
                # Insert new driver with all required fields (removed driver_id)
                cursor.execute("""
                    INSERT INTO drivers (email, full_name, phoneno, profile_image, status, password)
                    VALUES (%s, %s, %s, %s, 'pending', '');
                """, (email, name, phone_number, profile_image_data))

            # Check if car record exists, then upsert
            cursor.execute("SELECT email FROM cars WHERE email = %s", (email,))
            car_exists = cursor.fetchone()

            if car_exists:
                # Update existing car
                cursor.execute("""
                    UPDATE cars
                    SET 
                        description = %s,
                        front_image = %s,
                        side_image = %s
                    WHERE
                        email = %s;
                """, (car_description, front_image_data, side_image_data, email))
            else:
                # Insert new car record
                cursor.execute("""
                    INSERT INTO cars (email, description, front_image, side_image)
                    VALUES (%s, %s, %s, %s);
                """, (email, car_description, front_image_data, side_image_data))

            # Commit the transaction
            conn.commit()

            # Update original values
            self.original_name = name
            self.original_phone = phone_number
            self.original_car_description = car_description

            # Show success message
            messagebox.showinfo("Success", "Profile updated successfully!")

            # Disable editing
            self.name_entry.config(state=DISABLED)
            self.car_description_entry.config(state=DISABLED)
            self.mobile_entry.config(state=DISABLED)

            # Disable image uploads
            self.profile_image_uploader.disable_upload()
            self.front_image_uploader.disable_upload()
            self.side_image_uploader.disable_upload()

            # Enable edit button, disable save
            self.edit_button.config(state=NORMAL)
            if self.edit_active_overlay:
                self.edit_button.config(image=self.edit_active_overlay)

            self.save_button.config(state=DISABLED)
            if self.save_inactive_overlay:
                self.save_button.config(image=self.save_inactive_overlay)

        except Exception as e:
            # Rollback in case of error
            conn.rollback()

            # Show error message
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")


if __name__ == "__main__":
    user_email = "user@example.com"
    app = DriverProfileApp(user_email)
    app.mainloop()