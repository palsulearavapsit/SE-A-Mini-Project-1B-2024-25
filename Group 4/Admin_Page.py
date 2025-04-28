from pathlib import Path
from tkinter import Tk, Canvas, Button, Label, messagebox, PhotoImage, Scrollbar, ttk
import mysql.connector
import WelcomePage

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="carpooling_db"
)
cursor = conn.cursor()


class AdminDashboard(Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\PoolifyFInal\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self, user_email):
        super().__init__()
        self.title("Poolify App")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.user_email = user_email

        # Configure Treeview style
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=50)

        self.create_ui()

    def welcome_page(self):
        self.destroy()
        WelcomePage.WelcomePage()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_ui(self):
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Header
        self.canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        self.canvas.create_text(15, 9, anchor="nw", text="POOLIFY", fill="#FFFFFF", font=("Italiana Regular", -36))

        # Dashboard Title
        self.canvas.create_text(29, 72, anchor="nw", text="Admin Dashboard", fill="#000000",
                                font=("Inter SemiBold", -32))

        # Verified Drivers Box
        self.canvas.create_rectangle(29, 135, 379, 260, fill="#F7F7F7", outline="Black")
        self.verified_drivers_label = self.canvas.create_text(173, 204, anchor="nw", text="0", fill="#000000",
                                                              font=("Inter SemiBold", -24))
        self.canvas.create_text(176, 161, anchor="nw", text="Verified drivers", fill="#000000",
                                font=("Inter Medium", -24))

        # Pending Approvals Box
        self.canvas.create_rectangle(465, 135, 815, 260, fill="#F7F7F7", outline="Black")
        self.pending_drivers_label = self.canvas.create_text(597, 201, anchor="nw", text="0", fill="#000000",
                                                             font=("Inter SemiBold", -24))
        self.canvas.create_text(587, 167, anchor="nw", text="Pending Approvals", fill="#000000",
                                font=("Inter Medium", -24))

        # Buttons and Images
        self.image_refresh = PhotoImage(file=self.relative_to_assets("refresh_button.png"))
        Button(self, image=self.image_refresh, borderwidth=0, highlightthickness=0,
               command=self.refresh_pending_drivers).place(x=498, y=159)

        self.image_people = PhotoImage(file=self.relative_to_assets("people_button.png"))
        self.canvas.create_image(92, 198, image=self.image_people)

        self.image_signout = PhotoImage(file=self.relative_to_assets("signout_button.png"))
        Button(self, image=self.image_signout, borderwidth=0, highlightthickness=0, command=self.welcome_page).place(
            x=1146, y=68, width=115, height=45)

        self.tm_signout = PhotoImage(file=self.relative_to_assets("tickmark_button.png"))
        Button(self, image=self.tm_signout, borderwidth=0, highlightthickness=0, command=self.quit).place(x=36, y=276,
                                                                                                          width=40,
                                                                                                          height=33)

        # Pending Drivers Section with Treeview and Scrollbar
        self.canvas.create_rectangle(29, 274, 1244, 676, fill="#F0F0F0", outline="Black")
        self.canvas.create_text(85, 282, anchor="nw", text="Pending Drivers Verifications", fill="#000000",
                                font=("Inter Medium", -20))

        # Create Treeview with Scrollbar
        self.pending_drivers_tree = ttk.Treeview(self, columns=("Driver", "Vehicle", "Approve", "Reject"),
                                                 show="headings", height=10, style="Custom.Treeview")
        self.pending_drivers_tree.heading("Driver", text="Driver")
        self.pending_drivers_tree.heading("Vehicle", text="Vehicle")
        self.pending_drivers_tree.heading("Approve", text="Approve")
        self.pending_drivers_tree.heading("Reject", text="Reject")

        # Set column widths
        self.pending_drivers_tree.column("Driver", width=400, anchor="center")
        self.pending_drivers_tree.column("Vehicle", width=400, anchor="center")
        self.pending_drivers_tree.column("Approve", width=200, anchor="center")
        self.pending_drivers_tree.column("Reject", width=200, anchor="center")

        # Place Treeview
        self.pending_drivers_tree.place(x=40, y=350, width=1200, height=300)

        # Add Scrollbar
        scrollbar = Scrollbar(self, orient="vertical", command=self.pending_drivers_tree.yview)
        scrollbar.place(x=1240, y=350, height=300)
        self.pending_drivers_tree.configure(yscrollcommand=scrollbar.set)

        # Initialize counts and drivers
        self.update_driver_counts()
        self.display_pending_drivers()

    def fetch_pending_drivers(self):
        cursor.execute("""
            SELECT d.email, d.full_name, IFNULL(c.description, 'No vehicle') 
            FROM drivers d
            LEFT JOIN cars c ON d.email = c.email
            WHERE d.status = 'pending'
        """)
        result = cursor.fetchall()
        return result

    def fetch_verified_drivers_count(self):
        cursor.execute("SELECT COUNT(*) FROM drivers WHERE status = 'verified'")
        return cursor.fetchone()[0]

    def fetch_pending_drivers_count(self):
        cursor.execute("SELECT COUNT(*) FROM drivers WHERE status = 'pending'")
        return cursor.fetchone()[0]

    def approve_driver(self, driver_email):
        try:
            cursor.execute("UPDATE drivers SET status = 'verified' WHERE email = %s", (driver_email,))
            conn.commit()
            messagebox.showinfo("Success", "Driver approved successfully!")
            self.update_driver_counts()
            self.refresh_pending_drivers()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}")

    def reject_driver(self, driver_email):
        try:
            cursor.execute("DELETE FROM cars WHERE email = %s", (driver_email,))
            cursor.execute("DELETE FROM drivers WHERE email = %s", (driver_email,))
            conn.commit()
            messagebox.showinfo("Success", "Driver rejected successfully!")
            self.update_driver_counts()
            self.refresh_pending_drivers()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_driver_counts(self):
        verified_count = self.fetch_verified_drivers_count()
        pending_count = self.fetch_pending_drivers_count()
        self.canvas.itemconfig(self.verified_drivers_label, text=str(verified_count))
        self.canvas.itemconfig(self.pending_drivers_label, text=str(pending_count))

    def refresh_pending_drivers(self):
        # Clear existing items
        for item in self.pending_drivers_tree.get_children():
            self.pending_drivers_tree.delete(item)

        # Repopulate the treeview
        self.display_pending_drivers()

    def display_pending_drivers(self):
        drivers = self.fetch_pending_drivers()
        for driver_email, driver_name, vehicle_description in drivers:
            # Insert row with buttons
            self.pending_drivers_tree.insert("", "end", values=(
                driver_name,
                vehicle_description,
                "Approve",
                "Reject"
            ), tags=(driver_email,))

        # Bind double-click to handle approval/rejection
        self.pending_drivers_tree.bind('<Double-1>', self.on_driver_row_double_click)

    def on_driver_row_double_click(self, event):
        # Get the row that was clicked
        row = self.pending_drivers_tree.identify_row(event.y)

        # Get the column that was clicked
        column = self.pending_drivers_tree.identify_column(event.x)

        if row and column:
            # Get the driver email from the row tags
            driver_email = self.pending_drivers_tree.item(row, "tags")[0]

            # Determine action based on column
            if column == "#3":  # Approve column
                self.approve_driver(driver_email)
            elif column == "#4":  # Reject column
                self.reject_driver(driver_email)

if __name__ == "__main__":
    app = AdminDashboard("user@example.com")
    app.resizable(False, False)
    app.mainloop()