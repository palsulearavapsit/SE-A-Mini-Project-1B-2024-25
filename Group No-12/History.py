from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk
import mysql.connector

# Database configuration (update with your credentials)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aayush@0909',
    'database': 'findr',
    'auth_plugin': 'mysql_native_password'
}

# Assume current user ID (replace with actual user ID retrieval logic) 

# GUI setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\History")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_history_page(previous_window, user_id, user_name):  # put these two line and select code and press tab
    previous_window.destroy()
    window = Tk()
    window.geometry("700x840")
    window.configure(bg="#FFFFFF")

    def fetch_history_data():
        """Fetch history data from MySQL database for the current user."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT sname, service, amount, dd, mm, yyyy, hh, min FROM history WHERE uid = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def open_home():
        from Home import open_home_page
        open_home_page(window, user_id, user_name)
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=840,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Header rectangle
    canvas.create_rectangle(0.0, 0.0, 700.0, 76.0, fill="#044389", outline="")

    # Footer rectangle
    canvas.create_rectangle(0.0, 719.0, 700.0, 840.0, fill="#ECECEE", outline="")

    # Buttons and images (unchanged from original)
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(x=33.0, y=19.0, width=77.0, height=31.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(x=621.0, y=18.0, width=31.0, height=31.0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(348.0, 145.0, image=image_image_1)

    # Replace rectangle with Treeview
    tree_frame = ttk.Frame(window)
    tree_frame.place(x=48, y=243, width=600, height=417)

    # Configure Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    style.configure("Treeview", font=('Arial', 9), rowheight=25)

    tree = ttk.Treeview(
        tree_frame,
        columns=("Name", "Service", "Amount", "Date", "Time"),
        show="headings",
        style="Treeview"
    )
    tree.heading("Name", text="Name")
    tree.heading("Service", text="Service")
    tree.heading("Amount", text="Amount")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")

    tree.column("Name", width=120, anchor="center")
    tree.column("Service", width=120, anchor="center")
    tree.column("Amount", width=120, anchor="center")
    tree.column("Date", width=120, anchor="center")
    tree.column("Time", width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    # Fetch and insert data
    history_data = fetch_history_data()
    for row in history_data:
        sname, service, amount, dd, mm, yyyy, hh, min = row
        
        # Handle date components
        if None in (dd, mm, yyyy):
            formatted_date = "N/A"
        else:
            formatted_date = f"{int(dd):02d}-{int(mm):02d}-{int(yyyy)}"
        
        # Handle time components
        if None in (hh, min):
            formatted_time = "N/A"
        else:
            formatted_time = f"{int(hh):02d}:{int(min):02d}"
        
        tree.insert("", "end", values=(sname, service, amount, formatted_date, formatted_time))

    # Footer buttons (unchanged from original)
    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=open_home,
        relief="flat"
    )
    button_3.place(x=43.0, y=760.0, width=49.0, height=49.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(x=603.0, y=758.0, width=49.0, height=49.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    button_5.place(x=408.0, y=758.0, width=49.0, height=49.0)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
        relief="flat"
    )
    button_6.place(x=214.0, y=760.0, width=49.0, height=49.0)

    window.resizable(False, False)
    window.mainloop()