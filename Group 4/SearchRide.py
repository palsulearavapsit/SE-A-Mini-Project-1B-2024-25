from pathlib import Path
import tkinter as Tk
from tkinter import Canvas, Entry, Button, PhotoImage, messagebox, Frame, Label, Scrollbar
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
import HomePage
import ConfirmationPage


class RideBookingApp(Tk.Tk):
    def __init__(self, user_email):
        super().__init__()
        self.title("Poolify App")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.user_email = user_email
        self.passenger_email = user_email
        # Define paths
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(
            r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=750,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.create_widgets()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def poolify(self, event=None):
        self.destroy()
        HomePage.HomePage(self.user_email)

    def create_widgets(self):
        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 50.0, fill="#000000", outline="")
        self.canvas.create_rectangle(0.0, 725.0, 1280.0, 750.0, fill="#000000", outline="")

        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -36), cursor="hand2")
        poolify_label.place(x=15, y=3)
        poolify_label.bind("<Button-1>", self.poolify)

        self.canvas.create_rectangle(105.0, 136.0, 605.0, 674.0, fill="#FFFFFF", outline="")

        # Entry fields and labels
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("EntryImage.png"))
        self.canvas.create_image(354.0, 205.0, image=self.entry_image_1)
        self.entry_1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=174.0, y=189, width=362.0, height=27.35)

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("EntryImage.png"))
        self.canvas.create_image(354.0, 310.0, image=self.entry_image_2)
        self.entry_2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=174.0, y=294, width=362.0, height=27.35)

        self.canvas.create_text(169.0, 162.0, anchor="nw", text="Start Destination:", fill="#000000",
                                font=("Poppins Medium", 20 * -1))
        self.canvas.create_text(169.0, 264.0, anchor="nw", text="End Destination:", fill="#000000",
                                font=("Poppins Medium", 20 * -1))
        self.canvas.create_text(169.0, 369.0, anchor="nw", text="Date:", fill="#000000",
                                font=("Poppins Medium", 20 * -1))

        # DateChooser (calendar)
        self.date_picker = DateEntry(self, width=19, background='darkblue', foreground='white', borderwidth=2)
        self.date_picker.place(x=174.0, y=399.0, width=362.0, height=30)

        self.canvas.create_text(286.0, 71.0, anchor="nw", text="Search Ride!!", fill="#000000",
                                font=("Inter Bold", 32 * -1))

        # Right container (Scrollable Ride List)
        self.right_container = Frame(self, bg="#FFFFFF")
        self.right_container.place(x=610, y=50, width=670, height=675)

        # Create a canvas inside right_container for scrolling
        ride_canvas = Canvas(self.right_container, bg="#FFFFFF", height=675, width=670)
        ride_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar for ride list
        scrollbar = Scrollbar(self.right_container, orient="vertical", command=ride_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure Canvas with Scrollbar
        ride_canvas.configure(yscrollcommand=scrollbar.set)
        ride_canvas.bind("<Configure>", lambda e: ride_canvas.configure(scrollregion=ride_canvas.bbox("all")))

        # Frame inside Canvas for Ride Entries
        self.scrollable_frame = Frame(ride_canvas, bg="#F5F5F5")
        ride_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=650)

        # Search Button
        button_image_1 = PhotoImage(file=self.relative_to_assets("SearchRide.png"))
        self.button_1 = Button(image=button_image_1, borderwidth=0, cursor="hand2", highlightthickness=0,
                               command=self.search_ride, relief="flat")
        self.button_1.place(x=169.0, y=579.0, width=372.0, height=44.0)
        self.button_image_2 = button_image_1

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="carpooling_db"
        )

    def book_ride(self, ride_id, seats_available_label):
        try:
            conn = self.connect_to_database()
            cursor = conn.cursor()

            cursor.execute("SELECT seats_available FROM createride WHERE id = %s", (ride_id,))
            seats_available = cursor.fetchone()[0]

            if seats_available > 0:
                cursor.execute("UPDATE createride SET seats_available = seats_available - 1 WHERE id = %s", (ride_id,))
                conn.commit()

                seats_available_label.config(text=f"Seats Available: {seats_available - 1}")
                messagebox.showinfo("Success", "Ride booked successfully!")
            else:
                messagebox.showerror("Error", "No seats available!")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def search_ride(self):
        start = self.entry_1.get().strip()
        end = self.entry_2.get().strip()
        date = self.date_picker.get()

        if not start or not end:
            messagebox.showerror("Error", "Start and End destinations are required!")
            return

        try:
            date_obj = datetime.strptime(date, "%m/%d/%y")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            conn = self.connect_to_database()
            cursor = conn.cursor()

            query = """
            SELECT id, driver_name, car_details, ride_date, ride_time, seats_available, price, email
            FROM createride 
            WHERE start_location = %s AND end_location = %s AND ride_date = %s
            """
            cursor.execute(query, (start, end, formatted_date))
            rides = cursor.fetchall()

            # Clear previous results
            for widget in self.right_container.winfo_children():
                widget.destroy()

            # Create a Frame that will contain the Canvas and Scrollbar
            container = Frame(self.right_container, bg="#FFFFFF")
            container.pack(fill="both", expand=True)

            # Create a Canvas for scrollable content
            ride_canvas = Canvas(container, bg="#FFFFFF", height=650)
            ride_canvas.pack(side="left", fill="both", expand=True)

            # Scrollbar for the canvas
            scrollbar = Scrollbar(container, orient="vertical", command=ride_canvas.yview)
            scrollbar.pack(side="right", fill="y")

            # Configure canvas to work with scrollbar
            ride_canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame inside the Canvas to hold ride details
            scrollable_frame = Frame(ride_canvas, bg="#F5F5F5")

            # Add the frame to the Canvas
            ride_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=650)

            def update_scroll_region(event=None):
                """Update scroll region when new rides are added"""
                ride_canvas.configure(scrollregion=ride_canvas.bbox("all"))

            scrollable_frame.bind("<Configure>", update_scroll_region)

            # Enable mouse scrolling (Windows, macOS, Linux)
            def _on_mouse_wheel(event):
                ride_canvas.yview_scroll(-1 * (event.delta // 120), "units")

            ride_canvas.bind("<Enter>", lambda e: ride_canvas.bind_all("<MouseWheel>", _on_mouse_wheel))
            ride_canvas.bind("<Leave>", lambda e: ride_canvas.unbind_all("<MouseWheel>"))

            if rides:
                for ride in rides:
                    ride_id, driver_name, car_details, ride_date, ride_time, seats_available, price, driver_email = ride

                    # Ride Container (Each ride inside the scrollable frame)
                    ride_frame = Frame(scrollable_frame, bg="#FFFFFF", bd=1, relief="solid")
                    ride_frame.pack(fill="x", padx=10, pady=5)

                    # Ride Details
                    Label(ride_frame, text=f"Driver: {driver_name}", bg="#FFFFFF", font=("Poppins Medium", 12)).pack(
                        anchor="w")
                    Label(ride_frame, text=f"Car: {car_details}", bg="#FFFFFF", font=("Poppins Medium", 12)).pack(
                        anchor="w")
                    Label(ride_frame, text=f"Date: {ride_date}", bg="#FFFFFF", font=("Poppins Medium", 12)).pack(
                        anchor="w")
                    Label(ride_frame, text=f"Time: {ride_time}", bg="#FFFFFF", font=("Poppins Medium", 12)).pack(
                        anchor="w")
                    seats_label = Label(ride_frame, text=f"Seats Available: {seats_available}", bg="#FFFFFF",
                                        font=("Poppins Medium", 12))
                    seats_label.pack(anchor="w")
                    Label(ride_frame, text=f"Price: {price}", bg="#FFFFFF", font=("Poppins Medium", 12)).pack(
                        anchor="w")
                    Label(ride_frame, text=f"Contact: {driver_email}", bg="#FFFFFF", font=("Poppins Medium", 12)).pack(
                        anchor="w")

                    # Book Button
                    # Here we create a lambda function that remembers the specific driver_email for this ride
                    book_button = Button(
                        ride_frame,
                        text="Book",
                        bg="#4CAF50",
                        fg="white",
                        font=("Poppins Medium", 12),
                        command=lambda email=driver_email, e_start=start, e_end=end: self.confirmpage(email, e_start, e_end)
                    )
                    book_button.pack(anchor="e")

            else:
                Label(scrollable_frame, text="No rides found for the given destinations or date.", bg="#FFFFFF",
                      font=("Poppins Medium", 16)).pack(pady=20)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except ValueError as ve:
            messagebox.showerror("Date Format Error", f"Error: {ve}")

    def confirmpage(self, driver_email, start, end):
        # Now the method accepts the specific driver email from the button that was clicked
        self.destroy()
        ConfirmationPage.RideConfirmationPage(self.passenger_email, driver_email, start, end)


if __name__ == "__main__":
    user_email = "user@example.com"
    app = RideBookingApp(user_email)
    app.resizable(False, False)
    app.mainloop()