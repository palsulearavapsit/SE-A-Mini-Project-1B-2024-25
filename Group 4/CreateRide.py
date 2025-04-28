from pathlib import Path
import tkinter as Tk
from tkinter import Canvas, Button, PhotoImage, Frame, Label, ttk, messagebox, Entry, StringVar
from tkcalendar import DateEntry
import requests
from io import BytesIO
from PIL import Image, ImageTk
import mysql.connector
import DriverHomePage
import SearchRide


class CreateRidePage(Tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Nikhil\PycharmProjects\Poolify\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self,user_email):
        super().__init__()

        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.image_references = []  # Prevent garbage collection
        self.menu_frame = None  # Global frame reference
        self.setup_ui()
        self.user_email = user_email
        self.price_var = StringVar()
        self.current_frame = None

        # self.show_frame1()

    def set_price(self, price_value, car_no):
        price = price_value.strip()  # Ensure no leading/trailing spaces
        car_no = car_no.strip()  # Ensure no spaces in car number

        if not price.isdigit():  # Validate input
            messagebox.showerror("Input Error", "Please enter a valid numeric price.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            cursor = conn.cursor()

            query = "UPDATE createride SET price = %s WHERE car_details = %s"
            values = (price, car_no)  # Ensure car_no is included

            cursor.execute(query, values)
            conn.commit()

            if cursor.rowcount > 0:  # Check if any rows were updated
                self.current_frame.destroy()
                messagebox.showinfo("Success", "Ride created successfully!")
            else:
                messagebox.showwarning("Not Found", "No record found with this car number.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    def poolify(self, event=None):
        self.destroy()
        DriverHomePage.HomePage(self.user_email)

    def sbs(self):
        self.destroy()
        SearchRide.RideBookingApp(self.user_email)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_form_entries(self):
        self.entries = {}
        fields = [
            ("Driver Name", "entry_1", 78),  # Shifted 25 points up
            ("Car Details", "entry_2", 160),  # Shifted 25 points up
            ("Start Destination", "entry_3", 242),  # Shifted 25 points up
            ("End Destination", "entry_4", 323),  # Shifted 25 points up
            ("Seats Available", "entry_5", 406),  # Shifted 25 points up
        ]

        for label, entry_name, y_pos in fields:
            # Create text labels
            self.canvas.create_text(51.0, y_pos, anchor="nw", text=label, fill="#000000",
                                    font=("Poppins Medium", 17 * -1))

            # Create entry field background image
            entry_image = PhotoImage(file=self.relative_to_assets("EntryImage.png"))
            self.canvas.create_image(235.0, y_pos + 53, image=entry_image)
            self.image_references.append(entry_image)  # Keep reference to avoid garbage collection

            # Create entry field itself
            entry = Tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
            entry.place(x=55.0, y=y_pos + 34, width=350.0, height=30.0)
            self.entries[entry_name] = entry

        # Entry field for price
        # Date field
        self.canvas.create_text(51.0, 485.0, anchor="nw", text="Date:", fill="#000000",
                                font=("Poppins Medium", 14 * -1))
        self.date_picker = DateEntry(self, width=19, background="darkblue", foreground="white", borderwidth=2,
                                     date_pattern="yyyy-MM-dd")
        self.date_picker.place(x=55.0, y=511.0, width=350.0, height=30.0)

        # Time field
        self.canvas.create_text(51.0, 565.0, anchor="nw", text="Time:", fill="#000000",
                                font=("Poppins Medium", 14 * -1))
        self.time_picker = ttk.Combobox(self, values=[f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)],
                                        state="readonly")
        self.time_picker.place(x=55.0, y=593.0, width=350.0, height=30.0)


    def show_frame1(self):
        if self.current_frame:
            self.current_frame.destroy()

        # Create frame1
        self.current_frame = Frame(self.right_container, bg="white", width=300, height=310, highlightthickness=2)
        self.current_frame.place(x=0, y=50)

        # Label for price
        price_label = Label(self.current_frame, text="Set a price", fg="black", bg="#FFFFFF",
                            font=("Italiana Regular", 18))
        price_label.place(x=90, y=50)

        # Entry field for price
        rupee_label = Label(self.current_frame, text="₹", fg="black", bg="#FFFFFF",
                            font=("Italiana Regular", 18))
        rupee_label.place(x=20, y=105)
        self.price_entry = Entry(self.current_frame, textvariable=self.price_var, bd=0, bg="white", fg="#000716",
                                 highlightthickness=2)
        self.price_entry.place(x=50, y=105, width=180, height=30)

        # Price button
        price_button = Button(self.current_frame, text="Set",
                              command=lambda: self.set_price(self.price_entry.get(), self.entries["entry_2"].get()))
        price_button.place(x=100.0, y=195.0, width=100.0, height=40.0)

        Button(self.current_frame, text="Calculate Fare", command=self.calculate_fare).place(x=100, y=150, width=100,
                                                                                        height=30)

    def setup_ui(self):
        # Create the main canvas
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Black frames and Poolify label
        self.canvas.create_rectangle(0, 0, 1280, 50, fill="#000000", outline="")
        self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")

        # Poolify Label
        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -36), cursor="hand2")
        poolify_label.place(x=15, y=3)
        poolify_label.bind("<Button-1>", self.poolify)

        # Form Labels and Entries
        self.create_form_entries()

        # Buttons for creating ride and showing map
        self.create_ride_button = Button(self, text="Create Ride", command=self.create_ride, relief="flat", bg="#000000", fg="#FFFFFF", font=("Poppins Medium", 18))
        self.create_ride_button.place(x=50.0, y=640.0, width=362.0, height=40.0)

        # Right container for map
        self.right_container = Frame(self, bg="#FFFFFF")
        self.right_container.place(x=450, y=50, width=850, height=646)

        # self.sbs = Button(self.right_container, text="SR", command=self.sbs, relief="flat",
        #                   bg="#000000", fg="#FFFFFF", font=("Poppins Medium", 18))
        # self.sbs.place(x=00.0, y=600.0, width=50.0, height=40.0)

        self.map_label = Label(self.right_container, bg="#FFFFFF")
        self.map_label.place(x=0, y=20, width=950, height=580)
        self.map_label.place_forget()

    def calculate_fare(self):
        if not self.entries or "entry_3" not in self.entries or "entry_4" not in self.entries:
            messagebox.showerror("Error", "Form fields are not initialized! Please open the form first.")
            return

        start_location = self.entries["entry_3"].get()
        drop_location = self.entries["entry_4"].get()

        if not start_location.strip() or not drop_location.strip():
            messagebox.showwarning("Input Error", "Please fill all fields!")
            return

        try:
            API_KEY = "AIzaSyDCZYDh2wDMslhEdFFDQp2ctXqTJ8MehjM"
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={start_location}&destinations={drop_location}&key={API_KEY}"
            response = requests.get(url).json()

            if response["status"] == "OK":
                distance = response["rows"][0]["elements"][0]["distance"]["value"] / 1000  # Convert meters to km
                fare = distance * 18  # ₹18 per km

                self.price_var.set(f"{int(fare)}")  # ₹ sign + integer conversion


                # if self.conn.is_connected():
                #     self.cursor.execute(
                #         "INSERT INTO rides (start_location, drop_location, distance, fare) VALUES (%s, %s, %s, %s)",
                #         (start_location, drop_location, distance, fare)
                #     )
                #     self.conn.commit()
                # else:
                #     messagebox.showerror("Database Error", "Database connection lost!")

        except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_ride(self):
        driver_name = self.entries["entry_1"].get().strip()
        email_name = self.user_email
        car_details = self.entries["entry_2"].get().strip()
        start_location = self.entries["entry_3"].get().strip()
        end_location = self.entries["entry_4"].get().strip()
        seats_available = self.entries["entry_5"].get().strip()
        ride_date = self.date_picker.get()
        ride_time = self.time_picker.get()

        if not all([driver_name, car_details, start_location, end_location, ride_date, ride_time, seats_available]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            seats_available = int(seats_available)
        except ValueError:
            messagebox.showerror("Error", "Seats Available must be a number!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="carpooling_db"
            )
            cursor = conn.cursor()

            # Insert into database
            query = """
            INSERT INTO createride (driver_name,email, car_details, start_location, end_location, seats_available, ride_date, ride_time)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
            """
            values = (driver_name,email_name, car_details, start_location, end_location, seats_available, ride_date, ride_time)

            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            self.show_frame1()


            # end

            # Show map after creating the ride
            self.map_label.place(x=0, y=20, width=950, height=580)
            api_key = "AIzaSyDCZYDh2wDMslhEdFFDQp2ctXqTJ8MehjM"
            base_url = "https://maps.googleapis.com/maps/api/staticmap"
            params = {
                "size": "900x580",
                "maptype": "roadmap",
                "markers": [f"color:blue|label:S|{start_location}", f"color:red|label:E|{end_location}"],
                "path": f"color:0xff0000ff|weight:5|{start_location}|{end_location}",
                "key": api_key,
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            map_image = Image.open(image_data)
            map_photo = ImageTk.PhotoImage(map_image)
            self.map_label.config(image=map_photo)
            self.map_label.image = map_photo

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Map Error", f"Error fetching map: {e}")

if __name__ == "__main__":
    user_email = "nik"
    app = CreateRidePage(user_email)
    app.resizable(False, False)
    app.mainloop()